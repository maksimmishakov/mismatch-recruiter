lamoda.py"""Lamoda Integration Configuration

Configuration settings, constants, and environment variables
for Lamoda API integration.
"""
from typing import Optional, Dict, Any
from pydantic import BaseSettings, SecretStr, AnyUrl
import os
from functools import lru_cache


class LamodaSettings(BaseSettings):
    """Lamoda API Configuration Settings"""
    
    # Lamoda API Credentials
    lamoda_api_key: SecretStr = SecretStr(os.getenv("LAMODA_API_KEY", ""))
    lamoda_api_secret: SecretStr = SecretStr(os.getenv("LAMODA_API_SECRET", ""))
    lamoda_api_base_url: AnyUrl = AnyUrl(os.getenv(
        "LAMODA_API_BASE_URL",
        "https://api.lamoda.ru/v1"
    ))
    
    # Lamoda Integration Settings
    lamoda_sync_enabled: bool = bool(os.getenv("LAMODA_SYNC_ENABLED", True))
    lamoda_sync_interval_hours: int = int(os.getenv("LAMODA_SYNC_INTERVAL_HOURS", 24))
    lamoda_max_jobs_per_sync: int = int(os.getenv("LAMODA_MAX_JOBS_PER_SYNC", 1000))
    lamoda_max_candidates_per_sync: int = int(os.getenv("LAMODA_MAX_CANDIDATES_PER_SYNC", 500))
    
    # Request Configuration
    lamoda_request_timeout_seconds: int = int(os.getenv("LAMODA_REQUEST_TIMEOUT", 30))
    lamoda_max_retries: int = int(os.getenv("LAMODA_MAX_RETRIES", 3))
    lamoda_retry_backoff_factor: float = float(os.getenv("LAMODA_RETRY_BACKOFF", 1.5))
    
    # Matching Engine Settings
    lamoda_min_match_score: float = float(os.getenv("LAMODA_MIN_MATCH_SCORE", 0.7))
    lamoda_skill_weight: float = float(os.getenv("LAMODA_SKILL_WEIGHT", 0.4))
    lamoda_experience_weight: float = float(os.getenv("LAMODA_EXPERIENCE_WEIGHT", 0.3))
    lamoda_salary_weight: float = float(os.getenv("LAMODA_SALARY_WEIGHT", 0.3))
    
    # Database Configuration
    lamoda_db_connection: Optional[str] = os.getenv("LAMODA_DB_CONNECTION")
    lamoda_db_pool_size: int = int(os.getenv("LAMODA_DB_POOL_SIZE", 20))
    lamoda_db_echo: bool = bool(os.getenv("LAMODA_DB_ECHO", False))
    
    # Webhook Configuration
    lamoda_webhook_enabled: bool = bool(os.getenv("LAMODA_WEBHOOK_ENABLED", False))
    lamoda_webhook_secret: Optional[SecretStr] = SecretStr(os.getenv("LAMODA_WEBHOOK_SECRET", ""))
    lamoda_webhook_events: list = ["job.created", "job.updated", "candidate.matched"]
    
    # Notification Configuration
    lamoda_notify_on_placement: bool = bool(os.getenv("LAMODA_NOTIFY_ON_PLACEMENT", True))
    lamoda_notify_on_match_score: float = float(os.getenv("LAMODA_NOTIFY_ON_MATCH_SCORE", 0.85))
    
    class Config:
        """Pydantic config for settings"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Lamoda API Constants
LAMODA_JOB_STATUS_OPTIONS = {
    "active": "Active job listing",
    "archived": "Archived job",
    "expired": "Expired job listing"
}

LAMODA_EXPERIENCE_LEVELS = {
    "junior": 0,
    "mid": 1,
    "senior": 2,
    "lead": 3
}

LAMODA_EMPLOYMENT_TYPES = {
    "full_time": "Full-time",
    "part_time": "Part-time",
    "contract": "Contract",
    "internship": "Internship",
    "freelance": "Freelance"
}

LAMODA_PLACEMENT_STATUSES = {
    "submitted": "Submitted to employer",
    "viewed": "Viewed by employer",
    "interview_scheduled": "Interview scheduled",
    "accepted": "Accepted by employer",
    "rejected": "Rejected by employer",
    "hired": "Candidate hired",
    "withdrawn": "Withdrawn"
}

LAMODA_SYNC_TYPES = {
    "full": "Full synchronization of all data",
    "incremental": "Incremental sync of changed data",
    "jobs_only": "Sync jobs only",
    "candidates_only": "Sync candidates only"
}


@lru_cache()
def get_settings() -> LamodaSettings:
    """Get cached Lamoda settings instance"""
    return LamodaSettings()


def get_lamoda_config() -> Dict[str, Any]:
    """Get Lamoda configuration as dictionary"""
    settings = get_settings()
    return {
        "api_key": settings.lamoda_api_key.get_secret_value(),
        "api_secret": settings.lamoda_api_secret.get_secret_value(),
        "api_base_url": str(settings.lamoda_api_base_url),
        "sync_interval_hours": settings.lamoda_sync_interval_hours,
        "min_match_score": settings.lamoda_min_match_score,
        "request_timeout": settings.lamoda_request_timeout_seconds,
        "max_retries": settings.lamoda_max_retries,
        "webhook_enabled": settings.lamoda_webhook_enabled
    }


# Default matching weights
MATCHING_WEIGHTS = {
    "skills": 0.4,
    "experience": 0.3,
    "salary": 0.2,
    "location": 0.1
}

# Error codes
LAMODA_ERROR_CODES = {
    "INVALID_API_KEY": "Invalid or missing API key",
    "RATE_LIMITED": "API rate limit exceeded",
    "INVALID_REQUEST": "Invalid request parameters",
    "RESOURCE_NOT_FOUND": "Resource not found",
    "SERVER_ERROR": "Internal server error",
    "SYNC_FAILED": "Synchronization failed"
}
