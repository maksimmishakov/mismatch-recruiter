# MisMatch Recruiter API Documentation

## Base URL
- Development: `http://localhost:5000`
- Staging: `https://mismatch-staging.amvera.io`
- Production: `https://api.mismatch.ru`

## Authentication
All endpoints require `Authorization: Bearer <token>` header (except login/signup)

### POST /api/auth/signup
Create new user account

**Request:**
```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "name": "John Doe"
}
```

**Response (201):**
```json
{
  "user_id": 1,
  "email": "user@example.com",
  "access_token": "eyJhbGci..."
}
```

### POST /api/auth/login
Authenticate user

**Request:**
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGci...",
  "user_id": 1,
  "email": "user@example.com"
}
```

### GET /api/candidates
List all candidates

**Response (200):**
```json
{
  "candidates": [
    {
      "id": 1,
      "name": "Alice",
      "email": "alice@example.com",
      "experience_years": 5,
      "skills": ["Python", "React"],
      "created_at": "2026-01-11T10:00:00"
    }
  ]
}
```

### POST /api/candidates
Create candidate

**Request:**
```json
{
  "name": "Bob",
  "email": "bob@example.com",
  "experience_years": 3,
  "skills": ["Go", "PostgreSQL"],
  "languages": ["Russian", "English"]
}
```

**Response (201):**
```json
{
  "id": 2,
  "name": "Bob",
  "email": "bob@example.com",
  "experience_years": 3,
  "skills": ["Go", "PostgreSQL"],
  "created_at": "2026-01-11T10:00:00"
}
```

### GET /api/jobs
List all job postings

**Response (200):**
```json
{
  "jobs": [
    {
      "id": 1,
      "title": "Senior Python Developer",
      "description": "Looking for experienced Python dev",
      "required_skills": ["Python", "Django", "PostgreSQL"],
      "salary_range": "200k-300k RUB",
      "location": "Moscow",
      "created_at": "2026-01-11T10:00:00"
    }
  ]
}
```

### POST /api/jobs
Create job posting

**Request:**
```json
{
  "title": "Senior Python Developer",
  "description": "Looking for experienced Python dev",
  "required_skills": ["Python", "Django", "PostgreSQL"],
  "salary_range": "200k-300k RUB",
  "location": "Moscow"
}
```

**Response (201):**
```json
{
  "id": 1,
  "title": "Senior Python Developer",
  "description": "Looking for experienced Python dev",
  "required_skills": ["Python", "Django", "PostgreSQL"],
  "salary_range": "200k-300k RUB",
  "location": "Moscow",
  "created_at": "2026-01-11T10:00:00"
}
```

### POST /api/jobs/{job_id}/match
Run matching algorithm

**Response (200):**
```json
{
  "job_id": 1,
  "matches": [
    {
      "id": 1,
      "candidate_id": 1,
      "match_score": 0.95,
      "reasoning": "Has all required skills and 5 years experience",
      "status": "pending",
      "matched_at": "2026-01-11T10:00:00"
    }
  ]
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Bad Request",
  "message": "Missing required field: email"
}
```

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing token"
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "Resource not found"
}
```

### 422 Unprocessable Entity
```json
{
  "error": "Unprocessable Entity",
  "message": "Invalid email format"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "Database connection failed"
}
```

## Rate Limiting
- 100 requests per minute per IP
- Rate limit headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`

## Versioning
- Current API version: 1.0
- All endpoints are prefixed with `/api/v1` for future compatibility
