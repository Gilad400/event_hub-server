import json

from bson import ObjectId

from app import mongo, bcrypt

def __init__(self, username, email, password, favorites=None):
    self.username = username
    self.email = email
    self.password = password
    self.favorites = favorites if favorites else []

def register(self):
        try:
            users = mongo.db.users
            if users is None:
                return False, 'Error occur try again later'
            existing_user = users.find_one({'email': self.email}) if users is not None else None
            if existing_user is None:
                hashpass = bcrypt.generate_password_hash(self.password).decode('utf-8')
                result = users.insert_one({'username': self.username, 'email': self.email, 'password': hashpass, 'favorites': self.favorites})
                user = {
                    '_id': result.inserted_id,
                    'favorites': self.favorites
                }
                return True, user
            return False, None if existing_user else 'Error occur try again later'
        except RuntimeError as e:
            return False, 'Error occur try again later'

    @staticmethod
    def login(email, password):
        users = mongo.db.users
        login_user = users.find_one({'email': email}) if users is not None else None
        if login_user:
            if bcrypt.check_password_hash(login_user['password'], password):
                user = {
                    '_id': str(login_user['_id']),
                    'favorites': login_user['favorites'] if 'favorites' in login_user else []
                }
                return True, user
        return False, None

    def add_to_favorites(user_id, cocktail):
            users = mongo.db.users
            user = users.find_one({'_id': ObjectId(user_id)})
            if user:
                favorites = user.get('favorites', [])
                if not any(f for f in favorites if isinstance(f, dict) and f.get('idDrink') == cocktail['idDrink']):
                    favorites.append(cocktail)
                    users.update_one({'_id': ObjectId(user_id)}, {'$set': {'favorites': favorites}})
                return True, 'Cocktail added to favorites'
            return False, 'Error occur try again later'

        @staticmethod
        def remove_from_favorites(user_id, cocktail_id):
            users = mongo.db.users
            user = users.find_one({'_id': ObjectId(user_id)})
            if user:
                favorites = user['favorites'] if 'favorites' in user else []
                favorite = next((f for f in favorites if isinstance(f, dict) and f.get('idDrink') == cocktail_id), None)
                if favorite:
                    favorites.remove(favorite)
                    users.update_one({'_id': ObjectId(user_id)}, {'$set': {'favorites': favorites}})
                return True, 'Cocktail added to favorites'
            return False, 'Error occur try again later'
