"""Test API endpoints."""

def test_health_check(client):
    """Test health check endpoint."""
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_register(client):
    """Test user registration."""
    response = client.post('/api/auth/register', json={
        'email': 'newuser@test.com',
        'username': 'newuser',
        'password': 'password123',
        'full_name': 'New User'
    })
    assert response.status_code == 201
    assert 'user_id' in response.json

def test_register_duplicate_email(client):
    """Test registration with duplicate email."""
    # Register first user
    client.post('/api/auth/register', json={
        'email': 'test@test.com',
        'username': 'user1',
        'password': 'pass123'
    })
    # Try to register with same email
    response = client.post('/api/auth/register', json={
        'email': 'test@test.com',
        'username': 'user2',
        'password': 'pass123'
    })
    assert response.status_code == 409

def test_login(client, test_user):
    """Test user login."""
    response = client.post('/api/auth/login', json={
        'email': 'test@test.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_login_invalid_credentials(client, test_user):
    """Test login with wrong password."""
    response = client.post('/api/auth/login', json={
        'email': 'test@test.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401

def test_get_current_user(client, test_user):
    """Test getting current user."""
    # Login first to get token
    login_response = client.post('/api/auth/login', json={
        'email': 'test@test.com',
        'password': 'password123'
    })
    token = login_response.json['access_token']
    # Get current user
    response = client.get(
        '/api/auth/me',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert response.json['email'] == 'test@test.com'
