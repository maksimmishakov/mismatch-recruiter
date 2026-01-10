"""Pytest configuration and fixtures for testing."""

import pytest
import sys
import os
from sqlalchemy.pool import NullPool

# Add backend directory to Python path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, backend_path)
from app import create_app


@pytest.fixture(scope='function')
def app():
    """Create application for testing."""
    app = create_app('testing')
        # Configure SQLAlchemy to use NullPool for SQLite to avoid pool_size errors
    app.config['SQLALCHEMY_ENGINE_OPTIONS']['poolclass'] = NullPool


    
    from app.database import db
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Provides a test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Provides a CLI test runner."""
    return app.test_cli_runner()


@pytest.fixture
def db_session(app):
    """Provides database session for tests."""
    from app.database import db
    with app.app_context():
        yield db.session
        db.session.rollback()
                db.session.close()


# Fixtures for test data

@pytest.fixture
def test_recruiter(db_session):
    """Fixture for a test recruiter user."""
    from app.models import User
    recruiter = User(
        email='recruiter@example.com',
        username='recruiter_test',
        password_hash='hashed_password',
        first_name='Test', last_name='Recruiter',
        role='RECRUITER',
        is_active=True
    )
    db_session.add(recruiter)
    db_session.commit()
    return recruiter


@pytest.fixture
def test_candidate(db_session):
    """Fixture for a test candidate user."""
    from app.models import User, Candidate
    candidate_user = User(
        email='candidate@example.com',
        username='candidate_test',
        password_hash='hashed_password',
        first_name='Test', last_name='Candidate',
        role='CANDIDATE',
        is_active=True
    )
    db_session.add(candidate_user)
    db_session.commit()
    
    candidate = Candidate(
        user_id=candidate_user.id,
        bio='Experienced software engineer',
        skills=['Python', 'JavaScript', 'React'],
        experience_years=5,
        location='San Francisco, CA'
    )
    db_session.add(candidate)
    db_session.commit()
    return candidate


@pytest.fixture
def test_job(db_session, test_recruiter):
    """Fixture for a test job posting."""
    from app.models import Job
    job = Job(
        recruiter_id=test_recruiter.id,
        title='Senior Python Developer',
        description='Looking for experienced Python developer',
        requirements=['Python', 'JavaScript', 'React'],
        location='San Francisco, CA',
        salary_min=120000,
        salary_max=160000,
        is_active=True
    )
    db_session.add(job)
    db_session.commit()
    return job


@pytest.fixture
def test_match(db_session, test_candidate, test_job):
    """Fixture for a test match between candidate and job."""
    from app.models import Match
    match = Match(
        candidate_id=test_candidate.id,
        job_id=test_job.id,
        match_score=0.85,
        status='pending'
    )
    db_session.add(match)
    db_session.commit()
    return match
