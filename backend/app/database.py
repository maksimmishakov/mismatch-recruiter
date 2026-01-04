from flask import Flask
from flask_migrate import Migrate
from app.models import db
import os

migrate = Migrate()

def init_db(app: Flask):
    """
    Initialize database with the Flask app.
    Creates all tables and applies migrations.
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:postgres@postgres:5432/mismatch_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = os.getenv('DEBUG', False)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        db.create_all()
        print('[DB] Database initialized successfully')

def reset_db(app: Flask):
    """
    Drop all tables and recreate them.
    WARNING: This will delete all data!
    """
    with app.app_context():
        db.drop_all()
        db.create_all()
        print('[DB] Database reset successfully')
