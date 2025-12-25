"""Prometheus Metrics Service - Comprehensive Monitoring"""
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CollectorRegistry
from functools import wraps
import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Create registry
registry = CollectorRegistry()

# Define metrics
REQUEST_COUNT = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status'],
    registry=registry
)

REQUEST_DURATION = Histogram(
    'api_request_duration_seconds',
    'API request duration',
    ['method', 'endpoint'],
    registry=registry
)

DB_QUERIES = Counter(
    'database_queries_total',
    'Total database queries',
    ['operation', 'table', 'status'],
    registry=registry
)

DB_QUERY_DURATION = Histogram(
    'database_query_duration_seconds',
    'Database query duration',
    ['operation', 'table'],
    registry=registry
)

CACHE_HITS = Counter(
    'cache_hits_total',
    'Total cache hits',
    ['key'],
    registry=registry
)

CACHE_MISSES = Counter(
    'cache_misses_total',
    'Total cache misses',
    ['key'],
    registry=registry
)

ACTIVE_CONNECTIONS = Gauge(
    'active_connections',
    'Number of active connections',
    registry=registry
)

ERROR_COUNT = Counter(
    'errors_total',
    'Total errors',
    ['type', 'endpoint'],
    registry=registry
)

def track_request(func):
    """Decorator to track API request metrics"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        status = 200
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            status = 500
            raise
        finally:
            duration = time.time() - start
            endpoint = getattr(func, '__name__', 'unknown')
            REQUEST_DURATION.labels(method='GET', endpoint=endpoint).observe(duration)
            REQUEST_COUNT.labels(method='GET', endpoint=endpoint, status=status).inc()
    return wrapper

def get_metrics():
    """Get all metrics in Prometheus format"""
    return generate_latest(registry)

class MetricsService:
    """Central metrics service for monitoring"""
    
    @staticmethod
    def increment_request(method, endpoint, status):
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
    
    @staticmethod
    def observe_request_duration(method, endpoint, duration):
        REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)
    
    @staticmethod
    def increment_db_query(operation, table, status='success'):
        DB_QUERIES.labels(operation=operation, table=table, status=status).inc()
    
    @staticmethod
    def observe_db_query_duration(operation, table, duration):
        DB_QUERY_DURATION.labels(operation=operation, table=table).observe(duration)
    
    @staticmethod
    def increment_cache_hit(key):
        CACHE_HITS.labels(key=key).inc()
    
    @staticmethod
    def increment_cache_miss(key):
        CACHE_MISSES.labels(key=key).inc()
    
    @staticmethod
    def set_active_connections(count):
        ACTIVE_CONNECTIONS.set(count)
    
    @staticmethod
    def increment_error(error_type, endpoint):
        ERROR_COUNT.labels(type=error_type, endpoint=endpoint).inc()
