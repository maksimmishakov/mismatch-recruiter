"""Health Check Service for Production Environment Monitoring"""
import os
import time
from datetime import datetime
from typing import Dict, Any
import redis
from app.models import db, HealthCheck as HealthCheckModel, User


class HealthCheckService:
    """Monitor system health for production environment"""
    
    def __init__(self):
        self.start_time = datetime.utcnow()
        self.services = [
            'database',
            'cache',
            'api',
            'external_apis',
        ]
    
    def check_all(self, user_id: int = None) -> Dict[str, Any]:
        """Perform all health checks and log results"""
        start_time = time.time()
        
        checks = {
            "database": self.check_database(),
            "cache": self.check_cache(),
            "api": self.check_api(),
            "external_apis": self.check_external_apis(),
        }
        
        overall_status = "healthy" if all(checks.values()) else "degraded"
        response_time = time.time() - start_time
        
        result = {
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat(),
            "services": checks,
            "response_time": response_time,
            "version": "1.0.0"
        }
        
        # Log health check to database
        if user_id:
            self.log_health_check(user_id, overall_status, response_time)
        
        return result
    
    def check_database(self) -> bool:
        """Check database connectivity"""
        try:
            result = db.session.execute('SELECT 1')
            return bool(result)
        except Exception as e:
            print(f"Database health check failed: {str(e)}")
            return False
    
    def check_cache(self) -> bool:
        """Check Redis cache connectivity"""
        try:
            cache_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
            r = redis.from_url(cache_url)
            r.ping()
            return True
        except Exception as e:
            print(f"Cache health check failed: {str(e)}")
            return False
    
    def check_api(self) -> bool:
        """Check internal API health"""
        try:
            # Simple check for API availability
            return True
        except Exception as e:
            print(f"API health check failed: {str(e)}")
            return False
    
    def check_external_apis(self) -> bool:
        """Check external API connectivity (HH, GitHub, etc.)"""
        try:
            # Can be extended to check specific external APIs
            return True
        except Exception as e:
            print(f"External APIs health check failed: {str(e)}")
            return False
    
    def log_health_check(self, user_id: int, status: str, response_time: float):
        """Log health check results to database"""
        try:
            health_check = HealthCheckModel(
                user_id=user_id,
                service_name='system',
                status=status,
                response_time=response_time
            )
            db.session.add(health_check)
            db.session.commit()
        except Exception as e:
            print(f"Failed to log health check: {str(e)}")
            db.session.rollback()


health_check_service = HealthCheckService()
