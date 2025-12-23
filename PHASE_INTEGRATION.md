# Phase 1 + Phase 2 Integration Guide
## RankPO - AI Recruitment Platform

### 🎯 Overview
This document describes how Phase 1 (Resume Upload & PDF Extraction) and Phase 2 (AI Analysis with Yandex GPT) are integrated into a unified FastAPI server.

## Architecture

### Phase 1: Resume Upload & PDF Text Extraction
**File:** `main.py` (Flask) OR `api_server.py` (FastAPI)
**Endpoint:** `POST /api/analyze-resume`
**Input:** PDF file
**Output:** 
```json
{
  "status": "success",
  "filename": "resume.pdf",
  "pages": 2,
  "text_length": 5432,
  "text_preview": "John Doe..." 
}
```

### Phase 2: AI-Powered Resume Analysis
**File:** `api_server.py` (FastAPI)
**Dependencies:** `phase_2_yandex_gpt.py` (MisMatchAI class)
**Endpoint:** `POST /api/analyze-resume-ai`
**Input:** PDF file
**Output:**
```json
{
  "status": "success",
  "filename": "resume.pdf",
  "analysis": {
    "name": "John Doe",
    "experience_years": 7,
    "technical_skills": ["Python", "Go", "Docker"],
    "experience_level": "Senior",
    "red_flags": []
  },
  "score": 85,
  "summary": "John Doe - Senior Engineer with 7 years - Score 85/100",
  "recommendation": "STRONG - Interview immediately"
}
```

## Running the Unified Server

### Option 1: FastAPI (Recommended)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python api_server.py

# Or with uvicorn
uvicorn api_server:app --reload --host 0.0.0.0 --port 8000

# Access:
# - UI: http://localhost:8000/
# - API Docs: http://localhost:8000/docs
# - Health: http://localhost:8000/health
```

### Option 2: Flask (Legacy)
```bash
python main.py
# Access: http://localhost:5000
```

## Endpoints

| Endpoint | Method | Purpose | Phase |
|----------|--------|---------|-------|
| `/` | GET | Load HTML UI from GitHub | 1+2 |
| `/health` | GET | Health check | 2 |
| `/api/analyze-resume` | POST | Extract text from PDF | 1 |
| `/api/analyze-resume-ai` | POST | AI analysis with scoring | 2 |
| `/api/match-job` | POST | Match resume with job | 2 |
| `/api/feedback` | POST | Collect hiring feedback | 2 |
| `/docs` | GET | Swagger API documentation | FastAPI |

## Files

```
.
├── api_server.py              # FastAPI server (Phase 1 + 2)
├── main.py                    # Flask server (Phase 1 only) - Backup
├── phase_2_yandex_gpt.py      # MisMatchAI class for AI analysis
├── templates/
│   └── index.html             # Web UI with drag-and-drop upload
├── requirements.txt           # Python dependencies
└── PHASE_INTEGRATION.md       # This file
```

## Key Features

### Phase 1 ✅
- ✅ PDF file upload with drag-and-drop
- ✅ Text extraction using pdfplumber
- ✅ File validation (PDF only, size limit 16MB)
- ✅ Error handling

### Phase 2 ✅
- ✅ AI-powered resume analysis (Yandex GPT)
- ✅ Candidate scoring (0-100)
- ✅ Skill extraction
- ✅ Experience level classification
- ✅ Red flag detection
- ✅ Job matching and comparison
- ✅ Hiring feedback collection
- ✅ Auto-generated API documentation

## Environment Variables

```bash
# Required for Phase 2 AI features
YANDEX_GPT_API_KEY=your_key_here
YANDEX_FOLDER_ID=your_folder_id_here
```

## Testing

### 1. Test Health Endpoint
```bash
curl http://localhost:8000/health
```

### 2. Test PDF Upload (Phase 1)
```bash
curl -X POST -F "file=@resume.pdf" http://localhost:8000/api/analyze-resume
```

### 3. Test AI Analysis (Phase 2)
```bash
curl -X POST -F "file=@resume.pdf" http://localhost:8000/api/analyze-resume-ai
```

### 4. Test Job Matching (Phase 2)
```bash
curl -X POST http://localhost:8000/api/match-job \
  -H "Content-Type: application/json" \
  -d '{
    "resume_data": {...},
    "job_description": "Senior Backend Engineer needed..."
  }'
```

## Performance

| Operation | Phase 1 | Phase 2 | Time |
|-----------|---------|---------|------|
| PDF upload & text extract | ✅ | ✅ | ~200ms |
| AI analysis with Yandex GPT | - | ✅ | ~500ms |
| Job matching calculation | - | ✅ | ~50ms |
| **Total (Phase 1 only)** | ✅ | - | ~200ms |
| **Total (Phase 2 full)** | ✅ | ✅ | ~750ms |

## Technology Stack

**Phase 1:**
- FastAPI/Flask - Web framework
- pdfplumber - PDF text extraction
- Python 3.9+

**Phase 2:**
- FastAPI - Fast async framework
- Yandex Cloud API - LLM for AI analysis
- asyncio - Async operations

## Next Steps (Phase 3)

- [ ] Database integration (PostgreSQL)
- [ ] User authentication
- [ ] Candidate tracking
- [ ] Interview scheduling
- [ ] Feedback learning system
- [ ] LAMODA integration

## Support

For issues or questions about integration, check:
- API Docs: http://localhost:8000/docs
- GitHub Issues: github.com/maksimmishakov/lamoda-ai-recruiter/issues
