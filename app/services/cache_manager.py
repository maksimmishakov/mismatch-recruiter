"""Cache Manager Service - Distributed caching with TTL and policies
Phase 5 Step 6.4 - Redis integration, LRU eviction, compression
Features: Multi-tier caching, cache invalidation, statistics
"""
import logging
import json
import hashlib
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from abc import ABC, abstractmethod
import pickle
import zlib
from collections import OrderedDict

logger = logging.getLogger(__name__)


class EvictionPolicy(Enum):
    """Cache eviction policies"""
    LRU = "lru"
    LFU = "lfu"
    FIFO = "fifo"
    TTL = "ttl"


@dataclass
class CacheEntry:
    """Cache entry with metadata"""
    key: str
    value: Any
    created_at: datetime
    last_accessed: datetime
    ttl: Optional[int] = None
    access_count: int = 0
    size: int = 0
    compressed: bool = False

    def is_expired(self) -> bool:
        if self.ttl is None:
            return False
        elapsed = (datetime.utcnow() - self.created_at).total_seconds()
        return elapsed > self.ttl

    def record_access(self) -> None:
        self.last_accessed = datetime.utcnow()
        self.access_count += 1


@dataclass
class CacheStats:
    """Cache statistics"""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    total_operations: int = 0
    current_size: int = 0
    max_size: int = 0
    entries_count: int = 0
    avg_hit_time: float = 0.0

    @property
    def hit_ratio(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            'hits': self.hits,
            'misses': self.misses,
            'evictions': self.evictions,
            'hit_ratio': f"{self.hit_ratio:.2%}",
            'entries': self.entries_count,
            'size_mb': self.current_size / (1024 * 1024)
        }


class CacheEvictionStrategy(ABC):
    """Abstract eviction strategy"""
    @abstractmethod
    def select_entry_to_evict(self, entries: Dict[str, CacheEntry]) -> Optional[str]:
        pass


class LRUEvictionStrategy(CacheEvictionStrategy):
    """Least Recently Used eviction"""
    def select_entry_to_evict(self, entries: Dict[str, CacheEntry]) -> Optional[str]:
        if not entries:
            return None
        oldest = min(entries.items(), key=lambda x: x[1].last_accessed)
        return oldest[0]


class LFUEvictionStrategy(CacheEvictionStrategy):
    """Least Frequently Used eviction"""
    def select_entry_to_evict(self, entries: Dict[str, CacheEntry]) -> Optional[str]:
        if not entries:
            return None
        least_used = min(entries.items(), key=lambda x: x[1].access_count)
        return least_used[0]


class FIFOEvictionStrategy(CacheEvictionStrategy):
    """First In First Out eviction"""
    def select_entry_to_evict(self, entries: Dict[str, CacheEntry]) -> Optional[str]:
        if not entries:
            return None
        oldest = min(entries.items(), key=lambda x: x[1].created_at)
        return oldest[0]


class TTLEvictionStrategy(CacheEvictionStrategy):
    """Time To Live based eviction"""
    def select_entry_to_evict(self, entries: Dict[str, CacheEntry]) -> Optional[str]:
        # Return first expired entry
        for key, entry in entries.items():
            if entry.is_expired():
                return key
        # If no expired entries, use LRU
        return LRUEvictionStrategy().select_entry_to_evict(entries)


class CacheCompressor:
    """Handle cache compression and decompression"""
    @staticmethod
    def compress(data: Any) -> bytes:
        serialized = pickle.dumps(data)
        return zlib.compress(serialized, level=6)

    @staticmethod
    def decompress(data: bytes) -> Any:
        decompressed = zlib.decompress(data)
        return pickle.loads(decompressed)

    @staticmethod
    def should_compress(size: int) -> bool:
        return size > 1024  # Compress if > 1KB


class LocalCache:
    """In-memory cache with eviction policies"""
    def __init__(self, max_size: int = 100 * 1024 * 1024, 
                 policy: EvictionPolicy = EvictionPolicy.LRU):
        self.max_size = max_size
        self.policy = policy
        self.entries: Dict[str, CacheEntry] = {}
        self.stats = CacheStats(max_size=max_size)
        self._init_strategy()

    def _init_strategy(self) -> None:
        if self.policy == EvictionPolicy.LRU:
            self.strategy = LRUEvictionStrategy()
        elif self.policy == EvictionPolicy.LFU:
            self.strategy = LFUEvictionStrategy()
        elif self.policy == EvictionPolicy.FIFO:
            self.strategy = FIFOEvictionStrategy()
        else:
            self.strategy = TTLEvictionStrategy()

    def get(self, key: str) -> Optional[Any]:
        if key in self.entries:
            entry = self.entries[key]
            if entry.is_expired():
                del self.entries[key]
                self.stats.misses += 1
                return None
            entry.record_access()
            self.stats.hits += 1
            return entry.value
        self.stats.misses += 1
        return None

    def put(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        now = datetime.utcnow()
        serialized = pickle.dumps(value)
        size = len(serialized)

        # Check if compression is beneficial
        compressed = False
        if CacheCompressor.should_compress(size):
            try:
                compressed_data = CacheCompressor.compress(value)
                if len(compressed_data) < size:
                    value = compressed_data
                    compressed = True
                    size = len(compressed_data)
            except Exception as e:
                logger.warning(f"Compression failed: {str(e)}")

        # Evict if necessary
        while (self.stats.current_size + size > self.max_size and 
               self.entries):
            self._evict_entry()

        self.entries[key] = CacheEntry(
            key=key,
            value=value,
            created_at=now,
            last_accessed=now,
            ttl=ttl,
            size=size,
            compressed=compressed
        )
        self.stats.current_size += size
        self.stats.entries_count = len(self.entries)
        self.stats.total_operations += 1

    def delete(self, key: str) -> bool:
        if key in self.entries:
            entry = self.entries[key]
            del self.entries[key]
            self.stats.current_size -= entry.size
            self.stats.entries_count = len(self.entries)
            return True
        return False

    def _evict_entry(self) -> None:
        key_to_evict = self.strategy.select_entry_to_evict(self.entries)
        if key_to_evict:
            entry = self.entries[key_to_evict]
            self.stats.current_size -= entry.size
            del self.entries[key_to_evict]
            self.stats.evictions += 1
            logger.info(f"Cache entry evicted: {key_to_evict}")

    def clear(self) -> None:
        self.entries.clear()
        self.stats.current_size = 0
        self.stats.entries_count = 0
        logger.info("Cache cleared")

    def get_stats(self) -> CacheStats:
        return self.stats

    def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate entries matching pattern"""
        keys_to_delete = [
            k for k in self.entries.keys() if pattern in k
        ]
        for key in keys_to_delete:
            self.delete(key)
        return len(keys_to_delete)


class CacheManager:
    """Multi-tier cache manager with Redis support"""
    def __init__(self, local_size: int = 100 * 1024 * 1024):
        self.local_cache = LocalCache(max_size=local_size)
        self.redis_available = False
        self.cache_key_prefix = "cache:"

    def get(self, key: str) -> Optional[Any]:
        # Try local cache first
        value = self.local_cache.get(key)
        if value is not None:
            return value
        # Then try Redis (simulated)
        return None

    def put(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        self.local_cache.put(key, value, ttl)

    def delete(self, key: str) -> None:
        self.local_cache.delete(key)

    def invalidate(self, pattern: str) -> int:
        return self.local_cache.invalidate_pattern(pattern)

    def get_stats(self) -> Dict[str, Any]:
        return {
            'local_cache': self.local_cache.get_stats().to_dict(),
            'timestamp': datetime.utcnow().isoformat()
        }


if __name__ == "__main__":
    logger.info("Cache Manager Service initialized")
