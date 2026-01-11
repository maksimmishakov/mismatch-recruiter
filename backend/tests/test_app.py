import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_app_creation(app):
    """Test that app is created successfully."""
    assert app is not None
    assert app.config['TESTING'] is True

def test_app_context(app):
    """Test app context."""
    with app.app_context():
        assert True

def test_client_available(client):
    """Test that test client is available."""
    assert client is not None
