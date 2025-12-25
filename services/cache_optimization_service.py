import logging
import redis
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import hashlib

logger = logging.getLogger(__name__)

@dataclass
class CacheEntry:
    key: str
    value: Any
    created_at: datetime
    expires_at: Optional[datetime] = None
    hit_count: int = 0
    size_bytes: int = 0

class CacheOptimizationService:
    def __init__(self, redis_host: str = 'localhost', redis_port: int = 6379, db: int = 0):
        try:
            self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=db, decode_responses=True)
            self.redis_client.ping()
            self.using_redis = True
            logger.info('Connected to Redis')
        except Exception as e:
            logger.warning(f'Redis connection failed: {str(e)}, using in-memory cache')
            self.using_redis = False
            self.memory_cache = {}
        
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'total_operations': 0,
            'cache_size_mb': 0
        }
    
    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> bool:
        """Set a value in cache with optional TTL"""
        try:
            serialized_value = json.dumps(value, default=str)
            size_bytes = len(serialized_value.encode('utf-8'))
            
            if self.using_redis:
                if ttl_seconds:
                    self.redis_client.setex(key, ttl_seconds, serialized_value)
                else:
                    self.redis_client.set(key, serialized_value)
            else:
                expires_at = None
                if ttl_seconds:
                    expires_at = datetime.now() + timedelta(seconds=ttl_seconds)
                
                self.memory_cache[key] = CacheEntry(
                    key=key,
                    value=value,
                    created_at=datetime.now(),
                    expires_at=expires_at,
                    size_bytes=size_bytes
                )
            
            self.cache_stats['total_operations'] += 1
            logger.info(f'Cache set: {key}, size: {size_bytes} bytes')
            return True
        except Exception as e:
            logger.error(f'Cache set error: {str(e)}')
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache"""
        try:
            if self.using_redis:
                cached_value = self.redis_client.get(key)
                if cached_value:
                    self.cache_stats['hits'] += 1
                    return json.loads(cached_value)
                else:
                    self.cache_stats['misses'] += 1
                    return None
            else:
                if key in self.memory_cache:
                    entry = self.memory_cache[key]
                    if entry.expires_at and entry.expires_at < datetime.now():
                        del self.memory_cache[key]
                        self.cache_stats['misses'] += 1
                        return None
                    
                    entry.hit_count += 1
                    self.cache_stats['hits'] += 1
                    return entry.value
                else:
                    self.cache_stats['misses'] += 1
                    return None
        except Exception as e:
            logger.error(f'Cache get error: {str(e)}')
            return None
    
    def delete(self, key: str) -> bool:
        """Delete a key from cache"""
        try:
            if self.using_redis:
                self.redis_client.delete(key)
            else:
                if key in self.memory_cache:
                    del self.memory_cache[key]
            
            logger.info(f'Cache deleted: {key}')
            return True
        except Exception as e:
            logger.error(f'Cache delete error: {str(e)}')
            return False
    
    def clear(self) -> bool:
        """Clear entire cache"""
        try:
            if self.using_redis:
                self.redis_client.flushdb()
            else:
                self.memory_cache.clear()
            
            logger.info('Cache cleared')
            return True
        except Exception as e:
            logger.error(f'Cache clear error: {str(e)}')
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        try:
            if self.using_redis:
                return self.redis_client.exists(key) > 0
            else:
                if key in self.memory_cache:
                    entry = self.memory_cache[key]
                    if entry.expires_at and entry.expires_at < datetime.now():
                        del self.memory_cache[key]
                        return False
                    return True
                return False
        except Exception as e:
            logger.error(f'Cache exists error: {str(e)}')
            return False
    
    def get_ttl(self, key: str) -> int:
        """Get remaining TTL for a key (in seconds)"""
        try:
            if self.using_redis:
                ttl = self.redis_client.ttl(key)
                return ttl if ttl >= 0 else -1
            else:
                if key in self.memory_cache:
                    entry = self.memory_cache[key]
                    if entry.expires_at:
                        remaining = (entry.expires_at - datetime.now()).total_seconds()
                        return max(0, int(remaining))
                    return -1
                return -1
        except Exception as e:
            logger.error(f'Cache TTL error: {str(e)}')
            return -1
    
    def mget(self, keys: List[str]) -> Dict[str, Any]:
        """Get multiple values from cache"""
        result = {}
        for key in keys:
            value = self.get(key)
            if value is not None:
                result[key] = value
        return result
    
    def mset(self, data: Dict[str, Any], ttl_seconds: Optional[int] = None) -> bool:
        """Set multiple values in cache"""
        try:
            if self.using_redis:
                if ttl_seconds:
                    for key, value in data.items():
                        self.set(key, value, ttl_seconds)
                else:
                    serialized_data = {k: json.dumps(v, default=str) for k, v in data.items()}
                    self.redis_client.mset(serialized_data)
            else:
                for key, value in data.items():
                    self.set(key, value, ttl_seconds)
            
            return True
        except Exception as e:
            logger.error(f'Cache mset error: {str(e)}')
            return False
    
    def increment(self, key: str, amount: int = 1) -> Optional[int]:
        """Increment a numeric value in cache"""
        try:
            if self.using_redis:
                return self.redis_client.incrby(key, amount)
            else:
                if key in self.memory_cache:
                    current = self.memory_cache[key].value
                    if isinstance(current, int):
                        new_value = current + amount
                        self.memory_cache[key].value = new_value
                        return new_value
                else:
                    self.memory_cache[key] = CacheEntry(
                        key=key,
                        value=amount,
                        created_at=datetime.now()
                    )
                    return amount
            return None
        except Exception as e:
            logger.error(f'Cache increment error: {str(e)}')
            return None
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        hit_rate = 0
        if self.cache_stats['total_operations'] > 0:
            hit_rate = (self.cache_stats['hits'] / (self.cache_stats['hits'] + self.cache_stats['misses'])) * 100
        
        if self.using_redis:
            info = self.redis_client.info()
            cache_size_mb = info.get('used_memory', 0) / (1024 * 1024)
        else:
            total_size = sum(entry.size_bytes for entry in self.memory_cache.values())
            cache_size_mb = total_size / (1024 * 1024)
        
        return {
            'total_operations': self.cache_stats['total_operations'],
            'cache_hits': self.cache_stats['hits'],
            'cache_misses': self.cache_stats['misses'],
            'hit_rate_percent': round(hit_rate, 2),
            'cache_size_mb': round(cache_size_mb, 2),
            'backend': 'Redis' if self.using_redis else 'Memory',
            'total_keys': len(self.memory_cache) if not self.using_redis else int(self.redis_client.dbsize())
        }
