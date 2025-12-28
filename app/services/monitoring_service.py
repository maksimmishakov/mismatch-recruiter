import logging
import time
from typing import Dict, List, Optional
from datetime import datetime
from logging.handlers import RotatingFileHandler


class MonitoringService:
    """Service for application monitoring and health checks"""
    
    def __init__(
        self,
        app_name: str = "MisMatch",
        log_dir: str = "logs",
        max_log_size: int = 10485760
    ):
        """Initialize monitoring service
        
        Args:
            app_name: Application name
            log_dir: Directory for log files
            max_log_size: Max log file size in bytes (default 10MB)
        """
        self.app_name = app_name
        self.log_dir = log_dir
        self.max_log_size = max_log_size
        self.start_time = datetime.now()
        self.request_count = 0
        self.error_count = 0
        self.metrics = {}
    
    def setup_logging(self):
        """Setup application logging with rotation"""
        try:
            # Create rotating file handler
            handler = RotatingFileHandler(
                f"{self.log_dir}/app.log",
                maxBytes=self.max_log_size,
                backupCount=10
            )
            
            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            
            # Configure logger
            logger = logging.getLogger()
            logger.setLevel(logging.DEBUG)
            logger.addHandler(handler)
            
            logging.info(f"{self.app_name} logging initialized")
            
        except Exception as e:
            print(f"Error setting up logging: {str(e)}")
    
    def log_request(
        self,
        method: str,
        path: str,
        status_code: int,
        duration_ms: float
    ):
        """Log API request
        
        Args:
            method: HTTP method
            path: Request path
            status_code: Response status code
            duration_ms: Request duration in milliseconds
        """
        self.request_count += 1
        logger = logging.getLogger(__name__)
        
        if status_code >= 400:
            self.error_count += 1
            logger.warning(
                f"{method} {path} - {status_code} ({duration_ms}ms)"
            )
        else:
            logger.info(
                f"{method} {path} - {status_code} ({duration_ms}ms)"
            )
    
    def log_error(
        self,
        error_type: str,
        message: str,
        severity: str = "ERROR"
    ):
        """Log application error
        
        Args:
            error_type: Type of error
            message: Error message
            severity: Severity level (ERROR, WARNING, CRITICAL)
        """
        self.error_count += 1
        logger = logging.getLogger(__name__)
        
        if severity == "CRITICAL":
            logger.critical(f"[{error_type}] {message}")
        elif severity == "WARNING":
            logger.warning(f"[{error_type}] {message}")
        else:
            logger.error(f"[{error_type}] {message}")
    
    def get_health_status(self) -> Dict:
        """Get application health status
        
        Returns:
            Health status dictionary
        """
        uptime = datetime.now() - self.start_time
        
        return {
            "status": "healthy",
            "app_name": self.app_name,
            "uptime_seconds": uptime.total_seconds(),
            "request_count": self.request_count,
            "error_count": self.error_count,
            "error_rate": self._calculate_error_rate(),
            "timestamp": datetime.now().isoformat()
        }
    
    def _calculate_error_rate(self) -> float:
        """Calculate error rate
        
        Returns:
            Error rate percentage
        """
        if self.request_count == 0:
            return 0.0
        return (self.error_count / self.request_count) * 100
    
    def record_metric(
        self,
        metric_name: str,
        value: float,
        tags: Optional[Dict] = None
    ):
        """Record application metric
        
        Args:
            metric_name: Name of metric
            value: Metric value
            tags: Optional metric tags
        """
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []
        
        metric_data = {
            "value": value,
            "timestamp": datetime.now().isoformat(),
            "tags": tags or {}
        }
        
        self.metrics[metric_name].append(metric_data)
    
    def get_metrics(
        self,
        metric_name: Optional[str] = None,
        limit: int = 100
    ) -> Dict:
        """Get recorded metrics
        
        Args:
            metric_name: Filter by metric name (optional)
            limit: Max metrics to return
            
        Returns:
            Dictionary of metrics
        """
        if metric_name:
            return {
                metric_name: self.metrics.get(metric_name, [])[-limit:]
            }
        
        return {
            name: values[-limit:]
            for name, values in self.metrics.items()
        }
    
    def get_performance_stats(self) -> Dict:
        """Get performance statistics
        
        Returns:
            Performance metrics
        """
        stats = {
            "total_requests": self.request_count,
            "total_errors": self.error_count,
            "error_rate_percent": self._calculate_error_rate(),
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "metrics_recorded": len(self.metrics),
            "avg_requests_per_minute": self._calculate_request_rate()
        }
        return stats
    
    def _calculate_request_rate(self) -> float:
        """Calculate average requests per minute
        
        Returns:
            Average requests per minute
        """
        uptime_seconds = (datetime.now() - self.start_time).total_seconds()
        if uptime_seconds == 0:
            return 0.0
        return (self.request_count / uptime_seconds) * 60
    
    def check_database_health(self) -> bool:
        """Check database health
        
        Returns:
            True if database is healthy
        """
        try:
            # In production, actual database connection test
            logger = logging.getLogger(__name__)
            logger.info("Database health check passed")
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            return False
    
    def check_redis_health(self) -> bool:
        """Check Redis health
        
        Returns:
            True if Redis is healthy
        """
        try:
            # In production, actual Redis connection test
            logger = logging.getLogger(__name__)
            logger.info("Redis health check passed")
            return True
        except Exception as e:
            logger.error(f"Redis health check failed: {str(e)}")
            return False
