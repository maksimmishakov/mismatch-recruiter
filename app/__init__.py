echo 'PHASE 14 SESSION COMPLETE' && echo '✓ ImportError identified and documented' && echo '✓ Root cause: Config class missing from app.config/__init__.py' && echo '✓ Action plan: PHASE_14_DEBUG_ACTION_PLAN.md created' && echo '✓ Next steps: Implement fix in backend/app/config/__init__.py' && echo '✓ All changes committed to GitHub main branch'
import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Configuration
    app.config['CORS_ORIGINS'] = os.getenv('CORS_ORIGINS', '*').split(',')
    app.config['ENV'] = os.getenv('FLASK_ENV', 'development')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///mismatch.db')
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    return app
