import re
from bson import ObjectId
from app import mongo, bcrypt

class User:
    def __init__(self, username, email, password, favorites=None):
        self.username = username
        self.email = email
        self.password = password
        self.favorites = favorites if favorites else []

    def validate_email(self):
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        return bool(email_pattern.match(self.email))

    def validate_password(self):
        return len(self.password) >= 8

    def register(self):
        try:
            if not all([self.username, self.email, self.password]):
                return False, 'All fields are required'
            
            if not self.validate_email():
                return False, 'Invalid email format'
                
            if not self.validate_password():
                return False, 'Password must be at least 8 characters long'

            users = mongo.db.users
            existing_user = users.find_one({
                '$or': [
                    {'email': self.email},
                    {'username': self.username}
                ]
            })
            
            if existing_user:
                if existing_user['email'] == self.email:
                    return False, 'Email already registered'
                return False, 'Username already taken'

            hashpass = bcrypt.generate_password_hash(self.password).decode('utf-8')
            result = users.insert_one({
                'username': self.username,
                'email': self.email,
                'password': hashpass,
                'favorites': self.favorites
            })
            
            user = {
                '_id': str(result.inserted_id),
                'username': self.username,
                'favorites': self.favorites
            }
            return True, user

        except Exception as e:
            return False, f'Error occurred: {str(e)}'

    @staticmethod
    def login(email, password):
        try:
            users = mongo.db.users
            user = users.find_one({'email': email})
            
            if user and bcrypt.check_password_hash(user['password'], password):
                return True, {
                    '_id': str(user['_id']),
                    'username': user['username'],
                    'favorites': user.get('favorites', [])
                }
            return False, 'Invalid email or password'
            
        except Exception as e:
            return False, f'Error occurred: {str(e)}'

    @staticmethod
    def add_to_favorites(user_id, favorite):
        try:
            users = mongo.db.users
            result = users.update_one(
                {'_id': ObjectId(user_id)},
                {'$addToSet': {'favorites': favorite}}
            )
            
            if result.modified_count:
                return True, 'Added to favorites'
            return False, 'Already in favorites'
            
        except Exception as e:
            return False, f'Error occurred: {str(e)}'

    @staticmethod
    def remove_from_favorites(user_id, favorite):
        try:
            users = mongo.db.users
            result = users.update_one(
                {'_id': ObjectId(user_id)},
                {'$pull': {'favorites': favorite}}
            )
            
            if result.modified_count:
                return True, 'Removed from favorites'
            return False, 'Favorite not found'
            
        except Exception as e:
            return False, f'Error occurred: {str(e)}'