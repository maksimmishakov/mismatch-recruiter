from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Configuration
    if config_name == 'testing':
        from app.config import TestingConfig
        app.config.from_object(TestingConfig)
    elif config_name == 'production':
        from app.config import ProductionConfig
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from app.api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
