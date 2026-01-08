"""Analytics service for tracking and analyzing application metrics."""
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from app.models import db, User, Candidate, Vacancy, Application, Match
import logging

logger = logging.getLogger(__name__)

class AnalyticsService:
    """Service for generating analytics and insights."""
    
    @staticmethod
    def get_dashboard_metrics(days: int = 30) -> dict:
        """Get key metrics for analytics dashboard."""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        metrics = {
            'total_users': User.query.count(),
            'total_candidates': Candidate.query.count(),
            'total_vacancies': Vacancy.query.count(),
            'total_applications': Application.query.count(),
            'total_matches': Match.query.count(),
            'new_users_period': User.query.filter(User.created_at >= start_date).count(),
            'new_candidates_period': Candidate.query.filter(Candidate.created_at >= start_date).count(),
            'new_vacancies_period': Vacancy.query.filter(Vacancy.created_at >= start_date).count(),
            'new_applications_period': Application.query.filter(Application.created_at >= start_date).count(),
        }
        
        # Conversion metrics
        metrics['application_rate'] = AnalyticsService.calc_application_rate()
        metrics['match_acceptance_rate'] = AnalyticsService.calc_match_acceptance_rate()
        metrics['hiring_completion_rate'] = AnalyticsService.calc_hiring_rate()
        
        return metrics
    
    @staticmethod
    def get_user_funnel_metrics(days: int = 30) -> dict:
        """Get user conversion funnel metrics."""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        total_registered = User.query.filter(User.created_at >= start_date).count()
        total_completed_profile = Candidate.query.filter(
            Candidate.created_at >= start_date,
            Candidate.profile_complete == True
        ).count()
        total_viewed_jobs = Application.query.filter(
            Application.created_at >= start_date
        ).group_by(Application.userid).count()
        total_applied = Application.query.filter(
            Application.created_at >= start_date
        ).group_by(Application.userid).count()
        total_hired = Application.query.filter(
            Application.created_at >= start_date,
            Application.status == 'hired'
        ).group_by(Application.userid).count()
        
        return {
            'registered': total_registered,
            'profile_completed': total_completed_profile,
            'viewed_jobs': total_viewed_jobs,
            'applied': total_applied,
            'hired': total_hired,
            'profile_completion_rate': (total_completed_profile / total_registered * 100) if total_registered > 0 else 0,
            'application_rate': (total_applied / total_completed_profile * 100) if total_completed_profile > 0 else 0,
            'hiring_rate': (total_hired / total_applied * 100) if total_applied > 0 else 0,
        }
    
    @staticmethod
    def get_match_quality_metrics(days: int = 30) -> dict:
        """Analyze match quality and effectiveness."""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        matches = Match.query.filter(Match.created_at >= start_date).all()
        scores = [m.score for m in matches if m.score]
        
        if not scores:
            return {
                'total_matches': 0,
                'average_match_score': 0,
                'high_quality_matches': 0,
                'medium_quality_matches': 0,
                'low_quality_matches': 0,
            }
        
        return {
            'total_matches': len(matches),
            'average_match_score': sum(scores) / len(scores),
            'high_quality_matches': sum(1 for s in scores if s >= 80),
            'medium_quality_matches': sum(1 for s in scores if 50 <= s < 80),
            'low_quality_matches': sum(1 for s in scores if s < 50),
            'max_score': max(scores),
            'min_score': min(scores),
        }
    
    @staticmethod
    def calc_application_rate() -> float:
        """Calculate percentage of matches that lead to applications."""
        total_matches = Match.query.count()
        if total_matches == 0:
            return 0.0
        return 50.0  # Placeholder - implement actual calculation
    
    @staticmethod
    def calc_match_acceptance_rate() -> float:
        """Calculate percentage of matches leading to hired status."""
        total_matches = Match.query.count()
        if total_matches == 0:
            return 0.0
        hired_matches = Match.query.filter(Match.status == 'hired').count()
        return (hired_matches / total_matches * 100) if total_matches > 0 else 0.0
    
    @staticmethod
    def calc_hiring_rate() -> float:
        """Calculate hiring completion rate."""
        total_vacancies = Vacancy.query.count()
        if total_vacancies == 0:
            return 0.0
        filled_vacancies = Vacancy.query.filter(Vacancy.status == 'filled').count()
        return (filled_vacancies / total_vacancies * 100) if total_vacancies > 0 else 0.0
