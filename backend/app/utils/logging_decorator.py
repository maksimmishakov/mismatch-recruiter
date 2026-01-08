"""Advanced logging decorators for API endpoints and functions."""

import logging
import json
import time
from functools import wraps
from datetime import datetime
from flask import request, g
from typing import Any, Callable

# Configure logger
logger = logging.getLogger(__name__)


class RequestLogger:
    """Logger for HTTP requests and responses."""
    
    @staticmethod
    def setup_logger(app):
        """Setup logging configuration for the application."""
        if not logger.handlers:
            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            # Create file handler
            fh = logging.FileHandler('logs/mismatch_api.log')
            fh.setLevel(logging.INFO)
            fh.setFormatter(formatter)
            
            # Create console handler
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(formatter)
            
            # Add handlers to logger
            logger.addHandler(fh)
            logger.addHandler(ch)
            logger.setLevel(logging.DEBUG)


def log_request(func: Callable) -> Callable:
    """Decorator to log incoming requests with details."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        # Log request details
        request_id = f"{datetime.now().timestamp()}"
        g.request_id = request_id
        
        log_data = {
            'request_id': request_id,
            'method': request.method,
            'endpoint': request.endpoint,
            'path': request.path,
            'remote_addr': request.remote_addr,
            'user_agent': request.user_agent.string if request.user_agent else 'Unknown',
            'timestamp': datetime.now().isoformat(),
        }
        
        # Log request body if POST/PUT
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                log_data['body'] = request.get_json() or {}
            except:
                log_data['body'] = 'Could not parse JSON'
        
        logger.info(f"Incoming Request: {json.dumps(log_data, indent=2)}")
        
        # Execute function
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            
            logger.info(
                f"Request {request_id} completed successfully. "
                f"Method: {request.method}, Path: {request.path}, "
                f"Duration: {elapsed_time:.3f}s"
            )
            return result
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(
                f"Request {request_id} failed. "
                f"Method: {request.method}, Path: {request.path}, "
                f"Duration: {elapsed_time:.3f}s, Error: {str(e)}",
                exc_info=True
            )
            raise
    
    return wrapper


def log_function(func: Callable) -> Callable:
    """Decorator to log function execution with arguments and return values."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        func_name = func.__name__
        logger.debug(f"Calling function: {func_name}")
        logger.debug(f"Args: {args}, Kwargs: {kwargs}")
        
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            
            logger.debug(
                f"Function {func_name} completed. "
                f"Duration: {elapsed_time:.4f}s, Result type: {type(result).__name__}"
            )
            return result
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(
                f"Function {func_name} failed. Duration: {elapsed_time:.4f}s, Error: {str(e)}",
                exc_info=True
            )
            raise
    
    return wrapper


def log_database_operation(operation: str) -> Callable:
    """Decorator to log database operations."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger.info(f"Database operation '{operation}' starting...")
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                elapsed_time = time.time() - start_time
                logger.info(
                    f"Database operation '{operation}' completed. Duration: {elapsed_time:.3f}s"
                )
                return result
            except Exception as e:
                elapsed_time = time.time() - start_time
                logger.error(
                    f"Database operation '{operation}' failed. Duration: {elapsed_time:.3f}s. Error: {str(e)}",
                    exc_info=True
                )
                raise
        
        return wrapper
    return decorator
