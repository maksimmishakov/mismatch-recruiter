"""
E2E Tests - End-to-End Integration Testing
Tests complete user workflows and API integration
"""
import pytest
from app import create_app
import json


class TestE2EWorkflows:
    """Test complete application workflows"""

    def test_health_check_exists(self, client):
        """Test health check endpoint exists and is accessible"""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data or 'ok' in data

    def test_candidates_endpoint_accessible(self, client):
        """Test candidates endpoint is accessible"""
        response = client.get('/api/candidates')
        # Endpoint exists and returns appropriate response
        assert response.status_code in [200, 204]

    def test_invalid_endpoint_returns_404(self, client):
        """Test invalid endpoint returns 404"""
        response = client.get('/api/nonexistent/route')
        assert response.status_code == 404


class TestE2EPerformance:
    """Test application performance under normal conditions"""

    def test_rapid_health_checks(self, client):
        """Test application handles rapid health checks"""
        responses = []
        for i in range(3):
            response = client.get('/api/health')
            responses.append(response.status_code)
        
        # All health checks should succeed
        assert all(code == 200 for code in responses)

    def test_error_response_consistency(self, client):
        """Test error responses are consistent"""
        # Multiple 404 errors should all return consistent status codes
        for endpoint in ['/api/missing1', '/api/missing2', '/api/missing3']:
            response = client.get(endpoint)
            assert response.status_code == 404

    def test_available_endpoints(self, client):
        """Test key application endpoints are available"""
        # Test endpoints that exist
        endpoints_get = [
            '/api/health',
            '/api/candidates',
        ]
        
        for endpoint in endpoints_get:
            response = client.get(endpoint)
            # All endpoints should exist (not return 404)
            assert response.status_code != 404, f"{endpoint} not found"

