# 🧪 Testing Guide - MisMatch Features

## Overview
This guide provides comprehensive testing procedures for the three core features implemented in the MisMatch recruitment bot.

**Status**: Ready for Testing
**Last Updated**: December 23, 2025
**Application URL**: https://Mismatch-recruiter-maksmisakov.amvera.io

---

## Prerequisites

- [ ] Application is deployed and running
- [ ] API endpoints are accessible
- [ ] Database is initialized
- [ ] OpenAI API key is configured
- [ ] Browser has JavaScript enabled
- [ ] Network connectivity to Amvera cloud

---

## Test Environment Setup

### 1. Health Check

**Endpoint**: `GET /api/status`
**Expected Response**: `{"status": "ok", "timestamp": "..."}`

```bash
curl -X GET https://Mismatch-recruiter-maksmisakov.amvera.io/api/status
```

✅ **Pass Criteria**: HTTP 200 with status="ok"

---

## Feature 1: Batch Upload Testing

### Test Case 1.1: Single PDF Upload

**UI Path**: Navigate to `/batch`

**Steps**:
1. Open batch upload page
2. Click on upload area or drag-drop a PDF file
3. Wait for processing to complete
4. Verify success message appears

**Expected Result**:
```json
{
  "success": true,
  "total_files": 1,
  "successful": 1,
  "results": [
    {
      "filename": "resume.pdf",
      "status": "success",
      "skills": ["Python", "JavaScript"],
      "score": 75
    }
  ]
}
```

✅ **Pass Criteria**: 
- Response status HTTP 200
- successful count = total_files
- Skills array is non-empty
- Score is between 0-100

### Test Case 1.2: Multiple File Upload (Batch)

**Steps**:
1. Select 3-5 PDF files
2. Drop all at once on upload area
3. Verify all files process
4. Check results for each file

✅ **Pass Criteria**: 
- All files processed
- Each file has individual result
- No files failed without reason

### Test Case 1.3: Invalid File Type Rejection

**Steps**:
1. Try uploading a .txt or .exe file
2. Verify error message appears

✅ **Pass Criteria**: 
- Error: "File type not allowed"
- HTTP 400 status

### API Test: Batch Upload Endpoint

```bash
curl -X POST https://Mismatch-recruiter-maksmisakov.amvera.io/api/batch-upload \
  -F "files[]=@resume1.pdf" \
  -F "files[]=@resume2.pdf"
```

---

## Feature 2: Job Matcher Testing

### Test Case 2.1: High Skill Match (GOOD_FIT)

**UI Path**: Navigate to `/job-matcher`

**Test Data**:
```
Job Title: Senior Python Developer
Job Description: Looking for experienced Python developer with 5+ years experience in FastAPI, PostgreSQL, and cloud deployment.
Resume: 8 years Python experience, FastAPI expert, PostgreSQL proficient, deployed 20+ cloud applications
```

**Expected Result**:
```json
{
  "success": true,
  "match_percentage": 85,
  "verdict": "GOOD_FIT"
}
```

✅ **Pass Criteria**: 
- match_percentage >= 70
- verdict = "GOOD_FIT"
- Response time < 5 seconds

### Test Case 2.2: Medium Skill Match (MODERATE_FIT)

**Test Data**:
```
Job Title: Backend Developer
Job Description: Need developer with Python and JavaScript
Resume: Intermediate Python skills, advanced JavaScript, some React experience
```

**Expected Result**:
```json
{
  "match_percentage": 55,
  "verdict": "MODERATE_FIT"
}
```

✅ **Pass Criteria**: 
- 50 <= match_percentage < 70
- verdict = "MODERATE_FIT"

### Test Case 2.3: Low Skill Match (POOR_FIT)

**Test Data**:
```
Job Title: Data Scientist
Job Description: Machine Learning, TensorFlow, statistical analysis
Resume: Web developer, HTML, CSS, JavaScript only
```

**Expected Result**:
```json
{
  "match_percentage": 25,
  "verdict": "POOR_FIT"
}
```

✅ **Pass Criteria**: 
- match_percentage < 50
- verdict = "POOR_FIT"

### API Test: Job Matcher Endpoint

```bash
curl -X POST https://Mismatch-recruiter-maksmisakov.amvera.io/api/match-resume-to-job \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Senior Python Developer",
    "job_description": "Looking for experienced Python developer...",
    "resume_text": "8 years Python experience..."
  }'
```

---

## Feature 3: Interview Questions Generator Testing

### Test Case 3.1: Basic Level Questions

**UI Path**: Navigate to `/interview-questions` (or endpoint path)

**Test Data**:
```
Job Position: Junior Developer
Job Description: Entry-level backend developer position
Resume Summary: Recent bootcamp graduate, basic Python skills
```

**Expected Result**:
```json
{
  "success": true,
  "job_title": "Junior Developer",
  "total": 10,
  "questions": [
    {"level": "basic", "question": "Tell us about your experience"},
    {"level": "basic", "question": "Why are you interested in this position?"},
    {"level": "intermediate", "question": "How do you approach problem-solving?"},
    {"level": "advanced", "question": "How would you optimize a system?"}
  ]
}
```

✅ **Pass Criteria**: 
- Total questions = 10
- Questions distributed across 3 levels
- Each question is non-empty
- Level distribution: ~3 basic, ~4 intermediate, ~3 advanced

### Test Case 3.2: Advanced Position Questions

**Test Data**:
```
Job Position: Principal Architect
Job Description: Lead technical decisions, design systems, mentor team
Resume Summary: 15 years experience, CTO background, multiple startups
```

✅ **Pass Criteria**: 
- More advanced-level questions
- Questions focus on architecture and leadership
- Response time < 3 seconds

### Test Case 3.3: Question Variety

**Verification**:
- Questions are unique (no duplicates)
- Questions are specific to job position
- Questions target candidate experience level

### API Test: Interview Questions Endpoint

```bash
curl -X POST https://Mismatch-recruiter-maksmisakov.amvera.io/api/generate-interview-questions \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Senior Backend Developer",
    "job_description": "Looking for experienced backend developer...",
    "resume_analysis": {"summary": "8 years experience..."}
  }'
```

---

## Performance Testing

### Response Time Benchmarks

| Endpoint | Target | Acceptable Range |
|----------|--------|------------------|
| Batch Upload (1 file) | < 30s | < 60s |
| Batch Upload (5 files) | < 120s | < 300s |
| Job Matcher | < 5s | < 10s |
| Interview Questions | < 3s | < 5s |

### Concurrent User Testing

**Test**: 10 simultaneous requests to each endpoint

✅ **Pass Criteria**: 
- All requests complete successfully
- No timeout errors
- Response times remain within acceptable range

---

## Error Handling Testing

### Test Case 4.1: Missing Required Fields

**Request**:
```bash
curl -X POST https://Mismatch-recruiter-maksmisakov.amvera.io/api/match-resume-to-job \
  -H "Content-Type: application/json" \
  -d '{"job_title": "Position"}'
```

**Expected Response**: HTTP 400 with error message

✅ **Pass Criteria**: 
- HTTP 400 status
- Error message describes missing field

### Test Case 4.2: Invalid File Type in Batch Upload

**Expected Response**: HTTP 400

✅ **Pass Criteria**: 
- Error message: "File type not allowed"

### Test Case 4.3: Large File Upload (> 50MB)

**Expected Response**: HTTP 413 or timeout

✅ **Pass Criteria**: 
- Graceful error handling
- Clear error message

---

## UI/UX Testing

### Visual Elements Checklist

- [ ] Batch Upload: Drag-drop zone is clearly visible
- [ ] Job Matcher: Form fields are properly labeled
- [ ] Interview Questions: Questions are readable and well-formatted
- [ ] All pages: Responsive design works on mobile
- [ ] All pages: Colors and styling match brand guidelines

### Functionality Checklist

- [ ] Form validation works correctly
- [ ] Error messages are helpful
- [ ] Success messages appear appropriately
- [ ] Results display correctly
- [ ] No console JavaScript errors

---

## Browser Compatibility Testing

**Browsers to Test**:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)

---

## Security Testing

### Test Case 5.1: Input Validation

- [ ] SQL injection attempts are blocked
- [ ] XSS payloads are sanitized
- [ ] File upload validates type and size

### Test Case 5.2: API Security

- [ ] Endpoints require valid input
- [ ] No sensitive data in error messages
- [ ] CORS properly configured

---

## Test Execution Checklist

**Feature 1: Batch Upload**
- [ ] Single file upload works
- [ ] Multiple file upload works
- [ ] Invalid file types rejected
- [ ] Response format correct
- [ ] UI displays results properly

**Feature 2: Job Matcher**
- [ ] High match case (GOOD_FIT)
- [ ] Medium match case (MODERATE_FIT)
- [ ] Low match case (POOR_FIT)
- [ ] Response time acceptable
- [ ] UI color coding correct

**Feature 3: Interview Questions**
- [ ] Questions generated successfully
- [ ] 10 questions returned
- [ ] Question levels distributed
- [ ] Questions are relevant
- [ ] Response time acceptable

**General**
- [ ] Health check passes
- [ ] No database errors
- [ ] API responses valid JSON
- [ ] Performance within limits
- [ ] No security vulnerabilities

---

## Known Issues & Limitations

### Current Limitations

1. **File Size**: Maximum 50MB per file
2. **Batch Processing**: Maximum 10 files per request
3. **Response Time**: Initial requests may take longer due to model loading
4. **Language**: Currently supports English only

### Known Issues

- None reported at this time

---

## Sign-Off

**Tester Name**: ________________
**Date**: ________________
**Overall Status**: [ ] PASS [ ] FAIL [ ] CONDITIONAL

**Notes**:
_____________________________________________

---

**Next Steps After Testing**:
1. Document any bugs found
2. Create GitHub issues for failures
3. Perform regression testing if changes made
4. Schedule production deployment
5. Set up monitoring and alerts
