"""Flask application factory"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Configuration
    app.config['ENV'] = config_name
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mismatch.db')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key-change-me')
    
    # CORS
    cors_origins = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')
    CORS(app, resources={r"/api/*": {"origins": cors_origins}})
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from app.routes import create_routes
    create_routes(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
