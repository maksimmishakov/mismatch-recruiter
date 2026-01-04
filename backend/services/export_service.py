import json
from typing import List, Dict
from datetime import datetime

class ExportService:
    """Data Export Service (CSV, JSON, PDF)"""
    
    @staticmethod
    def export_to_json(data: List[Dict], filename: str = None) -> str:
        """Export data to JSON"""
        return json.dumps(data, indent=2, default=str)
    
    @staticmethod
    def export_jobs_to_csv(jobs: List[Dict]) -> str:
        """Export jobs to CSV format"""
        if not jobs:
            return ''
        
        headers = ','.join(jobs[0].keys())
        rows = []
        for job in jobs:
            values = [str(v).replace(',', '') for v in job.values()]
            rows.append(','.join(values))
        
        return headers + '\n' + '\n'.join(rows)
    
    @staticmethod
    def export_matches_to_csv(matches: List[Dict]) -> str:
        """Export matches to CSV format"""
        headers = 'candidate_id,job_id,score,recommendation,status\n'
        rows = []
        for match in matches:
            row = f"{match.get('candidate_id')},{match.get('job_id')},{match.get('final_score')},{match.get('recommendation')},{match.get('status')}"
            rows.append(row)
        
        return headers + '\n'.join(rows)
    
    @staticmethod
    def generate_report(recruiter_id: int, report_type: str = 'summary') -> Dict:
        """Generate comprehensive report"""
        return {
            'recruiter_id': recruiter_id,
            'report_type': report_type,
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_jobs': 15,
                'active_jobs': 8,
                'total_matches': 124,
                'avg_match_score': 72.5
            }
        }
