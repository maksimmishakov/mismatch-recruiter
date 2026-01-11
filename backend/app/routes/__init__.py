from flask import Blueprint, jsonify, request
from app import db
from app.models import User, Candidate, Job, Match

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Server is running'}), 200

@api_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username, 'email': u.email} for u in users]), 200

@api_bp.route('/candidates', methods=['GET'])
def get_candidates():
    candidates = Candidate.query.all()
    return jsonify([{'id': c.id, 'email': c.email, 'first_name': c.first_name, 'last_name': c.last_name} for c in candidates]), 200

