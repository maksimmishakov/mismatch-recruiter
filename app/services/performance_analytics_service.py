"""Performance Monitoring & Analytics Service - Request metrics, latency tracking, performance insights."""

import logging
import time
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict, deque
import statistics


logger = logging.getLogger(__name__)


class MetricType(str, Enum):
    """Metric types."""
    LATENCY = "latency"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    CACHE_HIT = "cache_hit"
    MEMORY = "memory"
    CPU = "cpu"


@dataclass
class RequestMetric:
    """Request performance metric."""
    endpoint: str
    method: str
    status_code: int
    latency_ms: float
    timestamp: datetime
    user_id: Optional[str] = None
    cache_hit: bool = False
    error: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "endpoint": self.endpoint,
            "method": self.method,
            "status_code": self.status_code,
            "latency_ms": self.latency_ms,
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id,
            "cache_hit": self.cache_hit,
            "error": self.error,
        }


@dataclass
class PerformanceStats:
    """Performance statistics."""
    endpoint: str
    total_requests: int
    avg_latency_ms: float
    median_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    min_latency_ms: float
    max_latency_ms: float
    error_count: int
    error_rate: float
    cache_hit_rate: float

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "endpoint": self.endpoint,
            "total_requests": self.total_requests,
            "avg_latency_ms": round(self.avg_latency_ms, 2),
            "median_latency_ms": round(self.median_latency_ms, 2),
            "p95_latency_ms": round(self.p95_latency_ms, 2),
            "p99_latency_ms": round(self.p99_latency_ms, 2),
            "min_latency_ms": round(self.min_latency_ms, 2),
            "max_latency_ms": round(self.max_latency_ms, 2),
            "error_count": self.error_count,
            "error_rate": round(self.error_rate, 4),
            "cache_hit_rate": round(self.cache_hit_rate, 4),
        }


class PerformanceAnalyticsService:
    """Performance monitoring and analytics service."""

    def __init__(self, max_metrics: int = 10000):
        self.max_metrics = max_metrics
        self.metrics: deque = deque(maxlen=max_metrics)
        self.endpoint_metrics: Dict[str, List[RequestMetric]] = defaultdict(list)
        self.user_metrics: Dict[str, List[RequestMetric]] = defaultdict(list)

    def record_request(
        self,
        endpoint: str,
        method: str,
        status_code: int,
        latency_ms: float,
        user_id: Optional[str] = None,
        cache_hit: bool = False,
        error: Optional[str] = None,
    ) -> None:
        """Record a request metric.
        
        Args:
            endpoint: Endpoint path
            method: HTTP method
            status_code: Response status code
            latency_ms: Request latency in milliseconds
            user_id: User ID if applicable
            cache_hit: Whether cache was hit
            error: Error message if applicable
        """
        metric = RequestMetric(
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            latency_ms=latency_ms,
            timestamp=datetime.utcnow(),
            user_id=user_id,
            cache_hit=cache_hit,
            error=error,
        )
        self.metrics.append(metric)
        self.endpoint_metrics[endpoint].append(metric)
        if user_id:
            self.user_metrics[user_id].append(metric)

        # Log slow requests
        if latency_ms > 1000:
            logger.warning(
                f"Slow request detected: {method} {endpoint} - {latency_ms:.0f}ms"
            )

    def get_endpoint_stats(self, endpoint: str) -> Optional[PerformanceStats]:
        """Get performance statistics for endpoint.
        
        Args:
            endpoint: Endpoint path
            
        Returns:
            Performance statistics
        """
        metrics = self.endpoint_metrics.get(endpoint, [])
        if not metrics:
            return None

        latencies = [m.latency_ms for m in metrics]
        errors = [m for m in metrics if m.status_code >= 400]
        cache_hits = [m for m in metrics if m.cache_hit]

        sorted_latencies = sorted(latencies)
        p95_idx = int(len(sorted_latencies) * 0.95)
        p99_idx = int(len(sorted_latencies) * 0.99)

        return PerformanceStats(
            endpoint=endpoint,
            total_requests=len(metrics),
            avg_latency_ms=statistics.mean(latencies),
            median_latency_ms=statistics.median(latencies),
            p95_latency_ms=sorted_latencies[p95_idx] if p95_idx < len(sorted_latencies) else sorted_latencies[-1],
            p99_latency_ms=sorted_latencies[p99_idx] if p99_idx < len(sorted_latencies) else sorted_latencies[-1],
            min_latency_ms=min(latencies),
            max_latency_ms=max(latencies),
            error_count=len(errors),
            error_rate=len(errors) / len(metrics) if metrics else 0,
            cache_hit_rate=len(cache_hits) / len(metrics) if metrics else 0,
        )

    def get_top_slow_endpoints(
        self,
        limit: int = 10,
        minutes: int = 60,
    ) -> List[PerformanceStats]:
        """Get top slowest endpoints.
        
        Args:
            limit: Number of endpoints to return
            minutes: Time window in minutes
            
        Returns:
            List of performance statistics
        """
        cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
        endpoint_stats = []

        for endpoint in self.endpoint_metrics:
            recent_metrics = [
                m for m in self.endpoint_metrics[endpoint]
                if m.timestamp >= cutoff_time
            ]
            if recent_metrics:
                stats = self.get_endpoint_stats(endpoint)
                if stats:
                    endpoint_stats.append(stats)

        return sorted(
            endpoint_stats,
            key=lambda s: s.avg_latency_ms,
            reverse=True,
        )[:limit]

    def get_error_rate_by_endpoint(self) -> Dict[str, float]:
        """Get error rates by endpoint.
        
        Returns:
            Dictionary of endpoint -> error_rate
        """
        error_rates = {}
        for endpoint in self.endpoint_metrics:
            stats = self.get_endpoint_stats(endpoint)
            if stats:
                error_rates[endpoint] = stats.error_rate
        return error_rates

    def get_user_performance(
        self,
        user_id: str,
    ) -> Dict[str, Any]:
        """Get performance metrics for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            User performance data
        """
        metrics = self.user_metrics.get(user_id, [])
        if not metrics:
            return {}

        latencies = [m.latency_ms for m in metrics]
        return {
            "user_id": user_id,
            "request_count": len(metrics),
            "avg_latency_ms": round(statistics.mean(latencies), 2),
            "total_errors": sum(1 for m in metrics if m.status_code >= 400),
            "first_request": metrics[0].timestamp.isoformat(),
            "last_request": metrics[-1].timestamp.isoformat(),
        }

    def get_overall_health(self) -> Dict[str, Any]:
        """Get overall system health metrics.
        
        Returns:
            Overall health metrics
        """
        if not self.metrics:
            return {"status": "no_data"}

        latencies = [m.latency_ms for m in self.metrics]
        errors = [m for m in self.metrics if m.status_code >= 400]
        cache_hits = [m for m in self.metrics if m.cache_hit]

        return {
            "total_requests": len(self.metrics),
            "avg_latency_ms": round(statistics.mean(latencies), 2),
            "median_latency_ms": round(statistics.median(latencies), 2),
            "p95_latency_ms": round(
                sorted(latencies)[int(len(latencies) * 0.95)], 2
            ),
            "error_count": len(errors),
            "error_rate": round(len(errors) / len(self.metrics), 4),
            "cache_hit_rate": round(len(cache_hits) / len(self.metrics), 4),
            "unique_endpoints": len(self.endpoint_metrics),
            "unique_users": len(self.user_metrics),
            "timestamp": datetime.utcnow().isoformat(),
        }

    def clear_old_metrics(self, hours: int = 24) -> int:
        """Clear metrics older than specified hours.
        
        Args:
            hours: Hours to retain
            
        Returns:
            Number of metrics removed
        """
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        initial_count = len(self.metrics)

        for endpoint_metrics in self.endpoint_metrics.values():
            endpoint_metrics[:] = [
                m for m in endpoint_metrics if m.timestamp >= cutoff_time
            ]

        for user_metrics in self.user_metrics.values():
            user_metrics[:] = [
                m for m in user_metrics if m.timestamp >= cutoff_time
            ]

        logger.info(f"Cleared {initial_count - len(self.metrics)} old metrics")
        return initial_count - len(self.metrics)
