"""
Input validation schemas for API endpoints
Using marshmallow for data validation and serialization
"""

from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime

class UserCreateSchema(Schema):
    """Validation schema for user creation"""
    email = fields.Email(required=True)
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8, max=128),
        description="Password must be 8-128 characters"
    )
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=50)
    )
    first_name = fields.Str(validate=validate.Length(max=50))
    last_name = fields.Str(validate=validate.Length(max=50))

class UserLoginSchema(Schema):
    """Validation schema for user login"""
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class CandidateQuerySchema(Schema):
    """Validation schema for candidate queries"""
    skill = fields.Str(validate=validate.Length(min=1, max=100))
    experience_min = fields.Int(validate=validate.Range(min=0))
    experience_max = fields.Int(validate=validate.Range(min=0))
    location = fields.Str(validate=validate.Length(max=100))
    salary_min = fields.Int(validate=validate.Range(min=0))
    salary_max = fields.Int(validate=validate.Range(min=0))
    limit = fields.Int(
        validate=validate.Range(min=1, max=100),
        load_default=10
    )
    offset = fields.Int(
        validate=validate.Range(min=0),
        load_default=0
    )

class MatchCreateSchema(Schema):
    """Validation schema for creating matches"""
    candidate_id = fields.Int(required=True)
    job_id = fields.Int(required=True)
    score = fields.Float(validate=validate.Range(min=0, max=100))
    notes = fields.Str(validate=validate.Length(max=1000))

class ValidationManager:
    """Manager for input validation"""
    
    def __init__(self):
        self.user_create_schema = UserCreateSchema()
        self.user_login_schema = UserLoginSchema()
        self.candidate_query_schema = CandidateQuerySchema()
        self.match_create_schema = MatchCreateSchema()
    
    def validate_user_creation(self, data):
        """Validate user creation data"""
        try:
            return self.user_create_schema.load(data)
        except ValidationError as e:
            return None, e.messages
    
    def validate_user_login(self, data):
        """Validate user login data"""
        try:
            return self.user_login_schema.load(data)
        except ValidationError as e:
            return None, e.messages
    
    def validate_candidate_query(self, data):
        """Validate candidate query parameters"""
        try:
            return self.candidate_query_schema.load(data)
        except ValidationError as e:
            return None, e.messages
    
    def validate_match_creation(self, data):
        """Validate match creation data"""
        try:
            return self.match_create_schema.load(data)
        except ValidationError as e:
            return None, e.messages

# Singleton instance
validation_manager = ValidationManager()
