# STEP 7: AMVERA STAGING DEPLOYMENT GUIDE

**Status:** Ready for Deployment
**Date:** January 12, 2026
**Target:** Amvera Platform (https://amvera.io/)
**Branch:** main (all 10 tests passing)

## STEP 7.2: DEPLOY TO AMVERA

### Prerequisites
- Amvera account (https://amvera.io/)
- GitHub repository access (already configured)
- Project linked to Amvera

### Deployment Method 1: Amvera Web Dashboard (RECOMMENDED)

1. **Login to Amvera:**
   - Go to https://amvera.io/
   - Sign in with your credentials

2. **Navigate to Project:**
   - Click "Projects" in sidebar
   - Find "mismatch-recruiter" project
   - Click to open

3. **Trigger Deployment:**
   - Look for "Deploy" or "Redeploy" button
   - Select branch: **main**
   - Click "Deploy"

4. **Monitor Deployment:**
   - Amvera will start build process
   - Watch progress in Logs section
   - Expected time: 4-5 minutes

   **Expected Log Messages:**
   ```
   Installing dependencies... [OK]
   Building application... [OK]
   Starting application... [OK]
   Health check: [PASSED]
   ```

### Deployment Method 2: Git Push Trigger (AUTO-DEPLOY)

If configured, just push to main:
```bash
git push origin main
```

Amvera will automatically detect and deploy.

### Deployment Method 3: Amvera CLI

```bash
# Install Amvera CLI
pip install amvera

# Login
amvera login

# Deploy
amvera deploy --branch main
```

## STEP 7.3: VERIFY STAGING DEPLOYMENT

### 1. Find Your Staging URL

- Go to Amvera Dashboard
- Open mismatch-recruiter project
- Look for "Staging URL" or "Application URL"
- Format: `https://mismatch-recruiter-[ID].amvera.io`

### 2. Test Health Endpoint

```bash
# Replace with your actual URL
STAGING_URL="https://mismatch-recruiter-YOUR_ID.amvera.io"

# Test health endpoint
curl -s "$STAGING_URL/api/health" | jq .

# Expected response:
# {
#   "status": "ok",
#   "service": "mismatch-recruiter",
#   "version": "1.0"
# }
```

### 3. Verify HTTP Status Code

```bash
curl -s -o /dev/null -w "%{http_code}\n" "$STAGING_URL/api/health"

# Expected: 200
```

### 4. Check Deployment Logs

If health check fails:
1. Go to Amvera Dashboard
2. Open mismatch-recruiter
3. Click "Logs" tab
4. Look for error messages
5. Search for specific errors below

## Troubleshooting Common Deployment Issues

### ERROR: "Port already in use"
**Solution:** Amvera automatically assigns ports. No action needed.

### ERROR: "ModuleNotFoundError: No module named 'app'"
**Solution:** 
- Check that app/__init__.py exists
- Verify requirements.txt is installed
- Check wsgi.py imports are correct

### ERROR: "Database connection failed"
**Solution:**
- SQLite database is created automatically
- First startup may take longer (2-3 minutes)
- No DATABASE_URL configuration needed for SQLite

### ERROR: "SECRET_KEY not found"
**Solution:**
- Go to Amvera Dashboard → Project Settings → Environment Variables
- Add: `SECRET_KEY=your-secret-key-here`
- Redeploy application

### ERROR: "500 Internal Server Error"
**Solution:**
1. Check Amvera logs for specific error
2. Verify flask app structure:
   - app/__init__.py creates app
   - app/routes.py or api/ folder exists
   - wsgi.py imports app correctly
3. Ensure no syntax errors in Python code

### ERROR: "404 Not Found on /api/health"
**Solution:**
- Verify app/__init__.py has health endpoint registered
- Check that routes are registered in create_app()
- Redeploy if routes were updated

## Success Criteria - Deployment Complete

You know deployment is successful when:

✅ Amvera Dashboard shows "ACTIVE" status
✅ Health endpoint returns 200 OK
✅ Staging URL is accessible
✅ Logs show "Health check: [PASSED]"
✅ No error messages in recent logs

## Post-Deployment Checklist

- [ ] Application status is "Active" in Amvera
- [ ] Health endpoint responds with 200 OK
- [ ] Staging URL is bookmarked
- [ ] Logs show successful startup
- [ ] No critical errors in logs
- [ ] Time to proceed to STEP 8

## Expected Deployment Timeline

| Phase | Duration | Status |
|-------|----------|--------|
| Build | 2-3 min | Dependencies, pip install |
| Deploy | 1-2 min | Application startup |
| Health Check | 30 sec | API responds |
| **Total** | **4-5 min** | **Ready** |

## What's Running

- **Framework:** Flask (Python)
- **WSGI Server:** Gunicorn
- **Database:** SQLite (local)
- **API Endpoints:** 6+ endpoints
- **Health Check:** /api/health → 200 OK

## Next Step

Once deployment is verified:
1. Save staging URL
2. Note deployment time
3. Proceed to STEP 8 (E2E Testing)

---

**Generated:** January 12, 2026
**Status:** Ready for Staging Deployment
