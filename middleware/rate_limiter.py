from flask import request
from functools import wraps
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_requests: int = 100, window: int = 60):
        self.max_requests = max_requests
        self.window = window
        self.requests = {}
    
    def is_rate_limited(self, client_id: str) -> bool:
        now = datetime.now()
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        # Remove old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < timedelta(seconds=self.window)
        ]
        
        if len(self.requests[client_id]) < self.max_requests:
            self.requests[client_id].append(now)
            return False
        return True

if __name__ == '__main__':
    limiter = RateLimiter(max_requests=5, window=60)
    for i in range(10):
        is_limited = limiter.is_rate_limited("user_123")
        status = "BLOCKED" if is_limited else "ALLOWED"
        print(f"Request {i+1}: {status}")
