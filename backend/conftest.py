"""Test configuration and fixtures."""

import os
import pytest
from flask import Flask
from app.models import db, User, Candidate, Job, Match, UserRole
from app.api.routes import api_bp

# Удаляем переменные окружения которые могут помешать
for key in list(os.environ.keys()):
    if 'DATABASE' in key or 'FLASK' in key:
        os.environ.pop(key, None)

@pytest.fixture(scope='function')
def app():
    """Create application for testing with SQLite in memory."""
    # Создаём приложение с нулевой конфигурацией
    app = Flask(__name__)
    
    # Устанавливаем конфигурацию ПЕРЕД инициализацией SQLAlchemy
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    # Инициализируем SQLAlchemy
    db.init_app(app)
    
    # Регистрируем blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
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
def test_user(app):
    """Create test user."""
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com',
            role=UserRole.RECRUITER,
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture
def test_candidate(app, test_user):
    """Create test candidate."""
    with app.app_context():
        candidate = Candidate(
            name='John Doe',
        first_name='John',
            email='john@example.com',
            skills=['Python', 'JavaScript'],
            experience_years=3,
            experience_level='junior',
            recruiter_id=test_user.id,
        )
        db.session.add(candidate)
        db.session.commit()
        return candidate

@pytest.fixture
def test_job(app, test_user):
    """Create test job."""
    with app.app_context():
        job = Job(
            title='Python Developer',
            description='We are looking for a Python developer',
            company='Tech Company',
            location='Moscow',
            required_skills=['Python', 'Flask'],
            experience_level='junior',
            min_experience_years=1,
            recruiter_id=test_user.id,
        )
        db.session.add(job)
        db.session.commit()
        return job
