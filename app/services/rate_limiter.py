"""Rate Limiter Service"""
import time
from collections import deque
from typing import Dict, Deque


class RateLimiter:
    """Simple rate limiter to limit requests per time window."""

    def __init__(self, max_requests: int = 100, time_window: int = 3600):
        """
        Initialize RateLimiter.
        
        Args:
            max_requests: Maximum number of requests allowed
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: Dict[str, Deque[float]] = {}

    def is_allowed(self, identifier: str) -> bool:
        """
        Check if a request from identifier is allowed.
        
        Args:
            identifier: Unique identifier (e.g., IP address, user ID)
            
        Returns:
            True if request is allowed, False otherwise
        """
        current_time = time.time()
        
        # Initialize deque for new identifier
        if identifier not in self.requests:
            self.requests[identifier] = deque()
        
        # Remove old requests outside the time window
        while self.requests[identifier] and \
              self.requests[identifier][0] <= current_time - self.time_window:
            self.requests[identifier].popleft()
        
        # Check if under limit
        if len(self.requests[identifier]) < self.max_requests:
            self.requests[identifier].append(current_time)
            return True
        
        return False

    def reset(self, identifier: str = None) -> None:
        """
        Reset rate limiter for identifier or all identifiers.
        
        Args:
            identifier: Specific identifier to reset, or None to reset all
        """
        if identifier is None:
            self.requests.clear()
        elif identifier in self.requests:
            self.requests[identifier].clear()
