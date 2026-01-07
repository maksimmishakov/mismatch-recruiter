import json

def test_health_check(client):
    """Test API health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'service' in data

def test_user_registration(client):
    """Test user registration"""
    response = client.post('/api/auth/register', 
        json={
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'secure_password123',
            'full_name': 'New User'
        })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'user_id' in data

def test_user_registration_missing_fields(client):
    """Test user registration with missing fields"""
    response = client.post('/api/auth/register',
        json={
            'email': 'test@example.com'
        })
    assert response.status_code == 400

def test_user_registration_duplicate_email(client, test_user):
    """Test user registration with duplicate email"""
    response = client.post('/api/auth/register',
        json={
            'email': 'test@example.com',
            'username': 'another',
            'password': 'password123'
        })
    assert response.status_code == 409

def test_user_login(client, test_user):
    """Test user login"""
    response = client.post('/api/auth/login',
        json={
            'email': 'test@example.com',
            'password': 'password123'
        })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data
    assert 'user' in data

def test_user_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post('/api/auth/login',
        json={
            'email': 'nonexistent@example.com',
            'password': 'wrong_password'
        })
    assert response.status_code == 401
