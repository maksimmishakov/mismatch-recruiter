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


# Performance Monitoring
class PerformanceMonitor:
    """Monitor and log performance metrics."""
    
    def __init__(self):
        self.metrics = {}
        self.start_times = {}
    
    def start_timer(self, operation_name):
        """Start timing an operation."""
        from datetime import datetime
        self.start_times[operation_name] = datetime.utcnow()
    
    def end_timer(self, operation_name, logger=None):
        """End timing an operation and log the duration."""
        from datetime import datetime
        if operation_name in self.start_times:
            duration = (datetime.utcnow() - self.start_times[operation_name]).total_seconds()
            
            if operation_name not in self.metrics:
                self.metrics[operation_name] = []
            
            self.metrics[operation_name].append(duration)
            
            if logger:
                logger.info(f"Performance: {operation_name} completed in {duration:.3f}s")
            
            del self.start_times[operation_name]
            return duration
        return None
    
    def get_average(self, operation_name):
        """Get average execution time for an operation."""
        if operation_name in self.metrics and self.metrics[operation_name]:
            return sum(self.metrics[operation_name]) / len(self.metrics[operation_name])
        return 0
    
    def get_stats(self, operation_name):
        """Get detailed statistics for an operation."""
        if operation_name in self.metrics and self.metrics[operation_name]:
            metrics = self.metrics[operation_name]
            return {
                'count': len(metrics),
                'average': sum(metrics) / len(metrics),
                'min': min(metrics),
                'max': max(metrics),
                'total': sum(metrics)
            }
        return None


# Create global performance monitor
performance_monitor = PerformanceMonitor()


def log_api_request(f):
    """Decorator to log API requests with timing."""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logger = logging.getLogger(__name__)
        
        # Start timer
        operation = f.__name__
        performance_monitor.start_timer(operation)
        
        try:
            # Log incoming request
            if has_request_context():
                logger.info(f"API Request: {request.method} {request.path}", extra={
                    'extra_data': {
                        'endpoint': operation,
                        'method': request.method,
                        'path': request.path,
                        'ip': request.remote_addr
                    }
                })
            
            # Execute function
            result = f(*args, **kwargs)
            
            # End timer and log duration
            duration = performance_monitor.end_timer(operation, logger)
            
            # Log successful completion
            if has_request_context():
                logger.info(f"API Response: {operation} completed successfully", extra={
                    'extra_data': {
                        'endpoint': operation,
                        'duration': duration,
                        'status': 'success'
                    }
                })
            
            return result
            
        except Exception as e:
            # End timer
            performance_monitor.end_timer(operation)
            
            # Log error
            logger.error(f"API Error in {operation}: {str(e)}", extra={
                'extra_data': {
                    'endpoint': operation,
                    'error': str(e),
                    'error_type': type(e).__name__
                }
            }, exc_info=True)
            
            raise
    
    return decorated_function


def log_database_query(query_type, table_name=None):
    """Decorator to log database queries with performance metrics."""
    from functools import wraps
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            logger = logging.getLogger(__name__)
            operation = f"{query_type}_{table_name}" if table_name else f"{query_type}_query"
            
            # Start timer
            performance_monitor.start_timer(operation)
            
            try:
                result = f(*args, **kwargs)
                duration = performance_monitor.end_timer(operation)
                
                # Log query execution
                logger.debug(f"DB Query: {query_type} on {table_name or 'unknown'} took {duration:.3f}s")
                
                # Warn on slow queries
                if duration and duration > 1.0:  # More than 1 second
                    logger.warning(f"Slow DB Query detected: {operation} took {duration:.3f}s")
                
                return result
                
            except Exception as e:
                performance_monitor.end_timer(operation)
                logger.error(f"DB Query Error: {query_type} on {table_name}: {str(e)}", exc_info=True)
                raise
        
        return decorated_function
    return decorator


def log_external_api_call(service_name):
    """Decorator to log external API calls."""
    from functools import wraps
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            logger = logging.getLogger(__name__)
            operation = f"{service_name}_api_call"
            
            performance_monitor.start_timer(operation)
            
            try:
                logger.info(f"External API Call: {service_name}")
                result = f(*args, **kwargs)
                duration = performance_monitor.end_timer(operation)
                
                logger.info(f"External API Response: {service_name} completed in {duration:.3f}s")
                return result
                
            except Exception as e:
                performance_monitor.end_timer(operation)
                logger.error(f"External API Error: {service_name} - {str(e)}", exc_info=True)
                raise
        
        return decorated_function
    return decorator


def get_performance_report():
    """Generate a performance report for all monitored operations."""
    report = {}
    for operation in performance_monitor.metrics.keys():
        stats = performance_monitor.get_stats(operation)
        if stats:
            report[operation] = stats
    return report

    
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
