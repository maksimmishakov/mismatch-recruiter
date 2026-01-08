"""Pytest configuration and fixtures."""
import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    """Create app for testing."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Test client."""
    return app.test_client()

@pytest.fixture
def test_user(app):
    """Create test user."""
    user = User(email='test@test.com', username='testuser')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user
