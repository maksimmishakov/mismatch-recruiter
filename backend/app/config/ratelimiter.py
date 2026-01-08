import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Rate limit configurations
RATE_LIMITS = {
    'public': '10 per minute',
    'authenticated': '100 per minute',
    'search': '30 per minute',
    'create': '20 per minute',
    'auth_login': '5 per minute',
    'health': '1000 per minute',
}

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=['200 per day', '50 per hour'],
    storage_uri=os.getenv('REDIS_URL', 'memory://')
)
