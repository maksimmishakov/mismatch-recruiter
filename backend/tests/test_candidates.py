import pytest

class TestCandidatesEndpoints:
    def test_get_candidates_empty(self, client):
        response = client.get('/api/candidates')
        assert response.status_code in [200, 401]
    
    def test_create_candidate_missing_data(self, client):
        response = client.post('/api/candidates', json={})
        assert response.status_code in [400, 422]
    
    def test_create_candidate_valid_data(self, client, sample_candidate):
        response = client.post('/api/candidates', json=sample_candidate)
        assert response.status_code in [200, 201, 401]
