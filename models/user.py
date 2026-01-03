"""User Model - Authentication and Profiles"""
from datetime import datetime
from enum import Enum

class UserRole(Enum):
    """User role enumeration"""
    ADMIN = 'admin'
    RECRUITER = 'recruiter'
    HIRING_MANAGER = 'hiring_manager'
    CANDIDATE = 'candidate'

class User:
    """User model for authentication and authorization"""
    
    def __init__(self, email: str, password_hash: str, role: UserRole):
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.created_at = datetime.utcnow()
        self.is_active = True
        self.mfa_enabled = False
        self.last_login = None
    
    def to_dict(self) -> dict:
        """Convert user to dictionary"""
        return {
            'email': self.email,
            'role': self.role.value,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active,
            'mfa_enabled': self.mfa_enabled,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
