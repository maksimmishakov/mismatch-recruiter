# MisMatch Recruiter - API Documentation

## Base URL
```
http://localhost:5000/api
```

## Health Check

### GET /health
Check if API is running.

**Response:**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "timestamp": "2026-01-08T09:00:00Z"
}
```

## Authentication

All protected endpoints require JWT token in Authorization header:
```
Authorization: Bearer <jwt_token>
```

### POST /auth/register
Register new user.

**Request:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}
```

**Response:** 201 Created
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "created_at": "2026-01-08T09:00:00Z"
}
```

### POST /auth/login
Login user.

**Request:**
```json
{
  "username": "john_doe",
  "password": "SecurePass123!"
}
```

**Response:** 200 OK
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

## Candidates

### GET /candidates
Get list of candidates with pagination.

**Query Parameters:**
- `page` (int, default: 1)
- `per_page` (int, default: 20)
- `status` (string): "active", "hired", "rejected"

**Response:** 200 OK
```json
{
  "candidates": [
    {
      "id": 1,
      "name": "Jane Smith",
      "email": "jane@example.com",
      "phone": "+1234567890",
      "skills": ["Python", "React"],
      "experience_years": 5,
      "current_position": "Senior Developer",
      "status": "active"
    }
  ],
  "total": 100,
  "pages": 5,
  "current_page": 1
}
```

### POST /candidates
Create new candidate.

**Request:**
```json
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "+1234567890",
  "skills": ["Python", "React"],
  "experience_years": 5,
  "current_position": "Senior Developer"
}
```

**Response:** 201 Created
```json
{
  "id": 1,
  "name": "Jane Smith",
  "email": "jane@example.com",
  "status": "active",
  "created_at": "2026-01-08T09:00:00Z"
}
```

### GET /candidates/{id}
Get candidate by ID.

**Response:** 200 OK (or 404 Not Found)

## Jobs

### GET /jobs
Get list of job postings.

**Query Parameters:**
- `page` (int, default: 1)
- `per_page` (int, default: 20)
- `status` (string): "open", "closed", "filled"

**Response:** 200 OK
```json
{
  "jobs": [
    {
      "id": 1,
      "title": "Senior Backend Engineer",
      "description": "We are looking for...",
      "required_skills": ["Python", "PostgreSQL"],
      "required_experience": 5,
      "salary_min": 150000,
      "salary_max": 200000,
      "location": "Moscow",
      "company": "TechCorp",
      "status": "open"
    }
  ],
  "total": 50,
  "pages": 3,
  "current_page": 1
}
```

### POST /jobs
Create new job posting.

**Request:**
```json
{
  "title": "Senior Backend Engineer",
  "description": "We are looking for...",
  "required_skills": ["Python", "PostgreSQL"],
  "required_experience": 5,
  "salary_min": 150000,
  "salary_max": 200000,
  "location": "Moscow",
  "company": "TechCorp"
}
```

**Response:** 201 Created

## Matches

### GET /matches
Get list of candidate-job matches.

**Response:** 200 OK
```json
{
  "matches": [
    {
      "id": 1,
      "candidate_id": 1,
      "job_id": 5,
      "match_score": 0.92,
      "status": "pending",
      "reason": "Strong technical match. Experience aligns well.",
      "created_at": "2026-01-08T09:00:00Z"
    }
  ]
}
```

### POST /matches
Create new match.

**Request:**
```json
{
  "candidate_id": 1,
  "job_id": 5
}
```

**Response:** 201 Created

## Error Responses

All error responses follow this format:
```json
{
  "error": "Error title",
  "message": "Detailed error message",
  "code": "ERROR_CODE"
}
```

### Common Status Codes
- 200: OK
- 201: Created
- 400: Bad Request (validation error)
- 401: Unauthorized (missing/invalid token)
- 403: Forbidden (insufficient permissions)
- 404: Not Found
- 429: Too Many Requests (rate limited)
- 500: Internal Server Error

## Rate Limiting

API endpoints are rate limited:
- 200 requests per day
- 50 requests per hour
- Special limit on /auth endpoints: 5 requests per hour

## Example Usage

### Register and Login
```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "full_name": "John Doe"
  }'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePass123!"
  }'
```

### Get Candidates
```bash
curl -X GET http://localhost:5000/api/candidates?page=1&per_page=20
```

### Create Candidate
```bash
curl -X POST http://localhost:5000/api/candidates \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "skills": ["Python", "React"],
    "experience_years": 5
  }'
```

