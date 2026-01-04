from marshmallow import Schema, fields, validate
from enum import Enum

class UserRoleEnum(str, Enum):
    ADMIN = 'admin'
    RECRUITER = 'recruiter'
    CANDIDATE = 'candidate'

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=255))
    email = fields.Email(required=True)
    role = fields.Str(validate=validate.OneOf(['admin', 'recruiter', 'candidate']))
    is_active = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class CandidateSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    phone = fields.Str(allow_none=True)
    location = fields.Str(allow_none=True)
    bio = fields.Str(allow_none=True)
    resume_url = fields.Str(allow_none=True)
    is_verified = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class JobSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    description = fields.Str(required=True)
    company = fields.Str(required=True)
    location = fields.Str(required=True)
    salary_min = fields.Int(allow_none=True)
    salary_max = fields.Int(allow_none=True)
    job_type = fields.Str(required=True, validate=validate.OneOf(['full-time', 'part-time', 'contract']))
    required_skills = fields.List(fields.Str())
    is_active = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class MatchSchema(Schema):
    id = fields.Int(dump_only=True)
    candidate_id = fields.Int(required=True)
    job_id = fields.Int(required=True)
    match_score = fields.Float(required=True, validate=validate.Range(min=0, max=100))
    matched_skills = fields.List(fields.Str())
    matched_at = fields.DateTime(dump_only=True)

class ApplicationSchema(Schema):
    id = fields.Int(dump_only=True)
    candidate_id = fields.Int(required=True)
    job_id = fields.Int(required=True)
    status = fields.Str(validate=validate.OneOf(['pending', 'accepted', 'rejected']))
    applied_at = fields.DateTime(dump_only=True)
    reviewed_at = fields.DateTime(allow_none=True)
