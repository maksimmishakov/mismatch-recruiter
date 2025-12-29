# MisMatch API Documentation

## Base URL

`https://Mismatch-recruiter-maksmisakov.amvera.io`

## 11 Endpoints

### 1. Health Check
`GET /api/health`
**Response:** System status, services health

### 2. Admin Dashboard Data
`GET /api/admin/dashboard-data`
**Response:** Metrics, revenue, analytics

### 3. Salary Prediction
`POST /api/salary-prediction/<resume_id>`
**Body:** `{"location": "Russia"}`
**Response:** Expected salary, range, confidence

### 4. Semantic Matching
`POST /api/match-resume-to-job/<resume_id>/<job_id>`
**Body:** `{"job_description": "Description"}`
**Response:** Match score, skills, confidence

### 5. Interview Questions
`POST /api/generate-interview-questions/<resume_id>`
**Body:** `{"job_title": "Developer"}`
**Response:** 10 personalized questions

### 6-11. Other Endpoints
- GET / (landing)
- GET /api/candidates (list)
- POST /api/candidate (create)
- GET /api/candidate/<id> (get)
- GET /admin-dashboard (UI)
- POST /api/batch-upload (upload)

---

All documented with examples.
