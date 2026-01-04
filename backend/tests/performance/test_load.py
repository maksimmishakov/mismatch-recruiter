import pytest
import time
from concurrent.futures import ThreadPoolExecutor

class TestPerformance:
    """Performance and load testing"""
    
    @pytest.mark.slow
    def test_large_candidate_list_performance(self, client, auth_headers):
        """Test retrieving large candidate list performance"""
        start_time = time.time()
        response = client.get('/api/candidates?limit=1000', headers=auth_headers)
        elapsed = time.time() - start_time
        
        assert response.status_code == 200
        assert elapsed < 2.0  # Should complete in less than 2 seconds
    
    @pytest.mark.slow
    def test_large_job_list_performance(self, client, auth_headers):
        """Test retrieving large job list performance"""
        start_time = time.time()
        response = client.get('/api/jobs?limit=1000', headers=auth_headers)
        elapsed = time.time() - start_time
        
        assert response.status_code == 200
        assert elapsed < 2.0
    
    @pytest.mark.slow
    def test_concurrent_requests(self, client, auth_headers):
        """Test handling multiple concurrent requests"""
        def make_request():
            return client.get('/api/candidates', headers=auth_headers)
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [f.result() for f in futures]
        
        assert all(r.status_code == 200 for r in results)
    
    def test_database_query_optimization(self, client, auth_headers):
        """Test database queries are optimized"""
        start_time = time.time()
        response = client.get('/api/matches', headers=auth_headers)
        elapsed = time.time() - start_time
        
        assert response.status_code == 200
        assert elapsed < 1.0  # Should be fast with optimizations
    
    def test_response_time_under_load(self, client, auth_headers):
        """Test response time remains acceptable under load"""
        response_times = []
        
        for _ in range(20):
            start = time.time()
            response = client.get('/api/candidates', headers=auth_headers)
            elapsed = time.time() - start
            response_times.append(elapsed)
            assert response.status_code == 200
        
        avg_time = sum(response_times) / len(response_times)
        assert avg_time < 1.0  # Average should be under 1 second

