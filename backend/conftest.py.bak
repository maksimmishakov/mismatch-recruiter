"""Root pytest configuration for backend tests."""
import os
import pytest
from flask_sqlalchemy import SQLAlchemy

# Set test environment BEFORE app creation
os.environ['FLASK_ENV'] = 'testing'
os.environ['DATABASE_URL'] = 'postgresql://test:test@localhost:5432/testmismatch'
os.environ['JWT_SECRET_KEY'] = 'test-secret-key-do-not-use-in-production'

from app import create_app, db

@pytest.fixture(scope='session')
def app():
    """Create and configure app for testing session."""
    app = create_app('development')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Flask CLI runner."""
    return app.test_cli_runner()

@pytest.fixture
def db_session(app):
    """Database session for tests."""
    connection = db.engine.connect()
    transaction = connection.begin()
    session = db.Session(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()
