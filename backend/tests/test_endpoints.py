import json

def test_health_endpoint(client):
    """Test health endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'status' in data

def test_health_endpoint_post_fails(client):
    """Test health endpoint with POST (should fail)"""
    response = client.post('/api/health')
    assert response.status_code == 405  # Method Not Allowed

def test_invalid_route_404(client):
    """Test invalid route returns 404"""
    response = client.get('/api/nonexistent/route')
    assert response.status_code == 404

def test_login_missing_password(client):
    """Test login with missing password"""
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com'
    })
    assert response.status_code in [400, 401, 404]

def test_login_missing_email(client):
    """Test login with missing email"""
    response = client.post('/api/auth/login', json={
        'password': 'test123'
    })
    assert response.status_code in [400, 401, 404]

def test_get_candidates_endpoint(client):
    """Test get candidates endpoint"""
    response = client.get('/api/candidates')
    assert response.status_code in [200, 401]
    if response.status_code == 200:
        data = json.loads(response.data)
        assert isinstance(data, (dict, list))

def test_auth_register_missing_fields(client):
    """Test register with missing fields"""
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com'
    })
    assert response.status_code in [400, 401, 404]

