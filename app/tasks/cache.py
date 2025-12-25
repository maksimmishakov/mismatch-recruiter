"""Cache operation tasks for two-level caching strategy."""

import logging
from typing import Dict, Any, Optional
from celery import shared_task
from datetime import datetime, timedelta
import json
import redis

from app.services.health_check import log_service_operation
from app.config import settings

logger = logging.getLogger(__name__)

# Local in-memory cache (L1)
_local_cache = {}
_cache_timestamps = {}


@shared_task(bind=True)
def warm_cache(
    self,
    cache_key: str,
    data: Dict[str, Any],
    ttl: int = 3600
) -> Dict[str, Any]:
    """
    Warm up cache with data across two levels (L1 local + L2 Redis).
    
    Args:
        cache_key: Cache key identifier
        data: Data to cache
        ttl: Time to live in seconds
        
    Returns:
        Dict with cache warm up result
    """
    try:
        start_time = datetime.utcnow()
        
        # Store in L1 local cache
        _local_cache[cache_key] = data
        _cache_timestamps[cache_key] = datetime.utcnow() + timedelta(seconds=ttl)
        
        # Store in L2 Redis cache
        try:
            redis_client = redis.from_url(settings.REDIS_URL)
            redis_client.setex(
                cache_key,
                ttl,
                json.dumps(data)
            )
        except Exception as e:
            logger.warning(f"Failed to set Redis cache for {cache_key}: {e}")
        
        # Log operation
        duration = (datetime.utcnow() - start_time).total_seconds()
        log_service_operation(
            service="cache",
            operation="warm_cache",
            status="success",
            duration=duration,
            metadata={"cache_key": cache_key, "ttl": ttl}
        )
        
        logger.info(f"Warmed cache for key {cache_key}")
        return {"status": "success", "cache_key": cache_key}
        
    except Exception as exc:
        logger.error(f"Error warming cache for {cache_key}: {exc}")
        return {"status": "error", "error": str(exc)}


@shared_task(bind=True)
def clear_cache(self, cache_key: str) -> Dict[str, Any]:
    """
    Clear cache from both L1 and L2.
    
    Args:
        cache_key: Cache key to clear
        
    Returns:
        Dict with clear result
    """
    try:
        start_time = datetime.utcnow()
        
        # Clear from L1 local cache
        if cache_key in _local_cache:
            del _local_cache[cache_key]
        if cache_key in _cache_timestamps:
            del _cache_timestamps[cache_key]
        
        # Clear from L2 Redis cache
        try:
            redis_client = redis.from_url(settings.REDIS_URL)
            redis_client.delete(cache_key)
        except Exception as e:
            logger.warning(f"Failed to delete Redis cache for {cache_key}: {e}")
        
        # Log operation
        duration = (datetime.utcnow() - start_time).total_seconds()
        log_service_operation(
            service="cache",
            operation="clear_cache",
            status="success",
            duration=duration,
            metadata={"cache_key": cache_key}
        )
        
        logger.info(f"Cleared cache for key {cache_key}")
        return {"status": "success", "cache_key": cache_key}
        
    except Exception as exc:
        logger.error(f"Error clearing cache for {cache_key}: {exc}")
        return {"status": "error", "error": str(exc)}


@shared_task(bind=True)
def clear_all_cache(self) -> Dict[str, Any]:
    """
    Clear all cache entries from both L1 and L2.
    
    Returns:
        Dict with clear result
    """
    try:
        start_time = datetime.utcnow()
        
        # Clear L1 local cache
        cleared_count = len(_local_cache)
        _local_cache.clear()
        _cache_timestamps.clear()
        
        # Clear L2 Redis cache
        try:
            redis_client = redis.from_url(settings.REDIS_URL)
            # Use pattern matching to clear cache entries
            cursor = 0
            pattern = "*"
            while True:
                cursor, keys = redis_client.scan(cursor, match=pattern, count=100)
                if keys:
                    redis_client.delete(*keys)
                if cursor == 0:
                    break
        except Exception as e:
            logger.warning(f"Failed to clear Redis cache: {e}")
        
        # Log operation
        duration = (datetime.utcnow() - start_time).total_seconds()
        log_service_operation(
            service="cache",
            operation="clear_all_cache",
            status="success",
            duration=duration,
            metadata={"cleared_entries": cleared_count}
        )
        
        logger.info(f"Cleared all cache entries ({cleared_count})")
        return {"status": "success", "cleared_entries": cleared_count}
        
    except Exception as exc:
        logger.error(f"Error clearing all cache: {exc}")
        return {"status": "error", "error": str(exc)}


def get_cache(cache_key: str) -> Optional[Dict[str, Any]]:
    """
    Get cache value from L1 or L2 with fallback.
    
    Args:
        cache_key: Cache key to retrieve
        
    Returns:
        Cached data or None
    """
    # Check L1 first
    if cache_key in _local_cache:
        timestamp = _cache_timestamps.get(cache_key)
        if timestamp and datetime.utcnow() < timestamp:
            logger.debug(f"Cache hit in L1 for {cache_key}")
            return _local_cache[cache_key]
        else:
            # L1 cache expired
            del _local_cache[cache_key]
            if cache_key in _cache_timestamps:
                del _cache_timestamps[cache_key]
    
    # Check L2 Redis
    try:
        redis_client = redis.from_url(settings.REDIS_URL)
        value = redis_client.get(cache_key)
        if value:
            data = json.loads(value)
            # Populate L1 cache from L2
            _local_cache[cache_key] = data
            logger.debug(f"Cache hit in L2 for {cache_key}")
            return data
    except Exception as e:
        logger.warning(f"Failed to get Redis cache for {cache_key}: {e}")
    
    logger.debug(f"Cache miss for {cache_key}")
    return None
