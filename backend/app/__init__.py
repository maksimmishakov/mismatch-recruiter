from flask import Flask
from app.database import db
import logging
import os

logger = logging.getLogger(__name__)

def create_app(config_name='development'):
    """Application factory function."""
    app = Flask(__name__)
    
    # Load configuration based on config name
    if config_name == 'testing':
        from app.config import TestingConfig
        app.config.from_object(TestingConfig)
    elif config_name == 'production':
        from app.config import ProductionConfig
        app.config.from_object(ProductionConfig)
    else:
        # Default development config
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///mismatch.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['DEBUG'] = True
    
    # Initialize extensions
    db.init_app(app)
    
    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.warning(f"Could not create database tables: {e}")
    
    # Register API blueprints
    try:
        from app.routes.auth import auth_bp
        from app.routes.candidates import candidates_bp
        from app.routes.jobs import jobs_bp
        
        app.register_blueprint(auth_bp)
        app.register_blueprint(candidates_bp)
        app.register_blueprint(jobs_bp)
        
        logger.info("API blueprints registered")
    except Exception as e:
        logger.warning(f"Could not register API blueprints: {e}")
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health():
        return {'status': 'ok', 'message': 'MisMatch Recruiter API is running'}, 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f'Internal error: {error}')
        return {'error': 'Internal server error'}, 500
    
    return app
