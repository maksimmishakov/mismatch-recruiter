"""Optimized API routes with caching and performance enhancements"""

from flask import Blueprint, request, jsonify
from functools import wraps
from app import db
from app.models import Candidate, Match
from app.services.candidate_service import CandidateService
from app.config.ratelimiter import limiter, RATE_LIMITS
import redis
import json

# Initialize Redis cache
cache = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

api_bp = Blueprint('api_optimized', __name__, url_prefix='/api/v2')

def cached_route(timeout=300):
    """Decorator to cache API responses"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = f"{f.__name__}:{request.full_path}"
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
            
            # If not in cache, execute function
            result = f(*args, **kwargs)
            
            # Cache the result
            if isinstance(result, dict):
                cache.setex(cache_key, timeout, json.dumps(result))
            
            return result
        return decorated_function
    return decorator

@api_bp.route('/candidates', methods=['GET'])
@limiter.limit(RATE_LIMITS['authenticated'])
@cached_route(timeout=60)
def get_candidates():
    """Get candidates with caching and optimization"""
    user_id = request.args.get('user_id')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    location = request.args.get('location')
    
    if not user_id:
        return {'error': 'user_id required'}, 400
    
    try:
        result = CandidateService.get_candidates_optimized(
            user_id=user_id,
            page=page,
            per_page=per_page,
            location=location
        )
        return result, 200
    except Exception as e:
        return {'error': str(e)}, 500

@api_bp.route('/candidates/search', methods=['GET'])
@limiter.limit(RATE_LIMITS['search'])
def search_candidates():
    """Search candidates with advanced filtering"""
    user_id = request.args.get('user_id')
    location = request.args.get('location')
    skills = request.args.getlist('skills')
    experience_min = request.args.get('experience_min', type=int)
    
    if not user_id:
        return {'error': 'user_id required'}, 400
    
    try:
        results = CandidateService.search_candidates(
            user_id=user_id,
            location=location,
            skills=skills,
            experience_min=experience_min
        )
        
        return {
            'candidates': [c.to_dict() for c in results],
            'count': len(results)
        }, 200
    except Exception as e:
        return {'error': str(e)}, 500

@api_bp.route('/matches', methods=['GET'])
@limiter.limit(RATE_LIMITS['authenticated'])
@cached_route(timeout=120)
def get_matches():
    """Get matches with optimized queries"""
    user_id = request.args.get('user_id')
    status = request.args.get('status')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    
    if not user_id:
        return {'error': 'user_id required'}, 400
    
    try:
        query = db.session.query(Match).filter(Match.user_id == user_id)
        
        if status:
            query = query.filter(Match.status == status)
        
        total = query.count()
        matches = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return {
            'items': [m.to_dict() for m in matches],
            'total': total,
            'page': page,
            'per_page': per_page
        }, 200
    except Exception as e:
        return {'error': str(e)}, 500

@api_bp.route('/health/detailed', methods=['GET'])
@limiter.limit(RATE_LIMITS['health'])
def health_detailed():
    """Detailed health check with performance metrics"""
    import time
    
    checks = {}
    
    # Database check
    try:
        db.session.execute('SELECT 1')
        checks['database'] = 'healthy'
    except Exception as e:
        checks['database'] = f'unhealthy: {str(e)}'
    
    # Redis check
    try:
        cache.ping()
        checks['redis'] = 'healthy'
    except Exception as e:
        checks['redis'] = f'unhealthy: {str(e)}'
    
    # Connection pool stats
    checks['pool_size'] = db.engine.pool.size()
    checks['pool_checked_in'] = db.engine.pool.checkedin()
    checks['pool_checked_out'] = db.engine.pool.checkedout()
    
    return {
        'service': 'mismatch-recruiter-api',
        'status': 'healthy',
        'timestamp': time.time(),
        'checks': checks
    }, 200
