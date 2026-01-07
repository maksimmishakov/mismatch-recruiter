import pytest

class TestAuthEndpoints:
    def test_health_check(self, client):
        response = client.get('/health')
        assert response.status_code == 200
    
    def test_login_missing_credentials(self, client):
        response = client.post('/login', json={})
        assert response.status_code in [400, 401, 422]
    
    def test_login_invalid_credentials(self, client):
        response = client.post('/login', json={
            'username': 'invalid',
            'password': 'invalid'
        })
        assert response.status_code in [401, 404]
