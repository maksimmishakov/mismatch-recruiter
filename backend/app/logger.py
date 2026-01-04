import logging
import json
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger
from flask import request, g
from datetime import datetime
import os

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['timestamp'] = datetime.utcnow().isoformat()
        log_record['level'] = record.levelname
        log_record['logger'] = record.name
        
        # Add request context if available
        if has_request_context():
            log_record['request_id'] = g.get('request_id', 'N/A')
            log_record['path'] = request.path
            log_record['method'] = request.method
            log_record['remote_addr'] = request.remote_addr

def has_request_context():
    try:
        from flask import has_request_context
        return has_request_context()
    except:
        return False

def init_logging(app):
    """
    Initialize structured logging for the application.
    Supports both console (development) and file (production) logging.
    """
    # Remove default handlers
    app.logger.handlers.clear()
    
    # Set log level
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    app.logger.setLevel(getattr(logging, log_level))
    
    # Create console handler with JSON formatter
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))
    
    json_formatter = CustomJsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s'
    )
    console_handler.setFormatter(json_formatter)
    app.logger.addHandler(console_handler)
    
    # Create file handler if LOG_DIR is set
    log_dir = os.getenv('LOG_DIR', None)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
        
        # Application logs
        file_handler = RotatingFileHandler(
            f'{log_dir}/app.log',
            maxBytes=10485760,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(json_formatter)
        app.logger.addHandler(file_handler)
        
        # Error logs
        error_handler = RotatingFileHandler(
            f'{log_dir}/error.log',
            maxBytes=10485760,
            backupCount=10
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(json_formatter)
        app.logger.addHandler(error_handler)
    
    return app.logger

def log_request(response):
    """
    Log incoming request with response status.
    """
    try:
        from flask import g, request
        duration = (datetime.utcnow() - g.start_time).total_seconds() if hasattr(g, 'start_time') else 0
        
        log_data = {
            'event': 'http_request',
            'method': request.method,
            'path': request.path,
            'status_code': response.status_code,
            'duration_ms': round(duration * 1000, 2),
            'remote_addr': request.remote_addr
        }
        
        if response.status_code >= 400:
            from flask import current_app
            current_app.logger.warning(json.dumps(log_data))
        else:
            from flask import current_app
            current_app.logger.info(json.dumps(log_data))
    except Exception as e:
        pass
    
    return response
