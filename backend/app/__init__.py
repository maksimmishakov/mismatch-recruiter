"""Flask application factory for MisMatch Recruiter."""
import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import Config, ProductionConfig, DevelopmentConfig, TestingConfig
from app.models import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app(config_name='development'):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    if config_name == 'production':
        app.config.from_object(ProductionConfig)
    elif config_name == 'testing':
        app.config.from_object(TestingConfig)
    elif config_name == 'development':
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(Config)


        
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    jwt = JWTManager(app)
    
    # Create app context and initialize database
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.warning(f"Could not create database tables: {e}")
    
    # Register API blueprints
    try:
        from app.api.routes import api_bp
        app.register_blueprint(api_bp, url_prefix='/api')
        logger.info("API blueprint registered")
    except Exception as e:
        logger.warning(f"Could not register API blueprint: {e}")
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({
            'status': 'healthy',
            'message': 'MisMatch Recruiter API is running'
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app
