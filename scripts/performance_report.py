from typing import Dict, List
from datetime import datetime

class PerformanceReporter:
    def __init__(self):
        self.metrics: Dict[str, List[float]] = {}
    
    def add_metric(self, name: str, value: float) -> None:
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(value)
    
    def generate_report(self) -> str:
        report = f"Performance Report - {datetime.now().isoformat()}\n"
        report += "=" * 50 + "\n"
        
        for metric_name, values in self.metrics.items():
            if values:
                avg = sum(values) / len(values)
                max_val = max(values)
                min_val = min(values)
                report += f"\n{metric_name}:\n"
                report += f"  Average: {avg:.2f}\n"
                report += f"  Max: {max_val:.2f}\n"
                report += f"  Min: {min_val:.2f}\n"
        
        return report

if __name__ == '__main__':
    reporter = PerformanceReporter()
    reporter.add_metric('response_time', 0.45)
    reporter.add_metric('response_time', 0.52)
    reporter.add_metric('response_time', 0.48)
    report = reporter.generate_report()
    print(report)
