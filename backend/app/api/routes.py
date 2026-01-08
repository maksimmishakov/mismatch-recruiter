from flask import Blueprint, jsonify

api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'API is running'}), 200

@api_bp.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'MisMatch Recruiter API',
        'version': '1.0.0',
        'endpoints': {
            'matching': '/api/matching',
            'analytics': '/api/analytics',
            'notifications': '/api/notifications'
        }
    }), 200
