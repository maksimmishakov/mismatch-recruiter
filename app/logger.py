"""Production-ready logging configuration."""
import logging
import sys
import os
import json
from logging.handlers import RotatingFileHandler
from datetime import datetime
from flask import request, g
import traceback

class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'message': record.getMessage(),
        }
        
        # Add request context if available
        if has_request_context():
            log_data['request'] = {
                'method': request.method,
                'path': request.path,
                'ip': request.remote_addr,
                'user_agent': request.user_agent.string if request.user_agent else None,
            }
            
            # Add user info if available
            if hasattr(g, 'current_user'):
                log_data['user_id'] = g.current_user.id
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': traceback.format_exception(*record.exc_info)
            }
        
        # Add extra fields
        if hasattr(record, 'extra_data'):
            log_data['extra'] = record.extra_data
        
        return json.dumps(log_data)

def has_request_context():
    """Check if we're in a request context."""
    try:
        from flask import has_request_context as _has_request_context
        return _has_request_context()
    except:
        return False

def setup_logger(app):
    """Configure application logger."""
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Clear existing handlers
    app.logger.handlers.clear()
    
    # Set log level based on environment
    if app.config.get('ENV') == 'production':
        log_level = logging.INFO
    elif app.config.get('ENV') == 'testing':
        log_level = logging.WARNING
    else:
        log_level = logging.DEBUG
    
    app.logger.setLevel(log_level)
    
    # Console handler (human-readable for development)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    if app.config.get('ENV') == 'production':
        # JSON format for production
        console_handler.setFormatter(JSONFormatter())
    else:
        # Simple format for development
        console_format = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_format)
    
    app.logger.addHandler(console_handler)
    
    # File handler with rotation (production only)
    if app.config.get('ENV') == 'production':
        # Main application log
        file_handler = RotatingFileHandler(
            'logs/mismatch.log',
            maxBytes=10485760,  # 10MB
            backupCount=10
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(JSONFormatter())
        app.logger.addHandler(file_handler)
        
        # Error log (errors and above)
        error_handler = RotatingFileHandler(
            'logs/errors.log',
            maxBytes=10485760,  # 10MB
            backupCount=10
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(JSONFormatter())
        app.logger.addHandler(error_handler)
        
        # Access log
        access_handler = RotatingFileHandler(
            'logs/access.log',
            maxBytes=10485760,  # 10MB
            backupCount=30
        )
        access_handler.setLevel(logging.INFO)
        access_handler.setFormatter(JSONFormatter())
        
        # Create access logger
        access_logger = logging.getLogger('access')
        access_logger.setLevel(logging.INFO)
        access_logger.addHandler(access_handler)
    
    app.logger.info('Logging system initialized', extra={
        'extra_data': {
            'environment': app.config.get('ENV'),
            'log_level': logging.getLevelName(log_level)
        }
    })
    
    return app.logger

def log_request():
    """Log incoming request."""
    access_logger = logging.getLogger('access')
    access_logger.info('Request received', extra={
        'extra_data': {
            'method': request.method,
            'path': request.path,
            'ip': request.remote_addr,
            'content_length': request.content_length,
        }
    })

def log_response(response):
    """Log outgoing response."""
    access_logger = logging.getLogger('access')
    access_logger.info('Response sent', extra={
        'extra_data': {
            'status_code': response.status_code,
            'content_length': response.content_length,
        }
    })
    return response
