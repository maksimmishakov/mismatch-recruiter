python3 << 'ENDSCRIPT'
import re

# Fix 1: Add test_user fixture to conftest.py if it doesn't exist
with open('tests/conftest.py', 'r') as f:
    conftest_content = f.read()

# Check if test_user fixture exists
if '@pytest.fixture' not in conftest_content or 'def test_user' not in conftest_content:
    # Find the end of file and add the test_user fixture
    new_fixture = '''
@pytest.fixture
def test_user(db_session, app):
    """Create a test user for authentication tests."""
    from app.models import User, UserRole
    user = User(
        email='test@example.com',
        username='testuser',
        first_name='Test',
        last_name='User',
        role=UserRole.RECRUITER
    )
    user.set_password('password123')
    db_session.add(user)
    db_session.commit()
    return user
'''
    conftest_content += new_fixture
    with open('tests/conftest.py', 'w') as f:
        f.write(conftest_content)
    print('✓ Added test_user fixture to conftest.py')
else:
    print('✓ test_user fixture already exists')

ENDSCRIPT
from datetime import datetime
from sqlalchemy import Boolean, DateTime, String, Enum
import enum
from passlib.context import CryptContext

from app.models import db

# Password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRole(enum.Enum):
    """User roles for RBAC."""
    ADMIN = 'admin'
    RECRUITER = 'recruiter'
    CANDIDATE = 'candidate'
    VIEWER = 'viewer'


class User(db.Model):
    """User model for authentication."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(String(120), unique=True, nullable=False, index=True)
    email = db.Column(String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(String(255), nullable=False)
    first_name = db.Column(String(120))
    last_name = db.Column(String(120))
    role = db.Column(Enum(UserRole), default=UserRole.VIEWER, nullable=False)
    is_active = db.Column(Boolean, default=True, nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    candidates = db.relationship('Candidate', backref='recruiter', lazy=True, foreign_keys='Candidate.recruiter_id')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role.value,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
        }
    def set_password(self, password: str) -> None:
        """Hash and set password."""
        # Truncate password to 72 bytes (bcrypt limit)
        if len(password) > 72:
            password = password[:72]
        self.password_hash = pwd_context.hash(password)

    def check_password(self, password: str) -> bool:
        """Verify password against hash."""
        return pwd_context.verify(password, self.password_hash)

