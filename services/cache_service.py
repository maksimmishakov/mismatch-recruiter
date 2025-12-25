import redis
import json
from typing import Any

class CacheService:
    def __init__(self, redis_url):
        self.redis = redis.from_url(redis_url)
    
    def get(self, key: str) -> Any:
        value = self.redis.get(key)
        return json.loads(value) if value else None
    
    def set(self, key: str, value: Any, ttl=3600):
        self.redis.setex(key, ttl, json.dumps(value))
    
    def delete(self, key: str):
        self.redis.delete(key)
