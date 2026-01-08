import pytest
from app import create_app, db

class TestHealth:
    """Health check endpoint tests"""
    
    def test_health_endpoint_success(self, client):
        """Test health endpoint returns healthy status"""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert 'service' in data
    
    def test_health_endpoint_json_format(self, client):
        """Test health endpoint returns proper JSON"""
        response = client.get('/api/health')
        assert response.content_type == 'application/json'
        data = response.get_json()
        assert isinstance(data, dict)
