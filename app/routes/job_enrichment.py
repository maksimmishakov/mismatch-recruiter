"""АПИ endpoints для обогащения вакансий."""

from flask import Blueprint, request, jsonify
from app.database import SessionLocal
from app.models import Job
from app.tasks.job_enrichment import enrich_job
from app.logger import get_logger

logger = get_logger("routes.job_enrichment")

job_enrichment_bp = Blueprint('job_enrichment', __name__, url_prefix='/api/jobs')

@job_enrichment_bp.route('/<int:job_id>/enrich', methods=['POST'])
def trigger_job_enrichment(job_id):
    """
    Запустить обогащение вакансии.
    
    POST /api/jobs/123/enrich
    """
    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        task = enrich_job.delay(job_id)
        
        logger.info(f"Triggered enrichment for job {job_id}, task_id={task.id}")
        
        return jsonify({
            'job_id': job_id,
            'task_id': task.id,
            'status': 'queued',
            'message': 'Job enrichment started'
        }), 202
        
    finally:
        db.close()

@job_enrichment_bp.route('/<int:job_id>/enriched', methods=['GET'])
def get_enriched_job(job_id):
    """
    Получить обогащенные данные вакансии.
    
    GET /api/jobs/123/enriched
    """
    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        return jsonify({
            'id': job.id,
            'title': job.title,
            'required_skills': job.required_skills or [],
            'seniority_level': job.seniority_level,
            'difficulty_score': job.difficulty_score,
            'benefits': job.benefits_json or [],
            'salary_min': job.salary_min,
            'salary_max': job.salary_max,
            'enrichment_status': job.enrichment_status or 'pending',
            'enriched_at': job.enriched_at.isoformat() if job.enriched_at else None
        })
        
    finally:
        db.close()

@job_enrichment_bp.route('/<int:job_id>/re-enrich', methods=['POST'])
def re_enrich_job(job_id):
    """
    Переобогатить вакансию (очистить и заново).
    
    POST /api/jobs/123/re-enrich
    """
    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        job.enrichment_status = 'pending'
        job.required_skills = None
        job.seniority_level = None
        job.difficulty_score = None
        job.benefits_json = None
        job.salary_min = None
        job.salary_max = None
        
        db.commit()
        
        task = enrich_job.delay(job_id)
        
        logger.info(f"Triggered re-enrichment for job {job_id}")
        
        return jsonify({
            'job_id': job_id,
            'task_id': task.id,
            'status': 'requeued'
        }), 202
        
    finally:
        db.close()

@job_enrichment_bp.route('/enrich-status/<task_id>', methods=['GET'])
def get_enrich_status(task_id):
    """
    Получить статус задачи обогащения.
    
    GET /api/jobs/enrich-status/abc123
    """
    from celery.result import AsyncResult
    
    task = AsyncResult(task_id)
    
    return jsonify({
        'task_id': task_id,
        'state': task.state,
        'result': task.result if task.successful() else None,
        'error': str(task.info) if task.failed() else None
    })
