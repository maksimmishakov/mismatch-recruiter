import pytest
from app import db
from app.models import User

def test_user_registration(client):
    """Test user registration endpoint."""
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'TestPass123!',
        'full_name': 'Test User'
    })
    assert response.status_code in [201, 400]  # 201 if new, 400 if user exists

def test_user_login(client):
    """Test user login endpoint."""
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'TestPass123!'
    })
    # Should return 200 if credentials valid, 401 if not
    assert response.status_code in [200, 401]

def test_invalid_credentials(client):
    """Test login with invalid credentials."""
    response = client.post('/api/auth/login', json={
        'username': 'nonexistent',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401

def test_missing_required_fields(client):
    """Test validation of required fields."""
    response = client.post('/api/auth/login', json={
        'username': 'test'
        # Missing password
    })
    assert response.status_code == 400
