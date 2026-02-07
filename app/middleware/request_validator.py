"""Request validation middleware."""
from functools import wraps
from flask import request, jsonify
from marshmallow import ValidationError
import re


class RequestValidator:
    """Middleware for validating incoming requests."""
    
    @staticmethod
    def validate_json(f):
        """Decorator to validate that request contains valid JSON."""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({
                    'error': 'Content-Type must be application/json',
                    'status': 'error'
                }), 400
            
            try:
                request.get_json()
            except Exception as e:
                return jsonify({
                    'error': 'Invalid JSON format',
                    'details': str(e),
                    'status': 'error'
                }), 400
            
            return f(*args, **kwargs)
        return decorated_function
    
    @staticmethod
    def validate_schema(schema_class):
        """Decorator to validate request data against a marshmallow schema."""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                try:
                    data = request.get_json()
                    if data is None:
                        return jsonify({
                            'error': 'Request body is required',
                            'status': 'error'
                        }), 400
                    
                    # Validate data against schema
                    schema = schema_class()
                    validated_data = schema.load(data)
                    
                    # Add validated data to request context
                    request.validated_data = validated_data
                    
                    return f(*args, **kwargs)
                    
                except ValidationError as err:
                    return jsonify({
                        'error': 'Validation failed',
                        'details': err.messages,
                        'status': 'error'
                    }), 400
                except Exception as e:
                    return jsonify({
                        'error': 'Validation error',
                        'details': str(e),
                        'status': 'error'
                    }), 400
            
            return decorated_function
        return decorator
    
    @staticmethod
    def validate_email(email):
        """Validate email format."""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None
    
    @staticmethod
    def validate_required_fields(required_fields):
        """Decorator to validate that required fields are present in request."""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                data = request.get_json()
                if not data:
                    return jsonify({
                        'error': 'Request body is required',
                        'status': 'error'
                    }), 400
                
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    return jsonify({
                        'error': 'Missing required fields',
                        'missing_fields': missing_fields,
                        'status': 'error'
                    }), 400
                
                # Validate empty values
                empty_fields = [
                    field for field in required_fields 
                    if field in data and (data[field] is None or str(data[field]).strip() == '')
                ]
                
                if empty_fields:
                    return jsonify({
                        'error': 'Required fields cannot be empty',
                        'empty_fields': empty_fields,
                        'status': 'error'
                    }), 400
                
                return f(*args, **kwargs)
            
            return decorated_function
        return decorator
    
    @staticmethod
    def validate_file_upload(allowed_extensions=None, max_size_mb=10):
        """Decorator to validate file uploads."""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if 'file' not in request.files:
                    return jsonify({
                        'error': 'No file uploaded',
                        'status': 'error'
                    }), 400
                
                file = request.files['file']
                
                if file.filename == '':
                    return jsonify({
                        'error': 'No file selected',
                        'status': 'error'
                    }), 400
                
                # Check file extension
                if allowed_extensions:
                    file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
                    if file_ext not in allowed_extensions:
                        return jsonify({
                            'error': f'File type not allowed. Allowed types: {", ".join(allowed_extensions)}',
                            'status': 'error'
                        }), 400
                
                # Check file size
                file.seek(0, 2)  # Seek to end
                file_size = file.tell()
                file.seek(0)  # Reset to beginning
                
                max_size_bytes = max_size_mb * 1024 * 1024
                if file_size > max_size_bytes:
                    return jsonify({
                        'error': f'File size exceeds {max_size_mb}MB limit',
                        'status': 'error'
                    }), 400
                
                return f(*args, **kwargs)
            
            return decorated_function
        return decorator
    
    @staticmethod
    def sanitize_input(data):
        """Sanitize input data to prevent XSS and injection attacks."""
        if isinstance(data, str):
            # Remove potentially dangerous characters
            data = data.replace('<', '&lt;').replace('>', '&gt;')
            data = data.replace('"', '&quot;').replace("'", '&#x27;')
            return data
        elif isinstance(data, dict):
            return {key: RequestValidator.sanitize_input(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [RequestValidator.sanitize_input(item) for item in data]
        return data
    
    @staticmethod
    def validate_pagination(max_limit=100):
        """Decorator to validate pagination parameters."""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                try:
                    page = request.args.get('page', 1, type=int)
                    limit = request.args.get('limit', 20, type=int)
                    
                    if page < 1:
                        return jsonify({
                            'error': 'Page number must be greater than 0',
                            'status': 'error'
                        }), 400
                    
                    if limit < 1 or limit > max_limit:
                        return jsonify({
                            'error': f'Limit must be between 1 and {max_limit}',
                            'status': 'error'
                        }), 400
                    
                    # Add pagination params to kwargs
                    kwargs['page'] = page
                    kwargs['limit'] = limit
                    
                    return f(*args, **kwargs)
                    
                except ValueError as e:
                    return jsonify({
                        'error': 'Invalid pagination parameters',
                        'details': str(e),
                        'status': 'error'
                    }), 400
            
            return decorated_function
        return decorator


def validate_request_size(max_content_length=16 * 1024 * 1024):  # 16MB default
    """Middleware to validate request size."""
    def middleware(app):
        app.config['MAX_CONTENT_LENGTH'] = max_content_length
        
        @app.errorhandler(413)
        def request_too_large(e):
            return jsonify({
                'error': 'Request payload too large',
                'max_size': f'{max_content_length / (1024 * 1024)}MB',
                'status': 'error'
            }), 413
        
        return app
    return middleware
