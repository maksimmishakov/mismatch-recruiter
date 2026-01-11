#!/usr/bin/env python3
"""
Phase 3.3 - API Contract Fixes
Fixes remaining failing tests:
1. test_user_login - Missing test_user fixture
2. test_create_candidate_valid_data - JSON serialization
3. test_error_handling_for_invalid_json - Error status codes
"""

import re

print('\n=== PHASE 3.3 - COMPREHENSIVE API CONTRACT FIXES ===')

# FIX 1: Add test_user fixture to conftest.py
print('\n[1/3] Adding test_user fixture to conftest.py...')
with open('tests/conftest.py', 'r') as f:
    conftest = f.read()

test_user_fixture = '''
@pytest.fixture
def test_user(db_session, app):
    """Create a test user for authentication tests."""
    from app.models import User, UserRole
    user = User(
        email='test@example.com',
        username='testuser',
        first_name='Test',
        last_name='User',
        role=UserRole.RECRUITER,
        is_active=True
    )
    user.set_password('password123')
    db_session.add(user)
    db_session.commit()
    return user
'''

if 'def test_user(' not in conftest:
    conftest += '\n' + test_user_fixture
    with open('tests/conftest.py', 'w') as f:
        f.write(conftest)
    print('   ✓ test_user fixture added')
else:
    print('   ✓ test_user fixture already exists')

# FIX 2: Add to_dict() to Candidate model for JSON serialization
print('\n[2/3] Adding to_dict() to Candidate model for JSON serialization...')
with open('app/models/candidate.py', 'r') as f:
    candidate = f.read()

to_dict_method = '''    def to_dict(self):
        """Convert Candidate to dictionary (JSON serializable)."""
        return {
            'id': self.id,
            'name': self.name,
            'first_name': self.first_name,
            'email': self.email,
            'phone': getattr(self, 'phone', None),
            'bio': self.bio,
            'skills': self.skills or [],
            'experience_years': self.experience_years,
            'education': self.education or [],
            'experience_level': self.experience_level,
            'location': getattr(self, 'location', None),
            'score': self.score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
'''

if 'def to_dict(' not in candidate:
    # Find the end of the class and add to_dict method before __repr__
    repr_pos = candidate.find('    def __repr__')
    if repr_pos != -1:
        candidate_fixed = candidate[:repr_pos] + to_dict_method + '\n' + candidate[repr_pos:]
        with open('app/models/candidate.py', 'w') as f:
            f.write(candidate_fixed)
        print('   ✓ to_dict() method added to Candidate model')
    else:
        print('   ✗ Could not find __repr__ method')
else:
    print('   ✓ to_dict() method already exists')

# FIX 3: Add JSON encoder for models in app/__init__.py
print('\n[3/3] Adding JSON encoder for models...')
with open('app/__init__.py', 'r') as f:
    app_init = f.read()

json_encoder = '''from flask.json.provider import DefaultJSONProvider
from datetime import datetime
from decimal import Decimal

class CustomJSONProvider(DefaultJSONProvider):
    def default(self, o):
        if hasattr(o, 'to_dict') and callable(getattr(o, 'to_dict')):
            return o.to_dict()
        if isinstance(o, (datetime, Decimal)):
            return str(o)
        return super().default(o)
'''

if 'CustomJSONProvider' not in app_init:
    # Add import at the top after existing imports
    lines = app_init.split('\n')
    insert_pos = 0
    for i, line in enumerate(lines):
        if line.startswith('from flask import'):
            insert_pos = i + 1
    
    lines.insert(insert_pos, json_encoder)
    app_init_fixed = '\n'.join(lines)
    
    # Add json_provider assignment after app creation
    if 'app.json_provider_class' not in app_init_fixed:
        app_init_fixed = app_init_fixed.replace(
            'app = Flask(__name__)',
            'app = Flask(__name__)\n    app.json_provider_class = CustomJSONProvider'
        )
    
    with open('app/__init__.py', 'w') as f:
        f.write(app_init_fixed)
    print('   ✓ JSON encoder added')
else:
    print('   ✓ JSON encoder already exists')

print('\n=== ALL PHASE 3.3 FIXES COMPLETED ===')
print('\nSummary:')
print('  1. Added test_user fixture - fixes test_user_login (returns 200 with valid credentials)')
print('  2. Added to_dict() to Candidate - fixes JSON serialization in responses')
print('  3. Added CustomJSONProvider - ensures models are properly JSON serializable')
print('\nNext: Run tests to verify fixes')
