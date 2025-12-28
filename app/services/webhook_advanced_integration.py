"""Advanced Webhook Integration Service
Phase 5 Step 6.2 - Event routing, retry mechanisms, encryption
Supports: HMAC signing, exponential backoff, webhook templates
"""
import asyncio
import hmac
import hashlib
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import aiohttp
from abc import ABC, abstractmethod
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class WebhookEventType(Enum):
    """Webhook event types"""
    CANDIDATE_UPDATED = "candidate.updated"
    JOB_MATCHED = "job.matched"
    APPLICATION_SUBMITTED = "application.submitted"
    INTERVIEW_SCHEDULED = "interview.scheduled"
    OFFER_EXTENDED = "offer.extended"
    INTEGRATION_ERROR = "integration.error"


class RetryStrategy(Enum):
    """Retry strategies for webhook delivery"""
    EXPONENTIAL = "exponential"
    LINEAR = "linear"
    IMMEDIATE = "immediate"


@dataclass
class WebhookEvent:
    """Webhook event data structure"""
    event_type: str
    timestamp: datetime
    correlation_id: str
    payload: Dict[str, Any]
    source_system: str
    user_id: str
    metadata: Optional[Dict] = None

    def to_json(self) -> str:
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return json.dumps(data)


@dataclass
class WebhookConfig:
    """Webhook configuration"""
    url: str
    event_types: List[str]
    secret_key: str
    retry_count: int = 3
    retry_strategy: str = RetryStrategy.EXPONENTIAL.value
    timeout: int = 30
    headers: Optional[Dict[str, str]] = None
    active: bool = True
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()


class WebhookEventRepository:
    """Repository for webhook events"""
    def __init__(self):
        self.events: Dict[str, WebhookEvent] = {}
        self.delivery_log: List[Dict] = []

    async def store_event(self, event: WebhookEvent) -> None:
        self.events[event.correlation_id] = event

    async def get_event(self, correlation_id: str) -> Optional[WebhookEvent]:
        return self.events.get(correlation_id)

    async def log_delivery(self, event_id: str, url: str, status: int, 
                          attempts: int, error: Optional[str] = None) -> None:
        self.delivery_log.append({
            'event_id': event_id,
            'url': url,
            'status': status,
            'attempts': attempts,
            'timestamp': datetime.utcnow().isoformat(),
            'error': error
        })


class WebhookSignatureGenerator:
    """Generate HMAC signatures for webhook authenticity"""
    @staticmethod
    def generate(payload: str, secret: str) -> str:
        signature = hmac.new(
            secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        return f"sha256={signature}"

    @staticmethod
    def verify(payload: str, signature: str, secret: str) -> bool:
        expected = WebhookSignatureGenerator.generate(payload, secret)
        return hmac.compare_digest(expected, signature)


class WebhookDeliveryStrategy(ABC):
    """Abstract base for delivery strategies"""
    @abstractmethod
    async def deliver(self, url: str, event: WebhookEvent, 
                     config: WebhookConfig) -> Dict[str, Any]:
        pass


class ExponentialBackoffStrategy(WebhookDeliveryStrategy):
    """Exponential backoff retry strategy"""
    async def deliver(self, url: str, event: WebhookEvent, 
                     config: WebhookConfig) -> Dict[str, Any]:
        payload = event.to_json()
        signature = WebhookSignatureGenerator.generate(payload, config.secret_key)
        
        headers = {
            'Content-Type': 'application/json',
            'X-Webhook-Signature': signature,
            'X-Event-Type': event.event_type,
            'X-Correlation-ID': event.correlation_id,
            'X-Timestamp': event.timestamp.isoformat()
        }
        if config.headers:
            headers.update(config.headers)

        async with aiohttp.ClientSession() as session:
            for attempt in range(config.retry_count):
                try:
                    async with session.post(
                        url, 
                        data=payload,
                        headers=headers,
                        timeout=aiohttp.ClientTimeout(total=config.timeout)
                    ) as response:
                        if response.status in [200, 201, 202]:
                            logger.info(f"Webhook delivered: {event.correlation_id}")
                            return {
                                'success': True,
                                'status': response.status,
                                'attempts': attempt + 1
                            }
                        elif attempt < config.retry_count - 1:
                            wait_time = 2 ** attempt
                            logger.warning(
                                f"Webhook retry {attempt + 1}, waiting {wait_time}s"
                            )
                            await asyncio.sleep(wait_time)
                except asyncio.TimeoutError:
                    if attempt < config.retry_count - 1:
                        await asyncio.sleep(2 ** attempt)
                except Exception as e:
                    logger.error(f"Webhook delivery error: {str(e)}")
                    if attempt < config.retry_count - 1:
                        await asyncio.sleep(2 ** attempt)

        return {'success': False, 'attempts': config.retry_count}


class LinearBackoffStrategy(WebhookDeliveryStrategy):
    """Linear backoff retry strategy"""
    async def deliver(self, url: str, event: WebhookEvent, 
                     config: WebhookConfig) -> Dict[str, Any]:
        payload = event.to_json()
        signature = WebhookSignatureGenerator.generate(payload, config.secret_key)
        
        headers = {
            'Content-Type': 'application/json',
            'X-Webhook-Signature': signature,
            'X-Event-Type': event.event_type,
            'X-Correlation-ID': event.correlation_id
        }

        async with aiohttp.ClientSession() as session:
            for attempt in range(config.retry_count):
                try:
                    async with session.post(
                        url,
                        data=payload,
                        headers=headers,
                        timeout=aiohttp.ClientTimeout(total=config.timeout)
                    ) as response:
                        if response.status in [200, 201, 202]:
                            return {'success': True, 'status': response.status}
                        elif attempt < config.retry_count - 1:
                            wait_time = (attempt + 1) * 5
                            await asyncio.sleep(wait_time)
                except Exception:
                    if attempt < config.retry_count - 1:
                        await asyncio.sleep((attempt + 1) * 5)

        return {'success': False}


class WebhookDispatcher:
    """Main webhook dispatcher service"""
    def __init__(self):
        self.repository = WebhookEventRepository()
        self.strategies: Dict[str, WebhookDeliveryStrategy] = {
            RetryStrategy.EXPONENTIAL.value: ExponentialBackoffStrategy(),
            RetryStrategy.LINEAR.value: LinearBackoffStrategy()
        }
        self.webhooks: Dict[str, WebhookConfig] = {}

    def register_webhook(self, webhook_id: str, config: WebhookConfig) -> None:
        self.webhooks[webhook_id] = config
        logger.info(f"Webhook registered: {webhook_id}")

    def unregister_webhook(self, webhook_id: str) -> None:
        if webhook_id in self.webhooks:
            del self.webhooks[webhook_id]
            logger.info(f"Webhook unregistered: {webhook_id}")

    async def dispatch(self, event: WebhookEvent) -> Dict[str, Any]:
        """Dispatch event to registered webhooks"""
        await self.repository.store_event(event)
        results = {}

        for webhook_id, config in self.webhooks.items():
            if not config.active or event.event_type not in config.event_types:
                continue

            strategy = self.strategies.get(
                config.retry_strategy,
                self.strategies[RetryStrategy.EXPONENTIAL.value]
            )
            
            result = await strategy.deliver(config.url, event, config)
            results[webhook_id] = result
            await self.repository.log_delivery(
                event.correlation_id,
                config.url,
                result.get('status', 0),
                result.get('attempts', 0),
                result.get('error')
            )

        return results

    async def dispatch_batch(self, events: List[WebhookEvent]) -> Dict[str, Dict]:
        """Dispatch multiple events"""
        tasks = [self.dispatch(event) for event in events]
        return dict(zip([e.correlation_id for e in events], 
                       await asyncio.gather(*tasks)))


class WebhookService:
    """High-level webhook service API"""
    def __init__(self):
        self.dispatcher = WebhookDispatcher()

    def register_webhook(self, webhook_id: str, url: str, event_types: List[str],
                        secret_key: str, retry_strategy: str = "exponential") -> None:
        config = WebhookConfig(
            url=url,
            event_types=event_types,
            secret_key=secret_key,
            retry_strategy=retry_strategy
        )
        self.dispatcher.register_webhook(webhook_id, config)

    async def publish_event(self, event_type: str, user_id: str, 
                           payload: Dict[str, Any], source_system: str,
                           correlation_id: str) -> Dict[str, Any]:
        event = WebhookEvent(
            event_type=event_type,
            timestamp=datetime.utcnow(),
            correlation_id=correlation_id,
            payload=payload,
            source_system=source_system,
            user_id=user_id
        )
        return await self.dispatcher.dispatch(event)


if __name__ == "__main__":
    logger.info("Advanced Webhook Integration Service initialized")
