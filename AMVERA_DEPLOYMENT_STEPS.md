# 🚀 AMVERA DEPLOYMENT STEPS FOR MISMATCH-RECRUITER

## STEP 1.1: Login to Amvera

1. Go to https://amvera.io
2. Login with your credentials
3. If you don't have an account, create one first

## STEP 1.2: Create New Application

1. Click "Create Application" or "New Project"
2. Select "GitHub" as deployment source
3. Authorize GitHub access (if prompted)

## STEP 1.3: Configure GitHub Repository

1. Select repository: **maksimmishakov/mismatch-recruiter**
2. Select branch: **main** (not master)
3. Click "Connect" or "Continue"

## STEP 1.4: Configure Runtime & Deployment

1. Runtime: **Python 3.11**
2. Port: **8000** (or auto-detect from Procfile)
3. Amvera will automatically read:
   - Procfile (deployment command)
   - .amvera (configuration)
   - requirements.txt (dependencies)
   - .env (environment variables)

## STEP 1.5: Deploy

1. Review configuration
2. Click "Deploy" button
3. Wait for deployment (5-10 minutes)
4. Watch logs:
   - INFO Cloning repository...
   - INFO Installing dependencies...
   - INFO Starting application...
   - SUCCESS Application deployed

## STEP 1.6: Get Production URL

After deployment completes:
- Your application URL will be: **https://mismatch-recruiter-XXXXX.amvera.io**
- Replace XXXXX with your unique identifier
- Save this URL for LAMODA demo

## TROUBLESHOOTING

**If deployment fails:**
1. Check GitHub authentication
2. Verify branch is "main"
3. Check logs for errors
4. Try redeploying from Amvera dashboard

**If API returns 502 Bad Gateway:**
1. Wait 1-2 minutes for application to start
2. Try again or redeploy
3. Check database connection in logs

