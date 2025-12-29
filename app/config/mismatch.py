"""Mismatch Integration Configuration."""
from typing import Optional, Dict, Any
from pydantic import BaseSettings, SecretStr, AnyUrl
import os
from functools import lru_cache


class MismatchSettings(BaseSettings):
    """Mismatch API Configuration Settings"""
    
    # Mismatch API Credentials
    Mismatch_api_key: SecretStr = SecretStr(os.getenv("Mismatch_API_KEY", ""))
    Mismatch_api_secret: SecretStr = SecretStr(os.getenv("Mismatch_API_SECRET", ""))
    Mismatch_api_base_url: AnyUrl = AnyUrl(os.getenv(
        "Mismatch_API_BASE_URL",
        "https://api.Mismatch.ru/v1"
    ))
    
    # Mismatch Integration Settings
    Mismatch_sync_enabled: bool = bool(os.getenv("Mismatch_SYNC_ENABLED", True))
    Mismatch_sync_interval_hours: int = int(os.getenv("Mismatch_SYNC_INTERVAL_HOURS", 24))
    Mismatch_max_jobs_per_sync: int = int(os.getenv("Mismatch_MAX_JOBS_PER_SYNC", 1000))
    Mismatch_max_candidates_per_sync: int = int(os.getenv("Mismatch_MAX_CANDIDATES_PER_SYNC", 500))
    
    # Request Configuration
    Mismatch_request_timeout_seconds: int = int(os.getenv("Mismatch_REQUEST_TIMEOUT", 30))
    Mismatch_max_retries: int = int(os.getenv("Mismatch_MAX_RETRIES", 3))
    Mismatch_retry_backoff_factor: float = float(os.getenv("Mismatch_RETRY_BACKOFF", 1.5))
    
    # Matching Engine Settings
    Mismatch_min_match_score: float = float(os.getenv("Mismatch_MIN_MATCH_SCORE", 0.7))
    Mismatch_skill_weight: float = float(os.getenv("Mismatch_SKILL_WEIGHT", 0.4))
    Mismatch_experience_weight: float = float(os.getenv("Mismatch_EXPERIENCE_WEIGHT", 0.3))
    Mismatch_salary_weight: float = float(os.getenv("Mismatch_SALARY_WEIGHT", 0.3))
    
    # Database Configuration
    Mismatch_db_connection: Optional[str] = os.getenv("Mismatch_DB_CONNECTION")
    Mismatch_db_pool_size: int = int(os.getenv("Mismatch_DB_POOL_SIZE", 20))
    Mismatch_db_echo: bool = bool(os.getenv("Mismatch_DB_ECHO", False))
    
    # Webhook Configuration
    Mismatch_webhook_enabled: bool = bool(os.getenv("Mismatch_WEBHOOK_ENABLED", False))
    Mismatch_webhook_secret: Optional[SecretStr] = SecretStr(os.getenv("Mismatch_WEBHOOK_SECRET", ""))
    Mismatch_webhook_events: list = ["job.created", "job.updated", "candidate.matched"]
    
    # Notification Configuration
    Mismatch_notify_on_placement: bool = bool(os.getenv("Mismatch_NOTIFY_ON_PLACEMENT", True))
    Mismatch_notify_on_match_score: float = float(os.getenv("Mismatch_NOTIFY_ON_MATCH_SCORE", 0.85))
    
    class Config:
        """Pydantic config for settings"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Mismatch API Constants
Mismatch_JOB_STATUS_OPTIONS = {
    "active": "Active job listing",
    "archived": "Archived job",
    "expired": "Expired job listing"
}

Mismatch_EXPERIENCE_LEVELS = {
    "junior": 0,
    "mid": 1,
    "senior": 2,
    "lead": 3
}

Mismatch_EMPLOYMENT_TYPES = {
    "full_time": "Full-time",
    "part_time": "Part-time",
    "contract": "Contract",
    "internship": "Internship",
    "freelance": "Freelance"
}

Mismatch_PLACEMENT_STATUSES = {
    "submitted": "Submitted to employer",
    "viewed": "Viewed by employer",
    "interview_scheduled": "Interview scheduled",
    "accepted": "Accepted by employer",
    "rejected": "Rejected by employer",
    "hired": "Candidate hired",
    "withdrawn": "Withdrawn"
}

Mismatch_SYNC_TYPES = {
    "full": "Full synchronization of all data",
    "incremental": "Incremental sync of changed data",
    "jobs_only": "Sync jobs only",
    "candidates_only": "Sync candidates only"
}


@lru_cache()
def get_settings() -> MismatchSettings:
    """Get cached Mismatch settings instance"""
    return MismatchSettings()


def get_Mismatch_config() -> Dict[str, Any]:
    """Get Mismatch configuration as dictionary"""
    settings = get_settings()
    return {
        "api_key": settings.Mismatch_api_key.get_secret_value(),
        "api_secret": settings.Mismatch_api_secret.get_secret_value(),
        "api_base_url": str(settings.Mismatch_api_base_url),
        "sync_interval_hours": settings.Mismatch_sync_interval_hours,
        "min_match_score": settings.Mismatch_min_match_score,
        "request_timeout": settings.Mismatch_request_timeout_seconds,
        "max_retries": settings.Mismatch_max_retries,
        "webhook_enabled": settings.Mismatch_webhook_enabled
    }


# Default matching weights
MATCHING_WEIGHTS = {
    "skills": 0.4,
    "experience": 0.3,
    "salary": 0.2,
    "location": 0.1
}

# Error codes
Mismatch_ERROR_CODES = {
    "INVALID_API_KEY": "Invalid or missing API key",
    "RATE_LIMITED": "API rate limit exceeded",
    "INVALID_REQUEST": "Invalid request parameters",
    "RESOURCE_NOT_FOUND": "Resource not found",
    "SERVER_ERROR": "Internal server error",
    "SYNC_FAILED": "Synchronization failed"
}
