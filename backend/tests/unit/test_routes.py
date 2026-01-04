import pytest
import json

class TestAuthRoutes:
    """Test cases for authentication routes"""
    
    def test_login_success(self, client, test_user):
        """Test successful login"""
        response = client.post('/api/auth/login', json={
            'email': 'user@test.com',
            'password': 'testpass'
        })
        assert response.status_code == 200
        assert 'access_token' in response.json
    
    def test_login_invalid_password(self, client, test_user):
        """Test login with invalid password"""
        response = client.post('/api/auth/login', json={
            'email': 'user@test.com',
            'password': 'wrongpass'
        })
        assert response.status_code == 401
    
    def test_register_new_user(self, client):
        """Test user registration"""
        response = client.post('/api/auth/register', json={
            'email': 'newuser@test.com',
            'name': 'New User',
            'password': 'password123'
        })
        assert response.status_code in [200, 201]

class TestCandidateRoutes:
    """Test cases for candidate routes"""
    
    def test_get_candidates(self, client, auth_headers, test_candidate):
        """Test getting candidates list"""
        response = client.get('/api/candidates', headers=auth_headers)
        assert response.status_code == 200
    
    def test_create_candidate(self, client, auth_headers):
        """Test creating a candidate"""
        response = client.post('/api/candidates', headers=auth_headers, json={
            'skills': ['Python', 'Flask'],
            'experience_years': 5,
            'salary_expectation': 100000
        })
        assert response.status_code in [200, 201]

class TestJobRoutes:
    """Test cases for job routes"""
    
    def test_get_jobs(self, client, auth_headers, test_job):
        """Test getting jobs list"""
        response = client.get('/api/jobs', headers=auth_headers)
        assert response.status_code == 200
    
    def test_create_job(self, client, auth_headers):
        """Test creating a job"""
        response = client.post('/api/jobs', headers=auth_headers, json={
            'title': 'Python Developer',
            'description': 'Looking for Python experts',
            'required_skills': ['Python'],
            'salary_min': 50000,
            'salary_max': 100000
        })
        assert response.status_code in [200, 201]

class TestMatchRoutes:
    """Test cases for match routes"""
    
    def test_get_matches(self, client, auth_headers):
        """Test getting matches"""
        response = client.get('/api/matches', headers=auth_headers)
        assert response.status_code == 200
    
    def test_calculate_matches(self, client, auth_headers, test_candidate, test_job):
        """Test match calculation"""
        response = client.post('/api/matches/calculate', headers=auth_headers)
        assert response.status_code in [200, 201]

class TestHealthRoutes:
    """Test cases for health check routes"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/api/health')
        assert response.status_code == 200

