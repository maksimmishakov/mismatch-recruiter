"""Celery Asynchronous Processing Configuration"""
from celery import Celery
from celery.schedules import crontab
import os
from datetime import datetime, timedelta


def make_celery(app):
    """Create and configure Celery instance"""
    celery = Celery(
        app.import_name,
        backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1'),
        broker=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    )
    
    # Task configuration
    celery.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        task_track_started=True,
        task_time_limit=30 * 60,  # 30 minutes hard limit
        task_soft_time_limit=25 * 60,  # 25 minutes soft limit
        worker_prefetch_multiplier=1,
        worker_max_tasks_per_child=1000,
        task_acks_late=True,
        result_expires=3600,
    )
    
    # Periodic tasks (Celery Beat schedule)
    celery.conf.beat_schedule = {
        'cleanup-old-logs': {
            'task': 'app.tasks.maintenance.cleanup_old_logs',
            'schedule': crontab(hour=2, minute=0),  # Every day at 2 AM
        },
        'process-webhook-retries': {
            'task': 'app.tasks.webhooks.process_webhook_retries',
            'schedule': crontab(minute='*/5'),  # Every 5 minutes
        },
        'update-match-cache': {
            'task': 'app.tasks.cache.update_match_cache',
            'schedule': crontab(hour='*/1'),  # Every hour
        },
        'send-weekly-digest': {
            'task': 'app.tasks.notifications.send_weekly_digest',
            'schedule': crontab(day_of_week=0, hour=9, minute=0),  # Every Monday at 9 AM
        },
        'backup-database': {
            'task': 'app.tasks.maintenance.backup_database',
            'schedule': crontab(hour=3, minute=0),  # Every day at 3 AM
        },
    }
    
    # Application context task
    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
        
        def on_retry(self, exc, task_id, args, kwargs, einfo):
            """Called when task is retried"""
            super().on_retry(exc, task_id, args, kwargs, einfo)
        
        def on_failure(self, exc, task_id, args, kwargs, einfo):
            """Called when task fails permanently"""
            super().on_failure(exc, task_id, args, kwargs, einfo)
        
        def on_success(self, result, task_id, args, kwargs):
            """Called when task succeeds"""
            super().on_success(result, task_id, args, kwargs)
    
    celery.Task = ContextTask
    return celery
