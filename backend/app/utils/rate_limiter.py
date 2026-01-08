"""Rate limiting configuration for API endpoints."""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Create limiter instance
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)


# Define specific rate limits for endpoints
AUTH_LIMITS = {
    'register': "5 per hour",
    'login': "10 per minute",
    'refresh': "30 per hour"
}

API_LIMITS = {
    'candidates_list': "100 per hour",
    'candidates_create': "20 per hour",
    'jobs_list': "100 per hour",
    'jobs_create': "20 per hour",
    'matches_list': "100 per hour",
    'matches_create': "50 per hour",
}
