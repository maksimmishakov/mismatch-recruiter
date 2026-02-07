"""Test configuration and fixtures."""
import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Get test client."""
    return app.test_client()

@pytest.fixture
def test_user(app):
    """Create a test user."""
    with app.app_context():
        user = User(
            email='test@example.com',
            name='Test User'
        )
        user.set_password('TestPassword123!')
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture
def auth_token(client, test_user):
    """Get authentication token for test user."""
    response = client.post('/api/v1/auth/login',
        json={
            'email': 'test@example.com',
            'password': 'TestPassword123!'
        }
    )
    if response.status_code == 200:
        return response.json.get('token')
    return None
