import hashlib
import json
from typing import Any, Dict, Optional

class CacheService:
    def __init__(self):
        self._cache: Dict[str, Any] = {}
    
    def get_cache_key(self, resume_id: str, job_id: str) -> str:
        key_str = f"{resume_id}:{job_id}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        return self._cache.get(key)
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        self._cache[key] = value
    
    def clear(self) -> None:
        self._cache.clear()
