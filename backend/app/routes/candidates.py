from flask import Blueprint, request, jsonify
from sqlalchemy import desc
from app import db
from app.models import Candidate
from app.schemas import candidate_schema, candidates_schema

bp = Blueprint('candidates', __name__, url_prefix='/api/candidates')

# GET all candidates with pagination
@bp.route('', methods=['GET'])
def get_candidates():
    """
    Get all candidates with pagination and filtering
    Query parameters:
    - page: int (default 1)
    - per_page: int (default 20, max 100)
    - status: str (filter by status)
    - experience_min: int (filter by minimum years)
    """
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Validate pagination parameters
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 20
        
        # Build base query
        query = Candidate.query
        
        # Apply filters
        status = request.args.get('status')
        if status:
            query = query.filter_by(status=status)
        
        experience_min = request.args.get('experience_min', type=int)
        if experience_min is not None:
            query = query.filter(Candidate.experience_years >= experience_min)
        
        # Get total count before pagination
        total = query.count()
        
        # Apply pagination and sorting
        pagination = query.order_by(desc(Candidate.created_at)).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': candidates_schema.dump(pagination.items),
            'pagination': {
                'current_page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# GET single candidate
@bp.route('/<int:candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    candidate = Candidate.query.get_or_404(candidate_id)
    return jsonify({
        'success': True,
        'data': candidate_schema.dump(candidate)
    }), 200

# POST create new candidate
@bp.route('', methods=['POST'])
def create_candidate():
    try:
        data = candidate_schema.load(request.get_json())
        candidate = Candidate(**data)
        db.session.add(candidate)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Candidate created',
            'data': candidate_schema.dump(candidate)
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

# PUT update candidate
@bp.route('/<int:candidate_id>', methods=['PUT'])
def update_candidate(candidate_id):
    try:
        candidate = Candidate.query.get_or_404(candidate_id)
        data = candidate_schema.load(request.get_json(), partial=True)
        
        for key, value in data.items():
            setattr(candidate, key, value)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Candidate updated',
            'data': candidate_schema.dump(candidate)
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

# DELETE candidate
@bp.route('/<int:candidate_id>', methods=['DELETE'])
def delete_candidate(candidate_id):
    try:
        candidate = Candidate.query.get_or_404(candidate_id)
        db.session.delete(candidate)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Candidate deleted'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400
