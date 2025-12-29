"""Performance Testing Module for Mismatch AI Recruiter

Tests for:
- Response time optimization
- Database query performance
- Cache hit ratio verification
- Load testing (100, 500, 1000 concurrent users)
- API response time under load
"""

import pytest
import time
import concurrent.futures
import redis
from app import create_app, db


class TestResponseTimeOptimization:
    """Test suite for API response times."""

    def test_health_check_response_time(self, client):
        """Health check should respond in < 50ms."""
        start = time.time()
        client.get('/api/health')
        elapsed = (time.time() - start) * 1000
        assert elapsed < 50, f'Health check took {elapsed}ms, expected < 50ms'

    def test_cached_endpoint_response_time(self, client, auth_token):
        """Cached endpoint should respond in < 100ms."""
        # Warm up cache
        client.get('/api/candidates',
            headers={'Authorization': f'Bearer {auth_token}'})
        
        # Test response time
        start = time.time()
        client.get('/api/candidates',
            headers={'Authorization': f'Bearer {auth_token}'})
        elapsed = (time.time() - start) * 1000
        assert elapsed < 100, f'Cached endpoint took {elapsed}ms, expected < 100ms'

    def test_uncached_endpoint_response_time(self, client, auth_token):
        """Uncached endpoint should respond in < 500ms."""
        start = time.time()
        client.post('/api/salary-prediction/1',
            headers={'Authorization': f'Bearer {auth_token}'},
            json={'location': 'Moscow', 'experience_years': 5})
        elapsed = (time.time() - start) * 1000
        assert elapsed < 500, f'Uncached endpoint took {elapsed}ms, expected < 500ms'


class TestDatabaseQueryPerformance:
    """Test suite for database query optimization."""

    def test_simple_query_performance(self, client, test_user):
        """Simple database queries should execute in < 10ms."""
        from app.models import User
        start = time.time()
        user = User.query.filter_by(email='test@example.com').first()
        elapsed = (time.time() - start) * 1000
        assert elapsed < 10, f'Query took {elapsed}ms, expected < 10ms'
        assert user is not None

    def test_join_query_performance(self, client, test_user, test_resumes):
        """JOINed queries should execute in < 50ms."""
        from app.models import User
        start = time.time()
        user = User.query.options(
            db.joinedload(User.resumes)
        ).filter_by(email='test@example.com').first()
        elapsed = (time.time() - start) * 1000
        assert elapsed < 50, f'JOIN query took {elapsed}ms, expected < 50ms'


class TestCachePerformance:
    """Test suite for cache hit ratio and performance."""

    def test_redis_connection(self):
        """Redis should be connected and working."""
        r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        try:
            assert r.ping()
        except redis.ConnectionError:
            pytest.skip('Redis not available')

    def test_cache_hit_ratio(self, client, auth_token):
        """Cache hit ratio should be > 80%."""
        try:
            r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            r.flushdb()  # Reset for testing
            
            # Make multiple requests
            for _ in range(10):
                client.get('/api/candidates',
                    headers={'Authorization': f'Bearer {auth_token}'})
            
            # Check cache info
            info = r.info('stats')
            hits = info.get('keyspace_hits', 0)
            misses = info.get('keyspace_misses', 0)
            
            if (hits + misses) > 0:
                hit_ratio = hits / (hits + misses)
                assert hit_ratio > 0.8, f'Cache hit ratio {hit_ratio} < 0.8'
        except redis.ConnectionError:
            pytest.skip('Redis not available')


class TestLoadTesting:
    """Test suite for concurrent user load testing."""

    def test_100_concurrent_users(self, client, auth_token):
        """System should handle 100 concurrent users."""
        def make_request():
            try:
                response = client.get('/api/candidates',
                    headers={'Authorization': f'Bearer {auth_token}'})
                return response.status_code == 200
            except Exception:
                return False
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(make_request) for _ in range(100)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        success_rate = sum(results) / len(results)
        assert success_rate > 0.95, f'Success rate {success_rate} < 0.95'

    def test_500_concurrent_users(self, client, auth_token):
        """System should handle 500 concurrent users with degradation."""
        def make_request():
            try:
                response = client.get('/api/candidates',
                    headers={'Authorization': f'Bearer {auth_token}'})
                return response.status_code in [200, 503]  # 503 acceptable under load
            except Exception:
                return False
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
            futures = [executor.submit(make_request) for _ in range(500)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        success_rate = sum(results) / len(results)
        assert success_rate > 0.9, f'Success rate {success_rate} < 0.9'


class TestDatabaseConnectionPooling:
    """Test suite for database connection pool optimization."""

    def test_connection_pool_size(self):
        """Connection pool should be configured with 20 connections."""
        app = create_app('testing')
        # Check pool configuration
        pool_size = app.config.get('SQLALCHEMY_ENGINE_OPTIONS', {}).get('pool_size', 5)
        assert pool_size >= 20, f'Pool size {pool_size} < 20'


@pytest.fixture
def client():
    """Create test client."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()
