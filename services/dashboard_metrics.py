from datetime import datetime
from typing import Dict, Any

class DashboardMetrics:
    def __init__(self):
        self.metrics = {}
    
    def record_request(self, endpoint: str, duration: float, status: int) -> None:
        key = f"{endpoint}:{status}"
        if key not in self.metrics:
            self.metrics[key] = {'count': 0, 'total_duration': 0, 'timestamp': datetime.now()}
        
        self.metrics[key]['count'] += 1
        self.metrics[key]['total_duration'] += duration
    
    def get_avg_response_time(self, endpoint: str) -> float:
        entries = [v for k, v in self.metrics.items() if k.startswith(endpoint)]
        if not entries:
            return 0
        total_time = sum(e['total_duration'] for e in entries)
        total_count = sum(e['count'] for e in entries)
        return total_time / total_count if total_count > 0 else 0

if __name__ == '__main__':
    metrics = DashboardMetrics()
    metrics.record_request('/api/match', 0.45, 200)
    metrics.record_request('/api/match', 0.52, 200)
    avg_time = metrics.get_avg_response_time('/api/match')
    print(f"Avg response time: {avg_time:.2f}s")
