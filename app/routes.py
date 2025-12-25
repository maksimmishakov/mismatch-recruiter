"""API Routes and Blueprints"""
from flask import Blueprint, jsonify, request, render_template
from app import db
from app.models import Candidate, Job
from datetime import datetime

main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)

# ==================== MAIN ROUTES ====================

@main_bp.route('/')
def index():
    return jsonify({
        'message': 'MisMatch Recruitment API v2.0',
        'version': '2.0.0',
        'status': 'running',
        'endpoints': {
            'health': '/api/health',
            'candidates': '/api/candidates',
            'upload': '/upload'
        }
    })

@main_bp.route('/upload')
def upload_page():
    return render_template('index.html')

# ==================== API ROUTES ====================

@api_bp.route('/health', methods=['GET'])
def health_check():
    try:
        db.session.execute('SELECT 1')
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'database': 'disconnected'
        }), 500

@api_bp.route('/candidates', methods=['GET'])
def get_candidates():
    try:
        candidates = Candidate.query.order_by(Candidate.score.desc()).all()
        return jsonify({
            'candidates': [c.to_dict() for c in candidates],
            'count': len(candidates)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/candidate/<int:candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    try:
        candidate = Candidate.query.get(candidate_id)
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        return jsonify(candidate.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/candidate', methods=['POST'])
def create_candidate():
    try:
        data = request.get_json()
        candidate = Candidate(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            position=data.get('position'),
            skills=data.get('skills', []),
            score=data.get('score', 0.0),
            status='pending'
        )
        db.session.add(candidate)
        db.session.commit()
        return jsonify({
            'success': True,
            'candidate_id': candidate.id,
            'candidate': candidate.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@api_bp.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ==================== INTERVIEW GENERATOR ENDPOINT ====================
from services.interview_generator import InterviewGenerator

@api_bp.route('/generate-interview-questions', methods=['POST'])
def generate_interview_questions():
    """Generate interview questions using AI"""
    try:
        data = request.get_json()
        resume_id = data.get('resume_id')
        
        if not resume_id:
            return jsonify({'error': 'resume_id is required'}), 400
        
        # Initialize interview generator
        generator = InterviewGenerator()
        
        # Generate questions
        questions = generator.generate_questions(resume_id)
        
        return jsonify({
            'success': True,
            'resume_id': resume_id,
            'questions': questions,
            'total': len(questions)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Interview generation failed: {str(e)}'
        }), 500
