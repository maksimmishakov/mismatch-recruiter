"""MisMatch Recruitment Bot - Application Package"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

from app.graphql.schema import schema

load_dotenv()

db = SQLAlchemy()

def create_app(config=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Config
    from app.config import Config
    app.config.from_object(Config)
    
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
    from app.graphql.schema import schema
    
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
    )
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

__version__ = '2.0.0'
__all__ = ['create_app', 'db']
