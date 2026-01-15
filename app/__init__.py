"""MisMatch Recruitment Bot - Application Package"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app(config=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Config
    from app.config import MismatchSettings, get_settings
settings = get_settings()
            app.config['SQLALCHEMY_DATABASE_URI'] = settings.Mismatch_db_connection or 'sqlite:////tmp/mismatch.db'
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    if config:
        app.config.update(config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from app.routes import api_bp, main_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # GraphQL API
    from graphene_flask import GraphQLView
    
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
    )
    
    # Create tables
    with app.app_context():
        db.create_all()

        # Error handlers
    from werkzeug.exceptions import BadRequest
    
    @app.errorhandler(BadRequest)
    def handle_bad_request(error):
        """Handle bad requests (e.g., invalid JSON)"""
        return {'error': 'Bad Request', 'message': str(error.description)}, 400
    
    @app.errorhandler(422)
    def handle_unprocessable_entity(error):
        """Handle unprocessable entities"""
        return {'error': 'Unprocessable Entity', 'message': str(error.description)}, 422
    
    return app

__version__ = '2.0.0'
__all__ = ['create_app', 'db']
