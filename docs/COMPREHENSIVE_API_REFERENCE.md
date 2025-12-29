# Mismatch AI Recruiter - Comprehensive API Reference

## Overview
This document provides complete API documentation for the Mismatch AI Recruiter platform, including all endpoints, request/response formats, authentication, and error handling.

## Base URL
```
Production: https://api.Mismatch-recruiter.com/v1
Staging: https://staging-api.Mismatch-recruiter.com/v1
Local: http://localhost:5000/api/v1
```

## Authentication

### JWT Bearer Token
All API requests require authentication using JWT bearer tokens.

**Header Format:**
```
Authorization: Bearer <jwt_token>
```

### Obtaining a Token
**Endpoint:** `POST /auth/login`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "usr_123",
    "email": "user@example.com",
    "role": "recruiter"
  }
}
```

---

## Candidates API

### 1. Create Candidate
**Endpoint:** `POST /candidates`
**Authentication:** Required (Recruiter role)

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "+1-555-0100",
  "position_id": "pos_123",
  "source": "linkedin",
  "resume_url": "https://example.com/resume.pdf"
}
```

**Response (201 Created):**
```json
{
  "id": "cand_456",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "+1-555-0100",
  "position_id": "pos_123",
  "source": "linkedin",
  "status": "initial_screening",
  "score": 0,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### 2. Get Candidate
**Endpoint:** `GET /candidates/{candidate_id}`
**Authentication:** Required

**Response (200 OK):**
```json
{
  "id": "cand_456",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "+1-555-0100",
  "position_id": "pos_123",
  "status": "initial_screening",
  "score": 85,
  "skills": ["Python", "Flask", "PostgreSQL"],
  "experience_years": 5,
  "education": {
    "degree": "Bachelor's",
    "field": "Computer Science",
    "institution": "MIT"
  },
  "resume_data": {...},
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### 3. List Candidates
**Endpoint:** `GET /candidates`
**Authentication:** Required

**Query Parameters:**
- `position_id` (optional): Filter by position
- `status` (optional): Filter by status (initial_screening, phone_screen, interview, offer, rejected)
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 20, max: 100)
- `sort` (optional): Sort field (score, created_at, updated_at)
- `order` (optional): asc or desc

**Response (200 OK):**
```json
{
  "data": [...],
  "pagination": {
    "total": 150,
    "page": 1,
    "limit": 20,
    "total_pages": 8
  }
}
```

### 4. Update Candidate
**Endpoint:** `PATCH /candidates/{candidate_id}`
**Authentication:** Required

**Request Body:**
```json
{
  "status": "phone_screen",
  "notes": "Great technical skills"
}
```

**Response (200 OK):**
```json
{
  "id": "cand_456",
  "status": "phone_screen",
  "notes": "Great technical skills",
  "updated_at": "2024-01-16T14:20:00Z"
}
```

---

## Resume Parsing API

### 1. Upload and Parse Resume
**Endpoint:** `POST /resumes/parse`
**Authentication:** Required
**Content-Type:** multipart/form-data

**Request:**
- File: Resume (PDF, DOCX, or DOC)
- candidate_id (optional): Link to existing candidate

**Response (200 OK):**
```json
{
  "resume_id": "res_789",
  "candidate_id": "cand_456",
  "parsed_data": {
    "personal_info": {
      "name": "John Doe",
      "email": "john.doe@example.com",
      "phone": "+1-555-0100"
    },
    "experience": [
      {
        "company": "Tech Corp",
        "position": "Senior Developer",
        "duration": "2 years",
        "description": "..."
      }
    ],
    "education": [
      {
        "institution": "MIT",
        "degree": "Bachelor's",
        "field": "Computer Science",
        "graduation_year": 2018
      }
    ],
    "skills": ["Python", "Flask", "PostgreSQL", "Docker"],
    "certifications": [...],
    "languages": ["English", "Spanish"]
  },
  "parsing_confidence": 0.95,
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

## Candidate Scoring API

### 1. Calculate Candidate Score
**Endpoint:** `POST /candidates/{candidate_id}/score`
**Authentication:** Required

**Request Body:**
```json
{
  "position_id": "pos_123",
  "criteria": {
    "required_skills": ["Python", "PostgreSQL"],
    "preferred_skills": ["Docker", "Kubernetes"],
    "min_experience_years": 3,
    "education_requirement": "Bachelor's"
  }
}
```

**Response (200 OK):**
```json
{
  "candidate_id": "cand_456",
  "position_id": "pos_123",
  "overall_score": 87,
  "skill_match": 90,
  "experience_match": 85,
  "education_match": 80,
  "cultural_fit": 88,
  "recommendation": "RECOMMEND",
  "reasoning": "Strong technical skills, excellent experience, good cultural alignment",
  "calculated_at": "2024-01-15T10:45:00Z"
}
```

---

## Interview Questions API

### 1. Generate Interview Questions
**Endpoint:** `POST /interviews/generate-questions`
**Authentication:** Required

**Request Body:**
```json
{
  "candidate_id": "cand_456",
  "position_id": "pos_123",
  "question_count": 5,
  "difficulty_level": "intermediate",
  "focus_areas": ["technical_skills", "problem_solving", "communication"]
}
```

**Response (200 OK):**
```json
{
  "interview_id": "int_234",
  "candidate_id": "cand_456",
  "position_id": "pos_123",
  "questions": [
    {
      "id": "q_1",
      "question": "Describe your experience with Python async/await patterns",
      "category": "technical_skills",
      "difficulty": "intermediate",
      "estimated_duration_minutes": 5
    },
    {
      "id": "q_2",
      "question": "Tell us about a challenging project you led",
      "category": "problem_solving",
      "difficulty": "intermediate",
      "estimated_duration_minutes": 8
    }
  ],
  "generated_at": "2024-01-15T11:00:00Z"
}
```

### 2. Get Interview Questions
**Endpoint:** `GET /interviews/{interview_id}/questions`
**Authentication:** Required

**Response (200 OK):**
```json
{
  "interview_id": "int_234",
  "questions": [...],
  "total_questions": 5,
  "total_estimated_duration_minutes": 30
}
```

---

## Error Handling

### Error Response Format
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid request parameters",
    "details": [
      {
        "field": "email",
        "message": "Email format is invalid"
      }
    ],
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### HTTP Status Codes
- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `204 No Content` - Successful request with no content
- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Authentication required or failed
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

---

## Rate Limiting

- **Limit:** 1000 requests per hour per API key
- **Headers:** 
  - `X-RateLimit-Limit: 1000`
  - `X-RateLimit-Remaining: 999`
  - `X-RateLimit-Reset: 1610695200`

---

## Pagination

All list endpoints support pagination with these parameters:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)

**Response format:**
```json
{
  "data": [...],
  "pagination": {
    "total": 150,
    "page": 1,
    "limit": 20,
    "total_pages": 8
  }
}
```

---

## Webhooks

### Supported Events
- `candidate.created`
- `candidate.updated`
- `candidate.scored`
- `interview.questions_generated`
- `interview.scheduled`
- `interview.completed`

**Webhook Payload:**
```json
{
  "event_type": "candidate.scored",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {...}
}
```

---

## SDKs and Libraries

- **Python:** `pip install Mismatch-recruiter`
- **JavaScript/Node.js:** `npm install @Mismatch/recruiter-sdk`
- **Go:** `go get github.com/Mismatch/recruiter-go`

---

## Support & Resources

- **Documentation:** https://docs.Mismatch-recruiter.com
- **API Status:** https://status.Mismatch-recruiter.com
- **Support Email:** api-support@Mismatch-recruiter.com
- **GitHub Issues:** https://github.com/Mismatch/recruiter-api/issues
