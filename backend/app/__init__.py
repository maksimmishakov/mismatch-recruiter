import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)

def create_app(config_name=None):
    app = Flask(__name__)
    
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    from app.config import config
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    from app.logger import setup_logging
    setup_logging(app)
    
    from app.errors import register_error_handlers
    register_error_handlers(app)
    
    # Register route blueprints
    from app.routes import auth_bp, candidates_bp, jobs_bp, matches_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(candidates_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(matches_bp)
    
    # Register health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'ok', 'message': 'Service is running'}, 200
    
    with app.app_context():
        db.create_all()
    
    return app
