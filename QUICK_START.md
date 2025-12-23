# 🚀 Quick Start Guide - MisMatch Features

**Status**: Production Ready  
**Live URL**: https://lamoda-recruiter-maksmisakov.amvera.io  
**Last Updated**: December 23, 2025

---

## 30-Second Overview

MisMatch provides three powerful features for recruitment automation:

1. **Batch Upload** - Process multiple resumes at once
2. **Job Matcher** - Match candidates with job descriptions
3. **Interview Questions** - Generate tailored interview questions

---

## Access the Application

### Web Interface

| Feature | URL |
|---------|-----|
| Batch Upload | `/batch` |
| Job Matcher | `/job-matcher` |
| Interview Questions | (see API below) |
| Health Check | `/api/status` |

**Example**: https://lamoda-recruiter-maksmisakov.amvera.io/batch

---

## API Quick Reference

### 1. Batch Upload Files

```bash
curl -X POST https://lamoda-recruiter-maksmisakov.amvera.io/api/batch-upload \\
  -F "files[]=@resume1.pdf" \\
  -F "files[]=@resume2.pdf"
```

**Response**:
```json
{
  "success": true,
  "total_files": 2,
  "successful": 2,
  "results": [
    {"filename": "resume1.pdf", "status": "success", "skills": ["Python"], "score": 85}
  ]
}
```

---

### 2. Match Resume to Job

```bash
curl -X POST https://lamoda-recruiter-maksmisakov.amvera.io/api/match-resume-to-job \\
  -H "Content-Type: application/json" \\
  -d '{
    "job_title": "Senior Python Developer",
    "job_description": "Looking for experienced Python developer with FastAPI experience",
    "resume_text": "8 years Python, FastAPI expert, deployed 50+ projects"
  }'
```

**Response**:
```json
{
  "success": true,
  "match_percentage": 85,
  "verdict": "GOOD_FIT",
  "candidate_name": "John Doe"
}
```

---

### 3. Generate Interview Questions

```bash
curl -X POST https://lamoda-recruiter-maksmisakov.amvera.io/api/generate-interview-questions \\
  -H "Content-Type: application/json" \\
  -d '{
    "job_title": "Backend Developer",
    "job_description": "Build scalable backend systems",
    "resume_analysis": {"summary": "5 years backend experience"}
  }'
```

**Response**:
```json
{
  "success": true,
  "job_title": "Backend Developer",
  "total": 10,
  "questions": [
    {"level": "basic", "question": "Tell us about your experience"},
    {"level": "intermediate", "question": "How do you approach system design?"},
    {"level": "advanced", "question": "How would you optimize database queries?"}
  ]
}
```

---

## Using the Web Interface

### Feature 1: Batch Upload

1. Open https://lamoda-recruiter-maksmisakov.amvera.io/batch
2. Drag-drop PDF files or click to upload
3. Wait for processing
4. View results with extracted skills and scores

### Feature 2: Job Matcher

1. Open https://lamoda-recruiter-maksmisakov.amvera.io/job-matcher
2. Enter job title (e.g., "Senior Python Developer")
3. Paste job description
4. Paste resume text
5. Click "Find Match"
6. View match percentage and verdict (GOOD_FIT, MODERATE_FIT, POOR_FIT)

### Feature 3: Interview Questions

1. Navigate to interview questions page
2. Enter job position
3. Provide job description
4. Add resume summary
5. Click "Generate Questions"
6. Review questions grouped by difficulty level

---

## Response Status Codes

| Code | Meaning |
|------|----------|
| 200 | Success |
| 400 | Bad request (missing/invalid fields) |
| 404 | Resource not found |
| 500 | Server error |
| 503 | Service unavailable (building/deploying) |

---

## Common Use Cases

### Use Case 1: Recruiting Campaign

1. Upload batch of 50 resumes
2. System extracts skills and scores each candidate
3. Use scores to shortlist top 10 candidates
4. Use job matcher to verify fit for specific role
5. Generate interview questions for finalists

### Use Case 2: Single Candidate Evaluation

1. Provide resume text
2. Get job match score instantly
3. Generate tailored interview questions
4. Conduct structured interview

### Use Case 3: Job Description Analysis

1. Paste job description
2. Match against candidate pool
3. Identify skill gaps
4. Generate questions targeting key competencies

---

## Troubleshooting

### Application Returns 503

**Cause**: Service is building/deploying  
**Solution**: Wait 5-10 minutes and try again

### File Upload Fails

**Possible Causes**:
- File size > 50MB (maximum)
- File type not supported (only PDF, DOCX, DOC)
- Network connectivity issue

**Solution**:
- Check file size
- Verify file format
- Try uploading fewer files

### Job Match Returns 0%

**Cause**: Resume has no matching skills with job  
**Solution**: 
- Verify resume content is pasted correctly
- Check job description has clear requirements
- Try with different resume/job combination

---

## Performance Targets

| Operation | Target Time |
|-----------|-------------|
| Single file upload | < 30 seconds |
| Batch upload (5 files) | < 2 minutes |
| Job matching | < 5 seconds |
| Question generation | < 3 seconds |

---

## System Requirements

- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection
- JavaScript enabled
- No additional software required

---

## Support & Documentation

- **Feature Details**: See `FEATURES_COMPLETION_SUMMARY.md`
- **Testing Guide**: See `TESTING_GUIDE.md`
- **Deployment**: See `AMVERA_DEPLOYMENT_GUIDE.md`
- **GitHub**: https://github.com/maksimmishakov/lamoda-ai-recruiter

---

## What's Next?

1. ✅ Test the application at https://lamoda-recruiter-maksmisakov.amvera.io
2. ✅ Try each of the 3 features
3. 📖 Read the detailed testing guide for comprehensive testing
4. 🚀 Deploy to your infrastructure
5. 📊 Monitor performance and gather feedback

---

## Key Features Summary

✅ **Batch Upload**
- Support for PDF, DOCX, DOC files
- Automatic skill extraction
- Candidate scoring
- Error handling with clear messages

✅ **Job Matcher**
- Skill-based matching algorithm
- Percentage score (0-100%)
- 3-level verdict system
- Experience consideration

✅ **Interview Questions**
- 10 tailored questions per candidate
- 3 difficulty levels
- Contextual to job and candidate
- Ready-to-use in interviews

---

**Version**: 1.0  
**Created**: December 23, 2025  
**Status**: ✅ Production Ready
