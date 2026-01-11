import pytest
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app import create_app, db

@pytest.fixture(scope='session')
def app():
    """Create application for tests."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Test client."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Test CLI runner."""
    return app.test_cli_runner()

@pytest.fixture
def db_session(app):
    """Database session for tests."""
    with app.app_context():
        yield db.session
        db.session.rollback()
