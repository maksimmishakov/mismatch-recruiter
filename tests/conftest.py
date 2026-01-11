"""Test configuration and fixtures for MisMatch Recruiter"""
import pytest
from app import create_app, db
from app.models import User, Resume, Job, Match, Prediction, Subscription


@pytest.fixture(scope='session')
def app():
    """Create application for the tests."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """A test runner for the app's CLI."""
    return app.test_cli_runner()


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
    response = client.post('/api/auth/login',
                          json={
                              'email': 'test@example.com',
                              'password': 'TestPassword123!'
                          })
    if response.status_code == 200:
        return response.json.get('token')
    return None
