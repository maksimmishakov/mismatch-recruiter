from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    """Register error handlers for all HTTP status codes"""
    
    @app.errorhandler(400)
    def bad_request(error):
        app.logger.warning(f"Bad request: {error}")
        return jsonify({'error': 'Bad request', 'message': str(error)}), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        app.logger.warning(f"Unauthorized access attempt")
        return jsonify({'error': 'Unauthorized'}), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        app.logger.warning(f"Forbidden: {error}")
        return jsonify({'error': 'Forbidden'}), 403
    
    @app.errorhandler(404)
    def not_found(error):
        app.logger.debug(f"Not found: {error}")
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(429)
    def too_many_requests(error):
        app.logger.warning(f"Rate limit exceeded")
        return jsonify({'error': 'Too many requests'}), 429
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Internal error: {error}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle unexpected exceptions"""
        if isinstance(e, HTTPException):
            return jsonify({'error': str(e)}), e.code
        
        app.logger.error(f"Unexpected error: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500
