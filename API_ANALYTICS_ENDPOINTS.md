# 📡 Analytics API Endpoints Documentation

## Overview

This document details all API endpoints related to the analytics dashboard for the recruitment bot.

**Base URL:** `https://lamoda-recruiter-maksmisakov.amvera.io` (Cloud) or `http://localhost:5000` (Local)

---

## Core Analytics Endpoints

### 1. GET /api/analytics

**Description:** Fetch comprehensive analytics metrics for the dashboard.

**Method:** `GET`

**Authentication:** None (requires implementation in Phase 3)

**Response Status Codes:**
- `200 OK` - Success
- `500 Internal Server Error` - Database error

**Response Format:**

```json
{
  "success": true,
  "total_candidates": 42,
  "status_breakdown": {
    "approved": 12,
    "rejected": 8,
    "pending": 22
  },
  "average_score": 72.5,
  "top_skills": [
    ["Python", 28],
    ["JavaScript", 15],
    ["React", 12],
    ["SQL", 10],
    ["AWS", 8]
  ],
  "timestamp": "2025-12-23T23:59:59.000Z"
}
```

**Query Parameters:** None

**Example Request:**

```bash
curl https://lamoda-recruiter-maksmisakov.amvera.io/api/analytics
```

**Caching:** Enabled (5-minute TTL)

---

### 2. GET /analytics-dashboard

**Description:** Render the analytics dashboard UI.

**Method:** `GET`

**Response:** HTML page with embedded JavaScript that calls `/api/analytics`

**Status Codes:**
- `200 OK` - Dashboard renders successfully
- `404 Not Found` - Template not found

**Example Request:**

```bash
# Browser: https://lamoda-recruiter-maksmisakov.amvera.io/analytics-dashboard
# Or via curl:
curl https://lamoda-recruiter-maksmisakov.amvera.io/analytics-dashboard
```

**Features:**
- Auto-refresh every 30 seconds
- 4 metric cards with real-time data
- Error handling with fallback values
- Responsive grid layout

---

## Future Endpoints (Phase 2)

### 3. GET /api/analytics/export?format=excel

**Status:** 🚧 In Development (Step 9)

**Description:** Export analytics data as Excel file.

**Parameters:**
- `format` (required): `excel` or `csv`

**Response:** Binary file (Excel/CSV)

**Example:**

```bash
curl -o analytics.xlsx "https://amvera.io/api/analytics/export?format=excel"
```

---

### 4. GET /api/analytics/trends?period=monthly

**Status:** 🚧 In Development (Step 10)

**Description:** Fetch time-series analytics data for trend visualization.

**Parameters:**
- `period` (optional): `daily`, `weekly`, `monthly` (default: `daily`)
- `start_date` (optional): ISO 8601 format
- `end_date` (optional): ISO 8601 format

**Response Format:**

```json
{
  "period": "monthly",
  "data": [
    {
      "date": "2025-11-01",
      "total_candidates": 35,
      "avg_score": 68.5,
      "matches": 8
    },
    {
      "date": "2025-12-01",
      "total_candidates": 42,
      "avg_score": 72.5,
      "matches": 12
    }
  ]
}
```

---

## Integration Examples

### Python (Requests Library)

```python
import requests

# Fetch analytics data
response = requests.get('http://localhost:5000/api/analytics')
data = response.json()

print(f"Total Candidates: {data['total_candidates']}")
print(f"Average Score: {data['average_score']}%")
print(f"Top Skills: {data['top_skills'][:3]}")
```

### JavaScript (Fetch API)

```javascript
// Fetch analytics in dashboard
fetch('/api/analytics')
  .then(response => response.json())
  .then(data => {
    document.getElementById('totalResumes').textContent = data.total_candidates;
    document.getElementById('avgScore').textContent = data.average_score.toFixed(1) + '%';
    document.getElementById('uniqueSkills').textContent = data.top_skills.length;
    document.getElementById('successMatches').textContent = data.status_breakdown.approved;
  })
  .catch(error => console.error('Error:', error));
```

### cURL

```bash
# Get analytics data
curl -X GET "http://localhost:5000/api/analytics" \
  -H "Content-Type: application/json"

# Export to Excel
curl -X GET "http://localhost:5000/api/analytics/export?format=excel" \
  -o analytics.xlsx
```

---

## Error Handling

### API Error Responses

**500 Internal Server Error:**

```json
{
  "error": "Database connection failed"
}
```

**404 Not Found:**

```json
{
  "error": "Not found"
}
```

---

## Performance Metrics

| Metric | Value |
|--------|-------|
| Response Time (cached) | <50ms |
| Response Time (uncached) | 100-200ms |
| Cache Duration | 300 seconds (5 minutes) |
| Database Query Time | ~50-100ms |
| Cache Hit Rate | ~85% |

---

## Rate Limiting

Not yet implemented. Coming in Phase 3 with authentication.

---

## Changelog

### v1.1.0 (December 23, 2025)
- ✅ `/api/analytics` endpoint operational
- ✅ `/analytics-dashboard` UI with 4 metric cards
- ✅ In-memory caching with 5-minute TTL
- ✅ Auto-refresh mechanism (30 seconds)

### v1.0.0 (Initial Release)
- Basic analytics endpoints
- Dashboard template

---

**Last Updated:** December 23, 2025, 11:59 PM MSK
**Maintained By:** maksimmishakov
