"""Comprehensive API Endpoint Tests for Mismatch AI Recruiter

This module contains comprehensive tests for all API endpoints including:
- Health check endpoint
- Authentication endpoints (register, login)
- Candidate management endpoints
- Salary prediction endpoint
- Resume-to-job matching endpoint
- Subscription endpoint
- Admin dashboard endpoint
"""

import pytest
import json
from datetime import datetime, timedelta
from app import create_app, db
from app.models import User, Resume, Job, Match, Prediction, Subscription


class TestHealthCheckEndpoint:
    """Test suite for health check endpoint."""

    def test_health_check_returns_200(self, client):
        """Health check should return 200 OK."""
        response = client.get('/api/health')
        assert response.status_code == 200

    def test_health_check_response_format(self, client):
        """Health check should return correct JSON format."""
        response = client.get('/api/health')
        data = json.loads(response.data)
        assert 'status' in data
        assert 'timestamp' in data
        assert 'version' in data
        assert data['status'] == 'healthy'

    def test_health_check_no_auth_required(self, client):
        """Health check should not require authentication."""
        response = client.get('/api/health')
        assert response.status_code == 200
        assert response.json['status'] == 'healthy'


class TestAuthEndpoints:
    """Test suite for authentication endpoints."""

    def test_register_success(self, client):
        """User registration should succeed with valid data."""
        response = client.post('/api/auth/register',
            json={
                'email': 'test@example.com',
                'password': 'SecurePassword123!',
                'name': 'Test User'
            })
        assert response.status_code == 201
        data = response.json
        assert 'user_id' in data
        assert 'token' in data
        assert data['email'] == 'test@example.com'

    def test_register_invalid_email(self, client):
        """Registration should fail with invalid email."""
        response = client.post('/api/auth/register',
            json={
                'email': 'invalid-email',
                'password': 'SecurePassword123!',
                'name': 'Test User'
            })
        assert response.status_code == 400

    def test_register_weak_password(self, client):
        """Registration should fail with weak password."""
        response = client.post('/api/auth/register',
            json={
                'email': 'test@example.com',
                'password': 'weak',
                'name': 'Test User'
            })
        assert response.status_code == 400

    def test_register_duplicate_email(self, client):
        """Registration should fail with duplicate email."""
        # First registration
        client.post('/api/auth/register',
            json={
                'email': 'duplicate@example.com',
                'password': 'SecurePassword123!',
                'name': 'First User'
            })
        # Second registration with same email
        response = client.post('/api/auth/register',
            json={
                'email': 'duplicate@example.com',
                'password': 'AnotherPassword123!',
                'name': 'Second User'
            })
        assert response.status_code == 409

    def test_login_success(self, client, test_user):
        """User login should succeed with valid credentials."""
        response = client.post('/api/auth/login',
            json={
                'email': 'test@example.com',
                'password': 'TestPassword123!'
            })
        assert response.status_code == 200
        data = response.json
        assert 'token' in data
        assert 'expires_in' in data
        assert data['expires_in'] == 86400  # 24 hours

    def test_login_invalid_email(self, client):
        """Login should fail with non-existent email."""
        response = client.post('/api/auth/login',
            json={
                'email': 'nonexistent@example.com',
                'password': 'SomePassword123!'
            })
        assert response.status_code == 401

    def test_login_invalid_password(self, client, test_user):
        """Login should fail with wrong password."""
        response = client.post('/api/auth/login',
            json={
                'email': 'test@example.com',
                'password': 'WrongPassword123!'
            })
        assert response.status_code == 401


class TestCandidatesEndpoint:
    """Test suite for candidates endpoint."""

    def test_get_candidates_requires_auth(self, client):
        """GET /api/candidates should require authentication."""
        response = client.get('/api/candidates')
        assert response.status_code == 401

    def test_get_candidates_success(self, client, auth_token, test_candidates):
        """GET /api/candidates should return list of candidates."""
        response = client.get('/api/candidates',
            headers={'Authorization': f'Bearer {auth_token}'})
        assert response.status_code == 200
        data = response.json
        assert 'candidates' in data
        assert 'total' in data
        assert 'page' in data
        assert 'per_page' in data
        assert len(data['candidates']) > 0

    def test_get_candidates_pagination(self, client, auth_token, test_candidates):
        """GET /api/candidates should support pagination."""
        response = client.get('/api/candidates?page=1&per_page=5',
            headers={'Authorization': f'Bearer {auth_token}'})
        assert response.status_code == 200
        data = response.json
        assert data['page'] == 1
        assert data['per_page'] == 5
        assert len(data['candidates']) <= 5

    def test_get_candidates_filtering(self, client, auth_token):
        """GET /api/candidates should support filtering."""
        response = client.get('/api/candidates?skills=Python',
            headers={'Authorization': f'Bearer {auth_token}'})
        assert response.status_code == 200
        data = response.json
        # All returned candidates should have Python skill
        for candidate in data['candidates']:
            assert 'Python' in candidate.get('skills', [])


class TestSalaryPredictionEndpoint:
    """Test suite for salary prediction endpoint."""

    def test_salary_prediction_requires_auth(self, client):
        """Salary prediction should require authentication."""
        response = client.post('/api/salary-prediction/1',
            json={'location': 'Moscow', 'experience_years': 5})
        assert response.status_code == 401

    def test_salary_prediction_success(self, client, auth_token, test_candidate):
        """Salary prediction should return prediction data."""
        response = client.post(f'/api/salary-prediction/{test_candidate.id}',
            headers={'Authorization': f'Bearer {auth_token}'},
            json={
                'location': 'Moscow',
                'experience_years': 5,
                'skills': ['Python', 'FastAPI', 'PostgreSQL']
            })
        assert response.status_code == 200
        data = response.json
        assert 'predicted_salary' in data
        assert 'salary_range' in data
        assert 'confidence' in data
        assert 'factors' in data
        assert 0 <= data['confidence'] <= 1

    def test_salary_prediction_invalid_candidate(self, client, auth_token):
        """Salary prediction should fail for non-existent candidate."""
        response = client.post('/api/salary-prediction/99999',
            headers={'Authorization': f'Bearer {auth_token}'},
            json={'location': 'Moscow', 'experience_years': 5})
        assert response.status_code == 404


class TestMatchResume ToJobEndpoint:
    """Test suite for resume-to-job matching endpoint."""

    def test_match_requires_auth(self, client):
        """Match endpoint should require authentication."""
        response = client.post('/api/match-resume-to-job/1/1', json={})
        assert response.status_code == 401

    def test_match_success(self, client, auth_token, test_resume, test_job):
        """Match endpoint should return match data."""
        response = client.post(
            f'/api/match-resume-to-job/{test_resume.id}/{test_job.id}',
            headers={'Authorization': f'Bearer {auth_token}'},
            json={})
        assert response.status_code == 200
        data = response.json
        assert 'match_score' in data
        assert 'match_level' in data
        assert 'skill_match' in data
        assert 'recommendation' in data
        assert 0 <= data['match_score'] <= 1

    def test_match_invalid_resume(self, client, auth_token, test_job):
        """Match should fail for non-existent resume."""
        response = client.post(
            f'/api/match-resume-to-job/99999/{test_job.id}',
            headers={'Authorization': f'Bearer {auth_token}'},
            json={})
        assert response.status_code == 404


@pytest.fixture
def client():
    """Create test client."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


@pytest.fixture
def test_user(client):
    """Create test user."""
    from app.models import User
    user = User(
        email='test@example.com',
        name='Test User'
    )
    user.set_password('TestPassword123!')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def auth_token(client, test_user):
    """Get authentication token for test user."""
    response = client.post('/api/auth/login',
        json={
            'email': 'test@example.com',
            'password': 'TestPassword123!'
        })
    return response.json['token']
