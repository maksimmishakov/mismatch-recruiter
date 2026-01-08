from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
# db is imported lazily to avoid circular imports
from flask import current_app

from app.models import User, Candidate, JobPosting, Match
from datetime import timedelta

api_bp = Blueprint('api', __name__)

def get_db():
    """Get database instance from current app"""
    from app import db
    return db

# ============== MATCHING ALGORITHM ==============

def calculate_match_score(candidate, job):
    """Calculate match score: 60% skills, 40% experience"""
    if not job.required_skills or len(job.required_skills) == 0:
        skill_score = 50  # Default if no skills required
    elif not candidate.skills or len(candidate.skills) == 0:
        skill_score = 0
    else:
        matched = len([s for s in candidate.skills if s in job.required_skills])
        skill_score = (matched / len(job.required_skills)) * 100
    
    # Experience match: assume 5 years = 100%
    exp_years = candidate.experience_years or 0
    exp_score = min((exp_years / 5) * 100, 100)
    
    # 60% skills + 40% experience
    final_score = (skill_score * 0.6) + (exp_score * 0.4)
    return round(final_score, 2)

# ============== AUTH ROUTES ==============

@api_bp.route('/auth/register', methods=['POST'])
def register():
    """Register new user"""
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    user = User(
        email=data['email'],
        username=data.get('username', data['email'].split('@')[0]),
        full_name=data.get('full_name', '')
    )
    user.set_password(data['password'])
    
    get_db().session.add(user)
    get_db().session.commit()
    
    return jsonify({'user_id': user.id, 'email': user.email}), 201

@api_bp.route('/auth/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing credentials'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.verify_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=24))
    return jsonify({'access_token': access_token, 'user': user.to_dict()}), 200

@api_bp.route('/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200

# ============== CANDIDATES ROUTES ==============

@api_bp.route('/candidates', methods=['GET'])
@jwt_required()
def list_candidates():
    """List all candidates"""
    candidates = Candidate.query.all()
    return jsonify([c.to_dict() for c in candidates]), 200

@api_bp.route('/candidates', methods=['POST'])
@jwt_required()
def create_candidate():
    """Create new candidate"""
    data = request.get_json()
    if not data or not data.get('first_name') or not data.get('email'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if Candidate.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Candidate email already exists'}), 409
    
    candidate = Candidate(
        first_name=data['first_name'],
        last_name=data.get('last_name', ''),
        email=data['email'],
        phone=data.get('phone', ''),
        location=data.get('location', ''),
        bio=data.get('bio', ''),
        skills=data.get('skills', []),
        experience_years=data.get('experience_years', 0),
        github_url=data.get('github_url', ''),
        linkedin_url=data.get('linkedin_url', ''),
        portfolio_url=data.get('portfolio_url', '')
    )
    
    get_db().session.add(candidate)
    get_db().session.commit()
    
    return jsonify({'id': candidate.id, 'candidate': candidate.to_dict()}), 201

@api_bp.route('/candidates/<int:candidate_id>', methods=['GET'])
@jwt_required()
def get_candidate(candidate_id):
    """Get specific candidate by ID"""
    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        return jsonify({'error': 'Candidate not found'}), 404
    return jsonify(candidate.to_dict()), 200

@api_bp.route('/candidates/<int:candidate_id>', methods=['PUT'])
@jwt_required()
def update_candidate(candidate_id):
    """Update candidate details"""
    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        return jsonify({'error': 'Candidate not found'}), 404
    
    data = request.get_json()
    
    if 'first_name' in data:
        candidate.first_name = data['first_name']
    if 'last_name' in data:
        candidate.last_name = data['last_name']
    if 'email' in data and data['email'] != candidate.email:
        if Candidate.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already in use'}), 409
        candidate.email = data['email']
    if 'phone' in data:
        candidate.phone = data['phone']
    if 'location' in data:
        candidate.location = data['location']
    if 'bio' in data:
        candidate.bio = data['bio']
    if 'skills' in data:
        candidate.skills = data['skills']
    if 'experience_years' in data:
        candidate.experience_years = data['experience_years']
    if 'github_url' in data:
        candidate.github_url = data['github_url']
    if 'linkedin_url' in data:
        candidate.linkedin_url = data['linkedin_url']
    if 'portfolio_url' in data:
        candidate.portfolio_url = data['portfolio_url']
    
    get_db().session.commit()
    return jsonify({'message': 'Candidate updated', 'candidate': candidate.to_dict()}), 200

@api_bp.route('/candidates/<int:candidate_id>', methods=['DELETE'])
@jwt_required()
def delete_candidate(candidate_id):
    """Delete candidate"""
    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        return jsonify({'error': 'Candidate not found'}), 404
    
    get_db().session.delete(candidate)
    get_db().session.commit()
    
    return jsonify({'message': 'Candidate deleted'}), 200

# ============== JOBS ROUTES ==============

@api_bp.route('/jobs', methods=['GET'])
@jwt_required()
def list_jobs():
    """List all job postings"""
    jobs = JobPosting.query.all()
    return jsonify([j.to_dict() for j in jobs]), 200

@api_bp.route('/jobs', methods=['POST'])
@jwt_required()
def create_job():
    """Create new job posting"""
    data = request.get_json()
    if not data or not data.get('title') or not data.get('company'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    job = JobPosting(
        title=data['title'],
        description=data.get('description', ''),
        company=data['company'],
        location=data.get('location', ''),
        salary_min=data.get('salary_min', 0),
        salary_max=data.get('salary_max', 0),
        required_skills=data.get('required_skills', []),
        experience_level=data.get('experience_level', 'mid'),
        job_type=data.get('job_type', 'full-time')
    )
    
    get_db().session.add(job)
    get_db().session.commit()
    
    return jsonify({'id': job.id, 'job': job.to_dict()}), 201

@api_bp.route('/jobs/<int:job_id>', methods=['GET'])
@jwt_required()
def get_job(job_id):
    """Get specific job posting by ID"""
    job = JobPosting.query.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    return jsonify(job.to_dict()), 200

@api_bp.route('/jobs/<int:job_id>', methods=['PUT'])
@jwt_required()
def update_job(job_id):
    """Update job posting"""
    job = JobPosting.query.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    data = request.get_json()
    
    if 'title' in data:
        job.title = data['title']
    if 'description' in data:
        job.description = data['description']
    if 'company' in data:
        job.company = data['company']
    if 'location' in data:
        job.location = data['location']
    if 'salary_min' in data:
        job.salary_min = data['salary_min']
    if 'salary_max' in data:
        job.salary_max = data['salary_max']
    if 'required_skills' in data:
        job.required_skills = data['required_skills']
    if 'experience_level' in data:
        job.experience_level = data['experience_level']
    if 'job_type' in data:
        job.job_type = data['job_type']
    
    get_db().session.commit()
    return jsonify({'message': 'Job updated', 'job': job.to_dict()}), 200

@api_bp.route('/jobs/<int:job_id>', methods=['DELETE'])
@jwt_required()
def delete_job(job_id):
    """Delete job posting"""
    job = JobPosting.query.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    get_db().session.delete(job)
    get_db().session.commit()
    
    return jsonify({'message': 'Job deleted'}), 200

# ============== MATCHES ROUTES ==============

@api_bp.route('/matches', methods=['GET'])
@jwt_required()
def list_matches():
    """List all matches"""
    matches = Match.query.all()
    return jsonify([m.to_dict() for m in matches]), 200

@api_bp.route('/matches', methods=['POST'])
@jwt_required()
def create_match():
    """Create new match between candidate and job"""
    data = request.get_json()
    if not data or not data.get('candidate_id') or not data.get('job_id'):
        return jsonify({'error': 'Missing candidate_id or job_id'}), 400
    
    candidate = Candidate.query.get(data['candidate_id'])
    job = JobPosting.query.get(data['job_id'])
    
    if not candidate:
        return jsonify({'error': 'Candidate not found'}), 404
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    # Check if match already exists
    existing = Match.query.filter_by(
        candidate_id=data['candidate_id'],
        job_posting_id=data['job_id']
    ).first()
    if existing:
        return jsonify({'error': 'Match already exists'}), 409
    
    # Calculate match score
    match_score = calculate_match_score(candidate, job)
    
    match = Match(
        candidate_id=data['candidate_id'],
        job_posting_id=data['job_id'],
        match_score=match_score,
        skill_match=calculate_skill_match(candidate, job),
        experience_match=calculate_experience_match(candidate, job),
        location_match=1.0 if candidate.location and job.location and candidate.location.lower() == job.location.lower() else 0.0,
        status='pending'
    )
    
    get_db().session.add(match)
    get_db().session.commit()
    
    return jsonify({'id': match.id, 'match_score': match_score, 'match': match.to_dict()}), 201

@api_bp.route('/candidates/<int:candidate_id>/matches', methods=['GET'])
@jwt_required()
def get_candidate_matches(candidate_id):
    """Get all matches for a specific candidate"""
    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        return jsonify({'error': 'Candidate not found'}), 404
    
    matches = Match.query.filter_by(candidate_id=candidate_id).all()
    return jsonify([m.to_dict() for m in matches]), 200

@api_bp.route('/jobs/<int:job_id>/matches', methods=['GET'])
@jwt_required()
def get_job_matches(job_id):
    """Get all matches for a specific job"""
    job = JobPosting.query.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    matches = Match.query.filter_by(job_posting_id=job_id).all()
    return jsonify([m.to_dict() for m in matches]), 200

# ============== HELPER FUNCTIONS ==============

def calculate_skill_match(candidate, job):
    """Calculate skill match percentage"""
    if not job.required_skills or len(job.required_skills) == 0:
        return 0.5  # 50% default
    if not candidate.skills or len(candidate.skills) == 0:
        return 0.0
    
    matched = len([s for s in candidate.skills if s in job.required_skills])
    return round(matched / len(job.required_skills), 2)

def calculate_experience_match(candidate, job):
    """Calculate experience match (0-1 scale)"""
    # Normalize to 0-1 scale (5 years = 1.0)
    exp_years = candidate.experience_years or 0
    return round(min(exp_years / 5, 1.0), 2)

# ============== HEALTH CHECK ==============

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'mismatch-recruiter-api'}), 200
