from typing import Dict, List
from datetime import datetime

class AnalyticsService:
    """Analytics & Reporting Service"""
    
    @staticmethod
    def get_dashboard_stats(user_id: int) -> Dict:
        """Get dashboard statistics"""
        return {
            'total_jobs': 15,
            'active_jobs': 8,
            'total_matches': 124,
            'average_match_score': 72.5,
            'open_positions': 5,
            'closed_positions': 10,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def get_job_performance(job_id: int) -> Dict:
        """Get job performance metrics"""
        return {
            'job_id': job_id,
            'job_title': 'Senior Python Developer',
            'total_matches': 34,
            'perfect_matches': 8,
            'good_matches': 16,
            'fair_matches': 7,
            'poor_matches': 3,
            'average_score': 71.2,
            'days_active': 21
        }
    
    @staticmethod
    def get_market_trends(location: str = 'USA') -> Dict:
        """Get market trends"""
        return {
            'location': location,
            'top_locations': [('San Francisco', 45), ('New York', 38), ('Remote', 32)],
            'seniority_dist': {'Junior': 25, 'Mid': 50, 'Senior': 25},
            'total_active_jobs': 542,
            'avg_salary_range': {'min': 75000, 'max': 125000},
            'market_temperature': 'Hot',
            'trend': 'Rising'
        }
    
    @staticmethod
    def get_recruiter_metrics(user_id: int) -> Dict:
        """Get recruiter performance metrics"""
        return {
            'recruiter_id': user_id,
            'jobs_posted': 12,
            'matches_created': 89,
            'placements': 5,
            'placement_rate': 0.056,
            'avg_time_to_hire': 21,
            'quality_score': 8.5,
            'level': 'Expert'
        }
