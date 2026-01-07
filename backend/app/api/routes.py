from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import User, Candidate, JobPosting, Match
from datetime import timedelta

api_bp = Blueprint('api', __name__)

# AUTH
@api_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing fields'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email exists'}), 409
    user = User(email=data['email'], username=data.get('username', data['email'].split('@')[0]))
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'user_id': user.id}), 201

@api_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing credentials'}), 400
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.verify_password(data['password']):
        return jsonify({'error': 'Invalid'}), 401
    token = create_access_token(identity=user.id)
    return jsonify({'access_token': token}), 200

@api_bp.route('/candidates', methods=['GET'])
def get_candidates():
    candidates = Candidate.query.all()
    return jsonify([c.to_dict() for c in candidates]), 200

@api_bp.route('/candidates', methods=['POST'])
def create_candidate():
    data = request.get_json()
    c = Candidate(first_name=data['first_name'], last_name=data['last_name'], email=data['email'])
    db.session.add(c)
    db.session.commit()
    return jsonify(c.to_dict()), 201

@api_bp.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = JobPosting.query.all()
    return jsonify([j.to_dict() for j in jobs]), 200

@api_bp.route('/jobs', methods=['POST'])
def create_job():
    data = request.get_json()
    j = JobPosting(title=data['title'], description=data['description'], company=data['company'])
    db.session.add(j)
    db.session.commit()
    return jsonify(j.to_dict()), 201

@api_bp.route('/matches', methods=['GET'])
def get_matches():
    matches = Match.query.all()
    return jsonify([m.to_dict() for m in matches]), 200

@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200
