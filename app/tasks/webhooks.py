"""Webhook event handler tasks."""

import logging
import json
from typing import Dict, Any
from celery import shared_task
from datetime import datetime
import hmac
import hashlib

from app.models import WebhookEvent, Job
from app.services.health_check import log_service_operation
from app.config import settings

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def process_webhook(self, webhook_id: int, event_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process incoming webhook events asynchronously.
    
    Args:
        webhook_id: ID of the webhook configuration
        event_data: The webhook event data payload
        
    Returns:
        Dict with processing result
    """
    try:
        start_time = datetime.utcnow()
        
        # Validate webhook signature
        if not _validate_webhook_signature(event_data):
            logger.warning(f"Invalid webhook signature for webhook {webhook_id}")
            return {"error": "Invalid signature", "webhook_id": webhook_id}
        
        # Process based on event type
        event_type = event_data.get('type')
        
        if event_type == 'job.created':
            result = _handle_job_created(event_data)
        elif event_type == 'job.updated':
            result = _handle_job_updated(event_data)
        elif event_type == 'job.closed':
            result = _handle_job_closed(event_data)
        elif event_type == 'application.submitted':
            result = _handle_application_submitted(event_data)
        else:
            logger.warning(f"Unknown webhook event type: {event_type}")
            result = {"error": f"Unknown event type: {event_type}"}
        
        # Store webhook event record
        from app import db
        webhook_event = WebhookEvent(
            webhook_id=webhook_id,
            event_type=event_type,
            payload=json.dumps(event_data),
            status='processed',
            created_at=datetime.utcnow()
        )
        db.session.add(webhook_event)
        db.session.commit()
        
        # Log operation
        duration = (datetime.utcnow() - start_time).total_seconds()
        log_service_operation(
            service="webhooks",
            operation="process_webhook",
            status="success",
            duration=duration,
            metadata={"webhook_id": webhook_id, "event_type": event_type}
        )
        
        logger.info(f"Processed webhook {webhook_id} with event {event_type}")
        return {"webhook_id": webhook_id, "event_type": event_type, **result}
        
    except Exception as exc:
        logger.error(f"Error processing webhook {webhook_id}: {exc}")
        raise self.retry(exc=exc)


def _validate_webhook_signature(event_data: Dict[str, Any]) -> bool:
    """
    Validate webhook signature to ensure authenticity.
    
    Args:
        event_data: The webhook event data
        
    Returns:
        True if signature is valid
    """
    try:
        signature = event_data.get('signature')
        if not signature:
            return False
        
        # Create expected signature
        payload = json.dumps(event_data.get('payload', {}))
        expected_sig = hmac.new(
            settings.WEBHOOK_SECRET.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_sig)
        
    except Exception as e:
        logger.error(f"Error validating webhook signature: {e}")
        return False


def _handle_job_created(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle job.created webhook event."""
    try:
        job_data = event_data.get('data', {})
        logger.info(f"New job created: {job_data.get('job_id')}")
        # Trigger candidate matching for new job
        from .matching import match_candidates
        match_candidates.delay(job_data.get('job_id'))
        return {"action": "matching_triggered"}
    except Exception as e:
        logger.error(f"Error handling job.created: {e}")
        return {"error": str(e)}


def _handle_job_updated(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle job.updated webhook event."""
    try:
        job_data = event_data.get('data', {})
        logger.info(f"Job updated: {job_data.get('job_id')}")
        return {"action": "job_updated"}
    except Exception as e:
        logger.error(f"Error handling job.updated: {e}")
        return {"error": str(e)}


def _handle_job_closed(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle job.closed webhook event."""
    try:
        job_data = event_data.get('data', {})
        logger.info(f"Job closed: {job_data.get('job_id')}")
        return {"action": "job_closed"}
    except Exception as e:
        logger.error(f"Error handling job.closed: {e}")
        return {"error": str(e)}


def _handle_application_submitted(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle application.submitted webhook event."""
    try:
        app_data = event_data.get('data', {})
        logger.info(f"Application submitted: {app_data.get('application_id')}")
        return {"action": "application_submitted"}
    except Exception as e:
        logger.error(f"Error handling application.submitted: {e}")
        return {"error": str(e)}
