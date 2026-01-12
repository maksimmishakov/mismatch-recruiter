import pytest
import os
from app import create_app, db

@pytest.fixture(scope='session')
def app():
    """Create and configure app for testing"""
    os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    os.environ['TESTING'] = 'True'
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    """Test client"""
    with app.app_context():
        yield app.test_client()

@pytest.fixture(autouse=True)
def reset_db(app):
    """Reset database between tests"""
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
        yield
