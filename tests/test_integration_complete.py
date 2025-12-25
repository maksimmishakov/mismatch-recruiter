"""Comprehensive integration tests for the complete workflow.
"""
import pytest
import json
from datetime import datetime


class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_check(self, client):
        """Test GET /health endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data
        assert data['status'] == 'healthy'


class TestAuthenticationFlow:
    """Test authentication and user registration."""

    def test_user_registration(self, client, db):
        """Test user registration endpoint."""
        user_data = {
            'email': 'testuser@example.com',
            'password': 'securepassword123',
            'name': 'Test User'
        }
        response = client.post('/api/register', json=user_data)
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'user_id' in data
        assert data['email'] == user_data['email']

    def test_user_login(self, client, user_fixture):
        """Test user login endpoint."""
        login_data = {
            'email': user_fixture['email'],
            'password': user_fixture['password']
        }
        response = client.post('/api/login', json=login_data)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'token' in data
        assert 'user_id' in data


class TestResumeMatching:
    """Test resume-to-job matching functionality."""

    def test_resume_upload(self, client, auth_token):
        """Test resume upload endpoint."""
        resume_data = {
            'content': 'Python Developer with 5 years experience',
            'skills': ['Python', 'Django', 'PostgreSQL'],
            'experience': 5
        }
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.post('/api/resumes', json=resume_data, headers=headers)
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'resume_id' in data

    def test_job_matching(self, client, auth_token, resume_fixture, job_fixture):
        """Test resume-to-job matching."""
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.post(
            f'/api/resumes/{resume_fixture["id"]}/match',
            json={'job_id': job_fixture['id']},
            headers=headers
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'match_score' in data
        assert 0 <= data['match_score'] <= 100


class TestGraphQLEndpoint:
    """Test GraphQL endpoint."""

    def test_graphql_query_resumes(self, client, auth_token):
        """Test GraphQL query for resumes."""
        query = '{resumes(limit: 10) {id content skills createdAt}}'
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.post(
            '/graphql',
            json={'query': query},
            headers=headers
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data

    def test_graphql_query_jobs(self, client, auth_token):
        """Test GraphQL query for jobs."""
        query = '{jobs(status: "open", limit: 10) {id title company}}'
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.post(
            '/graphql',
            json={'query': query},
            headers=headers
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data


class TestErrorHandling:
    """Test error handling and validation."""

    def test_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        login_data = {
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }
        response = client.post('/api/login', json=login_data)
        assert response.status_code == 401

    def test_unauthorized_access(self, client):
        """Test access without authentication."""
        response = client.get('/api/admin/metrics')
        assert response.status_code == 401


@pytest.fixture
def client():
    """Flask test client fixture."""
    from app import create_app
    app = create_app('testing')
    with app.test_client() as client:
        yield client


@pytest.fixture
def db():
    """Database fixture."""
    from app import db as database
    database.create_all()
    yield database
    database.session.remove()
    database.drop_all()


@pytest.fixture
def user_fixture(db):
    """Create test user."""
    from app.models import User
    user = User(
        email='testuser@example.com',
        password='securepassword123',
        name='Test User'
    )
    db.session.add(user)
    db.session.commit()
    return user.__dict__


@pytest.fixture
def auth_token(client, user_fixture):
    """Get authentication token for test user."""
    response = client.post('/api/login', json={
        'email': user_fixture['email'],
        'password': user_fixture['password']
    })
    return json.loads(response.data)['token']


@pytest.fixture
def resume_fixture(db, user_fixture):
    """Create test resume."""
    from app.models import Resume
    resume = Resume(
        user_id=user_fixture['id'],
        content='Senior Python Developer with 8 years experience',
        skills=['Python', 'Django', 'PostgreSQL', 'AWS'],
        experience=8
    )
    db.session.add(resume)
    db.session.commit()
    return resume.__dict__


@pytest.fixture
def job_fixture(db):
    """Create test job."""
    from app.models import Job
    job = Job(
        title='Senior Python Developer',
        company='Tech Company',
        description='Looking for experienced Python developer',
        skills=['Python', 'Django'],
        min_salary=80000,
        max_salary=120000,
        status='open'
    )
    db.session.add(job)
    db.session.commit()
    return job.__dict__
