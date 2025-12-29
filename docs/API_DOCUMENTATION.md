# API Documentation

## Overview
Comprehensive API specification for the MisMatch Recruitment Bot system.

## Base URL
```
https://Mismatch-recruiter-maksmisakov.amvera.io/api
```

## Authentication
All endpoints require Bearer token authentication in the Authorization header:
```
Authorization: Bearer <token>
```

## Endpoints

### 1. Health Check
**Endpoint:** `GET /health`

**Description:** Checks the health status of the API

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0"
}
```

### 2. Generate Interview Questions
**Endpoint:** `POST /generate-interview-questions`

**Description:** Generates interview questions using GPT-4o-mini based on job description and candidate profile

**Request Body:**
```json
{
  "job_description": "Senior Python Developer with 5+ years experience",
  "candidate_profile": "John Doe - 4 years Python, FastAPI, PostgreSQL",
  "num_questions": 5,
  "difficulty_level": "senior"
}
```

**Response:**
```json
{
  "questions": [
    {
      "id": 1,
      "question": "How would you design a scalable microservices architecture?",
      "difficulty": "senior",
      "category": "system_design",
      "hints": ["Consider database partitioning", "Think about caching strategies"]
    },
    {
      "id": 2,
      "question": "Explain your experience with async/await in Python",
      "difficulty": "senior",
      "category": "technical_knowledge",
      "hints": ["Event loops", "Coroutines"]
    }
  ],
  "generated_at": "2024-01-15T10:30:00Z",
  "model": "gpt-4o-mini"
}
```

**Status Codes:**
- `200 OK`: Successfully generated questions
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid authentication
- `500 Internal Server Error`: Server error during generation

### 3. Evaluate Candidate
**Endpoint:** `POST /evaluate-candidate`

**Description:** Evaluates candidate responses using AI

**Request Body:**
```json
{
  "candidate_id": "cand_12345",
  "interview_id": "int_67890",
  "responses": [
    {
      "question_id": 1,
      "response": "I would use microservices with load balancing..."
    }
  ]
}
```

**Response:**
```json
{
  "evaluation_id": "eval_11111",
  "candidate_id": "cand_12345",
  "scores": {
    "technical_knowledge": 8.5,
    "communication": 7.8,
    "problem_solving": 8.9,
    "overall_score": 8.4
  },
  "feedback": "Strong technical foundation with excellent system design thinking",
  "recommendation": "PASS"
}
```

## Error Handling

All errors follow this format:
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Description of the error",
    "details": {}
  }
}
```

## Rate Limiting
- **Default:** 1000 requests/hour per API key
- **Headers:** `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## Data Models

### Candidate
```json
{
  "id": "string",
  "name": "string",
  "email": "string",
  "experience_years": "integer",
  "skills": ["string"],
  "created_at": "ISO 8601 timestamp"
}
```

### Question
```json
{
  "id": "integer",
  "content": "string",
  "difficulty": "enum: easy, medium, senior",
  "category": "string",
  "tags": ["string"]
}
```

## Integration Examples

### Python (FastAPI)
```python
import httpx

async def generate_questions():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://Mismatch-recruiter-maksmisakov.amvera.io/api/generate-interview-questions",
            headers={"Authorization": f"Bearer {token}"},
            json={"job_description": "...", "candidate_profile": "..."}
        )
        return response.json()
```

### JavaScript
```javascript
fetch('https://Mismatch-recruiter-maksmisakov.amvera.io/api/generate-interview-questions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({job_description: '...', candidate_profile: '...'})
}).then(res => res.json())
```

## Changelog

### v1.0.0 (2024-01-15)
- Initial API release
- Interview question generation
- Candidate evaluation endpoints
- Redis caching integration

## Support
For API support, contact: api-support@Mismatch.ru
