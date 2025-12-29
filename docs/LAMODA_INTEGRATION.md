Mismatch_INTEGRATION.md# Mismatch Integration Guide

## Overview

This document describes the Mismatch job platform integration for the AI Recruiter system. Mismatch is a Russian job marketplace where we source real job listings and candidate profiles for matching and placement.

## Architecture

### Components

1. **API Client** (`app/services/Mismatch_api_client.py`)
   - Handles HTTP requests to Mismatch API
   - Manages HMAC authentication
   - Implements retry logic and error handling
   - Supports job and candidate data retrieval

2. **Routes** (`app/routes/Mismatch.py`)
   - REST API endpoints for Mismatch integration
   - Jobs endpoint: `GET /api/v1/Mismatch/jobs`
   - Candidates endpoint: `GET /api/v1/Mismatch/candidates`
   - Matching endpoint: `POST /api/v1/Mismatch/match`
   - Sync endpoint: `POST /api/v1/Mismatch/sync`
   - Placements endpoint: `POST /api/v1/Mismatch/placements`

3. **Background Tasks** (`app/tasks/Mismatch_sync.py`)
   - Celery tasks for background synchronization
   - Full and incremental sync tasks
   - Scheduled sync with configurable intervals
   - Error handling and retry mechanisms

4. **Database Models** (`app/models/Mismatch.py`)
   - `MismatchJob`: Job listings (19 fields)
   - `MismatchCandidate`: Candidate profiles (15 fields)
   - `MismatchPlacement`: Job-to-candidate placements (9 fields)
   - `MismatchSync`: Sync operation tracking (10 fields)
   - `MismatchIntegrationConfig`: Configuration storage (4 fields)

5. **Configuration** (`app/config/Mismatch.py`)
   - Pydantic settings with 25+ configurable parameters
   - Environment variable support
   - Constants for job statuses, experience levels, etc.
   - Error code mappings

6. **Initialization Service** (`app/services/Mismatch_initialization_service.py`)
   - Manages setup and initialization sequence
   - Database model initialization
   - Configuration storage setup
   - API credentials verification
   - Sync tracking initialization

## Configuration

### Environment Variables

```bash
# API Credentials
Mismatch_API_KEY=your_api_key
Mismatch_API_SECRET=your_api_secret
Mismatch_API_BASE_URL=https://api.Mismatch.ru/v1

# Sync Settings
Mismatch_SYNC_ENABLED=true
Mismatch_SYNC_INTERVAL_HOURS=24
Mismatch_MAX_JOBS_PER_SYNC=1000
Mismatch_MAX_CANDIDATES_PER_SYNC=500

# Request Configuration
Mismatch_REQUEST_TIMEOUT=30
Mismatch_MAX_RETRIES=3
Mismatch_RETRY_BACKOFF=1.5

# Matching Settings
Mismatch_MIN_MATCH_SCORE=0.7
Mismatch_SKILL_WEIGHT=0.4
Mismatch_EXPERIENCE_WEIGHT=0.3
Mismatch_SALARY_WEIGHT=0.3

# Webhook Settings
Mismatch_WEBHOOK_ENABLED=false
Mismatch_WEBHOOK_SECRET=your_webhook_secret
```

## API Usage

### Get Jobs

```bash
GET /api/v1/Mismatch/jobs?location=Moscow&min_salary=100000
```

### Get Candidates

```bash
GET /api/v1/Mismatch/candidates?skills=Python&experience=senior
```

### Match Candidates to Jobs

```bash
POST /api/v1/Mismatch/match
Content-Type: application/json

{
  "candidate_id": "cand-123",
  "job_id": "job-456"
}
```

### Trigger Sync

```bash
POST /api/v1/Mismatch/sync
Content-Type: application/json

{
  "sync_type": "full"
}
```

## Database Schema

### MismatchJob Table
- `id` (Primary Key)
- `Mismatch_id` (Unique, indexed)
- `title`, `company`, `location`
- `salary_min`, `salary_max`, `currency`
- `employment_type`, `experience_level`
- `skills` (JSON)
- `description`, `requirements`, `benefits`
- `external_url`
- `posted_at`, `synced_at`
- `active` (Boolean)

### MismatchCandidate Table
- `id` (Primary Key)
- `Mismatch_id` (Unique, indexed)
- `first_name`, `last_name`
- `email` (indexed), `phone`
- `location`, `title`
- `summary`, `skills` (JSON)
- `experience_years`
- `education`, `languages` (JSON)
- `external_url`
- `available_from`, `synced_at`
- `active` (Boolean)

## Matching Algorithm

Default matching weights:
- **Skills**: 40%
- **Experience**: 30%
- **Salary**: 20%
- **Location**: 10%

Minimum match score threshold: 0.7 (configurable)

## Testing

### Test Files

1. **test_Mismatch_api_client.py** (138 lines)
   - Client initialization tests
   - HMAC signature validation
   - Model serialization
   - Error handling

2. **test_Mismatch_routes.py** (246 lines)
   - Endpoint tests
   - Filter and parameter validation
   - Authentication tests
   - Response format validation

3. **test_Mismatch_models.py** (220 lines)
   - ORM model tests
   - Constraint validation
   - Relationship tests
   - Database operations

### Running Tests

```bash
pytest tests/test_Mismatch_api_client.py -v
pytest tests/test_Mismatch_routes.py -v
pytest tests/test_Mismatch_models.py -v
```

## Initialization

To initialize the Mismatch integration:

```python
from app.services.Mismatch_initialization_service import initialize_Mismatch

results = initialize_Mismatch()
print(results)
# {
#   "database_models": True,
#   "config_storage": True,
#   "api_credentials": True,
#   "sync_tracking": True,
#   "overall_status": "initialized",
#   "timestamp": "2025-12-28T17:00:00"
# }
```

## Error Handling

Error codes and messages:
- `INVALID_API_KEY`: Invalid or missing API key
- `RATE_LIMITED`: API rate limit exceeded
- `INVALID_REQUEST`: Invalid request parameters
- `RESOURCE_NOT_FOUND`: Resource not found
- `SERVER_ERROR`: Internal server error
- `SYNC_FAILED`: Synchronization failed

## Performance

- **Sync Operation**: ~500 jobs per minute
- **Candidate Matching**: ~1000 matches per minute
- **API Response Time**: <500ms average
- **Database Query Time**: <100ms for indexed queries

## Security

- HMAC-SHA256 authentication for API requests
- API keys stored securely in environment variables
- Webhook secret verification for incoming events
- Rate limiting on API endpoints
- SQL injection prevention via SQLAlchemy ORM

## Future Enhancements

1. **Webhook Support**: Real-time job and candidate updates
2. **Advanced Matching**: ML-based candidate scoring
3. **Bulk Operations**: Batch job/candidate import/export
4. **Analytics Dashboard**: Integration metrics and insights
5. **Notification System**: Email/Slack alerts for matches
