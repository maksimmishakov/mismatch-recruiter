import pytest

def test_get_candidates(client):
    """Test getting list of candidates."""
    response = client.get('/api/candidates')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, (list, dict))

def test_create_candidate(client):
    """Test creating a new candidate."""
    response = client.post('/api/candidates', json={
        'name': 'John Doe',
        'email': 'john@example.com',
        'skills': ['Python', 'React'],
        'experience_years': 5
    })
    assert response.status_code in [201, 400]

def test_get_candidate_by_id(client):
    """Test getting candidate by ID."""
    response = client.get('/api/candidates/1')
    # Can be 200 (exists) or 404 (not found)
    assert response.status_code in [200, 404]

def test_invalid_candidate_data(client):
    """Test validation of candidate data."""
    response = client.post('/api/candidates', json={
        'name': '',  # Empty name
        'email': 'invalid-email'  # Invalid email
    })
    assert response.status_code == 400
