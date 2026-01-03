# File: app/services/feedback_service.py
"""User feedback collection and analytics service"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum
from sqlalchemy import func
from app import db
from app.models import User, Feedback, FeatureRequest

class FeedbackType(str, Enum):
    BUG = "bug"
    FEATURE = "feature"
    GENERAL = "general"
    PERFORMANCE = "performance"
    UI_UX = "ui_ux"
    OTHER = "other"

class SatisfactionLevel(str, Enum):
    VERY_SATISFIED = 5
    SATISFIED = 4
    NEUTRAL = 3
    DISSATISFIED = 2
    VERY_DISSATISFIED = 1

class FeedbackService:
    """Service for collecting and analyzing user feedback"""
    
    @staticmethod
    def collect_feedback(
        user_id: int,
        rating: int,
        comment: Optional[str] = None,
        feedback_type: FeedbackType = FeedbackType.GENERAL,
        email: Optional[str] = None
    ) -> Dict:
        """Collect user feedback"""
        
        # Validate rating
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        
        # Create feedback record
        feedback = Feedback(
            user_id=user_id,
            rating=rating,
            comment=comment,
            feedback_type=feedback_type.value,
            email=email or User.query.get(user_id).email if user_id else None,
            created_at=datetime.utcnow()
        )
        
        db.session.add(feedback)
        db.session.commit()
        
        return {
            'id': feedback.id,
            'rating': feedback.rating,
            'type': feedback.feedback_type,
            'timestamp': feedback.created_at.isoformat(),
            'message': 'Feedback received. Thank you!'
        }
    
    @staticmethod
    def record_feature_request(
        user_id: int,
        feature_name: str,
        description: Optional[str] = None,
        priority: int = 3  # 1-5, higher is more important
    ) -> Dict:
        """Record user feature request"""
        
        feature_request = FeatureRequest(
            user_id=user_id,
            feature_name=feature_name,
            description=description,
            priority=priority,
            votes=1,
            created_at=datetime.utcnow()
        )
        
        db.session.add(feature_request)
        db.session.commit()
        
        return {
            'id': feature_request.id,
            'feature': feature_name,
            'message': 'Feature request recorded. We\'ll review it soon!'
        }
    
    @staticmethod
    def get_daily_feedback_summary() -> Dict:
        """Get daily feedback summary"""
        
        today = datetime.utcnow().date()
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())
        
        feedback_list = Feedback.query.filter(
            Feedback.created_at >= start_of_day,
            Feedback.created_at <= end_of_day
        ).all()
        
        if not feedback_list:
            return {
                'date': today.isoformat(),
                'total_feedback': 0,
                'average_rating': 0,
                'message': 'No feedback collected today yet'
            }
        
        # Calculate metrics
        total = len(feedback_list)
        ratings = [f.rating for f in feedback_list]
        avg_rating = sum(ratings) / total if ratings else 0
        
        # Break down by type
        by_type = {}
        for feedback_type in FeedbackType:
            count = sum(1 for f in feedback_list if f.feedback_type == feedback_type.value)
            if count > 0:
                by_type[feedback_type.value] = count
        
        # Get top comments
        comments = [f.comment for f in feedback_list if f.comment]
        
        return {
            'date': today.isoformat(),
            'total_feedback': total,
            'average_rating': round(avg_rating, 1),
            'breakdown_by_type': by_type,
            'satisfaction_level': _get_satisfaction_label(avg_rating),
            'sample_comments': comments[:3] if comments else [],
            'recommendation': _get_recommendation(avg_rating)
        }
    
    @staticmethod
    def get_weekly_feedback_summary() -> Dict:
        """Get weekly feedback summary"""
        
        today = datetime.utcnow().date()
        week_ago = today - timedelta(days=7)
        start_of_week = datetime.combine(week_ago, datetime.min.time())
        end_of_week = datetime.combine(today, datetime.max.time())
        
        feedback_list = Feedback.query.filter(
            Feedback.created_at >= start_of_week,
            Feedback.created_at <= end_of_week
        ).all()
        
        if not feedback_list:
            return {
                'week': f"{week_ago.isoformat()} to {today.isoformat()}",
                'total_feedback': 0,
                'message': 'No feedback collected this week'
            }
        
        # Calculate metrics
        total = len(feedback_list)
        ratings = [f.rating for f in feedback_list]
        avg_rating = sum(ratings) / total if ratings else 0
        
        # Daily breakdown
        daily_data = {}
        for i in range(7):
            day = week_ago + timedelta(days=i)
            day_feedback = [f for f in feedback_list if f.created_at.date() == day]
            if day_feedback:
                day_ratings = [f.rating for f in day_feedback]
                daily_data[day.isoformat()] = {
                    'count': len(day_feedback),
                    'average': round(sum(day_ratings) / len(day_ratings), 1)
                }
        
        return {
            'week': f"{week_ago.isoformat()} to {today.isoformat()}",
            'total_feedback': total,
            'average_rating': round(avg_rating, 1),
            'daily_breakdown': daily_data,
            'trend': _get_trend(daily_data),
            'satisfaction_level': _get_satisfaction_label(avg_rating)
        }
    
    @staticmethod
    def get_feature_requests_summary() -> Dict:
        """Get most requested features"""
        
        features = db.session.query(
            FeatureRequest.feature_name,
            func.count(FeatureRequest.id).label('request_count'),
            func.avg(FeatureRequest.votes).label('avg_votes')
        ).group_by(FeatureRequest.feature_name).order_by(
            func.count(FeatureRequest.id).desc()
        ).limit(10).all()
        
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'total_unique_features': len(features),
            'top_features': [
                {
                    'name': f.feature_name,
                    'requests': f.request_count,
                    'avg_priority': round(f.avg_votes, 1)
                }
                for f in features
            ]
        }
    
    @staticmethod
    def send_feedback_survey_reminder(user_id: int) -> bool:
        """Send feedback survey reminder to user"""
        # This would integrate with email service
        user = User.query.get(user_id)
        if not user or not user.email:
            return False
        
        # TODO: Send email with survey link
        return True

def _get_satisfaction_label(rating: float) -> str:
    """Convert rating to satisfaction label"""
    if rating >= 4.5:
        return "Very Satisfied"
    elif rating >= 3.5:
        return "Satisfied"
    elif rating >= 2.5:
        return "Neutral"
    else:
        return "Dissatisfied"

def _get_recommendation(rating: float) -> str:
    """Get recommendation based on rating"""
    if rating >= 4.5:
        return "Great! Keep up the current direction"
    elif rating >= 3.5:
        return "Good progress. Focus on user-reported issues"
    elif rating >= 2.5:
        return "Improvement needed. Prioritize feedback analysis"
    else:
        return "Critical: Urgent action needed. Review all feedback"

def _get_trend(daily_data: Dict) -> str:
    """Analyze rating trend"""
    if not daily_data:
        return "No data"
    
    values = [d['average'] for d in daily_data.values()]
    if len(values) < 2:
        return "Insufficient data"
    
    first_half = sum(values[:len(values)//2]) / (len(values)//2 or 1)
    second_half = sum(values[len(values)//2:]) / (len(values) - len(values)//2 or 1)
    
    if second_half > first_half + 0.2:
        return "Improving 📈"
    elif second_half < first_half - 0.2:
        return "Declining 📉"
    else:
        return "Stable ➡️"