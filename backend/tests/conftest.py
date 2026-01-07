"""Pytest configuration and fixtures for testing."""
import os
import pytest
from flask import Flask
from app import create_app
from app.extensions import db


@pytest.fixture(scope='session')
def app():
    """Create and configure a Flask test app."""
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    os.environ['SECRET_KEY'] = 'test-secret-key'
    
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Flask test client."""
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """Flask CLI runner."""
    return app.test_cli_runner()


@pytest.fixture(scope='function')
def db_session(app):
    """Database session for tests."""
    with app.app_context():
        yield db.session
        db.session.rollback()
