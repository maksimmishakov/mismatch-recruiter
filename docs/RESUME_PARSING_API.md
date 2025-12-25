# Resume Parsing API Documentation

## Overview

The Resume Parsing API provides endpoints for processing, analyzing, and retrieving parsed resume data. It extracts structured information including skills, education, work experience, and other relevant details from resume text.

## Base URL

```
/api/resumes
```

## Authentication

All endpoints require JWT authentication via the `Authorization` header.

## Endpoints

### 1. Trigger Resume Parsing

**POST** `/api/resumes/{job_id}/parse`

Triggers asynchronous resume parsing for a specific job.

#### Parameters

- `job_id` (path, required): Job ID to associate the parsed resume with

#### Request Body

```json
{
  "resume_text": "String containing the complete resume text"
}
```

#### Response (202 Accepted)

```json
{
  "resume_id": 123,
  "task_id": "celery-task-uuid",
  "status": "pending"
}
```

#### Error Responses

- **400 Bad Request**: Resume text is required
- **404 Not Found**: Job not found
- **500 Internal Server Error**: Server error during parsing

---

### 2. Get Parsed Resume

**GET** `/api/resumes/{resume_id}`

Retrieve complete parsed resume data including all extracted information.

#### Parameters

- `resume_id` (path, required): Parsed resume ID

#### Response (200 OK)

```json
{
  "id": 123,
  "job_id": 456,
  "parsing_status": "completed",
  "skills": [
    {
      "id": 1,
      "skill_name": "Python",
      "skill_category": "Programming",
      "proficiency_level": "Advanced",
      "years_experience": 5.0
    }
  ],
  "education": [
    {
      "id": 1,
      "school_name": "MIT",
      "degree": "Bachelor",
      "field_of_study": "Computer Science",
      "start_date": "2016-09",
      "end_date": "2020-06",
      "gpa": 3.8
    }
  ],
  "experience": [
    {
      "id": 1,
      "company_name": "Tech Corp",
      "job_title": "Software Engineer",
      "start_date": "2020-07",
      "end_date": "2023-12",
      "description": "Developed backend systems",
      "duration_months": 42
    }
  ],
  "error_message": null,
  "created_at": "2024-12-25T16:00:00Z",
  "updated_at": "2024-12-25T16:00:30Z"
}
```

#### Error Responses

- **404 Not Found**: Resume not found

---

### 3. Get Resume Skills

**GET** `/api/resumes/{resume_id}/skills`

Retrieve all extracted skills from a parsed resume.

#### Parameters

- `resume_id` (path, required): Parsed resume ID

#### Response (200 OK)

```json
{
  "resume_id": 123,
  "total": 15,
  "skills": [
    {
      "id": 1,
      "skill_name": "Python",
      "skill_category": "Programming",
      "proficiency_level": "Advanced",
      "years_experience": 5.0
    },
    {
      "id": 2,
      "skill_name": "JavaScript",
      "skill_category": "Programming",
      "proficiency_level": "Intermediate",
      "years_experience": 3.0
    }
  ]
}
```

---

### 4. Get Resume Education

**GET** `/api/resumes/{resume_id}/education`

Retrieve all education entries from a parsed resume.

#### Parameters

- `resume_id` (path, required): Parsed resume ID

#### Response (200 OK)

```json
{
  "resume_id": 123,
  "total": 2,
  "education": [
    {
      "id": 1,
      "school_name": "MIT",
      "degree": "Bachelor",
      "field_of_study": "Computer Science",
      "start_date": "2016-09",
      "end_date": "2020-06",
      "gpa": 3.8
    }
  ]
}
```

---

### 5. Get Resume Experience

**GET** `/api/resumes/{resume_id}/experience`

Retrieve all work experience entries from a parsed resume.

#### Parameters

- `resume_id` (path, required): Parsed resume ID

#### Response (200 OK)

```json
{
  "resume_id": 123,
  "total": 3,
  "experience": [
    {
      "id": 1,
      "company_name": "Tech Corp",
      "job_title": "Senior Software Engineer",
      "start_date": "2020-07",
      "end_date": "2023-12",
      "description": "Led backend development team",
      "duration_months": 42
    }
  ]
}
```

---

### 6. Delete Parsed Resume

**DELETE** `/api/resumes/{resume_id}`

Delete a parsed resume and all associated data (skills, education, experience).

#### Parameters

- `resume_id` (path, required): Parsed resume ID

#### Response (200 OK)

```json
{
  "message": "Resume deleted successfully"
}
```

#### Error Responses

- **404 Not Found**: Resume not found

---

## Parsing Status Values

- `pending`: Parsing task is queued or in progress
- `processing`: Currently being processed
- `completed`: Successfully parsed
- `failed`: Parsing failed

## Error Handling

All error responses follow this format:

```json
{
  "error": "Error description"
}
```

## Rate Limiting

- 100 requests per minute per user
- Headers will include X-RateLimit-Limit and X-RateLimit-Remaining

## Examples

### Trigger Resume Parsing

```bash
curl -X POST http://localhost:5000/api/resumes/123/parse \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "John Doe... [full resume text]"
  }'
```

### Get Parsed Resume

```bash
curl -X GET http://localhost:5000/api/resumes/123 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Get Resume Skills

```bash
curl -X GET http://localhost:5000/api/resumes/123/skills \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Data Models

### ParsedResume

- `id` (integer): Unique resume identifier
- `job_id` (integer): Associated job ID
- `raw_text` (string): Original resume text
- `parsing_status` (string): Current parsing status
- `parsing_metadata` (object): JSON metadata from parsing
- `error_message` (string): Error details if parsing failed
- `created_at` (datetime): Timestamp of creation
- `updated_at` (datetime): Last update timestamp

### ResumeSkill

- `id` (integer): Unique skill identifier
- `resume_id` (integer): Associated resume ID
- `skill_name` (string): Name of the skill
- `skill_category` (string): Category (e.g., Programming, Design)
- `proficiency_level` (string): Proficiency level (e.g., Advanced)
- `years_experience` (float): Years of experience with skill

### ResumeEducation

- `id` (integer): Unique education identifier
- `resume_id` (integer): Associated resume ID
- `school_name` (string): Educational institution name
- `degree` (string): Degree type (e.g., Bachelor, Master)
- `field_of_study` (string): Field of study
- `start_date` (string): Start date (YYYY-MM format)
- `end_date` (string): End date (YYYY-MM format)
- `gpa` (float): Grade point average

### ResumeExperience

- `id` (integer): Unique experience identifier
- `resume_id` (integer): Associated resume ID
- `company_name` (string): Company name
- `job_title` (string): Job title
- `start_date` (string): Start date (YYYY-MM format)
- `end_date` (string): End date (YYYY-MM format)
- `description` (string): Job description and achievements
- `duration_months` (integer): Duration in months

## Best Practices

1. **Always validate resume text** before sending to the API
2. **Check parsing_status** before relying on extracted data
3. **Implement retry logic** for failed parsing attempts
4. **Cache resume data** when possible to reduce API calls
5. **Handle errors gracefully** and provide user feedback

## Support

For issues or questions, contact the development team or create an issue in the repository.
