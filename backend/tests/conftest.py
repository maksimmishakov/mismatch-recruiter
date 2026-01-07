import pytest
import os
from app import create_app, db

@pytest.fixture
def app():
    """Create application for testing."""
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Test runner for the app."""
    return app.test_cli_runner()
