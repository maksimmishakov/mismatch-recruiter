"""Tests for API endpoints."""
import json
import pytest


class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check(self, client):
        """Test that health endpoint returns 200 OK."""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'


class TestCandidateAPI:
    """Test Candidate API endpoints."""
    
    def test_get_candidates_empty(self, client):
        """Test getting candidates when none exist."""
        response = client.get('/api/candidates')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['candidates'] == []
    
    def test_create_candidate(self, client):
        """Test creating a new candidate."""
        payload = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '+1234567890',
            'experience_years': 5,
            'skills': ['Python', 'Flask']
        }
        response = client.post('/api/candidates',
                             data=json.dumps(payload),
                             content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'John Doe'
        assert data['email'] == 'john@example.com'


class TestJobAPI:
    """Test Job API endpoints."""
    
    def test_get_jobs_empty(self, client):
        """Test getting jobs when none exist."""
        response = client.get('/api/jobs')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['jobs'] == []
    
    def test_create_job(self, client):
        """Test creating a new job posting."""
        payload = {
            'title': 'Senior Python Developer',
            'description': 'We need a senior developer',
            'required_skills': ['Python', 'Flask', 'PostgreSQL'],
            'salary_min': 100000,
            'salary_max': 150000
        }
        response = client.post('/api/jobs',
                             data=json.dumps(payload),
                             content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['title'] == 'Senior Python Developer'


class TestMatchAPI:
    """Test Match API endpoints."""
    
    def test_get_matches_empty(self, client):
        """Test getting matches when none exist."""
        response = client.get('/api/matches')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['matches'] == []


class TestAuthAPI:
    """Test authentication endpoints."""
    
    def test_register_user(self, client):
        """Test user registration."""
        payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePassword123!'
        }
        response = client.post('/api/auth/register',
                             data=json.dumps(payload),
                             content_type='application/json')
        assert response.status_code in [201, 200]
    
    def test_login_user(self, client):
        """Test user login."""
        # First register a user
        register_payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePassword123!'
        }
        client.post('/api/auth/register',
                   data=json.dumps(register_payload),
                   content_type='application/json')
        
        # Then try to login
        login_payload = {
            'email': 'test@example.com',
            'password': 'SecurePassword123!'
        }
        response = client.post('/api/auth/login',
                             data=json.dumps(login_payload),
                             content_type='application/json')
        assert response.status_code in [200, 201]
