import os
from flask import current_app,  Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Configuration
    if config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///mismatch.db')
    
    app.config['ENV'] = os.getenv('FLASK_ENV', 'development')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['CORS_ORIGINS'] = os.getenv('CORS_ORIGINS', '*')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=app.config['CORS_ORIGINS'].split(','))
    
    with app.app_context():
        from app.models import User, Candidate, Job, Match
        db.create_all()
        
        # Register routes
        register_routes(app)
    
    return app

def register_routes(app):
    """Register all API routes"""
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'ok', 'service': 'mismatch-recruiter', 'version': '1.0'}), 200
    
    # Register blueprints
    try:
        from app.routes.auth import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/api')
    except:
        pass
    
    try:
        from app.routes.candidates import candidates_bp
        app.register_blueprint(candidates_bp, url_prefix='/api')
    except:
        pass
    
    try:
        from app.routes.jobs import jobs_bp
        app.register_blueprint(jobs_bp, url_prefix='/api')
    except:
        pass
