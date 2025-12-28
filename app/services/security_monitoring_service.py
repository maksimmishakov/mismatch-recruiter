"""Security Monitoring Service - JWT auth, rate limiting, audit logging, metrics."""

import hashlib
import hmac
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from functools import wraps
from collections import defaultdict
from enum import Enum

import jwt
from fastapi import HTTPException, Request, Depends
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Float, Text
from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)


class SecurityLevel(str, Enum):
    """Security audit levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AuditEntry:
    """Audit log entry."""

    def __init__(
        self,
        action: str,
        actor: str,
        resource: str,
        level: SecurityLevel,
        details: Dict,
        result: bool = True,
        timestamp: Optional[datetime] = None,
    ):
        self.action = action
        self.actor = actor
        self.resource = resource
        self.level = level
        self.details = details
        self.result = result
        self.timestamp = timestamp or datetime.utcnow()

    def to_dict(self) -> Dict:
        """Convert to dict."""
        return {
            "action": self.action,
            "actor": self.actor,
            "resource": self.resource,
            "level": self.level.value,
            "details": self.details,
            "result": self.result,
            "timestamp": self.timestamp.isoformat(),
        }


class RateLimiter:
    """Token bucket rate limiter."""

    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.buckets: Dict[str, List[datetime]] = defaultdict(list)

    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed."""
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=self.window_seconds)

        # Remove old entries
        self.buckets[client_id] = [
            ts for ts in self.buckets[client_id] if ts > window_start
        ]

        if len(self.buckets[client_id]) < self.max_requests:
            self.buckets[client_id].append(now)
            return True
        return False

    def get_retry_after(self, client_id: str) -> int:
        """Get seconds until next request allowed."""
        if not self.buckets[client_id]:
            return 0
        oldest = self.buckets[client_id][0]
        retry_at = oldest + timedelta(seconds=self.window_seconds)
        return int((retry_at - datetime.utcnow()).total_seconds()) + 1


class JWTManager:
    """JWT token management."""

    def __init__(self, secret: str, algorithm: str = "HS256"):
        self.secret = secret
        self.algorithm = algorithm

    def create_token(
        self,
        data: Dict,
        expires_in_minutes: int = 60,
    ) -> str:
        """Create JWT token."""
        payload = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
        payload.update({"exp": expire, "iat": datetime.utcnow()})

        return jwt.encode(
            payload,
            self.secret,
            algorithm=self.algorithm,
        )

    def verify_token(self, token: str) -> Dict:
        """Verify and decode JWT token."""
        try:
            return jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm],
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")


class SecurityMonitoringService:
    """Main security monitoring service."""

    def __init__(
        self,
        jwt_secret: str,
        max_requests: int = 100,
        window_seconds: int = 60,
    ):
        self.jwt_manager = JWTManager(jwt_secret)
        self.rate_limiter = RateLimiter(max_requests, window_seconds)
        self.audit_log: List[AuditEntry] = []
        self.metrics = {
            "total_requests": 0,
            "failed_auth": 0,
            "rate_limited": 0,
            "audit_events": 0,
        }

    def rate_limit(
        self,
        max_requests: int = 100,
        window_seconds: int = 60,
    ):
        """Rate limiting decorator."""

        def decorator(func):
            @wraps(func)
            async def wrapper(
                request: Request,
                *args,
                **kwargs,
            ):
                client_id = request.client.host
                if not self.rate_limiter.is_allowed(client_id):
                    self.metrics["rate_limited"] += 1
                    raise HTTPException(
                        status_code=429,
                        detail="Too many requests",
                        headers={
                            "Retry-After": str(
                                self.rate_limiter.get_retry_after(client_id)
                            )
                        },
                    )
                return await func(request, *args, **kwargs)

            return wrapper

        return decorator

    def log_audit(
        self,
        action: str,
        actor: str,
        resource: str,
        level: SecurityLevel,
        details: Dict,
        result: bool = True,
    ) -> None:
        """Log security audit event."""
        entry = AuditEntry(
            action=action,
            actor=actor,
            resource=resource,
            level=level,
            details=details,
            result=result,
        )
        self.audit_log.append(entry)
        self.metrics["audit_events"] += 1

        if level in [SecurityLevel.HIGH, SecurityLevel.CRITICAL]:
            logger.warning(
                f"Security event: {action} by {actor} on {resource}",
                extra={"security": entry.to_dict()},
            )

    def verify_signature(
        self,
        data: str,
        signature: str,
        secret: str,
    ) -> bool:
        """Verify HMAC signature."""
        expected = hmac.new(
            secret.encode(),
            data.encode(),
            hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(signature, expected)

    def get_audit_log(
        self,
        level: Optional[SecurityLevel] = None,
        actor: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict]:
        """Get audit log entries."""
        filtered = self.audit_log

        if level:
            filtered = [e for e in filtered if e.level == level]
        if actor:
            filtered = [e for e in filtered if e.actor == actor]

        return [e.to_dict() for e in filtered[-limit:]]

    def get_metrics(self) -> Dict:
        """Get security metrics."""
        return {
            **self.metrics,
            "audit_log_size": len(self.audit_log),
            "timestamp": datetime.utcnow().isoformat(),
        }
