"""Flask application factory."""
import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_name=None):
    """Create and configure Flask application.
    
    Args:
        config_name: Configuration name ('development', 'staging', 'production', 'testing')
                    If None, uses FLASK_ENV environment variable, defaults to 'development'
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Load configuration based on environment
    if config_name == 'production':
        from app.config.production import ProductionConfig
        app.config.from_object(ProductionConfig)
    elif config_name == 'staging':
        from app.config.staging import StagingConfig
        app.config.from_object(StagingConfig)
    elif config_name == 'testing':
        from app.config.testing import TestingConfig
        app.config.from_object(TestingConfig)
    else:
        from app.config.development import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Setup CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config.get('CORS_ORIGINS', ['*']),
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
        }
    })
    
    # Initialize Sentry if DSN provided
    if app.config.get('SENTRY_DSN'):
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration
        
        sentry_sdk.init(
            dsn=app.config['SENTRY_DSN'],
            integrations=[FlaskIntegration()],
            traces_sample_rate=app.config.get('SENTRY_TRACES_SAMPLE_RATE', 0.1),
            environment=app.config.get('SENTRY_ENVIRONMENT', 'development'),
        )
    
    # Register blueprints
    from app.api import api_bp
    from app.api import notifications_bp
from app.api import analytics_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(notifications_bp)
    app.register_blueprint(analytics_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    # Application context processors
    @app.context_processor
    def inject_config():
        return {
            'app_env': app.config.get('ENVIRONMENT', 'development'),
        }
    
    return app