# MisMatch Recruiter - Feedback & Analytics API Documentation

## Overview
This document describes the feedback collection and analytics API endpoints for the MisMatch Recruiter platform.

## Base URL
```
https://api.mismatch-recruiter-prod.amvera.io
```

## Feedback Endpoints

### 1. Submit Feedback
**Endpoint:** `POST /api/feedback/`

**Description:** Submit user feedback with a rating (1-5 stars) and optional comment.

**Request Body:**
```json
{
  "rating": 4,
  "comment": "Great platform! Love the accuracy.",
  "feedback_type": "general",
  "user_id": 123,
  "email": "user@example.com"
}
```

**Parameters:**
- `rating` (required): Integer 1-5
- `comment` (optional): String, max 1000 characters
- `feedback_type` (optional): "bug", "feature", "general", "performance", "ui_ux"
- `user_id` (optional): Integer
- `email` (optional): String

**Response (201 Created):**
```json
{
  "id": 1,
  "rating": 4,
  "type": "general",
  "timestamp": "2026-01-03T20:00:00",
  "message": "Feedback received. Thank you!"
}
```

### 2. Submit Feature Request
**Endpoint:** `POST /api/feedback/feature-request`

**Description:** Submit a feature request.

**Request Body:**
```json
{
  "feature_name": "Mobile App",
  "description": "Native iOS and Android applications",
  "priority": 4,
  "user_id": 123
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "feature": "Mobile App",
  "message": "Feature request recorded. We'll review it soon!"
}
```

### 3. Get Daily Feedback Summary
**Endpoint:** `GET /api/feedback/summary/daily`

**Description:** Get feedback statistics for today.

**Response (200 OK):**
```json
{
  "date": "2026-01-03",
  "total_feedback": 24,
  "average_rating": 4.6,
  "breakdown_by_type": {
    "general": 15,
    "feature": 5,
    "bug": 4
  },
  "satisfaction_level": "Very Satisfied",
  "sample_comments": [
    "Amazing platform!",
    "Great AI accuracy"
  ],
  "recommendation": "Great! Keep up the current direction"
}
```

### 4. Get Weekly Feedback Summary
**Endpoint:** `GET /api/feedback/summary/weekly`

**Description:** Get feedback statistics for the past 7 days.

**Response (200 OK):**
```json
{
  "week": "2025-12-27 to 2026-01-03",
  "total_feedback": 152,
  "average_rating": 4.5,
  "daily_breakdown": {
    "2025-12-27": {"count": 18, "average": 4.4},
    "2025-12-28": {"count": 21, "average": 4.5},
    ...
  },
  "trend": "Improving 📈",
  "satisfaction_level": "Satisfied"
}
```

### 5. Get Top Features
**Endpoint:** `GET /api/feedback/features/top`

**Description:** Get the top 10 most requested features.

**Response (200 OK):**
```json
{
  "timestamp": "2026-01-03T20:00:00",
  "total_unique_features": 23,
  "top_features": [
    {"name": "Mobile App", "requests": 45, "avg_priority": 4.8},
    {"name": "API Integration", "requests": 32, "avg_priority": 4.2},
    {"name": "Video Interview", "requests": 28, "avg_priority": 4.0}
  ]
}
```

### 6. List All Feedback
**Endpoint:** `GET /api/feedback/list`

**Description:** List feedback with pagination.

**Query Parameters:**
- `page` (optional): Integer, default 1
- `per_page` (optional): Integer, default 20
- `days` (optional): Integer, last N days, default 7

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": 1,
      "user_id": 123,
      "rating": 5,
      "comment": "Excellent platform!",
      "feedback_type": "general",
      "email": "user@example.com",
      "created_at": "2026-01-03T20:00:00"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 152,
    "pages": 8
  }
}
```

### 7. List Feature Requests
**Endpoint:** `GET /api/feedback/features/list`

**Description:** List feature requests with filtering.

**Query Parameters:**
- `page` (optional): Integer, default 1
- `per_page` (optional): Integer, default 20
- `status` (optional): "open", "in_progress", "done", "rejected"

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": 1,
      "user_id": 123,
      "feature_name": "Mobile App",
      "description": "Native iOS and Android apps",
      "priority": 5,
      "votes": 45,
      "status": "in_progress",
      "created_at": "2026-01-01T00:00:00"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 23,
    "pages": 2
  }
}
```

### 8. Get Feedback Statistics
**Endpoint:** `GET /api/feedback/stats`

**Description:** Get comprehensive feedback statistics.

**Response (200 OK):**
```json
{
  "total_feedback": 1234,
  "average_rating": 4.6,
  "feedback_by_type": {
    "general": 600,
    "feature": 350,
    "bug": 180,
    "performance": 104
  },
  "ratings_distribution": {
    "1": 15,
    "2": 25,
    "3": 120,
    "4": 450,
    "5": 624
  },
  "timestamp": "2026-01-03T20:00:00"
}
```

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid input
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

**Error Response Format:**
```json
{
  "error": "Description of the error"
}
```

## Rate Limiting
API requests are limited to 1000 requests per hour per IP address.

## Authentication
Currently, the feedback API is open (no authentication required). Authentication may be added in future versions.

## Usage Examples

### Submit Feedback
```bash
curl -X POST https://api.mismatch-recruiter-prod.amvera.io/api/feedback/ \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 4,
    "comment": "Great platform!",
    "feedback_type": "general"
  }'
```

### Get Daily Summary
```bash
curl https://api.mismatch-recruiter-prod.amvera.io/api/feedback/summary/daily
```

### Get Top Features
```bash
curl https://api.mismatch-recruiter-prod.amvera.io/api/feedback/features/top
```

## Database Models

### Feedback Model
```python
class Feedback(db.Model):
    id: Integer (Primary Key)
    user_id: Integer (Foreign Key)
    rating: Integer (1-5)
    comment: Text
    feedback_type: String (bug, feature, general, performance, ui_ux)
    email: String
    created_at: DateTime
    updated_at: DateTime
```

### FeatureRequest Model
```python
class FeatureRequest(db.Model):
    id: Integer (Primary Key)
    user_id: Integer (Foreign Key)
    feature_name: String
    description: Text
    priority: Integer (1-5)
    votes: Integer
    status: String (open, in_progress, done, rejected)
    created_at: DateTime
    updated_at: DateTime
```

## Database Initialization

To initialize the database with feedback tables:

```bash
# Create all tables
python init_db.py init

# Drop all tables (WARNING: destructive)
python init_db.py drop
```

## Version History
- **v1.0** (Jan 3, 2026) - Initial release with feedback collection endpoints

## Support
For API support and questions, contact: support@mismatch-recruiter.io