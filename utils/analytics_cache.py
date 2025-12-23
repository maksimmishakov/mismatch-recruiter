"""Analytics data caching utility for performance optimization."""

from datetime import datetime, timedelta
import json

class AnalyticsCache:
    """Simple in-memory cache for analytics data with TTL."""
    
    def __init__(self, ttl_seconds=300):
        """Initialize cache with time-to-live in seconds.
        
        Args:
            ttl_seconds: Cache validity duration (default: 300 seconds = 5 minutes)
        """
        self.ttl_seconds = ttl_seconds
        self.cache = {}
        self.timestamps = {}
    
    def get(self, key):
        """Get cached value if it exists and hasn't expired.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value if valid, None otherwise
        """
        if key not in self.cache:
            return None
        
        # Check if cache has expired
        cache_time = self.timestamps.get(key)
        if cache_time is None:
            return None
        
        if datetime.utcnow() - cache_time > timedelta(seconds=self.ttl_seconds):
            # Cache expired, remove it
            del self.cache[key]
            del self.timestamps[key]
            return None
        
        return self.cache[key]
    
    def set(self, key, value):
        """Set cache value with current timestamp.
        
        Args:
            key: Cache key
            value: Value to cache (should be serializable)
        """
        self.cache[key] = value
        self.timestamps[key] = datetime.utcnow()
    
    def invalidate(self, key=None):
        """Invalidate specific cache or all cache.
        
        Args:
            key: Specific key to invalidate, or None to invalidate all
        """
        if key is None:
            self.cache.clear()
            self.timestamps.clear()
        else:
            if key in self.cache:
                del self.cache[key]
                del self.timestamps[key]
    
    def is_valid(self, key):
        """Check if cache key has valid (non-expired) data.
        
        Args:
            key: Cache key
            
        Returns:
            True if cache is valid, False otherwise
        """
        return self.get(key) is not None

# Global cache instance
analytics_cache = AnalyticsCache(ttl_seconds=300)

def get_cached_analytics(db_session, Candidate):
    """Get analytics from cache or compute if expired.
    
    Args:
        db_session: SQLAlchemy database session
        Candidate: Candidate model class
        
    Returns:
        Analytics dictionary
    """
    cache_key = 'analytics_data'
    
    # Check if we have valid cached data
    cached_data = analytics_cache.get(cache_key)
    if cached_data is not None:
        return cached_data
    
    # Compute analytics
    candidates = db_session.query(Candidate).all()
    total_candidates = len(candidates)
    approved = len([c for c in candidates if c.status == 'approved'])
    rejected = len([c for c in candidates if c.status == 'rejected'])
    pending = len([c for c in candidates if c.status == 'pending'])
    
    avg_score = sum([c.score for c in candidates]) / total_candidates if total_candidates > 0 else 0
    
    all_skills = []
    for c in candidates:
        if c.skills:
            all_skills.extend(c.skills)
    
    skills_count = {}
    for skill in all_skills:
        skills_count[skill] = skills_count.get(skill, 0) + 1
    
    analytics_data = {
        'success': True,
        'total_candidates': total_candidates,
        'status_breakdown': {
            'approved': approved,
            'rejected': rejected,
            'pending': pending
        },
        'average_score': round(avg_score, 2),
        'top_skills': sorted(skills_count.items(), key=lambda x: x[1], reverse=True)[:10],
        'timestamp': datetime.utcnow().isoformat(),
        'cached': False
    }
    
    # Cache the result
    analytics_cache.set(cache_key, analytics_data)
    
    return analytics_data
