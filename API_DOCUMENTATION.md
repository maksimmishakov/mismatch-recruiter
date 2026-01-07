# MisMatch Recruiter API Documentation

Base URL: `http://localhost:5000/api`

## Authentication Endpoints

### Register User
**POST** `/auth/register`

Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "secure_password",
  "full_name": "Full Name"
}
```

**Response (201):**
```json
{
  "message": "User registered successfully",
  "user_id": 1
}
```

**Error Responses:**
- 400: Missing required fields
- 409: Email already registered

---

### Login
**POST** `/auth/login`

Authenticate user and get JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response (200):**
```json
{
  "access_token": "jwt_token_here",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "full_name": "Full Name",
    "role": "user",
    "is_active": true,
    "created_at": "2024-01-04T12:00:00"
  }
}
```

**Error Responses:**
- 400: Missing credentials
- 401: Invalid credentials

---

## Health Check

### Get API Status
**GET** `/health`

Check if the API is running.

**Response (200):**
```json
{
  "status": "healthy",
  "service": "mismatch-recruiter-api"
}
```

---

## Request Headers

For authenticated endpoints, include:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

## Error Codes

- **200**: Success
- **201**: Created
- **400**: Bad Request
- **401**: Unauthorized
- **409**: Conflict
- **500**: Internal Server Error

## Rate Limiting

No rate limiting is currently implemented. Rate limiting will be added in future versions.

## Versioning

Current API version: 1.0

Future versions will use URL versioning (e.g., `/api/v2/...`)
