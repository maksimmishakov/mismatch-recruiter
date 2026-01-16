"""Cache Optimization Service - Manage caching strategies"""

import logging
from typing import Dict, Optional, Any
import time

logger = logging.getLogger(__name__)


class CacheOptimizationService:
    """Service for optimizing cache strategies"""
    
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        """Initialize the cache optimization service
        
        Args:
            max_size: Maximum cache size
            ttl: Time to live in seconds
        """
        self.cache = {}
        self.max_size = max_size
        self.ttl = ttl
        self.access_count = {}
        logger.info(f"CacheOptimizationService initialized with max_size={max_size}, ttl={ttl}")
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found or expired
        """
        try:
            if key not in self.cache:
                return None
            
            value, timestamp = self.cache[key]
            
            # Check if expired
            if time.time() - timestamp > self.ttl:
                del self.cache[key]
                return None
            
            # Update access count
            self.access_count[key] = self.access_count.get(key, 0) + 1
            return value
        except Exception as e:
            logger.error(f"Error getting cache value: {e}")
            return None
    
    def set(self, key: str, value: Any) -> bool:
        """Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Evict least recently used if cache is full
            if len(self.cache) >= self.max_size and key not in self.cache:
                self._evict_lru()
            
            self.cache[key] = (value, time.time())
            self.access_count[key] = 1
            return True
        except Exception as e:
            logger.error(f"Error setting cache value: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete value from cache
        
        Args:
            key: Cache key
            
        Returns:
            True if deleted, False if key didn't exist
        """
        try:
            if key in self.cache:
                del self.cache[key]
                if key in self.access_count:
                    del self.access_count[key]
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting cache value: {e}")
            return False
    
    def clear(self) -> None:
        """Clear all cache"""
        self.cache.clear()
        self.access_count.clear()
        logger.info("Cache cleared")
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'usage_percentage': (len(self.cache) / self.max_size * 100) if self.max_size > 0 else 0,
            'total_accesses': sum(self.access_count.values())
        }
    
    def _evict_lru(self) -> None:
        """Evict least recently used item"""
        if not self.access_count:
            # If no access counts, just remove first item
            if self.cache:
                first_key = next(iter(self.cache))
                del self.cache[first_key]
            return
        
        # Find least accessed key
        lru_key = min(self.access_count, key=self.access_count.get)
        if lru_key in self.cache:
            del self.cache[lru_key]
        if lru_key in self.access_count:
            del self.access_count[lru_key]
        logger.info(f"Evicted LRU key: {lru_key}")
