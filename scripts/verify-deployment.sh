#!/bin/bash
# Deployment verification script

ENVIRONMENT=${1:-staging}

if [ "$ENVIRONMENT" = "staging" ]; then
  API_URL="https://staging-api.mismatch-recruiter.ru"
  APP_URL="https://staging.mismatch-recruiter.ru"
elif [ "$ENVIRONMENT" = "production" ]; then
  API_URL="https://api.mismatch-recruiter.ru"
  APP_URL="https://app.mismatch-recruiter.ru"
else
  echo "Usage: $0 staging|production"
  exit 1
fi

echo "Verifying deployment for $ENVIRONMENT"

echo "=== WEB ENDPOINT TESTS ==="
echo -n "Testing API Health... "
if curl -sf "$API_URL/api/health" > /dev/null; then
  echo "PASS"
else
  echo "FAIL"
  exit 1
fi

echo -n "Testing Frontend... "
if curl -sf "$APP_URL" > /dev/null; then
  echo "PASS"
else
  echo "FAIL"
  exit 1
fi

echo "=== API ENDPOINT TESTS ==="
echo -n "Testing GET /api/candidates... "
if curl -sf "$API_URL/api/candidates" > /dev/null; then
  echo "PASS"
else
  echo "FAIL"
fi

echo ""
echo "All checks passed!"
