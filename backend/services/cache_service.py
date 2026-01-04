from typing import Any, Dict
from datetime import datetime, timedelta

class CacheService:
    """Simple In-Memory Caching Service"""
    
    _cache: Dict[str, Dict[str, Any]] = {}
    
    @staticmethod
    def set(key: str, value: Any, ttl: int = 3600) -> bool:
        """Set cache value with TTL in seconds"""
        CacheService._cache[key] = {
            'value': value,
            'expires_at': datetime.now() + timedelta(seconds=ttl)
        }
        return True
    
    @staticmethod
    def get(key: str) -> Any:
        """Get cache value if not expired"""
        if key not in CacheService._cache:
            return None
        
        cache_item = CacheService._cache[key]
        if datetime.now() > cache_item['expires_at']:
            del CacheService._cache[key]
            return None
        
        return cache_item['value']
    
    @staticmethod
    def delete(key: str) -> bool:
        """Delete cache key"""
        if key in CacheService._cache:
            del CacheService._cache[key]
            return True
        return False
    
    @staticmethod
    def clear() -> int:
        """Clear all cache"""
        count = len(CacheService._cache)
        CacheService._cache.clear()
        return count
    
    @staticmethod
    def get_stats() -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            'size': len(CacheService._cache),
            'keys': list(CacheService._cache.keys())
        }
