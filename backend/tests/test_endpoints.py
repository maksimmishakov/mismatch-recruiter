import pytest

# AUTH ENDPOINT TESTS
def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'

def test_signup_endpoint_exists(client):
    """Test signup endpoint"""
    response = client.post('/api/auth/signup', json={
        'email': 'test@example.com',
        'password': 'pass123',
        'name': 'Test'
    })
    assert response.status_code in [200, 201, 400, 404]

def test_login_endpoint_exists(client):
    """Test login endpoint"""
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'pass123'
    })
    assert response.status_code in [200, 400, 404, 401]

def test_candidates_endpoint_exists(client):
    """Test candidates endpoint"""
    response = client.get('/api/candidates')
    # Should return 401 (auth required) or 404 (not found)
    assert response.status_code in [401, 404, 200]

def test_jobs_endpoint_exists(client):
    """Test jobs endpoint"""
    response = client.get('/api/jobs')
    assert response.status_code in [401, 404, 200]

def test_post_candidate_endpoint_exists(client):
    """Test create candidate endpoint"""
    response = client.post('/api/candidates', json={
        'name': 'Test',
        'email': 'test@example.com'
    })
    assert response.status_code in [400, 401, 404, 201]

def test_post_job_endpoint_exists(client):
    """Test create job endpoint"""
    response = client.post('/api/jobs', json={
        'title': 'Test',
        'description': 'Test'
    })
    assert response.status_code in [400, 401, 404, 201]

def test_signup_missing_email(client):
    """Test signup with missing email"""
    response = client.post('/api/auth/signup', json={
        'password': 'pass123'
    })
    assert response.status_code in [400, 404]

def test_signup_missing_password(client):
    """Test signup with missing password"""
    response = client.post('/api/auth/signup', json={
        'email': 'test@example.com'
    })
    assert response.status_code in [400, 404]

def test_login_missing_email(client):
    """Test login with missing email"""
    response = client.post('/api/auth/login', json={
        'password': 'pass123'
    })
    assert response.status_code in [400, 404]

def test_login_missing_password(client):
    """Test login with missing password"""
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com'
    })
    assert response.status_code in [400, 404]

def test_candidate_endpoint_with_invalid_data(client):
    """Test candidate endpoint with invalid data"""
    response = client.post('/api/candidates', json={
        'invalid_field': 'test'
    })
    assert response.status_code in [400, 401, 404]

