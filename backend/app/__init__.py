from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name='development'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    if config_name == 'development':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mismatch.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
        app.config['DEBUG'] = True
    elif config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['JWT_SECRET_KEY'] = 'test-secret'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mismatch.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-secret')
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    with app.app_context():
        # Register blueprints
        from backend.app.routes import health, auth, candidates, jobs, matches
        
        app.register_blueprint(health.bp)
        app.register_blueprint(auth.bp, url_prefix='/api/auth')
        app.register_blueprint(candidates.bp, url_prefix='/api/candidates')
        app.register_blueprint(jobs.bp, url_prefix='/api/jobs')
        app.register_blueprint(matches.bp, url_prefix='/api/matches')
        
        # Create tables
        db.create_all()
    
    return app
