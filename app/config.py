class Config:
    # Environment URLs
    BACKEND_URL = 'http://localhost:5000'
    FRONTEND_URL = 'http://localhost:3000'
    
    # CORS settings
    ALLOWED_ORIGINS = [
        'http://localhost:3000',  # Development
        # Add your deployed frontend URL when you deploy the application
    ]
    
    # MongoDB settings
    MONGO_URI = 'mongodb://localhost:27017/users?appName=local'
    # If using MongoDB Atlas, use this format: 
    # MONGO_URI = "mongodb+srv://username:password@cluster.mongodb.net/database?retryWrites=true&w=majority"?appName=local'