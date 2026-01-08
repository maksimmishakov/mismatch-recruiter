"""Matching API endpoints."""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.matching_service import matching_service
from app.models import Candidate, Vacancy, db
import logging

bp = Blueprint('matching', __name__, url_prefix='/api/matching')
logger = logging.getLogger(__name__)

@bp.route('/candidates-to-vacancy/<int:vacancy_id>', methods=['GET'])
@jwt_required()
def match_candidates_to_vacancy(vacancy_id):
    """Find best candidate matches for a vacancy."""
    try:
        vacancy = Vacancy.query.get_or_404(vacancy_id)
        candidates = Candidate.query.all()
        
        limit = int(request.args.get('limit', 20))
        matches = matching_service.batch_match_candidates(
            [c.to_dict() for c in candidates],
            vacancy.to_dict(),
            limit=limit
        )
        
        stats = matching_service.get_matching_stats(matches)
        
        response_matches = []
        for candidate, score, details in matches:
            response_matches.append({
                'candidate_id': candidate.get('id'),
                'score': round(score, 2),
                'details': {k: round(v, 2) if isinstance(v, float) else v 
                           for k, v in details.items()},
                'match_level': get_match_level(score)
            })
        
        return jsonify({
            'matches': response_matches,
            'statistics': stats
        }), 200
    except Exception as e:
        logger.error(f'Matching error: {e}')
        return jsonify({'error': str(e)}), 500

@bp.route('/vacancy-to-candidate/<int:candidate_id>', methods=['GET'])
@jwt_required()
def match_vacancies_to_candidate(candidate_id):
    """Find best vacancy matches for a candidate."""
    try:
        candidate = Candidate.query.get_or_404(candidate_id)
        vacancies = Vacancy.query.all()
        
        limit = int(request.args.get('limit', 20))
        matches = []
        for vacancy in vacancies:
            score, details = matching_service.match_candidate_to_vacancy(
                candidate.to_dict(),
                vacancy.to_dict()
            )
            matches.append((vacancy.to_dict(), score, details))
        
        matches.sort(key=lambda x: x[1], reverse=True)
        matches = matches[:limit]
        
        stats = matching_service.get_matching_stats(matches)
        
        response_matches = []
        for vacancy, score, details in matches:
            response_matches.append({
                'vacancy_id': vacancy.get('id'),
                'score': round(score, 2),
                'details': {k: round(v, 2) if isinstance(v, float) else v 
                           for k, v in details.items()},
                'match_level': get_match_level(score)
            })
        
        return jsonify({
            'matches': response_matches,
            'statistics': stats
        }), 200
    except Exception as e:
        logger.error(f'Matching error: {e}')
        return jsonify({'error': str(e)}), 500

def get_match_level(score):
    """Determine match level from score."""
    if score >= 80:
        return 'excellent'
    elif score >= 60:
        return 'good'
    elif score >= 40:
        return 'fair'
    else:
        return 'poor'
