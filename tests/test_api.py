"""API endpoint tests"""
import pytest
from app import create_app, db

@pytest.fixture
def app():
    """Create app for testing"""
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Test client"""
    return app.test_client()

def test_index(client):
    """Test GET /"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'MisMatch' in response.data

def test_health(client):
    """Test GET /api/health"""
    response = client.get('/api/health')
    assert response.status_code == 200
    assert b'healthy' in response.data

def test_get_candidates_empty(client):
    """Test GET /api/candidates when empty"""
    response = client.get('/api/candidates')
    assert response.status_code == 200
    assert response.json['count'] == 0

def test_create_candidate(client):
    """Test POST /api/candidate"""
    data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'phone': '1234567890',
        'position': 'Developer',
        'skills': ['Python', 'Flask']
    }
    response = client.post('/api/candidate', json=data)
    assert response.status_code == 201
    assert response.json['success']
    assert response.json['candidate']['name'] == 'John Doe'

def test_get_candidate(client):
    """Test GET /api/candidate/<id>"""
    # Create first
    data = {'name': 'Jane', 'email': 'jane@test.com'}
    resp = client.post('/api/candidate', json=data)
    cand_id = resp.json['candidate_id']
    
    # Get it
    response = client.get(f'/api/candidate/{cand_id}')
    assert response.status_code == 200
    assert response.json['name'] == 'Jane'

def test_404(client):
    """Test 404 handling"""
    response = client.get('/api/nonexistent')
    assert response.status_code == 404
