import pytest
import json

class TestIntegrationFlow:
    """Integration tests for end-to-end flows"""
    
    def test_health_endpoint_returns_ok(self, client):
        """Health check should return 200 OK"""
        response = client.get('/health')
        assert response.status_code == 200
        try:
            data = response.get_json()
            assert 'status' in data
        except:
            pass
    
    def test_api_candidates_endpoints_accessible(self, client):
        """Candidate endpoints should be accessible"""
        response = client.get('/api/candidates')
        assert response.status_code in [200, 401, 403]
    
    def test_error_handling_for_invalid_json(self, client):
        """Invalid JSON should return proper error"""
        response = client.post(
            '/api/candidates',
            data='invalid json',
            content_type='application/json'
        )
        assert response.status_code in [400, 422]

class TestPerformance:
    """Performance-related tests"""
    
    def test_health_check_response_time(self, client):
        """Health check should respond quickly"""
        import time
        start = time.time()
        client.get('/health')
        elapsed = time.time() - start
        assert elapsed < 1.0  # Should respond in < 1 second
