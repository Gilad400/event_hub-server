from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from app.config import Config

app = Flask(__name__)
allow_origins = [
    Config.DEV_ORIGIN,
    Config.PROD_ORIGIN
]
app.config['MONGO_URI'] = Config.MONGO_URI
CORS(app, resources={r"/*": {
    "origins": allow_origins,
    "methods": ["GET", "POST"],
    "allow_headers": ["Authorization", "Content-Type"],
    "supports_credentials": True
}})
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

from app.routes import auth_routes, cocktail_routes, favorite_routes

auth_routes.register_routes(app)
cocktail_routes.register_routes(app)
favorite_routes.register_routes(app)
