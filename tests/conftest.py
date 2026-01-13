import sys
import os
import pytest

# Add the parent directory to the path so we can import backend modules
sys_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if sys_path not in sys.path:
    sys.path.insert(0, sys_path)

from backend.app import create_app, db

@pytest.fixture(scope='function')
def app():
    """Create and configure a test instance of the app."""
    # Set test database to in-memory SQLite
    app_instance = create_app()
    app_instance.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app_instance.config['TESTING'] = True
    
    with app_instance.app_context():
        db.create_all()
        yield app_instance
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Test client for the app."""
    return app.test_client()
