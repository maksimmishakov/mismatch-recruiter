"""Rate limiting middleware for API endpoints."""
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Rate limit configurations for different endpoints
RATE_LIMIT_CONFIG = {
    'default': '100 per hour',
    'auth': '5 per minute',
    'api_critical': '10 per minute',
    'api_standard': '60 per hour',
    'api_heavy': '20 per hour',
    'upload': '10 per hour',
}


def get_rate_limit_key():
    """Custom key function for rate limiting based on user or IP."""
    from flask import request, g
    
    # Try to get user ID from g object (set during authentication)
    if hasattr(g, 'user') and g.user:
        return f'user:{g.user.id}'
    
    # Fall back to IP address
    return get_remote_address()


def rate_limit_error_handler(e):
    """Custom error handler for rate limit exceeded."""
    from flask import jsonify
    
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': str(e.description),
        'status': 'error'
    }), 429


def init_rate_limiter(app):
    """Initialize rate limiter with app."""
    limiter.init_app(app)
    app.errorhandler(429)(rate_limit_error_handler)
    return limiter

