from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum

Base = declarative_base()


class AnalyticsSnapshot(Base):
    """Model for storing analytics snapshots of system metrics."""
    __tablename__ = 'analytics_snapshots'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    total_jobs = Column(Integer, default=0)
    total_candidates = Column(Integer, default=0)
    matched_pairs = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    avg_match_score = Column(Float, default=0.0)
    job_categories = Column(JSON, nullable=True)  # {"category": count}
    skill_distribution = Column(JSON, nullable=True)  # {"skill": count}
    performance_metrics = Column(JSON, nullable=True)  # {"metric": value}
    created_at = Column(DateTime, default=datetime.utcnow)

    class Config:
        from_attributes = True


class Report(Base):
    """Model for storing generated reports."""
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True, index=True)
    report_type = Column(String(50), index=True)  # 'daily', 'weekly', 'monthly'
    period_start = Column(DateTime, index=True)
    period_end = Column(DateTime, index=True)
    generated_at = Column(DateTime, default=datetime.utcnow)
    total_jobs = Column(Integer, default=0)
    total_candidates = Column(Integer, default=0)
    total_matches = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    avg_match_score = Column(Float, default=0.0)
    key_insights = Column(JSON, nullable=True)  # List of insight objects
    recommendations = Column(JSON, nullable=True)  # List of recommendation objects
    report_data = Column(JSON, nullable=True)  # Full report JSON data
    created_at = Column(DateTime, default=datetime.utcnow)

    class Config:
        from_attributes = True


class UserPreference(Base):
    """Model for storing user dashboard preferences."""
    __tablename__ = 'user_preferences'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), unique=True, index=True)
    dashboard_layout = Column(JSON, nullable=True)  # Widget positions and sizes
    chart_preferences = Column(JSON, nullable=True)  # Chart types and settings
    report_frequency = Column(String(50), default='daily')  # 'daily', 'weekly', 'monthly'
    notification_enabled = Column(Integer, default=1)  # 1 for True, 0 for False
    auto_export = Column(Integer, default=0)  # 1 for True, 0 for False
    export_format = Column(String(50), default='pdf')  # 'pdf', 'excel', 'csv'
    theme = Column(String(50), default='light')  # 'light', 'dark'
    timezone = Column(String(50), default='UTC')
    custom_alerts = Column(JSON, nullable=True)  # {"alert_name": threshold}
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class Config:
        from_attributes = True
