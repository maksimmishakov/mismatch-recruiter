"""Flask Application Factory
Initializes and configures the Flask application with all extensions.
"""

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import timedelta
import os
import logging

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
cache = Cache()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def create_app(config_name='development'):
    """Create and configure the Flask application.
    
    Args:
        config_name: Configuration profile ('development', 'testing', 'production')
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'sqlite:///mismatch.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_SORT_KEYS'] = False
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = os.getenv(
        'JWT_SECRET_KEY',
        'dev-secret-key-change-in-production'
    )
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(
        hours=int(os.getenv('JWT_EXPIRATION_HOURS', 24))
    )
    app.config['JWT_ALGORITHM'] = 'HS256'
    
    # Cache Configuration
    app.config['CACHE_TYPE'] = 'redis'
    app.config['CACHE_REDIS_URL'] = os.getenv(
        'REDIS_URL',
        'redis://localhost:6379/0'
    )
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300
    
    # CORS Configuration
    cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    app.config['CORS_ORIGINS'] = cors_origins
    
    # Logging
    logging.basicConfig(
        level=os.getenv('LOG_LEVEL', 'INFO'),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    CORS(app, origins=cors_origins, supports_credentials=True)
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint for Kubernetes probes."""
        return jsonify({
            'status': 'healthy',
            'version': '1.0.0',
            'environment': config_name
        }), 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        """Root API endpoint."""
        return jsonify({
            'name': 'MisMatch Recruiter API',
            'version': '1.0.0',
            'status': 'running'
        }), 200
    
    # Metrics endpoint (for Prometheus)
    @app.route('/metrics', methods=['GET'])
    def metrics():
        """Prometheus metrics endpoint."""
        # This would be implemented with prometheus_client
        # For now, return placeholder
        return jsonify({'message': 'Metrics endpoint'}), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found',
            'status': 404
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        db.session.rollback()
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An internal server error occurred',
            'status': 500
        }), 500
    
    # Context processor for template globals
    @app.context_processor
    def inject_config():
        return dict(config=app.config)
    
    # Application context
    with app.app_context():
        # Create database tables
        db.create_all()
        
        # Register blueprints (when they exist)
        try:
            from backend.app.routes import candidates
            app.register_blueprint(candidates.bp, url_prefix='/api/v1/candidates')
        except ImportError:
            app.logger.warning('Candidates blueprint not found')
        
        try:
            from backend.app.routes import auth
            app.register_blueprint(auth.bp, url_prefix='/api/v1/auth')
        except ImportError:
            app.logger.warning('Auth blueprint not found')
    
    app.logger.info(f'Application created with config: {config_name}')
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
