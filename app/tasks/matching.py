"""ML candidate matching task."""

import logging
from typing import List, Dict, Any
from celery import shared_task
from datetime import datetime
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from app.models import Candidate, Job, Match
from app.services.health_check import log_service_operation
from app.config import settings

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def match_candidates(self, job_id: int) -> Dict[str, Any]:
    """
    Match candidates to a job using ML-based similarity scoring.
    
    Args:
        job_id: ID of the job to match candidates against
        
    Returns:
        Dict with matching results and statistics
    """
    try:
        start_time = datetime.utcnow()
        
        # Get job details
        job = Job.query.get(job_id)
        if not job:
            logger.error(f"Job {job_id} not found")
            return {"error": "Job not found", "job_id": job_id}
        
        # Get all active candidates
        candidates = Candidate.query.filter_by(is_active=True).all()
        if not candidates:
            logger.warning(f"No active candidates for job {job_id}")
            return {"message": "No candidates available", "matches": []}
        
        # Generate job embedding
        job_vector = _generate_embedding(job.description, job.requirements)
        
        matches = []
        for candidate in candidates:
            # Generate candidate embedding
            candidate_vector = _generate_embedding(
                candidate.skills, candidate.experience
            )
            
            # Calculate similarity score
            similarity = cosine_similarity(
                [job_vector], [candidate_vector]
            )[0][0]
            
            # Store match if score above threshold
            if similarity >= settings.MATCH_THRESHOLD:
                match = Match(
                    job_id=job_id,
                    candidate_id=candidate.id,
                    score=float(similarity),
                    created_at=datetime.utcnow()
                )
                matches.append(match)
        
        # Batch insert matches
        if matches:
            from sqlalchemy import insert
            from app import db
            db.session.bulk_save_objects(matches)
            db.session.commit()
        
        # Log operation
        duration = (datetime.utcnow() - start_time).total_seconds()
        log_service_operation(
            service="matching",
            operation="match_candidates",
            status="success",
            duration=duration,
            metadata={"job_id": job_id, "matches_created": len(matches)}
        )
        
        logger.info(f"Matched {len(matches)} candidates to job {job_id}")
        return {
            "job_id": job_id,
            "matches_created": len(matches),
            "duration": duration
        }
        
    except Exception as exc:
        logger.error(f"Error matching candidates for job {job_id}: {exc}")
        raise self.retry(exc=exc)


def _generate_embedding(text_data: str, additional_data: str = None) -> np.ndarray:
    """
    Generate vector embedding from text data.
    Uses simple TF-IDF approach as placeholder for advanced embeddings.
    
    Args:
        text_data: Primary text to embed
        additional_data: Optional secondary text
        
    Returns:
        Vector embedding as numpy array
    """
    try:
        combined_text = text_data
        if additional_data:
            combined_text = f"{text_data} {additional_data}"
        
        # Placeholder: in production, use transformers/embeddings service
        from sklearn.feature_extraction.text import TfidfVectorizer
        vectorizer = TfidfVectorizer(max_features=100)
        embedding = vectorizer.fit_transform([combined_text])
        return embedding.toarray().flatten()
        
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        return np.zeros(100)
