"""Authentication module for JWT-based authorization."""
from .jwt_handler import JWTHandler
from .decorators import require_auth

__all__ = ['JWTHandler', 'require_auth']
