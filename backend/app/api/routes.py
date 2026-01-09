from app.models import db, User, Candidate, Job, Match
import logging

logger = logging.getLogger(__name__)

from flask import Blueprint, jsonify, request

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


# ========== CANDIDATES ==========

@api_bp.route('/candidates', methods=['GET'])
def list_candidates():
    """Get all candidates with pagination."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        pagination = Candidate.query.paginate(page=page, per_page=per_page)
        return jsonify({
            'total': pagination.total,
            'pages': pagination.pages,
            'candidates': [c.to_dict() for c in pagination.items]
        }), 200
    except Exception as e:
        logger.error(f"Error listing candidates: {e}")
        return jsonify({'error': 'Failed to list candidates'}), 500


@api_bp.route('/candidates/<int:candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    """Get candidate by ID."""
    try:
        candidate = Candidate.query.get_or_404(candidate_id)
        return jsonify(candidate.to_dict()), 200
    except Exception as e:
        logger.error(f"Error getting candidate: {e}")
        return jsonify({'error': 'Candidate not found'}), 404


# ========== JOBS ==========

@api_bp.route('/jobs', methods=['GET'])
def list_jobs():
    """Get all active jobs."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        pagination = Job.query.filter_by(is_active=True).paginate(page=page, per_page=per_page)
        return jsonify({
            'total': pagination.total,
            'pages': pagination.pages,
            'jobs': [j.to_dict() for j in pagination.items]
        }), 200
    except Exception as e:
        logger.error(f"Error listing jobs: {e}")
        return jsonify({'error': 'Failed to list jobs'}), 500


@api_bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Get job by ID."""
    try:
        job = Job.query.get_or_404(job_id)
        return jsonify(job.to_dict()), 200
    except Exception as e:
        logger.error(f"Error getting job: {e}")
        return jsonify({'error': 'Job not found'}), 404


# ========== MATCHING ==========

@api_bp.route('/matching/candidates-to-vacancy/<int:job_id>', methods=['GET'])
def candidates_for_job(job_id):
    """Get best matching candidates for a job."""
    try:
        job = Job.query.get_or_404(job_id)
        matches = Match.query.filter_by(job_id=job_id).order_by(Match.overall_score.desc()).all()
        return jsonify({
            'job_id': job_id,
            'job_title': job.title,
            'total_matches': len(matches),
            'top_matches': [m.to_dict() for m in matches[:10]]
        }), 200
    except Exception as e:
        logger.error(f"Error getting candidates for job: {e}")
        return jsonify({'error': 'Job not found'}), 404


@api_bp.route('/matching/vacancy-to-candidate/<int:candidate_id>', methods=['GET'])
def jobs_for_candidate(candidate_id):
    """Get best matching jobs for a candidate."""
    try:
        candidate = Candidate.query.get_or_404(candidate_id)
        matches = Match.query.filter_by(candidate_id=candidate_id).order_by(Match.overall_score.desc()).all()
        return jsonify({
            'candidate_id': candidate_id,
            'candidate_name': candidate.name,
            'total_matches': len(matches),
            'top_matches': [m.to_dict() for m in matches[:10]]
        }), 200
    except Exception as e:
        logger.error(f"Error getting jobs for candidate: {e}")
        return jsonify({'error': 'Candidate not found'}), 404

# Auth endpoints
@api_bp.route('/auth/register', methods=['POST'])
def register():
    """Register a new user."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(k in data for k in ('email', 'username', 'password')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if user already exists
        existing_user = db.session.query(User).filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 409
        
        # Create new user
        new_user = User(
            email=data['email'],
            username=data['username'],
            password_hash=data['password'],  # In production, hash the password
            role='candidate'
        )
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': new_user.id,
            'email': new_user.email
        }), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f'Registration error: {str(e)}')
        return jsonify({'error': str(e)}), 500

@api_bp.route('/auth/login', methods=['POST'])
def login():
    """User login endpoint."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password required'}), 400
        
        # Find user
        user = db.session.query(User).filter_by(email=data['email']).first()
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # In production, verify hashed password
        if user.password_hash != data['password']:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        return jsonify({
            'message': 'Login successful',
            'user_id': user.id,
            'email': user.email,
            'token': f'token_{user.id}'  # Simplified token
        }), 200
    except Exception as e:
        logger.error(f'Login error: {str(e)}')
        return jsonify({'error': str(e)}), 500
