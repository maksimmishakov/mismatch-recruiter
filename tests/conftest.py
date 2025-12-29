import pytest
import os
from app import create_app

@pytest.fixture(scope='session')
def app():
    """Create and configure a Flask app for testing."""
    os.environ['TESTING'] = 'True'
    app = create_app(config_name='testing')
    return app

@pytest.fixture(scope='function')
def client(app):
    """Provide a test client for making requests."""
    return app.test_client()

@pytest.fixture(scope='function')
def runner(app):
    """Provide a click CLI test runner."""
    return app.test_cli_runner()
