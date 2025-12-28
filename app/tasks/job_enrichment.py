"""Асинхронная задача обогащения вакансий."""

from celery import shared_task
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Job
from app.services.job_enrichment_service import JobEnrichmentService
from app.logger import get_logger
from datetime import datetime

logger = get_logger("tasks.job_enrichment")
enricher = JobEnrichmentService()

@shared_task(bind=True, max_retries=3)
def enrich_job(self, job_id: int):
    """
    Обогатить вакансию асинхронно.
    
    Args:
        job_id: ID вакансии для обогащения
    """
    db = SessionLocal()
    try:
        logger.info(f"Starting enrich_job task for job_id={job_id}")
        
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            logger.error(f"Job {job_id} not found")
            return {'status': 'error', 'message': 'Job not found'}
        
        logger.info(f"Enriching job {job_id}")
        enriched = enricher.enrich(
            job_title=job.title,
            job_description=job.description or "",
            requirements=job.requirements or ""
        )
        
        job.required_skills = enriched['required_skills']
        job.seniority_level = enriched['seniority_level']
        job.difficulty_score = enriched['difficulty_score']
        job.benefits_json = enriched['benefits']
        job.salary_min = enriched.get('salary_min')
        job.salary_max = enriched.get('salary_max')
        job.enrichment_status = enriched['enrichment_status']
        job.enriched_at = datetime.utcnow()
        
        db.commit()
        logger.info(f"Job {job_id} enriched successfully: "
                   f"level={enriched['seniority_level']}, "
                   f"difficulty={enriched['difficulty_score']:.2f}")
        
        return {
            'status': 'success',
            'job_id': job_id,
            'seniority_level': enriched['seniority_level'],
            'difficulty_score': enriched['difficulty_score'],
            'skills_count': len(enriched['required_skills'])
        }
        
    except Exception as exc:
        logger.error(f"Error enriching job {job_id}: {exc}", exc_info=True)
        
        try:
            job = db.query(Job).filter(Job.id == job_id).first()
            if job:
                job.enrichment_status = 'error'
            db.commit()
        except Exception as db_exc:
            logger.error(f"Failed to save error status: {db_exc}")
        
        db.rollback()
        raise self.retry(exc=exc, countdown=60)
        
    finally:
        db.close()

@shared_task
def enrich_all_pending_jobs():
    """Обогатить все вакансии со статусом 'pending'."""
    db = SessionLocal()
    try:
        pending = db.query(Job).filter(
            Job.enrichment_status == 'pending'
        ).limit(100).all()
        
        logger.info(f"Found {len(pending)} pending jobs for enrichment")
        
        for job in pending:
            enrich_job.delay(job.id)
        
        return {'count': len(pending)}
    finally:
        db.close()
