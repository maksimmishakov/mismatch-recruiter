from flask import Blueprint
from flask import request, jsonify

# Temporary imports - will be replaced after models are created
try:
    from app.models.user import User
    from app.models.candidate import Candidate
    from app.models.job import Job
    from app.models.match import Match
except ImportError:
    pass

# Auth Blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/health', methods=['GET'])
def auth_health():
    return {'status': 'auth service ok'}, 200

@auth_bp.route('/register', methods=['POST'])
def register():
    from app import db
    try:
        from app.models.user import User
        data = request.get_json()
        if not data.get('email') or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Missing required fields'}), 400
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 409
        user = User(email=data['email'], username=data['username'], role=data.get('role', 'user'))
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        from app.models.user import User
        data = request.get_json()
        user = User.query.filter_by(email=data.get('email')).first()
        if not user or not user.check_password(data.get('password')):
            return jsonify({'error': 'Invalid credentials'}), 401
        import jwt, os
        from datetime import datetime, timedelta
        token = jwt.encode({'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=24)}, os.environ.get('SECRET_KEY', 'dev-secret'), algorithm='HS256')
        return jsonify({'token': token, 'user': user.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Candidates Blueprint
candidates_bp = Blueprint('candidates', __name__, url_prefix='/api/candidates')

@candidates_bp.route('', methods=['GET'])
def get_candidates():
    try:
        from app.models.candidate import Candidate
        candidates = Candidate.query.all()
        return jsonify([c.to_dict() for c in candidates]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@candidates_bp.route('', methods=['POST'])
def create_candidate():
    from app import db
    try:
        from app.models.candidate import Candidate
        data = request.get_json()
        candidate = Candidate(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], phone=data.get('phone'), experience_years=data.get('experience_years', 0), specialization=data.get('specialization'))
        if 'skills' in data:
            candidate.set_skills(data['skills'])
        db.session.add(candidate)
        db.session.commit()
        return jsonify(candidate.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Jobs Blueprint
jobs_bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')

@jobs_bp.route('', methods=['GET'])
def get_jobs():
    try:
        from app.models.job import Job
        jobs = Job.query.all()
        return jsonify([j.to_dict() for j in jobs]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@jobs_bp.route('', methods=['POST'])
def create_job():
    from app import db
    try:
        from app.models.job import Job
        data = request.get_json()
        job = Job(title=data['title'], description=data['description'], company=data['company'], location=data['location'], salary_min=data.get('salary_min'), salary_max=data.get('salary_max'), experience_required=data.get('experience_required', 0))
        if 'required_skills' in data:
            job.set_required_skills(data['required_skills'])
        db.session.add(job)
        db.session.commit()
        return jsonify(job.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Matches Blueprint
matches_bp = Blueprint('matches', __name__, url_prefix='/api/matches')

@matches_bp.route('', methods=['GET'])
def get_matches():
    try:
        from app.models.match import Match
        matches = Match.query.all()
        return jsonify([m.to_dict() for m in matches]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@matches_bp.route('', methods=['POST'])
def create_match():
    from app import db
    try:
        from app.models.match import Match
        data = request.get_json()
        match = Match(candidate_id=data['candidate_id'], job_id=data['job_id'], match_score=data.get('match_score', 0.0), status=data.get('status', 'pending'))
        db.session.add(match)
        db.session.commit()
        return jsonify(match.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

__all__ = ['auth_bp', 'candidates_bp', 'jobs_bp', 'matches_bp']
