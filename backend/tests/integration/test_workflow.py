import pytest
from app.models import User, Candidate, Job, Match

class TestCompleteWorkflow:
    """Test complete user workflow"""
    
    def test_user_registration_and_login(self, client):
        """Test user can register and login"""
        # Register
        register_response = client.post('/api/auth/register', json={
            'email': 'workflow@test.com',
            'name': 'Workflow User',
            'password': 'password123'
        })
        assert register_response.status_code in [200, 201]
        
        # Login
        login_response = client.post('/api/auth/login', json={
            'email': 'workflow@test.com',
            'password': 'password123'
        })
        assert login_response.status_code == 200
        assert 'access_token' in login_response.json
    
    def test_candidate_job_matching_workflow(self, client, auth_headers, test_user):
        """Test complete matching workflow"""
        # Create candidate
        candidate_response = client.post('/api/candidates', 
            headers=auth_headers, json={
            'skills': ['Python', 'SQL', 'Flask'],
            'experience_years': 5,
            'salary_expectation': 100000
        })
        assert candidate_response.status_code in [200, 201]
        
        # Create job
        job_response = client.post('/api/jobs', 
            headers=auth_headers, json={
            'title': 'Python Developer',
            'description': 'Looking for senior Python developer',
            'required_skills': ['Python', 'Flask'],
            'salary_min': 80000,
            'salary_max': 120000
        })
        assert job_response.status_code in [200, 201]
        
        # Calculate matches
        match_response = client.post('/api/matches/calculate', 
            headers=auth_headers)
        assert match_response.status_code in [200, 201]
        
        # Get matches
        get_matches_response = client.get('/api/matches', 
            headers=auth_headers)
        assert get_matches_response.status_code == 200

class TestErrorHandling:
    """Test error handling in workflows"""
    
    def test_missing_auth_header(self, client):
        """Test request without auth header"""
        response = client.get('/api/candidates')
        assert response.status_code == 401
    
    def test_invalid_candidate_data(self, client, auth_headers):
        """Test creating candidate with invalid data"""
        response = client.post('/api/candidates', 
            headers=auth_headers, json={
            'skills': [],
            'experience_years': -5
        })
        assert response.status_code == 400
    
    def test_invalid_job_salary_range(self, client, auth_headers):
        """Test creating job with invalid salary range"""
        response = client.post('/api/jobs', 
            headers=auth_headers, json={
            'title': 'Test Job',
            'description': 'Test',
            'required_skills': ['Python'],
            'salary_min': 120000,
            'salary_max': 80000
        })
        assert response.status_code == 400

