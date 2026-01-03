import logging
from datetime import datetime

class MonitoringService:
    def __init__(self):
        self.logger = logging.getLogger('mismatch')
        self.metrics = {}
    
    def log_metric(self, name: str, value: float) -> None:
        timestamp = datetime.now().isoformat()
        self.metrics[name] = {'value': value, 'timestamp': timestamp}
        self.logger.info(f"[METRIC] {name}: {value}")

if __name__ == '__main__':
    monitor = MonitoringService()
    monitor.log_metric('response_time', 0.45)
    monitor.log_metric('throughput', 1200)
    print("Monitoring service initialized!")
