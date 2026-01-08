import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/tmp/mismatch-api.log')
    ]
)

logger = logging.getLogger(__name__)

def log_request(endpoint, method, user_id=None):
    """Log API request"""
    logger.info(f"REQUEST: {method} {endpoint} | User: {user_id}")

def log_response(endpoint, status_code, response_time=None):
    """Log API response"""
    logger.info(f"RESPONSE: {endpoint} | Status: {status_code} | Time: {response_time}ms")

def log_error(endpoint, error_msg, status_code=500):
    """Log API error"""
    logger.error(f"ERROR: {endpoint} | Status: {status_code} | Message: {error_msg}")
