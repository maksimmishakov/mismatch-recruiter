"""Logging Configuration for MisMatch Recruiter"""
import logging
import logging.handlers
import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logging():
    """Setup complete logging system"""
    logger = logging.getLogger('mismatch')
    logger.setLevel(logging.DEBUG)
    
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler - debug logs
    debug_handler = logging.handlers.RotatingFileHandler(
        f"{LOG_DIR}/debug.log",
        maxBytes=10485760,
        backupCount=10
    )
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(log_format)
    logger.addHandler(debug_handler)
    
    # File handler - error logs
    error_handler = logging.handlers.RotatingFileHandler(
        f"{LOG_DIR}/errors.log",
        maxBytes=10485760,
        backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(log_format)
    logger.addHandler(error_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()
