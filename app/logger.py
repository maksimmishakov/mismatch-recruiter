"""Comprehensive Logging System for Production"""
import logging
import sys
from logging.handlers import RotatingFileHandler
from logging.formatters import ColoredFormatter
from pathlib import Path
import os


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = self.COLORS[levelname] + levelname + self.RESET
        return super().format(record)


def setup_logger(name, log_level=logging.INFO):
    """Setup logger with both file and console handlers"""
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Create logs directory if it doesn't exist
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # File handler - all logs
    file_handler = RotatingFileHandler(
        filename=log_dir / f'{name}.log',
        maxBytes=10485760,  # 10MB
        backupCount=10,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler - only WARNING and above
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Formatter
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_formatter = ColoredFormatter(
        '[%(levelname)s] %(asctime)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers if not already present
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger


# Application loggers
app_logger = setup_logger('app', log_level=logging.INFO)
db_logger = setup_logger('database', log_level=logging.INFO)
api_logger = setup_logger('api', log_level=logging.INFO)
service_logger = setup_logger('services', log_level=logging.INFO)
health_logger = setup_logger('health_check', log_level=logging.INFO)


def log_request(method, path, status_code, response_time):
    """Log HTTP request details"""
    api_logger.info(
        f'Request: {method} {path} - Status: {status_code} - Time: {response_time:.2f}ms'
    )


def log_error(error_type, message, details=None):
    """Log error with context"""
    error_msg = f'{error_type}: {message}'
    if details:
        error_msg += f' - Details: {details}'
    app_logger.error(error_msg)


def log_database_query(query, execution_time):
    """Log database query performance"""
    db_logger.debug(f'Query executed in {execution_time:.2f}ms: {query[:100]}...')


def log_service_event(service_name, event, details=None):
    """Log service-level events"""
    msg = f'[{service_name}] {event}'
    if details:
        msg += f': {details}'
    service_logger.info(msg)
