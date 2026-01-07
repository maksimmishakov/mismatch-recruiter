import pytest
from app import create_app, db
from app.models import User, Candidate, JobPosting, Match

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Test client"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Test CLI runner"""
    return app.test_cli_runner()

@pytest.fixture
def test_user(app):
    """Create a test user"""
    user = User(
        email='test@example.com',
        username='testuser',
        full_name='Test User'
    )
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def test_candidate(app):
    """Create a test candidate"""
    candidate = Candidate(
        first_name='John',
        last_name='Doe',
        email='john@example.com',
        skills=['Python', 'Flask', 'Docker'],
        experience_years=5
    )
    db.session.add(candidate)
    db.session.commit()
    return candidate

@pytest.fixture
def test_job(app):
    """Create a test job posting"""
    job = JobPosting(
        title='Senior Python Developer',
        description='Looking for an experienced Python developer',
        company='TechCorp',
        location='San Francisco, CA',
        salary_min=120000,
        salary_max=160000,
        required_skills=['Python', 'Flask', 'Docker'],
        experience_level='senior'
    )
    db.session.add(job)
    db.session.commit()
    return job
