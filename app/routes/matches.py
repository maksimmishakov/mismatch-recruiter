"""API Routes for Resume-Job Matching (Phase 2)

Endpoints for calculating match scores and finding best matches.
"""

from flask import Blueprint, request, jsonify
from app.ml.matcher import get_matcher
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

matches_bp = Blueprint('matches', __name__, url_prefix='/api/matches')


@matches_bp.route('/calculate-score', methods=['POST'])
def calculate_match_score():
    """Calculate match score between candidate and job.
    
    POST /api/matches/calculate-score
    
    Request body:
    {
        "candidate_id": 1,
        "job_id": 2,
        "use_defaults": true,
        "candidate": {
            "skills": ["Python", "Django", "React"],
            "experience_years": 5,
            "location": "Moscow",
            "resume_text": "...",
            "salary_expectation": 150000
        },
        "job": {
            "title": "Senior Backend Developer",
            "description": "...",
            "required_skills": ["Python", "Django"],
            "required_experience": 3,
            "location": "Moscow",
            "remote": false,
            "salary": 180000
        }
    }
    """
    try:
        data = request.get_json()
        matcher = get_matcher()
        
        # Option 1: Calculate from database IDs
        if data.get('candidate_id') and data.get('job_id'):
            from app.models import Candidate, Job
            
            candidate = Candidate.query.get(data['candidate_id'])
            job = Job.query.get(data['job_id'])
            
            if not candidate or not job:
                return jsonify({'error': 'Candidate or Job not found'}), 404
            
            candidate_data = {
                'skills': candidate.skills.split(',') if candidate.skills else [],
                'experience_years': candidate.experience_years or 0,
                'location': candidate.location or '',
                'resume_text': candidate.resume_text or '',
                'salary_expectation': candidate.salary_expectation or 0
            }
            
            job_data = {
                'title': job.title,
                'description': job.description,
                'required_skills': job.required_skills.split(',') if job.required_skills else [],
                'required_experience': job.experience_level or 0,
                'location': job.location or '',
                'remote': job.remote or False,
                'salary': job.salary or 0
            }
        else:
            # Option 2: Calculate from provided data
            candidate_data = data.get('candidate', {})
            job_data = data.get('job', {})
        
        # Calculate match score
        result = matcher.calculate_match_score(candidate_data, job_data)
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f'Error calculating match score: {e}')
        return jsonify({'error': str(e)}), 500


@matches_bp.route('/find-best-matches/<int:job_id>', methods=['GET'])
def find_best_matches(job_id):
    """Find best candidates for a job.
    
    GET /api/matches/find-best-matches/{job_id}?limit=10&min_score=0.5
    
    Query Parameters:
        limit (int): Maximum number of matches to return (default: 10)
        min_score (float): Minimum score threshold (default: 0.5)
    """
    try:
        from app.models import Candidate, Job
        
        limit = request.args.get('limit', 10, type=int)
        min_score = request.args.get('min_score', 0.5, type=float)
        
        job = Job.query.get(job_id)
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        candidates = Candidate.query.all()
        matcher = get_matcher()
        matches = []
        
        for candidate in candidates:
            candidate_data = {
                'skills': candidate.skills.split(',') if candidate.skills else [],
                'experience_years': candidate.experience_years or 0,
                'location': candidate.location or '',
                'resume_text': candidate.resume_text or '',
                'salary_expectation': candidate.salary_expectation or 0
            }
            
            job_data = {
                'title': job.title,
                'description': job.description,
                'required_skills': job.required_skills.split(',') if job.required_skills else [],
                'required_experience': job.experience_level or 0,
                'location': job.location or '',
                'remote': job.remote or False,
                'salary': job.salary or 0
            }
            
            score_result = matcher.calculate_match_score(candidate_data, job_data)
            
            if score_result['overall_score'] >= min_score:
                matches.append({
                    'candidate_id': candidate.id,
                    'candidate_name': candidate.fullname,
                    'email': candidate.email,
                    'overall_score': score_result['overall_score'],
                    'score_percentage': score_result['score_percentage'],
                    'match_quality': score_result['match_quality'],
                    'breakdown': score_result['breakdown']
                })
        
        # Sort by score (descending) and limit
        matches.sort(key=lambda x: x['overall_score'], reverse=True)
        matches = matches[:limit]
        
        return jsonify({
            'job_id': job_id,
            'job_title': job.title,
            'total_matches': len(matches),
            'matches': matches
        }), 200
    
    except Exception as e:
        logger.error(f'Error finding best matches: {e}')
        return jsonify({'error': str(e)}), 500


@matches_bp.route('/find-best-jobs/<int:candidate_id>', methods=['GET'])
def find_best_jobs(candidate_id):
    """Find best jobs for a candidate.
    
    GET /api/matches/find-best-jobs/{candidate_id}?limit=10&min_score=0.5
    
    Query Parameters:
        limit (int): Maximum number of matches to return (default: 10)
        min_score (float): Minimum score threshold (default: 0.5)
    """
    try:
        from app.models import Candidate, Job
        
        limit = request.args.get('limit', 10, type=int)
        min_score = request.args.get('min_score', 0.5, type=float)
        
        candidate = Candidate.query.get(candidate_id)
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        
        jobs = Job.query.all()
        matcher = get_matcher()
        matches = []
        
        candidate_data = {
            'skills': candidate.skills.split(',') if candidate.skills else [],
            'experience_years': candidate.experience_years or 0,
            'location': candidate.location or '',
            'resume_text': candidate.resume_text or '',
            'salary_expectation': candidate.salary_expectation or 0
        }
        
        for job in jobs:
            job_data = {
                'title': job.title,
                'description': job.description,
                'required_skills': job.required_skills.split(',') if job.required_skills else [],
                'required_experience': job.experience_level or 0,
                'location': job.location or '',
                'remote': job.remote or False,
                'salary': job.salary or 0
            }
            
            score_result = matcher.calculate_match_score(candidate_data, job_data)
            
            if score_result['overall_score'] >= min_score:
                matches.append({
                    'job_id': job.id,
                    'job_title': job.title,
                    'company': job.company or 'Unknown',
                    'location': job.location,
                    'overall_score': score_result['overall_score'],
                    'score_percentage': score_result['score_percentage'],
                    'match_quality': score_result['match_quality'],
                    'breakdown': score_result['breakdown']
                })
        
        # Sort by score (descending) and limit
        matches.sort(key=lambda x: x['overall_score'], reverse=True)
        matches = matches[:limit]
        
        return jsonify({
            'candidate_id': candidate_id,
            'candidate_name': candidate.fullname,
            'total_matches': len(matches),
            'matches': matches
        }), 200
    
    except Exception as e:
        logger.error(f'Error finding best jobs: {e}')
        return jsonify({'error': str(e)}), 500
