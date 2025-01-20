from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from app.config import Config
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['MONGO_URI'] = Config.MONGO_URI
CORS(app, resources={r"/*": {
    "origins": "http://localhost:3000",
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Authorization", "Content-Type"],
    "supports_credentials": True
}})
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

# Register blueprints
from app.routes import main_bp
app.register_blueprint(main_bp)