import logging
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import csv
from io import StringIO

logger = logging.getLogger(__name__)

class ReportFormat(Enum):
    JSON = 'json'
    CSV = 'csv'
    PDF = 'pdf'
    EXCEL = 'excel'

class ReportType(Enum):
    RECRUITMENT = 'recruitment'
    CANDIDATE = 'candidate'
    SALARY = 'salary'
    PERFORMANCE = 'performance'
    ANALYTICS = 'analytics'

@dataclass
class ReportConfig:
    report_type: ReportType
    format: ReportFormat
    title: str
    description: Optional[str] = None
    include_charts: bool = False
    time_period: Optional[str] = None
    filters: Optional[Dict] = None

@dataclass
class Report:
    id: str
    config: ReportConfig
    data: Dict[str, Any]
    created_at: datetime
    generated_by: str
    file_path: Optional[str] = None
    file_size: Optional[int] = None

class ReportGeneratorService:
    def __init__(self):
        self.reports = {}
        self.report_templates = {}
        self._setup_templates()
    
    def _setup_templates(self):
        """Setup default report templates"""
        self.report_templates = {
            ReportType.RECRUITMENT: self._template_recruitment,
            ReportType.CANDIDATE: self._template_candidate,
            ReportType.SALARY: self._template_salary,
            ReportType.PERFORMANCE: self._template_performance,
            ReportType.ANALYTICS: self._template_analytics,
        }
    
    def _template_recruitment(self) -> Dict:
        return {
            'title': 'Recruitment Report',
            'sections': ['Summary', 'Metrics', 'Pipeline', 'Timeline']
        }
    
    def _template_candidate(self) -> Dict:
        return {
            'title': 'Candidate Report',
            'sections': ['Profile', 'Assessment', 'History', 'Recommendations']
        }
    
    def _template_salary(self) -> Dict:
        return {
            'title': 'Salary Report',
            'sections': ['Summary', 'Distribution', 'Benchmarks', 'Trends']
        }
    
    def _template_performance(self) -> Dict:
        return {
            'title': 'Performance Report',
            'sections': ['KPIs', 'Metrics', 'Analysis', 'Recommendations']
        }
    
    def _template_analytics(self) -> Dict:
        return {
            'title': 'Analytics Report',
            'sections': ['Overview', 'Detailed Metrics', 'Trends', 'Insights']
        }
    
    def create_report(self,
                     report_type: ReportType,
                     report_format: ReportFormat,
                     data: Dict[str, Any],
                     title: str,
                     user_id: str,
                     description: Optional[str] = None,
                     filters: Optional[Dict] = None) -> Report:
        """Create a new report"""
        from uuid import uuid4
        
        report_id = str(uuid4())
        config = ReportConfig(
            report_type=report_type,
            format=report_format,
            title=title,
            description=description,
            filters=filters
        )
        
        report = Report(
            id=report_id,
            config=config,
            data=data,
            created_at=datetime.now(),
            generated_by=user_id
        )
        
        self.reports[report_id] = report
        logger.info(f'Report created: {report_id}')
        return report
    
    def generate_json(self, report: Report) -> str:
        """Generate report in JSON format"""
        report_dict = {
            'id': report.id,
            'title': report.config.title,
            'description': report.config.description,
            'type': report.config.report_type.value,
            'created_at': report.created_at.isoformat(),
            'generated_by': report.generated_by,
            'data': report.data
        }
        return json.dumps(report_dict, indent=2, default=str)
    
    def generate_csv(self, report: Report) -> str:
        """Generate report in CSV format"""
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=[])
        
        # Write header
        writer.writerow({
            'Report': report.config.title,
            'Type': report.config.report_type.value,
            'Generated': report.created_at.isoformat(),
            'By': report.generated_by
        })
        
        # Flatten and write data
        if isinstance(report.data, dict):
            for key, value in report.data.items():
                if isinstance(value, (list, dict)):
                    writer.writerow({key: json.dumps(value)})
                else:
                    writer.writerow({key: value})
        
        return output.getvalue()
    
    def generate_excel(self, report: Report) -> bytes:
        """Generate report in Excel format"""
        # Requires openpyxl library
        logger.info(f'Excel generation for report {report.id}')
        return b'Excel generation not implemented'
    
    def generate_pdf(self, report: Report) -> bytes:
        """Generate report in PDF format"""
        # Requires reportlab or similar
        logger.info(f'PDF generation for report {report.id}')
        return b'PDF generation not implemented'
    
    def export_report(self, report_id: str) -> Optional[str]:
        """Export report in configured format"""
        if report_id not in self.reports:
            logger.error(f'Report not found: {report_id}')
            return None
        
        report = self.reports[report_id]
        
        if report.config.format == ReportFormat.JSON:
            return self.generate_json(report)
        elif report.config.format == ReportFormat.CSV:
            return self.generate_csv(report)
        elif report.config.format == ReportFormat.EXCEL:
            return self.generate_excel(report).decode('utf-8', errors='ignore')
        elif report.config.format == ReportFormat.PDF:
            return self.generate_pdf(report).decode('utf-8', errors='ignore')
        
        return None
    
    def schedule_report(self,
                       report_config: ReportConfig,
                       schedule_type: str = 'daily',
                       recipients: Optional[List[str]] = None) -> str:
        """Schedule recurring report generation"""
        logger.info(f'Report scheduled: {schedule_type}')
        return f'Schedule_{schedule_type}'
    
    def get_report(self, report_id: str) -> Optional[Report]:
        """Get report by ID"""
        return self.reports.get(report_id)
    
    def list_reports(self, 
                    report_type: Optional[ReportType] = None,
                    limit: int = 100) -> List[Report]:
        """List reports with optional filtering"""
        reports = list(self.reports.values())
        
        if report_type:
            reports = [r for r in reports if r.config.report_type == report_type]
        
        return sorted(reports, key=lambda x: x.created_at, reverse=True)[:limit]
    
    def delete_report(self, report_id: str) -> bool:
        """Delete report"""
        if report_id in self.reports:
            del self.reports[report_id]
            logger.info(f'Report deleted: {report_id}')
            return True
        return False
    
    def get_report_stats(self) -> Dict:
        """Get report generation statistics"""
        by_type = {}
        by_format = {}
        
        for report in self.reports.values():
            type_name = report.config.report_type.value
            format_name = report.config.format.value
            
            by_type[type_name] = by_type.get(type_name, 0) + 1
            by_format[format_name] = by_format.get(format_name, 0) + 1
        
        return {
            'total_reports': len(self.reports),
            'by_type': by_type,
            'by_format': by_format,
            'registered_templates': len(self.report_templates)
        }
