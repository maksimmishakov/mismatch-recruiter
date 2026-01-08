"""Pytest configuration and fixtures for testing."""

import pytest
from backend.app import create_app
from backend.app.database import db
import os


@pytest.fixture(scope='session')
def app():
    """Create application for testing."""
    app = create_app('testing')
    
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
    with app.app_context():
        yield db.session
        db.session.rollback()
