from prometheus_client import Counter, Histogram, Gauge

# API Metrics
http_requests_total = Counter(
    'flask_http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'flask_http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint'],
    buckets=(0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0)
)

# Database Metrics
db_connection_pool_size = Gauge(
    'database_connection_pool_size',
    'Database connection pool size'
)

db_connection_pool_checked_out = Gauge(
    'database_connection_pool_checked_out',
    'Database connections checked out'
)

db_queries_total = Counter(
    'database_queries_total',
    'Total database queries',
    ['operation']
)

db_query_duration_seconds = Histogram(
    'database_query_duration_seconds',
    'Database query duration',
    ['operation']
)

# Cache Metrics
cache_hits_total = Counter(
    'cache_hits_total',
    'Total cache hits',
    ['cache_name']
)

cache_misses_total = Counter(
    'cache_misses_total',
    'Total cache misses',
    ['cache_name']
)

# Business Metrics
candidates_created_total = Counter(
    'candidates_created_total',
    'Total candidates created',
    ['user_id']
)

matches_found_total = Gauge(
    'matches_found_total',
    'Total matches found',
    ['status']
)
