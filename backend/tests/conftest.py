"""Pytest configuration and fixtures for testing."""

import pytest
import sys
import os
from sqlalchemy.pool import NullPool

# Add backend directory to Python path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, backend_path)
from app import create_app


@pytest.fixture(scope='session')
def app():
    """Create application for testing."""
    app = create_app('testing')
        # Configure SQLAlchemy to use NullPool for SQLite to avoid pool_size errors
    app.config['SQLALCHEMY_ENGINE_OPTIONS']['poolclass'] = NullPool


    
    from app.models import db
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
    from app.models import db
    with app.app_context():
        yield db.session
        db.session.rollback()
