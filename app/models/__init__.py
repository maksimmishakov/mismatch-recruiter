"""Models module."""
from app.models.mismatch import MismatchSync

try:
    from app.models.candidates_matches import Resume, Job, Match
except ImportError:
    Resume = None
    Job = None
    Match = None

__all__ = [
    "MismatchSync",
]

if Resume is not None:
    __all__.extend(["Resume", "Job", "Match"])
