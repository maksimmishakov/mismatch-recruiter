"""Webhook delivery service with signature verification."""

import json
import hmac
import hashlib
import requests
from typing import Dict, Any
from app.logger import get_logger

logger = get_logger("webhooks")


class WebhookService:
    """Service for managing webhook delivery and verification."""
   
    def __init__(self, timeout=10, max_retries=3):
        self.timeout = timeout
        self.max_retries = max_retries
   
    def send_webhook(self, webhook, payload: Dict[str, Any]) -> Dict:
        """Send webhook to target URL."""
        try:
            headers = {'Content-Type': 'application/json'}
           
            if webhook.secret:
                signature = self._create_signature(webhook.secret, payload)
                headers['X-Webhook-Signature'] = signature
           
            response = requests.post(
                webhook.url,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
           
            logger.info(f"Webhook sent to {webhook.url}: {response.status_code}")
           
            return {
                'success': response.status_code < 400,
                'status_code': response.status_code,
                'response': response.text[:500]
            }
           
        except requests.Timeout:
            logger.error(f"Webhook timeout: {webhook.url}")
            return {'success': False, 'status_code': 0, 'response': 'Timeout'}
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return {'success': False, 'status_code': 0, 'response': str(e)}
   
    @staticmethod
    def _create_signature(secret: str, payload: Dict) -> str:
        """Create HMAC SHA256 signature for webhook."""
        payload_str = json.dumps(payload, sort_keys=True)
        signature = hmac.new(
            secret.encode(),
            payload_str.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature
   
    @staticmethod
    def verify_signature(secret: str, payload: str, signature: str) -> bool:
        """Verify webhook signature authenticity."""
        expected_signature = hmac.new(
            secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(signature, expected_signature)
