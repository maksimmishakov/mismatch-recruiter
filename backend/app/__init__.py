from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .logger import setup_logging

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
    
        # Validate JWT_SECRET_KEY in production
    if app.config['ENV'] == 'production':
        jwt_secret = app.config.get('JWT_SECRET_KEY')
        if not jwt_secret or jwt_secret.startswith('dev-'):
            raise ValueError('JWT_SECRET_KEY must be set via environment variable in production')
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    # CORS Configuration
    cors_origins = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')
    CORS(app, resources={"/api/*": {"origins": cors_origins}})
    

        # Security Headers (Talisman)
    if app.config['ENV'] == 'production':
        Talisman(app, force_https=True, strict_transport_security=True, strict_transport_security_max_age=31536000)
    else:
        Talisman(app, force_https=False)
    
    # Rate Limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
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
    
        # Setup logging
    setup_logging(app)git add -A && git commit -m "database(day2): add postgresql models, database config, and marshmallow schemas"
    git push origin HEAD
    
    return app
