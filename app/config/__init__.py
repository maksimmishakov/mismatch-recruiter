"""Configuration module."""
from app.config.lamoda import (
    LamodaSettings,
    get_settings,
    get_lamoda_config,
    LAMODA_JOB_STATUS_OPTIONS,
    LAMODA_EXPERIENCE_LEVELS,
    LAMODA_EMPLOYMENT_TYPES,
    LAMODA_PLACEMENT_STATUSES,
    LAMODA_SYNC_TYPES,
    MATCHING_WEIGHTS,
    LAMODA_ERROR_CODES,
)

__all__ = [
    "LamodaSettings",
    "get_settings",
    "get_lamoda_config",
    "LAMODA_JOB_STATUS_OPTIONS",
    "LAMODA_EXPERIENCE_LEVELS",
    "LAMODA_EMPLOYMENT_TYPES",
    "LAMODA_PLACEMENT_STATUSES",
    "LAMODA_SYNC_TYPES",
    "MATCHING_WEIGHTS",
    "LAMODA_ERROR_CODES",
]
