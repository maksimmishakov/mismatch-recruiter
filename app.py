#!/usr/bin/env python3
"""
MisMatch Recruiter - Minimal Working Backend
Simple Flask app with PostgreSQL + Redis integration
"""

import os
import json
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://mismatch_user:secure_password@localhost:5432/mismatch_dev'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# ============================================================================
# MODELS
# ============================================================================

class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    skills = db.Column(db.JSON, default=list)
    experience_years = db.Column(db.Integer, default=0)
    salary_expectation = db.Column(db.Integer, nullable=True)
    score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'candidate_name': self.candidate_name,
            'email': self.email,
            'skills': self.skills,
            'experience_years': self.experience_years,
            'salary_expectation': self.salary_expectation,
            'score': self.score,
            'created_at': self.created_at.isoformat()
        }

class JobProfile(db.Model):
    __tablename__ = 'job_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(255), nullable=False)
    required_skills = db.Column(db.JSON, default=list)
    salary_min = db.Column(db.Integer, nullable=True)
    salary_max = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_title': self.job_title,
            'required_skills': self.required_skills,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        db.session.execute('SELECT 1')
        db_status = 'healthy'
    except Exception as e:
        db_status = f'error: {str(e)}'
    
    return jsonify({
        'status': 'ok',
        'service': 'mismatch-recruiter',
        'timestamp': datetime.utcnow().isoformat(),
        'database': db_status
    }), 200

@app.route('/api/resumes', methods=['POST'])
def create_resume():
    """Create new resume"""
    try:
        data = request.get_json()
        
        resume = Resume(
            candidate_name=data.get('candidate_name'),
            email=data.get('email'),
            skills=data.get('skills', []),
            experience_years=data.get('experience_years', 0),
            salary_expectation=data.get('salary_expectation'),
            score=data.get('score', 0.0)
        )
        
        db.session.add(resume)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Resume created successfully',
            'data': resume.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/resumes', methods=['GET'])
def list_resumes():
    """List all resumes"""
    try:
        resumes = Resume.query.all()
        return jsonify({
            'success': True,
            'count': len(resumes),
            'data': [r.to_dict() for r in resumes]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/resumes/<int:resume_id>', methods=['GET'])
def get_resume(resume_id):
    """Get single resume"""
    try:
        resume = Resume.query.get(resume_id)
        if not resume:
            return jsonify({'error': 'Resume not found'}), 404
        
        return jsonify({
            'success': True,
            'data': resume.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/job-profiles', methods=['POST'])
def create_job_profile():
    """Create new job profile"""
    try:
        data = request.get_json()
        
        job = JobProfile(
            job_title=data.get('job_title'),
            required_skills=data.get('required_skills', []),
            salary_min=data.get('salary_min'),
            salary_max=data.get('salary_max'),
            description=data.get('description')
        )
        
        db.session.add(job)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Job profile created',
            'data': job.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/job-profiles', methods=['GET'])
def list_job_profiles():
    """List all job profiles"""
    try:
        jobs = JobProfile.query.all()
        return jsonify({
            'success': True,
            'count': len(jobs),
            'data': [j.to_dict() for j in jobs]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/match', methods=['POST'])
def match_resume_to_job():
    """Match resume to job profile and calculate score"""
    try:
        data = request.get_json()
        resume_id = data.get('resume_id')
        job_id = data.get('job_id')
        
        resume = Resume.query.get(resume_id)
        job = JobProfile.query.get(job_id)
        
        if not resume or not job:
            return jsonify({'error': 'Resume or Job not found'}), 404
        
        # Simple matching algorithm
        resume_skills = set(resume.skills)
        job_skills = set(job.required_skills)
        
        if not job_skills:
            skill_match = 1.0
        else:
            matched = resume_skills.intersection(job_skills)
            skill_match = len(matched) / len(job_skills)
        
        # Experience match (basic)
        experience_match = min(resume.experience_years / 5, 1.0)  # Max 5 years considered
        
        # Salary check
        salary_match = 1.0
        if resume.salary_expectation and job.salary_min and job.salary_max:
            if resume.salary_expectation > job.salary_max:
                salary_match = 0.5
            elif resume.salary_expectation < job.salary_min:
                salary_match = 0.8
        
        # Overall score
        overall_score = (skill_match * 0.5 + experience_match * 0.3 + salary_match * 0.2)
        
        return jsonify({
            'success': True,
            'data': {
                'resume_id': resume_id,
                'job_id': job_id,
                'skill_match': round(skill_match, 2),
                'experience_match': round(experience_match, 2),
                'salary_match': round(salary_match, 2),
                'overall_score': round(overall_score, 2),
                'matched_skills': list(resume_skills.intersection(job_skills)),
                'missing_skills': list(job_skills - resume_skills)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get application statistics"""
    try:
        resume_count = Resume.query.count()
        job_count = JobProfile.query.count()
        avg_score = db.session.query(db.func.avg(Resume.score)).scalar() or 0
        
        return jsonify({
            'success': True,
            'data': {
                'total_resumes': resume_count,
                'total_jobs': job_count,
                'average_score': round(avg_score, 2),
                'timestamp': datetime.utcnow().isoformat()
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'available_endpoints': {
            'GET /health': 'Health check',
            'POST /api/resumes': 'Create resume',
            'GET /api/resumes': 'List resumes',
            'GET /api/resumes/<id>': 'Get resume',
            'POST /api/job-profiles': 'Create job',
            'GET /api/job-profiles': 'List jobs',
            'POST /api/match': 'Match resume to job',
            'GET /api/stats': 'Get statistics'
        }
    }), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'details': str(e)
    }), 500

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_db():
    """Initialize database tables"""
    with app.app_context():
        try:
            db.create_all()
            print('✅ Database initialized')
        except Exception as e:
            print(f'❌ Database error: {e}')

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    init_db()
    
    # Run Flask
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print(f"""
    ╔════════════════════════════════════════════╗
    ║   🚀 MisMatch Recruiter Started            ║
    ║   http://localhost:{port}             ║
    ║   Environment: {'development' if debug else 'production'}        ║
    ╚════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)