webhook_routes_integration_service.py"""Webhook Routes Integration Service

Handles webhook endpoint registration, verification, and routing for:
- Lamoda job updates
- Candidate profile changes
- Placement status updates
- External system events
"""
import logging
import hmac
import hashlib
from typing import Dict, Optional, Callable, Any
from datetime import datetime
from enum import Enum
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class WebhookEventType(Enum):
    """Webhook event types"""
    JOB_CREATED = "job.created"
    JOB_UPDATED = "job.updated"
    JOB_DELETED = "job.deleted"
    CANDIDATE_CREATED = "candidate.created"
    CANDIDATE_UPDATED = "candidate.updated"
    PLACEMENT_CREATED = "placement.created"
    PLACEMENT_UPDATED = "placement.updated"
    SYNC_COMPLETED = "sync.completed"
    SYNC_FAILED = "sync.failed"


@dataclass
class WebhookPayload:
    """Webhook payload structure"""
    event_type: str
    timestamp: str
    data: Dict[str, Any]
    event_id: str


class WebhookRoutesIntegrationService:
    """Service for webhook routing and verification"""
    
    def __init__(self, secret: Optional[str] = None):
        """Initialize webhook service
        
        Args:
            secret: Webhook signing secret
        """
        self.secret = secret
        self.routes: Dict[str, Callable] = {}
        self.event_handlers: Dict[str, list] = {}
    
    def register_route(self, event_type: str, handler: Callable) -> bool:
        """Register webhook event handler
        
        Args:
            event_type: Event type identifier
            handler: Callback function
            
        Returns:
            bool: True if registered
        """
        try:
            if event_type not in self.event_handlers:
                self.event_handlers[event_type] = []
            
            self.event_handlers[event_type].append(handler)
            logger.info(f"Registered handler for event: {event_type}")
            return True
        except Exception as e:
            logger.error(f"Failed to register handler: {e}")
            return False
    
    def verify_signature(self, payload: str, signature: str) -> bool:
        """Verify webhook signature
        
        Args:
            payload: Webhook payload string
            signature: Webhook signature header
            
        Returns:
            bool: True if signature is valid
        """
        if not self.secret:
            logger.warning("Webhook secret not configured")
            return False
        
        try:
            expected_signature = hmac.new(
                self.secret.encode(),
                payload.encode(),
                hashlib.sha256
            ).hexdigest()
            
            # Compare signatures safely
            return hmac.compare_digest(signature, expected_signature)
        except Exception as e:
            logger.error(f"Signature verification failed: {e}")
            return False
    
    async def process_webhook(self, payload: Dict[str, Any]) -> bool:
        """Process incoming webhook
        
        Args:
            payload: Webhook payload
            
        Returns:
            bool: True if processed successfully
        """
        try:
            event_type = payload.get("event_type")
            
            if event_type not in self.event_handlers:
                logger.warning(f"No handlers registered for: {event_type}")
                return False
            
            handlers = self.event_handlers[event_type]
            for handler in handlers:
                try:
                    result = await handler(payload) if hasattr(handler, '__await__') else handler(payload)
                    logger.info(f"Handler executed for {event_type}")
                except Exception as e:
                    logger.error(f"Handler failed: {e}")
                    return False
            
            return True
        except Exception as e:
            logger.error(f"Webhook processing failed: {e}")
            return False
    
    def format_webhook_event(self,
                            event_type: str,
                            data: Dict[str, Any],
                            event_id: str = None) -> WebhookPayload:
        """Format webhook event
        
        Args:
            event_type: Event type
            data: Event data
            event_id: Optional event ID
            
        Returns:
            WebhookPayload instance
        """
        import uuid
        return WebhookPayload(
            event_type=event_type,
            timestamp=datetime.utcnow().isoformat(),
            data=data,
            event_id=event_id or str(uuid.uuid4())
        )
    
    def get_registered_events(self) -> list:
        """Get list of registered events
        
        Returns:
            List of event types
        """
        return list(self.event_handlers.keys())
    
    def unregister_route(self, event_type: str) -> bool:
        """Unregister all handlers for event type
        
        Args:
            event_type: Event type
            
        Returns:
            bool: True if unregistered
        """
        try:
            if event_type in self.event_handlers:
                del self.event_handlers[event_type]
                logger.info(f"Unregistered handlers for: {event_type}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to unregister route: {e}")
            return False


# Singleton instance
_webhook_service: Optional[WebhookRoutesIntegrationService] = None


def get_webhook_service(secret: Optional[str] = None) -> WebhookRoutesIntegrationService:
    """Get or create singleton webhook service
    
    Args:
        secret: Optional webhook secret
        
    Returns:
        WebhookRoutesIntegrationService instance
    """
    global _webhook_service
    if _webhook_service is None:
        _webhook_service = WebhookRoutesIntegrationService(secret)
    return _webhook_service
