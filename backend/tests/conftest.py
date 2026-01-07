import pytest
from flask import Flask

@pytest.fixture(scope='session')
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def sample_candidate():
    return {
        'name': 'John Doe',
        'email': 'john@example.com',
        'position': 'Senior Developer',
        'status': 'pending'
    }
