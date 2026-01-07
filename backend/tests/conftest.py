import pytest
from app import create_app, db
import os

@pytest.fixture(scope='session')
def app():
    '''Create application for testing'''
    app = create_app('testing')
    return app

@pytest.fixture(scope='function')
def client(app):
    '''Create test client'''
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

@pytest.fixture
def runner(app):
    '''Create CLI runner'''
    return app.test_cli_runner()

@pytest.fixture
def auth_token(client):
    '''Create auth token for testing'''
    # Test user login
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    return response.json.get('token')
