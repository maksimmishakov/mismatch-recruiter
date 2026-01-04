import logging
import logging.handlers
import os
from datetime import datetime

def setup_logging(app):
    """Setup logging with file handler"""
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    app.logger.setLevel(getattr(logging, log_level))
    
    # File handler
    log_file = f'logs/mismatch_{datetime.now().strftime("%Y%m%d")}.log'
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    app.logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))
    app.logger.addHandler(console_handler)
