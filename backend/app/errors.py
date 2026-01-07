from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request', 'code': 400}), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': 'Unauthorized', 'code': 401}), 401
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found', 'code': 404}), 404
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({'error': 'Internal server error', 'code': 500}), 500
