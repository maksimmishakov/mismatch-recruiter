import pytest
from app import create_app

@pytest.fixture
def app():
    """Create and configure test app."""
    app = create_app('testing')
    return app

@pytest.fixture
def client(app):
    """Test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """CLI runner for the app."""
    return app.test_cli_runner()
