import pytest

class TestHealth:
    """Test health check endpoints."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json == {'status': 'healthy'}

    def test_api_root(self, client):
        """Test API root endpoint."""
        response = client.get('/api')
        assert response.status_code == 200
        assert 'version' in response.json or response.status_code == 404  # Accept both
