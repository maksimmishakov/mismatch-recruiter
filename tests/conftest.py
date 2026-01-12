import pytest
from app import create_app, db


@pytest.fixture(scope='function')
def app():
    """Create application for testing"""
    app_instance = create_app('testing')
    with app_instance.app_context():
        db.create_all()
        yield app_instance
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Test client"""
    return app.test_client()


@pytest.fixture(autouse=True)
def reset_db(app):
    """Reset database between tests"""
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
        yield
        db.session.remove()
