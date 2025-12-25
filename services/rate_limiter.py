from datetime import datetime, timedelta
from collections import defaultdict

class RateLimiter:
    """Prevent abuse by limiting requests per user/IP"""
    
    def __init__(self, max_requests=100, time_window=3600):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = defaultdict(list)
    
    def is_allowed(self, identifier):
        """Check if request is allowed"""
        now = datetime.now()
        
        # Remove old requests outside time window
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if now - req_time < timedelta(seconds=self.time_window)
        ]
        
        # Check if under limit
        if len(self.requests[identifier]) < self.max_requests:
            self.requests[identifier].append(now)
            return True
        
        return False
    
    def get_remaining(self, identifier):
        """Get remaining requests for identifier"""
        now = datetime.now()
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if now - req_time < timedelta(seconds=self.time_window)
        ]
        return self.max_requests - len(self.requests[identifier])

rate_limiter = RateLimiter(max_requests=100, time_window=3600)
