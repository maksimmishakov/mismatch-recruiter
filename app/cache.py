"""Redis caching layer for improved performance."""
import redis
import json
import pickle
from functools import wraps
from typing import Any, Optional, Callable
import logging
from datetime import timedelta


logger = logging.getLogger(__name__)


class RedisCache:
    """Redis cache manager with connection pooling and error handling."""
    
    def __init__(self, host='localhost', port=6379, db=0, password=None, 
                 default_ttl=300, decode_responses=True):
        """
        Initialize Redis cache.
        
        Args:
            host: Redis server host
            port: Redis server port
            db: Redis database number
            password: Redis password (if required)
            default_ttl: Default TTL in seconds (5 minutes)
            decode_responses: Whether to decode responses to strings
        """
        try:
            self.client = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=decode_responses,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
            self.default_ttl = default_ttl
            # Test connection
            self.client.ping()
            logger.info(f"Redis cache initialized successfully at {host}:{port}")
        except Exception as e:
            logger.error(f"Failed to initialize Redis cache: {str(e)}")
            self.client = None
    
    def is_available(self) -> bool:
        """Check if Redis is available."""
        if self.client is None:
            return False
        try:
            self.client.ping()
            return True
        except Exception:
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if not self.is_available():
            return None
        
        try:
            value = self.client.get(key)
            if value:
                logger.debug(f"Cache hit for key: {key}")
                try:
                    return json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    return value
            logger.debug(f"Cache miss for key: {key}")
            return None
        except Exception as e:
            logger.error(f"Error getting cache key {key}: {str(e)}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache with optional TTL."""
        if not self.is_available():
            return False
        
        ttl = ttl or self.default_ttl
        
        try:
            # Serialize complex objects to JSON
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            elif not isinstance(value, (str, int, float, bytes)):
                value = json.dumps(str(value))
            
            self.client.setex(key, ttl, value)
            logger.debug(f"Cache set for key: {key} with TTL: {ttl}s")
            return True
        except Exception as e:
            logger.error(f"Error setting cache key {key}: {str(e)}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        if not self.is_available():
            return False
        
        try:
            self.client.delete(key)
            logger.debug(f"Cache deleted for key: {key}")
            return True
        except Exception as e:
            logger.error(f"Error deleting cache key {key}: {str(e)}")
            return False
    
    def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching a pattern."""
        if not self.is_available():
            return 0
        
        try:
            keys = self.client.keys(pattern)
            if keys:
                deleted = self.client.delete(*keys)
                logger.info(f"Deleted {deleted} cache keys matching pattern: {pattern}")
                return deleted
            return 0
        except Exception as e:
            logger.error(f"Error deleting cache pattern {pattern}: {str(e)}")
            return 0
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        if not self.is_available():
            return False
        
        try:
            return bool(self.client.exists(key))
        except Exception as e:
            logger.error(f"Error checking cache key {key}: {str(e)}")
            return False
    
    def get_ttl(self, key: str) -> Optional[int]:
        """Get remaining TTL for a key."""
        if not self.is_available():
            return None
        
        try:
            return self.client.ttl(key)
        except Exception as e:
            logger.error(f"Error getting TTL for key {key}: {str(e)}")
            return None
    
    def incr(self, key: str, amount: int = 1) -> Optional[int]:
        """Increment a counter."""
        if not self.is_available():
            return None
        
        try:
            return self.client.incr(key, amount)
        except Exception as e:
            logger.error(f"Error incrementing key {key}: {str(e)}")
            return None
    
    def decr(self, key: str, amount: int = 1) -> Optional[int]:
        """Decrement a counter."""
        if not self.is_available():
            return None
        
        try:
            return self.client.decr(key, amount)
        except Exception as e:
            logger.error(f"Error decrementing key {key}: {str(e)}")
            return None
    
    def flush_all(self) -> bool:
        """Clear all cache entries. Use with caution!"""
        if not self.is_available():
            return False
        
        try:
            self.client.flushdb()
            logger.warning("All cache entries flushed")
            return True
        except Exception as e:
            logger.error(f"Error flushing cache: {str(e)}")
            return False
    
    def get_stats(self) -> dict:
        """Get Redis statistics."""
        if not self.is_available():
            return {}
        
        try:
            info = self.client.info()
            return {
                'used_memory': info.get('used_memory_human'),
                'connected_clients': info.get('connected_clients'),
                'total_commands_processed': info.get('total_commands_processed'),
                'keyspace_hits': info.get('keyspace_hits', 0),
                'keyspace_misses': info.get('keyspace_misses', 0),
                'hit_rate': self._calculate_hit_rate(info)
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {str(e)}")
            return {}
    
    def _calculate_hit_rate(self, info: dict) -> float:
        """Calculate cache hit rate."""
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        total = hits + misses
        
        if total == 0:
            return 0.0
        
        return round((hits / total) * 100, 2)


# Initialize global cache instance
cache = RedisCache()


def cached(ttl: Optional[int] = None, key_prefix: str = ''):
    """Decorator to cache function results.
    
    Args:
        ttl: Time to live in seconds
        key_prefix: Prefix for cache key
    
    Usage:
        @cached(ttl=300, key_prefix='user')
        def get_user(user_id):
            return fetch_user_from_db(user_id)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            cache_key = f"{key_prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.info(f"Returning cached result for {func.__name__}")
                return cached_result
            
            # Call function and cache result
            result = func(*args, **kwargs)
            
            if result is not None:
                cache.set(cache_key, result, ttl)
                logger.info(f"Cached result for {func.__name__}")
            
            return result
        
        return wrapper
    return decorator


def cache_invalidate(key_pattern: str):
    """Decorator to invalidate cache after function execution.
    
    Usage:
        @cache_invalidate(key_pattern='user:get_user:*')
        def update_user(user_id, data):
            return update_user_in_db(user_id, data)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            # Invalidate cache
            deleted = cache.delete_pattern(key_pattern)
            logger.info(f"Invalidated {deleted} cache entries matching {key_pattern}")
            
            return result
        
        return wrapper
    return decorator


def get_cache_instance() -> RedisCache:
    """Get the global cache instance."""
    return cache
