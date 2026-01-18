"""MisMatch Recruiter Bot - Application Package"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

from app.config import MismatchSettings

def create_app(config=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:////tmp/mismatch.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Config
    if config:
        config.update(config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from app.routes import candidates_bp, job_enrichment_bp, matches_bp
   app.register_blueprint(candidates_bp)
    app.register_blueprint(job_enrichment_bp)
app.register_blueprint(matches_bp)    
    # GraphQL API
    from graphene_flask import GraphQLView
    from app.graphql import schema
    
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
    )
    
    return app
