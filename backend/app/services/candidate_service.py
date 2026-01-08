from app import db
from app.models import Candidate, Match, User
from sqlalchemy.orm import joinedload
from sqlalchemy import and_, or_
import logging

logger = logging.getLogger(__name__)

class CandidateService:
    """Service for optimized candidate operations"""
    
    @staticmethod
    def get_candidates_optimized(user_id, page=1, per_page=20, location=None):
        """Get candidates with optimized query (uses indexes and joinedload)"""
        try:
            query = db.session.query(Candidate).filter(
                Candidate.user_id == user_id
            )
            
            if location:
                query = query.filter(Candidate.location == location)
            
            # Prevent N+1 queries with joinedload
            query = query.options(joinedload(Candidate.matches))
            
            total = query.count()
            candidates = query.offset((page - 1) * per_page).limit(per_page).all()
            
            return {
                'items': candidates,
                'total': total,
                'page': page,
                'per_page': per_page,
                'pages': (total + per_page - 1) // per_page
            }
        except Exception as e:
            logger.error(f'Error in get_candidates_optimized: {str(e)}')
            raise
    
    @staticmethod
    def search_candidates(user_id, skills=None, experience_min=None, location=None):
        """Advanced search with multiple filters - uses indexes"""
        query = db.session.query(Candidate).filter(
            Candidate.user_id == user_id
        )
        
        if location:
            query = query.filter(Candidate.location == location)
        
        if experience_min:
            query = query.filter(Candidate.experience >= experience_min)
        
        if skills:
            for skill in skills:
                query = query.filter(Candidate.skills.astext.cast(float) >= 0.7)
        
        return query.order_by(Candidate.created_at.desc()).all()
    
    @staticmethod
    def bulk_get_by_ids(candidate_ids):
        """Fetch multiple candidates in one query (no N+1 queries)"""
        return db.session.query(Candidate).filter(
            Candidate.id.in_(candidate_ids)
        ).all()
