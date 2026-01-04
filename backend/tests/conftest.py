import pytest
import os
from app import create_app, db
from app.models import User, Candidate, Job, Match

@pytest.fixture
def app():
    """Create application for tests"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Test client for the app"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """CLI runner for the app"""
    return app.test_cli_runner()

@pytest.fixture
def auth_headers(client):
    """Create test user and return auth headers"""
    user = User(email='test@example.com', name='Test User')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def test_user():
    """Create test user"""
    user = User(email='user@test.com', name='Test User')
    user.set_password('testpass')
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def test_candidate(test_user):
    """Create test candidate"""
    candidate = Candidate(
        user_id=test_user.id,
        skills=['Python', 'Flask'],
        experience_years=5,
        salary_expectation=100000
    )
    db.session.add(candidate)
    db.session.commit()
    return candidate

@pytest.fixture
def test_job(test_user):
    """Create test job"""
    job = Job(
        user_id=test_user.id,
        title='Senior Python Developer',
        description='We are looking for a Python expert',
        required_skills=['Python', 'Flask'],
        salary_min=80000,
        salary_max=120000
    )
    db.session.add(job)
    db.session.commit()
    return job

