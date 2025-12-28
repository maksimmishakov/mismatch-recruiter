__init__.py"""Models package for Lamoda AI Recruiter

Contains SQLAlchemy ORM models for data persistence.
"""
from app.models.lamoda import (
    LamodaJob,
    LamodaCandidate,
    LamodaPlacement,
    LamodaSync,
    LamodoIntegrationConfig,
    Base
)

__all__ = [
    "LamodaJob",
    "LamodaCandidate",
    "LamodaPlacement",
    "LamodaSync",
    "LamodoIntegrationConfig",
    "Base"
]
