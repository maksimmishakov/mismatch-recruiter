# services/cache_service.py - Caching Service

import logging
import json
from typing import Any, Optional, List
from datetime import datetime, timedelta
import hashlib

logger = logging.getLogger(__name__)


class CacheService:
    """In-memory caching service with optional Redis support."""
    
    def __init__(self, use_redis: bool = False, redis_url: str = 'redis://localhost:6379'):
        """Initialize cache service.
        
        Args:
            use_redis: Whether to use Redis (optional)
            redis_url: Redis connection URL
        """
        self.use_redis = use_redis
        self.redis_client = None
        self.memory_cache = {}  # Fallback in-memory cache
        
        if use_redis:
            try:
                import redis
                self.redis_client = redis.from_url(redis_url)
                self.redis_client.ping()
                logger.info("Connected to Redis")
            except ImportError:
                logger.warning("Redis not installed, using in-memory cache")
                self.use_redis = False
            except Exception as e:
                logger.warning(f"Redis connection failed: {e}, using in-memory cache")
                self.use_redis = False
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        try:
            if self.redis_client:
                value = self.redis_client.get(key)
                if value:
                    return json.loads(value)
            else:
                if key in self.memory_cache:
                    entry = self.memory_cache[key]
                    if entry['expires'] > datetime.now():
                        return entry['value']
                    else:
                        del self.memory_cache[key]
            return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl_seconds: int = 3600) -> bool:
        """Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl_seconds: Time to live in seconds
            
        Returns:
            Success status
        """
        try:
            if self.redis_client:
                self.redis_client.setex(key, ttl_seconds, json.dumps(value))
                return True
            else:
                self.memory_cache[key] = {
                    'value': value,
                    'expires': datetime.now() + timedelta(seconds=ttl_seconds)
                }
                return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Success status
        """
        try:
            if self.redis_client:
                self.redis_client.delete(key)
            elif key in self.memory_cache:
                del self.memory_cache[key]
            return True
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False
    
    def clear(self) -> bool:
        """Clear all cache.
        
        Returns:
            Success status
        """
        try:
            if self.redis_client:
                self.redis_client.flushdb()
            else:
                self.memory_cache.clear()
            logger.info("Cache cleared")
            return True
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return False
    
    def cache_key(self, *args) -> str:
        """Generate cache key from arguments.
        
        Args:
            *args: Arguments to hash
            
        Returns:
            Cache key
        """
        key_str = ':'.join(str(arg) for arg in args)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get_or_set(self, key: str, value_func, ttl_seconds: int = 3600) -> Any:
        """Get from cache or compute and cache.
        
        Args:
            key: Cache key
            value_func: Function to compute value
            ttl_seconds: Time to live in seconds
            
        Returns:
            Cached or computed value
        """
        # Try to get from cache
        cached = self.get(key)
        if cached is not None:
            return cached
        
        # Compute value
        try:
            value = value_func()
            # Cache it
            self.set(key, value, ttl_seconds)
            return value
        except Exception as e:
            logger.error(f"Error computing cached value: {e}")
            return None
    
    def cache_embedding(self, resume_id: str, embedding: list, ttl_seconds: int = 86400) -> bool:
        """Cache embedding for resume.
        
        Args:
            resume_id: Resume ID
            embedding: Embedding vector
            ttl_seconds: Time to live
            
        Returns:
            Success status
        """
        key = f"embedding:{resume_id}"
        return self.set(key, embedding, ttl_seconds)
    
    def get_embedding(self, resume_id: str) -> Optional[list]:
        """Get cached embedding.
        
        Args:
            resume_id: Resume ID
            
        Returns:
            Embedding vector or None
        """
        key = f"embedding:{resume_id}"
        return self.get(key)
    
    def cache_match_results(self, query_id: str, results: list, ttl_seconds: int = 3600) -> bool:
        """Cache match results.
        
        Args:
            query_id: Query ID
            results: Match results
            ttl_seconds: Time to live
            
        Returns:
            Success status
        """
        key = f"matches:{query_id}"
        return self.set(key, results, ttl_seconds)
    
    def get_match_results(self, query_id: str) -> Optional[list]:
        """Get cached match results.
        
        Args:
            query_id: Query ID
            
        Returns:
            Match results or None
        """
        key = f"matches:{query_id}"
        return self.get(key)
    
    def get_stats(self) -> dict:
        """Get cache statistics.
        
        Returns:
            Cache stats
        """
        if self.redis_client:
            try:
                info = self.redis_client.info()
                return {
                    'type': 'redis',
                    'connected': True,
                    'used_memory': info.get('used_memory_human', 'N/A'),
                    'keys': self.redis_client.dbsize(),
                }
            except Exception as e:
                logger.error(f"Error getting stats: {e}")
                return {'type': 'redis', 'connected': False}
        else:
            return {
                'type': 'memory',
                'entries': len(self.memory_cache),
                'connected': True,
            }


# Global instance
_cache_service = None


def get_cache_service(use_redis: bool = False) -> CacheService:
    """Get or create cache service instance."""
    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService(use_redis=use_redis)
    return _cache_service
