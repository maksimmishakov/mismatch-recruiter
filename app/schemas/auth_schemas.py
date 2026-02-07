"""Authentication validation schemas."""
from marshmallow import Schema, fields, validate

class RegisterSchema(Schema):
    """Schema for user registration."""
    email = fields.Email(required=True)
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8, max=128)
    )
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=50)
    )

class LoginSchema(Schema):
    """Schema for user login."""
    email = fields.Email(required=True)
    password = fields.Str(required=True)
