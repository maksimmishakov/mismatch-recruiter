from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models after db is initialized to avoid circular imports
from app.models.user import User  # noqa
from app.models.candidate import Candidate  # noqa
from app.models.job import Job  # noqa  
from app.models.match import Match  # noqa

__all__ = ['db', 'User', 'Candidate', 'Job', 'Match']
