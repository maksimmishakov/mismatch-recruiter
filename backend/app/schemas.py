# Pydantic schemas for request/response validation
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# ============== AUTH SCHEMAS ==============
class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    username: str = Field(..., min_length=3)
    full_name: Optional[str] = None

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    access_token: str
    user: UserResponse

# ============== CANDIDATE SCHEMAS ==============
class CandidateCreateRequest(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None
    portfolio_url: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    skills: Optional[List[str]] = None
    experience_years: Optional[int] = Field(None, ge=0)
    salary_expectation: Optional[float] = Field(None, gt=0)

class CandidateResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None
    portfolio_url: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    skills: Optional[List[str]] = None
    experience_years: Optional[int] = None
    salary_expectation: Optional[float] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ============== JOB SCHEMAS ==============
class JobCreateRequest(BaseModel):
    title: str = Field(..., min_length=1)
    description: str
    location: Optional[str] = None
    salary_min: Optional[float] = Field(None, gt=0)
    salary_max: Optional[float] = Field(None, gt=0)
    required_skills: Optional[List[str]] = None
    experience_required: Optional[int] = Field(None, ge=0)
    job_type: Optional[str] = None

class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    location: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    required_skills: Optional[List[str]] = None
    experience_required: Optional[int] = None
    job_type: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ============== MATCH SCHEMAS ==============
class MatchCreateRequest(BaseModel):
    candidate_id: int
    job_id: int

class MatchResponse(BaseModel):
    id: int
    candidate_id: int
    job_id: int
    match_score: float
    skill_match: float
    experience_match: float
    salary_match: float
    location_match: float
    status: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class MatchDetailResponse(MatchResponse):
    candidate: Optional[CandidateResponse] = None
    job: Optional[JobResponse] = None
