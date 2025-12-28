import hmac
import hashlib
import json
import logging
import requests
from typing import Optional, Dict, List
from datetime import datetime
from enum import Enum
import asyncio

logger = logging.getLogger(__name__)


class WebhookEvent(Enum):
    """Webhook event types"""
    MATCH_CREATED = "match.created"
    MATCH_PERFECT = "match.perfect"
    REPORT_GENERATED = "report.generated"
    ERROR_OCCURRED = "error.occurred"
    ANALYTICS_SUMMARY = "analytics.summary"


class WebhookIntegrationService:
    """Service for managing and triggering webhooks"""
    
    def __init__(self, secret_key: Optional[str] = None):
        """Initialize webhook service
        
        Args:
            secret_key: Secret key for HMAC signing
        """
        self.secret_key = secret_key or "default-secret-key"
        self.webhooks = {}  # In production, use database
        self.delivery_logs = []  # In production, use database
    
    def _generate_signature(self, payload: str) -> str:
        """Generate HMAC-SHA256 signature for webhook payload
        
        Args:
            payload: JSON payload to sign
            
        Returns:
            Hex-encoded HMAC-SHA256 signature
        """
        return hmac.new(
            self.secret_key.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def register_webhook(
        self,
        webhook_id: str,
        url: str,
        events: List[str],
        secret: Optional[str] = None,
        active: bool = True
    ) -> Dict:
        """Register a new webhook
        
        Args:
            webhook_id: Unique webhook identifier
            url: Webhook endpoint URL
            events: List of events to trigger on
            secret: Optional webhook secret for additional security
            active: Whether webhook is active
            
        Returns:
            Webhook registration details
        """
        try:
            webhook = {
                "id": webhook_id,
                "url": url,
                "events": events,
                "secret": secret or self.secret_key,
                "active": active,
                "created_at": datetime.now().isoformat(),
                "delivery_count": 0,
                "failed_count": 0
            }
            
            self.webhooks[webhook_id] = webhook
            logger.info(f"Webhook registered: {webhook_id} -> {url}")
            
            return webhook
            
        except Exception as e:
            logger.error(f"Failed to register webhook: {str(e)}")
            raise
    
    def unregister_webhook(self, webhook_id: str) -> bool:
        """Unregister a webhook
        
        Args:
            webhook_id: Webhook ID to unregister
            
        Returns:
            True if successful
        """
        try:
            if webhook_id in self.webhooks:
                del self.webhooks[webhook_id]
                logger.info(f"Webhook unregistered: {webhook_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to unregister webhook: {str(e)}")
            return False
    
    def trigger_webhook(
        self,
        event_type: str,
        data: Dict,
        webhook_id: Optional[str] = None
    ) -> Dict:
        """Trigger webhook event
        
        Args:
            event_type: Type of event (match.created, report.generated, etc.)
            data: Event payload data
            webhook_id: Optional specific webhook to trigger (all if None)
            
        Returns:
            Trigger result with delivery status
        """
        try:
            payload = {
                "event": event_type,
                "timestamp": datetime.now().isoformat(),
                "data": data
            }
            
            payload_json = json.dumps(payload)
            signature = self._generate_signature(payload_json)
            
            result = {
                "event": event_type,
                "triggered_at": datetime.now().isoformat(),
                "deliveries": []
            }
            
            # Trigger specific webhook or all matching webhooks
            webhooks_to_trigger = []
            if webhook_id:
                if webhook_id in self.webhooks:
                    webhooks_to_trigger = [self.webhooks[webhook_id]]
            else:
                # Find all webhooks subscribed to this event
                webhooks_to_trigger = [
                    w for w in self.webhooks.values()
                    if w["active"] and event_type in w["events"]
                ]
            
            # Deliver to all matching webhooks
            for webhook in webhooks_to_trigger:
                delivery = self._deliver_webhook(webhook, payload_json, signature)
                result["deliveries"].append(delivery)
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to trigger webhook: {str(e)}")
            raise
    
    def _deliver_webhook(
        self,
        webhook: Dict,
        payload: str,
        signature: str
    ) -> Dict:
        """Deliver webhook payload
        
        Args:
            webhook: Webhook configuration
            payload: JSON payload
            signature: HMAC signature
            
        Returns:
            Delivery result
        """
        delivery = {
            "webhook_id": webhook["id"],
            "url": webhook["url"],
            "timestamp": datetime.now().isoformat(),
            "status": "pending",
            "attempts": 0,
            "error": None
        }
        
        try:
            headers = {
                "Content-Type": "application/json",
                "X-Webhook-Signature": f"sha256={signature}",
                "X-Webhook-ID": webhook["id"]
            }
            
            # Attempt delivery with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = requests.post(
                        webhook["url"],
                        data=payload,
                        headers=headers,
                        timeout=10
                    )
                    
                    delivery["attempts"] = attempt + 1
                    
                    if response.status_code == 200:
                        delivery["status"] = "success"
                        webhook["delivery_count"] = webhook.get("delivery_count", 0) + 1
                        logger.info(f"Webhook delivered: {webhook['id']}")
                        break
                    else:
                        delivery["status"] = f"http_{response.status_code}"
                        if attempt < max_retries - 1:
                            asyncio.sleep(2 ** attempt)  # Exponential backoff
                        
                except requests.exceptions.RequestException as e:
                    delivery["status"] = "failed"
                    delivery["error"] = str(e)
                    webhook["failed_count"] = webhook.get("failed_count", 0) + 1
                    
                    if attempt < max_retries - 1:
                        asyncio.sleep(2 ** attempt)
                    else:
                        logger.error(f"Webhook delivery failed after {max_retries} attempts: {webhook['id']}")
                        
        except Exception as e:
            delivery["status"] = "error"
            delivery["error"] = str(e)
            logger.error(f"Error delivering webhook: {str(e)}")
        
        # Log delivery
        self.delivery_logs.append(delivery)
        
        return delivery
    
    def verify_signature(self, payload: str, signature: str) -> bool:
        """Verify webhook signature
        
        Args:
            payload: JSON payload
            signature: Provided signature
            
        Returns:
            True if signature is valid
        """
        expected_signature = self._generate_signature(payload)
        return hmac.compare_digest(signature, expected_signature)
    
    def get_webhook_status(self, webhook_id: str) -> Optional[Dict]:
        """Get webhook status
        
        Args:
            webhook_id: Webhook ID
            
        Returns:
            Webhook status or None
        """
        if webhook_id in self.webhooks:
            webhook = self.webhooks[webhook_id]
            return {
                "id": webhook["id"],
                "url": webhook["url"],
                "active": webhook["active"],
                "events": webhook["events"],
                "delivery_count": webhook.get("delivery_count", 0),
                "failed_count": webhook.get("failed_count", 0),
                "created_at": webhook["created_at"]
            }
        return None
    
    def get_delivery_logs(
        self,
        webhook_id: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict]:
        """Get webhook delivery logs
        
        Args:
            webhook_id: Filter by webhook ID (optional)
            limit: Maximum number of logs to return
            
        Returns:
            List of delivery logs
        """
        logs = self.delivery_logs
        if webhook_id:
            logs = [log for log in logs if log["webhook_id"] == webhook_id]
        return logs[-limit:]
    
    def list_webhooks(self) -> List[Dict]:
        """List all registered webhooks
        
        Returns:
            List of webhook configurations
        """
        return list(self.webhooks.values())
    
    def update_webhook(
        self,
        webhook_id: str,
        **kwargs
    ) -> Optional[Dict]:
        """Update webhook configuration
        
        Args:
            webhook_id: Webhook ID
            **kwargs: Fields to update (url, events, active, etc.)
            
        Returns:
            Updated webhook or None
        """
        if webhook_id in self.webhooks:
            webhook = self.webhooks[webhook_id]
            for key, value in kwargs.items():
                if key in webhook:
                    webhook[key] = value
            logger.info(f"Webhook updated: {webhook_id}")
            return webhook
        return None
