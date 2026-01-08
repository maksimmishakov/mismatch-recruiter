from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional
from datetime import datetime

# ============== AUTH SCHEMAS ==============

class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    username: str = Field(..., min_length=3, max_length=80)
    full_name: str = Field(..., max_length=200)
    
    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

# ============== CANDIDATE SCHEMAS ==============

class CandidateCreateSchema(BaseModel):
    first_name: str = Field(..., max_length=80)
    last_name: Optional[str] = Field(None, max_length=80)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    location: Optional[str] = Field(None, max_length=120)
    bio: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    experience_years: int = Field(default=0, ge=0, le=100)
    portfolio_url: Optional[str] = None
    salary_expectation: int = Field(default=0, ge=0)

class CandidateUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None
    skills: Optional[List[str]] = None
    experience_years: Optional[int] = None
    portfolio_url: Optional[str] = None
    salary_expectation: Optional[int] = None

# ============== JOB SCHEMAS ==============

class JobCreateSchema(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    company: str = Field(..., max_length=120)
    location: Optional[str] = Field(None, max_length=120)
    salary_min: int = Field(default=0, ge=0)
    salary_max: int = Field(default=0, ge=0)
    required_skills: List[str] = Field(default_factory=list)
    experience_level: str = Field(default='mid')
    job_type: str = Field(default='full-time')

class JobUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    required_skills: Optional[List[str]] = None
    experience_level: Optional[str] = None
    job_type: Optional[str] = None

# ============== MATCH SCHEMAS ==============

class MatchCreateSchema(BaseModel):
    candidate_id: int = Field(..., gt=0)
    job_id: int = Field(..., gt=0)

class MatchUpdateSchema(BaseModel):
    status: str = Field(..., pattern='^(pending|pattern="^(pending|accepted|rejected)$|rejected)$')
