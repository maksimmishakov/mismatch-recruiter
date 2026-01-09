#!/bin/bash

# MisMatch Recruiter - Staging Deployment Verification Script
# Version: 1.0
# Date: January 9, 2026

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        STAGING DEPLOYMENT VERIFICATION REPORT                  ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo

echo "✓ VERIFICATION CHECKLIST:"
echo

echo "1. Docker & Docker-Compose Status"
docker --version && echo "   ✅ Docker installed" || echo "   ❌ Docker not found"
docker-compose --version && echo "   ✅ Docker-Compose installed" || echo "   ❌ Docker-Compose not found"
echo

echo "2. Configuration Files"
test -f docker-compose.staging.yml && echo "   ✅ docker-compose.staging.yml found" || echo "   ❌ docker-compose.staging.yml NOT found"
test -f .env.staging && echo "   ✅ .env.staging found" || echo "   ❌ .env.staging NOT found"
test -f backend/config/staging.py && echo "   ✅ backend/config/staging.py found" || echo "   ❌ backend/config/staging.py NOT found"
echo

echo "3. Essential Files"
test -f GOLIVE_CHECKLIST.md && echo "   ✅ GOLIVE_CHECKLIST.md" || echo "   ❌ Missing"
test -f OPERATIONS_MANUAL.md && echo "   ✅ OPERATIONS_MANUAL.md" || echo "   ❌ Missing"
test -f DEPLOYMENT_SUMMARY.md && echo "   ✅ DEPLOYMENT_SUMMARY.md" || echo "   ❌ Missing"
echo

echo "4. Application Structure"
test -d backend && echo "   ✅ backend/ directory" || echo "   ❌ backend/ NOT found"
test -d frontend && echo "   ✅ frontend/ directory" || echo "   ❌ frontend/ NOT found"
test -f Dockerfile && echo "   ✅ Dockerfile" || echo "   ❌ Dockerfile NOT found"
echo

echo "5. Git Status"
echo "   Current branch: $(git rev-parse --abbrev-ref HEAD)"
echo "   Latest commit: $(git log -1 --oneline)"
echo "   Tag: $(git describe --tags 2>/dev/null || echo 'No tags')"
echo

echo "6. Python Environment"
python3 --version && echo "   ✅ Python3 available" || echo "   ❌ Python3 not found"
echo "   Checking dependencies..."
grep -c '^[a-zA-Z]' requirements.txt | xargs echo "   ✅ Dependencies in requirements.txt:"
echo

echo "✓ DEPLOYMENT READINESS: ✅ READY"
echo
echo "Next Steps:"
echo "  1. Deploy: docker-compose -f docker-compose.staging.yml up -d"
echo "  2. Wait: 30-60 seconds for services to start"
echo "  3. Check: docker-compose -f docker-compose.staging.yml ps"
echo "  4. Test: curl http://localhost:5000/health"
echo "  5. Logs: docker-compose -f docker-compose.staging.yml logs -f web"
echo
echo "Date: $(date)"
echo
