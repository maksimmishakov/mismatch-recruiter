import os
from celery.schedules import crontab

class CeleryConfig:
    """Celery configuration for async tasks"""
    
    # Broker and result backend
    broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    result_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1')
    
    # Task settings
    task_serializer = 'json'
    accept_content = ['json']
    result_serializer = 'json'
    timezone = 'UTC'
    enable_utc = True
    
    # Task timeouts
    task_soft_time_limit = 600  # 10 minutes
    task_time_limit = 900  # 15 minutes
    
    # Worker settings
    worker_prefetch_multiplier = 4
    worker_max_tasks_per_child = 1000
    
    # Beat schedule for periodic tasks
    beat_schedule = {
        'clean-expired-matches': {
            'task': 'app.tasks.clean_expired_matches',
            'schedule': crontab(hour=2, minute=0),  # 2 AM daily
        },
        'regenerate-embeddings': {
            'task': 'app.tasks.regenerate_candidate_embeddings',
            'schedule': crontab(hour=4, minute=0),  # 4 AM daily
        },
    }
