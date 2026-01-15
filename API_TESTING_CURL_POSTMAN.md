# API Testing Guide: curl & Postman Examples

## Overview

This document provides comprehensive examples for testing all API endpoints in the MisMatch Recruiter application using curl and Postman.

## Prerequisites

- Application running on `http://localhost:5000`
- curl installed on your system
- Postman installed (or use Postman online)
- Sample candidate and job data in database

## Base URL

```
http://localhost:5000
```

## Phase 2: ML Matching Endpoints

### 1. Calculate Match Score

**Endpoint:** `POST /api/matches/calculate-score`

**Description:** Calculate ML match score between a candidate and a job.

#### curl Example:
```bash
curl -X POST http://localhost:5000/api/matches/calculate-score \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "job_id": 1,
    "skills": ["Python", "JavaScript", "React"],
    "experience_years": 5,
    "location": "San Francisco",
    "salary_expectation": 120000,
    "required_skills": ["Python", "JavaScript"],
    "experience_required": 3,
    "job_location": "San Francisco",
    "salary_range": {"min": 100000, "max": 150000}
  }'
```

**Expected Response (200 OK):**
```json
{
  "overall_score": 85,
  "breakdown": {
    "skills": 90,
    "experience": 80,
    "location": 100,
    "salary": 75
  },
  "quality": "excellent",
  "recommendations": [
    "Strong technical skills match",
    "Excellent location fit",
    "Consider negotiating on salary"
  ]
}
```

#### Postman Configuration:
- **Method:** POST
- **URL:** `http://localhost:5000/api/matches/calculate-score`
- **Headers:** Content-Type: application/json
- **Body:** JSON (raw)

---

### 2. Get All Matches

**Endpoint:** `GET /api/matches`

**Description:** Retrieve all matches with optional filtering and sorting.

#### curl Example:
```bash
curl -X GET "http://localhost:5000/api/matches?min_score=50&status=pending&sort_by=score_desc" \
  -H "Content-Type: application/json"
```

**Query Parameters:**
- `min_score` (optional): Minimum match score (0-100)
- `status` (optional): Filter by status (pending, viewed, applied, rejected, hired)
- `sort_by` (optional): Sort order (score_desc, score_asc, recent, oldest)

**Expected Response (200 OK):**
```json
{
  "matches": [
    {
      "id": 1,
      "candidate_id": 1,
      "job_id": 1,
      "overall_score": 85,
      "score_breakdown": {
        "skills": 90,
        "experience": 80,
        "location": 100,
        "salary": 75
      },
      "status": "pending",
      "created_at": "2024-01-15T18:00:00Z"
    }
  ],
  "total": 1,
  "page": 1
}
```

#### Postman Configuration:
- **Method:** GET
- **URL:** `http://localhost:5000/api/matches`
- **Params:** Add query parameters via Params tab

---

### 3. Get Match Details

**Endpoint:** `GET /api/matches/{id}`

**Description:** Get detailed information about a specific match.

#### curl Example:
```bash
curl -X GET http://localhost:5000/api/matches/1 \
  -H "Content-Type: application/json"
```

**Expected Response (200 OK):**
```json
{
  "match": {
    "id": 1,
    "candidate": {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "experience_years": 5,
      "location": "San Francisco"
    },
    "job": {
      "id": 1,
      "title": "Senior Python Developer",
      "location": "San Francisco",
      "salary_min": 100000,
      "salary_max": 150000
    },
    "overall_score": 85,
    "score_breakdown": {
      "skills": 90,
      "experience": 80,
      "location": 100,
      "salary": 75
    },
    "status": "pending",
    "created_at": "2024-01-15T18:00:00Z"
  }
}
```

---

### 4. Update Match Status

**Endpoint:** `PUT /api/matches/{id}`

**Description:** Update the status of a match.

#### curl Example:
```bash
curl -X PUT http://localhost:5000/api/matches/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "viewed"
  }'
```

**Valid Status Values:** pending, viewed, applied, rejected, hired

**Expected Response (200 OK):**
```json
{
  "match": {
    "id": 1,
    "status": "viewed",
    "updated_at": "2024-01-15T18:05:00Z"
  }
}
```

---

## Phase 4: Email Notification Endpoints

### 5. Send Match Notification Email

**Endpoint:** `POST /api/notifications/send-match`

**Description:** Send match notification email to candidate (async via Celery).

#### curl Example:
```bash
curl -X POST http://localhost:5000/api/notifications/send-match \
  -H "Content-Type: application/json" \
  -d '{
    "match_id": 1,
    "candidate_email": "john@example.com",
    "candidate_name": "John Doe",
    "job_title": "Senior Python Developer",
    "match_score": 85,
    "breakdown": {
      "skills": 90,
      "experience": 80,
      "location": 100,
      "salary": 75
    }
  }'
```

**Expected Response (202 Accepted):**
```json
{
  "task_id": "abc123def456",
  "status": "queued",
  "message": "Email notification queued for sending"
}
```

---

### 6. Schedule Interview

**Endpoint:** `POST /api/interviews/schedule`

**Description:** Schedule an interview between candidate and hiring manager.

#### curl Example:
```bash
curl -X POST http://localhost:5000/api/interviews/schedule \
  -H "Content-Type: application/json" \
  -d '{
    "match_id": 1,
    "candidate_id": 1,
    "job_id": 1,
    "interview_date": "2024-02-15",
    "interview_time": "10:00",
    "interviewer_email": "hiring@example.com",
    "interviewer_name": "Jane Smith"
  }'
```

**Expected Response (201 Created):**
```json
{
  "interview": {
    "id": 1,
    "match_id": 1,
    "scheduled_date": "2024-02-15",
    "scheduled_time": "10:00",
    "status": "scheduled",
    "created_at": "2024-01-15T18:00:00Z"
  },
  "message": "Interview scheduled and confirmation email sent"
}
```

---

## Testing Workflow Examples

### Complete Recruitment Flow Test

```bash
# Step 1: Calculate match score
MATCH_RESPONSE=$(curl -s -X POST http://localhost:5000/api/matches/calculate-score \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "job_id": 1
  }')

echo "Match Score Response: $MATCH_RESPONSE"

# Step 2: Get match ID from response and verify score
MATCH_ID=$(echo $MATCH_RESPONSE | grep -o '"id": [0-9]*' | head -1 | grep -o '[0-9]*')
echo "Match ID: $MATCH_ID"

# Step 3: Get match details
curl -X GET http://localhost:5000/api/matches/$MATCH_ID \
  -H "Content-Type: application/json"

# Step 4: Update match status to viewed
curl -X PUT http://localhost:5000/api/matches/$MATCH_ID \
  -H "Content-Type: application/json" \
  -d '{"status": "viewed"}'

# Step 5: Send notification email
curl -X POST http://localhost:5000/api/notifications/send-match \
  -H "Content-Type: application/json" \
  -d '{"match_id": '$MATCH_ID'}'

# Step 6: Schedule interview
curl -X POST http://localhost:5000/api/interviews/schedule \
  -H "Content-Type: application/json" \
  -d '{
    "match_id": '$MATCH_ID',
    "interview_date": "2024-02-20",
    "interview_time": "14:00",
    "interviewer_email": "manager@example.com"
  }'
```

---

## Error Handling Examples

### 400 Bad Request - Invalid Input
```bash
curl -X POST http://localhost:5000/api/matches/calculate-score \
  -H "Content-Type: application/json" \
  -d '{"invalid_field": "value"}'
```

**Expected Response (400):**
```json
{
  "error": "Invalid request data",
  "details": "Missing required field: candidate_id"
}
```

### 404 Not Found - Resource doesn't exist
```bash
curl -X GET http://localhost:5000/api/matches/9999
```

**Expected Response (404):**
```json
{
  "error": "Match not found",
  "match_id": 9999
}
```

### 500 Internal Server Error
```bash
curl -X POST http://localhost:5000/api/matches/calculate-score \
  -H "Content-Type: application/json" \
  -d '{"candidate_id": 1, "job_id": 1}' \
  -v  # verbose mode to see detailed response
```

---

## Postman Collection Import

1. **Download Postman Collection:**
   - File: `postman_collection.json`
   - Location: `/docs/postman_collection.json`

2. **Import Steps:**
   - Open Postman
   - Click "Import"
   - Select file or paste raw JSON
   - Collection will be imported with all endpoints

3. **Set Environment Variables:**
   - Base URL: `{{base_url}}` = `http://localhost:5000`
   - Headers automatically configured

---

## Performance Testing

### Load Testing with Apache Bench

```bash
# Test 1000 requests with 10 concurrent connections
ab -n 1000 -c 10 http://localhost:5000/api/matches
```

### Test Celery Async Tasks

```bash
# Send 100 match notifications in parallel
for i in {1..100}; do
  curl -X POST http://localhost:5000/api/notifications/send-match \
    -H "Content-Type: application/json" \
    -d '{"match_id": '$i'}' &
done
wait
```

---

## Troubleshooting

### Issue: Connection Refused
```
curl: (7) Failed to connect to localhost:5000
```
**Solution:** Ensure Flask application is running on port 5000

### Issue: CORS Error
```json
{"error": "CORS policy error"}
```
**Solution:** Check CORS configuration in app/config.py

### Issue: Missing Database
```json
{"error": "Database connection failed"}
```
**Solution:** Run database migrations: `flask db upgrade`

---

## Additional Resources

- [API Documentation](docs/API_DOCUMENTATION.md)
- [Phase 2 ML Matching](docs/PHASE_2_ML_MATCHING_IMPLEMENTATION.md)
- [Phase 4 Advanced Features](docs/PHASE_4_ADVANCED_FEATURES.md)
- [Curl Manual](https://curl.se/docs/manpage.html)
- [Postman Documentation](https://learning.postman.com/docs/getting-started/introduction/)
