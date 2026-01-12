import pytest
import json
from app.models import User, Candidate, Job, Match

@pytest.fixture
def test_user(app):
    """Create test user"""
    with app.app_context():
        user = User(email='test@example.com', name='Test User')
        user.set_password('password123')
        from app import db
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture
def auth_token(client, test_user):
    """Get auth token for test user"""
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    if response.status_code == 200:
        return response.get_json().get('access_token')
    return None

# HEALTH CHECK TESTS
def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data
    assert data['status'] == 'ok'

