from flask import Blueprint, jsonify

bp = Blueprint('health', __name__)

@bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'message': 'MisMatch Recruiter API is running',
        'version': '1.0.0'
    }), 200
