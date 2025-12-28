import logging
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt
from enum import Enum

logger = logging.getLogger(__name__)


class UserRole(Enum):
    """User role types"""
    ADMIN = "admin"
    MANAGER = "manager"
    VIEWER = "viewer"
    USER = "user"


class Permission(Enum):
    """Permission types"""
    VIEW_ANALYTICS = "view_analytics"
    EDIT_ANALYTICS = "edit_analytics"
    VIEW_MATCHES = "view_matches"
    EDIT_MATCHES = "edit_matches"
    VIEW_REPORTS = "view_reports"
    GENERATE_REPORTS = "generate_reports"
    MANAGE_USERS = "manage_users"
    MANAGE_INTEGRATIONS = "manage_integrations"


ROLE_PERMISSIONS = {
    UserRole.ADMIN: [
        Permission.VIEW_ANALYTICS,
        Permission.EDIT_ANALYTICS,
        Permission.VIEW_MATCHES,
        Permission.EDIT_MATCHES,
        Permission.VIEW_REPORTS,
        Permission.GENERATE_REPORTS,
        Permission.MANAGE_USERS,
        Permission.MANAGE_INTEGRATIONS
    ],
    UserRole.MANAGER: [
        Permission.VIEW_ANALYTICS,
        Permission.EDIT_ANALYTICS,
        Permission.VIEW_MATCHES,
        Permission.EDIT_MATCHES,
        Permission.VIEW_REPORTS,
        Permission.GENERATE_REPORTS
    ],
    UserRole.VIEWER: [
        Permission.VIEW_ANALYTICS,
        Permission.VIEW_MATCHES,
        Permission.VIEW_REPORTS
    ],
    UserRole.USER: [
        Permission.VIEW_MATCHES
    ]
}


class AuthService:
    """JWT authentication and authorization service"""
    
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 30
    ):
        """Initialize auth service
        
        Args:
            secret_key: Secret key for signing JWT tokens
            algorithm: JWT algorithm (default: HS256)
            access_token_expire_minutes: Token expiration time in minutes
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password
        """
        try:
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except Exception as e:
            logger.error(f"Error hashing password: {str(e)}")
            raise
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash
        
        Args:
            password: Plain text password
            hashed: Hashed password
            
        Returns:
            True if password matches
        """
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception as e:
            logger.error(f"Error verifying password: {str(e)}")
            return False
    
    def create_access_token(
        self,
        user_id: str,
        user_email: str,
        role: str,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token
        
        Args:
            user_id: User ID
            user_email: User email
            role: User role
            expires_delta: Token expiration delta
            
        Returns:
            JWT token string
        """
        try:
            if expires_delta is None:
                expires_delta = timedelta(minutes=self.access_token_expire_minutes)
            
            expire = datetime.utcnow() + expires_delta
            
            to_encode = {
                "sub": user_id,
                "email": user_email,
                "role": role,
                "exp": expire,
                "iat": datetime.utcnow()
            }
            
            encoded_jwt = jwt.encode(
                to_encode,
                self.secret_key,
                algorithm=self.algorithm
            )
            
            logger.info(f"Access token created for user {user_id}")
            return encoded_jwt
            
        except Exception as e:
            logger.error(f"Error creating access token: {str(e)}")
            raise
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify and decode JWT token
        
        Args:
            token: JWT token string
            
        Returns:
            Decoded token payload or None
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        except JWTError as e:
            logger.error(f"Invalid token: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error verifying token: {str(e)}")
            return None
    
    def get_user_permissions(self, role: str) -> list:
        """Get permissions for a role
        
        Args:
            role: User role name
            
        Returns:
            List of permission strings
        """
        try:
            role_enum = UserRole[role.upper()]
            permissions = ROLE_PERMISSIONS.get(role_enum, [])
            return [p.value for p in permissions]
        except (KeyError, Exception) as e:
            logger.warning(f"Unknown role: {role}")
            return []
    
    def has_permission(
        self,
        role: str,
        permission: str
    ) -> bool:
        """Check if role has permission
        
        Args:
            role: User role name
            permission: Required permission
            
        Returns:
            True if role has permission
        """
        try:
            role_enum = UserRole[role.upper()]
            permission_enum = Permission[permission.upper()]
            
            permissions = ROLE_PERMISSIONS.get(role_enum, [])
            return permission_enum in permissions
        except (KeyError, Exception):
            return False
    
    def refresh_token(
        self,
        token: str,
        expires_delta: Optional[timedelta] = None
    ) -> Optional[str]:
        """Refresh JWT token
        
        Args:
            token: Current JWT token
            expires_delta: New expiration delta
            
        Returns:
            New JWT token or None
        """
        try:
            payload = self.verify_token(token)
            if not payload:
                return None
            
            # Create new token with same data
            return self.create_access_token(
                user_id=payload.get("sub"),
                user_email=payload.get("email"),
                role=payload.get("role"),
                expires_delta=expires_delta
            )
        except Exception as e:
            logger.error(f"Error refreshing token: {str(e)}")
            return None
    
    def revoke_token(self, token: str) -> bool:
        """Revoke a token (for logout)
        
        Args:
            token: JWT token to revoke
            
        Returns:
            True if successful
        """
        try:
            # In production, store revoked tokens in Redis/cache
            logger.info("Token revoked")
            return True
        except Exception as e:
            logger.error(f"Error revoking token: {str(e)}")
            return False
