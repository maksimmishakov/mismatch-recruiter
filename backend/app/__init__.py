import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name='development'):
    """Flask application factory"""
    app = Flask(__name__)
    
    # Configuration
    if config_name == 'production':
        from app.config import ProductionConfig
        app.config.from_object(ProductionConfig)
    elif config_name == 'testing':
        from app.config import TestingConfig
        app.config.from_object(TestingConfig)
    else:
        from app.config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Import models to register them with SQLAlchemy
    from app.models import User, Candidate, Job, Match
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Register route blueprints
    from app.routes import auth_bp, candidates_bp, jobs_bp, matches_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(candidates_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(matches_bp)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'ok', 'message': 'Service is running'}), 200
    
    return app
