# 🚀 MisMatch Deployment Guide - Amvera (Lamoda Cloud)

## Overview

This guide covers deploying the MisMatch AI Resume Analysis Platform to Amvera (Lamoda's cloud platform). Amvera is the recommended platform for Russian deployment with excellent support for FastAPI applications.

## Quick Start (5-10 minutes)

### ✅ Prerequisites
- Amvera account (free at amvera.ru)
- MisMatch code files (app.py, templates/, static/)
- OpenAI API key
- Files already prepared:
  - `requirements.txt` - Python dependencies
  - `Procfile` - Application startup command
  - `.env.example` - Environment variables template

### 🔧 Step 1: Prepare Your Code

1. Ensure you have all required files in root directory:
   ```
   app.py
   requirements.txt
   Procfile
   templates/
   static/
   .gitignore
   .env
   ```

2. Verify `requirements.txt` contains:
   ```
   fastapi==0.104.1
   uvicorn==0.24.0
   python-multipart==0.0.6
   PyPDF2==3.17.1
   pydantic==2.5.0
   python-dotenv==1.0.0
   openai==1.3.6
   httpx==0.25.1
   ```

3. Verify `Procfile` contains:
   ```
   web: uvicorn app:app --host 0.0.0.0 --port 8000
   ```

### 📤 Step 2: Deploy to Amvera

#### Option A: Upload from GitHub (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Amvera deployment"
   git push origin master
   ```

2. **On amvera.ru Dashboard**
   - Login to your Amvera account
   - Click "New Application" or select existing "mismatch" app
   - Choose "Connect Repository"
   - Select GitHub
   - Choose `maksimmishakov/lamoda-ai-recruiter`
   - Set branch to `master`

3. **Configure Environment Variables**
   - Go to Application → Settings → Environment Variables
   - Add these variables:
     ```
     OPENAI_API_KEY = sk-proj-[YOUR_ACTUAL_KEY_HERE]
     LLM_MODEL = gpt-4o-mini
     BACKEND_PORT = 8000
     ```

4. **Deploy**
   - Click "Deploy" button
   - Wait 2-3 minutes for deployment
   - Check "Active" status shows green checkmark

#### Option B: Direct Upload

1. On amvera.ru Dashboard
2. Click "Upload Files"
3. Select entire project folder
4. Add environment variables (see Step 3 above)
5. Click "Deploy"

### ✅ Step 3: Verify Deployment

After deployment, Amvera provides a URL like:
```
https://mismatch-[random].amvera.io
```

**Test endpoints:**

1. **Health Check**
   ```bash
   curl https://mismatch-[random].amvera.io/health
   ```
   Expected response:
   ```json
   {
     "status": "healthy",
     "model": "gpt-4o-mini",
     "openai_api": "✓ Connected",
     "timestamp": "2025-12-23T16:00:00"
   }
   ```

2. **Open in Browser**
   ```
   https://mismatch-[random].amvera.io
   ```
   Should show MisMatch interface

3. **Test Resume Upload**
   - Click "Select File"
   - Upload a test resume PDF
   - Click "Analyze Resume"
   - Wait 15-30 seconds
   - Should display analysis results

## Troubleshooting

### Application doesn't start
- Check `Procfile` syntax: `web: uvicorn app:app --host 0.0.0.0 --port 8000`
- Check `requirements.txt` has all dependencies
- View logs in Amvera dashboard under "Logs" tab

### OpenAI API not working
- Verify `OPENAI_API_KEY` is correctly set in Environment Variables
- Key must start with `sk-proj-`
- Check key is not expired on platform.openai.com
- Test locally: `python app.py` with .env file

### Port issues
- Amvera automatically assigns port, Procfile must use `0.0.0.0`
- Never hardcode specific ports

### File upload not working
- Ensure `templates/` directory exists and is committed
- Ensure `static/` directory exists
- Check HTML form has `enctype="multipart/form-data"`

## After Deployment

### Share Your Application
- URL: `https://mismatch-[random].amvera.io`
- Share with:
  - Team members
  - Investors / stakeholders
  - Beta testers
  - Potential customers

### Monitor Performance
- Check logs regularly: Amvera Dashboard → Logs
- Monitor error rates
- Track API usage (OpenAI costs)

### Update Application

When you update code:

1. **Make changes locally**
   ```bash
   # Edit files
   git add .
   git commit -m "Update feature X"
   git push origin master
   ```

2. **Trigger Redeploy**
   - Amvera auto-deploys on GitHub push (if connected)
   - OR manually click "Redeploy" in dashboard
   - Wait 2-3 minutes

## Cost Information

### Amvera Pricing
- **Free tier**: Enough for development/demo
- **Production tier**: ~500₽/month (minimal)
- **High traffic**: Pay-as-you-go scaling

### OpenAI Costs
- **gpt-4o-mini**: ~$0.0015 per resume
- **Cost per user**: 
  - 100 resumes/month = $0.15
  - 1000 resumes/month = $1.50

## Security Best Practices

1. **Never commit .env file**
   - Use `.env.example` for template only
   - Set actual secrets in Amvera dashboard

2. **Rotate API keys regularly**
   - Update OpenAI key quarterly
   - Monitor usage for unauthorized access

3. **Enable Amvera access logs**
   - Check who accesses your app
   - Monitor traffic patterns

4. **Use HTTPS only**
   - Amvera provides free SSL/TLS
   - Always share https:// URLs

## Advanced: Custom Domain

To use your own domain (e.g., mismatch.company.com):

1. In Amvera Dashboard → Settings → Custom Domain
2. Add your domain
3. Follow DNS configuration steps
4. SSL certificate auto-generated

## Support & Resources

- **Amvera Docs**: https://amvera.ru/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **OpenAI API**: https://platform.openai.com/docs
- **GitHub Repo**: https://github.com/maksimmishakov/lamoda-ai-recruiter

## Checklist Before Going Live

- [ ] All files committed to GitHub
- [ ] OpenAI API key is valid
- [ ] requirements.txt has all dependencies
- [ ] Procfile syntax is correct
- [ ] .env file exists locally with real credentials
- [ ] .env is in .gitignore (not committed)
- [ ] App works locally: `python app.py`
- [ ] Health endpoint returns 200
- [ ] Resume upload works
- [ ] Analysis completes successfully
- [ ] No sensitive data in logs
- [ ] Custom domain configured (optional)

---

**Status**: ✅ Ready for Production Deployment
**Last Updated**: December 23, 2025
**Version**: 1.0 - Amvera Deployment Guide
