# Deployment Guide

## Automatic Deployment (Amvera)

### How It Works
1. You push code to GitHub
2. GitHub Actions tests your code (2 min)
3. If tests pass → Amvera webhook triggers (automatic)
4. Amvera rebuilds container (5 min)
5. Application updates live (zero downtime)

### Monitor Deployment

**GitHub Actions:**
- Go to: https://github.com/maksimmishakov/lamoda-ai-recruiter/actions
- Watch workflow progress
- Should see ✅ green check in 2-3 min

**Amvera Logs:**
- Dashboard → Your App → Logs
- Watch real-time deployment
- Look for "Application started"

### Environment Variables

On Amvera, make sure these exist:

```
DATABASE_URL=postgresql://...
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=sk-...
FLASK_ENV=production
```

---

That's it! Automatic deployment ready.
