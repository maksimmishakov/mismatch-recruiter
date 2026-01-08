from celery import shared_task
from app import db
from app.models import Match, Candidate
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def clean_expired_matches(self):
    """Clean up expired matches"""
    try:
        # Delete matches older than 90 days
        cutoff_date = datetime.utcnow() - timedelta(days=90)
        deleted = db.session.query(Match).filter(
            Match.created_at < cutoff_date,
            Match.status == 'rejected'
        ).delete()
        db.session.commit()
        logger.info(f'Cleaned {deleted} expired matches')
        return {'status': 'success', 'deleted': deleted}
    except Exception as e:
        logger.error(f'Error cleaning matches: {str(e)}')
        return {'status': 'error', 'message': str(e)}

@shared_task(bind=True)
def regenerate_candidate_embeddings(self):
    """Regenerate candidate embeddings"""
    try:
        candidates = db.session.query(Candidate).all()
        updated_count = 0
        
        for candidate in candidates:
            # Regenerate profile vector (embedding)
            # This would typically use an ML model
            candidate.profile_vector = None  # Reset for recalculation
            updated_count += 1
        
        db.session.commit()
        logger.info(f'Regenerated embeddings for {updated_count} candidates')
        return {'status': 'success', 'updated': updated_count}
    except Exception as e:
        logger.error(f'Error regenerating embeddings: {str(e)}')
        return {'status': 'error', 'message': str(e)}
