# MisMatch Recruiter - Launch Instructions

## Pre-Launch Verification (24 hours before)

### Step 1: Local Testing
```bash
# Navigate to project
cd /workspaces/mismatch-recruiter

# Install dependencies
cd frontend && npm install

# Run tests
npm run test

# Check coverage
npm run test:coverage

# Build production
npm run build

# Verify no errors
npm run lint
```

### Step 2: Security Verification
```bash
# Check dependencies
npm audit

# Review security findings
npm audit --json > audit-report.json

# Verify no critical vulnerabilities
```

### Step 3: Docker Verification
```bash
# Build Docker image
docker build -t mismatch-recruiter:latest .

# Test Docker image locally
docker run -p 3000:3000 mismatch-recruiter:latest

# Verify on http://localhost:3000
```

### Step 4: Environment Setup
```bash
# Configure production environment variables
# In GitHub repository settings:
# Settings > Secrets > Actions

# Add secrets:
AMVERA_TOKEN = your-actual-token-here

# Verify in .env.example
cat .env.example
```

## Launch Day (Main Branch Push)

### Step 1: Create Release Branch
```bash
# Create release branch
git checkout -b release/v1.0.0

# Update version in package.json if needed
# Then commit changes
git add .
git commit -m "Release: v1.0.0 - Production Ready"

# Push release branch
git push origin release/v1.0.0
```

### Step 2: Merge to Main
```bash
# Switch to main branch
git checkout main

# Pull latest
git pull origin main

# Merge release branch
git merge release/v1.0.0

# Push to main - THIS TRIGGERS GITHUB ACTIONS
git push origin main
```

### Step 3: Monitor CI/CD Pipeline
```bash
# Go to GitHub repository
# Navigate to Actions tab
# Watch CI/CD Pipeline:
# 1. test job (run tests)
# 2. lint job (code quality)
# 3. security job (vulnerability scan)
# 4. deploy job (push to Amvera)

# All jobs must pass before deploy executes
```

### Step 4: Verify Deployment
```bash
# After GitHub Actions completes:
# Visit: https://mismatch-recruiter-maksimisakov.amvera.io

# Perform smoke tests:
# 1. Page loads without errors
# 2. Navigation works (Candidates, Jobs, Matches)
# 3. Search/filter functionality works
# 4. Dark mode toggle works
# 5. Mobile responsive (use DevTools)
# 6. Console shows no critical errors

# Check browser console (F12 > Console):
# Should show no red error messages
```

### Step 5: Create Release Tag
```bash
# Create annotated tag
git tag -a v1.0.0 -m "Production Release v1.0.0"

# Push tag to GitHub
git push origin v1.0.0

# View releases
# Go to GitHub > Releases > Create release from v1.0.0
```

## Post-Launch Verification

### Hour 1-2: Immediate Monitoring
- [ ] Verify live URL accessible
- [ ] Check error rate (should be < 0.1%)
- [ ] Review server logs
- [ ] Test critical user flows
- [ ] Monitor browser console

### Day 1: Full Testing
- [ ] All pages load correctly
- [ ] Search functionality works
- [ ] Mobile experience is smooth
- [ ] Dark mode functions properly
- [ ] No 404 errors
- [ ] No security warnings
- [ ] Performance is acceptable (< 2s TTI)

### Day 2-3: Performance Review
- [ ] Monitor Lighthouse score
- [ ] Review PageSpeed Insights
- [ ] Check Core Web Vitals
- [ ] Analyze user sessions
- [ ] Review error logs

### Weekly: Ongoing Monitoring
- [ ] Uptime: 99.9%
- [ ] Error rate: < 0.1%
- [ ] Response time: < 500ms
- [ ] Security: Zero vulnerabilities
- [ ] Update dependencies

## Rollback Procedure (If Needed)

### Quick Rollback
```bash
# Get previous stable commit
git log --oneline -5

# Reset to previous version
git reset --hard <previous-commit-hash>

# Force push to main
git push origin main --force-with-lease

# GitHub Actions will redeploy previous version
```

### Alternative: Deploy from Tag
```bash
# If using tags
git checkout v0.9.9  # Previous release tag
git push origin v0.9.9:main --force-with-lease
```

## Success Indicators

### ✅ Launch Successful When:
- [ ] URL accessible globally
- [ ] All tests passing
- [ ] Lighthouse score: 90+
- [ ] Error rate: < 0.1%
- [ ] Page load: < 2s
- [ ] Mobile experience: Excellent
- [ ] No critical issues in console
- [ ] Security audit: Passed
- [ ] Uptime: 99.9%+

### ⚠️ Rollback If:
- [ ] Critical errors in logs
- [ ] Page not loading
- [ ] API connections failing
- [ ] Security vulnerabilities found
- [ ] Performance degradation
- [ ] Database connectivity issues

## Support Contacts

- **Developer**: Maksim Isimisakov
- **Repository**: https://github.com/maksimisakov/mismatch-recruiter
- **Live Demo**: https://mismatch-recruiter-maksimisakov.amvera.io
- **Amvera Panel**: https://amvera.io/dashboard

## Useful Commands

```bash
# View live logs
# Go to Amvera Dashboard > Application > Logs

# Restart application
# Through Amvera Dashboard > Application > Restart

# View metrics
# Through Amvera Dashboard > Application > Metrics

# Access admin panel
https://mismatch-recruiter-maksimisakov.amvera.io/admin-dashboard
```

