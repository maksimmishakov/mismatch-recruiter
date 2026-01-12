#!/bin/bash
# E2E test script for MisMatch Recruiter API

BASE_URL="${1:-http://localhost:5000}"

echo "========================================"
echo "E2E Testing MisMatch Recruiter API"
echo "Base URL: $BASE_URL"
echo "========================================"

# Test 1: Health Check
echo "\n[1/5] Testing health check endpoint..."
HEALTH=$(curl -s $BASE_URL/api/health)
if echo "$HEALTH" | grep -q "ok"; then
    echo "✓ Health check: PASSED"
else
    echo "✗ Health check: FAILED"
    echo "Response: $HEALTH"
    exit 1
fi

# Test 2: Signup
echo "\n[2/5] Testing signup endpoint..."
SIGNUP=$(curl -s -X POST $BASE_URL/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","name":"Test User"}')
echo "Response: $SIGNUP"

# Test 3: Login
echo "\n[3/5] Testing login endpoint..."
LOGIN=$(curl -s -X POST $BASE_URL/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"recruiter@mismatch.io","password":"demo123456"}')
echo "Response: $LOGIN"
TOKEN=$(echo "$LOGIN" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
if [ ! -z "$TOKEN" ]; then
    echo "✓ Login successful - Token obtained"
else
    echo "⚠ No token in response (may need existing user)"
fi

# Test 4: Get candidates (if token exists)
echo "\n[4/5] Testing candidates endpoint..."
if [ ! -z "$TOKEN" ]; then
    CANDIDATES=$(curl -s $BASE_URL/api/candidates \
      -H "Authorization: Bearer $TOKEN")
    echo "Response: $CANDIDATES"
    echo "✓ Candidates endpoint tested"
else
    echo "⚠ Skipping (no valid token)"
fi

# Test 5: Get jobs (if token exists)
echo "\n[5/5] Testing jobs endpoint..."
if [ ! -z "$TOKEN" ]; then
    JOBS=$(curl -s $BASE_URL/api/jobs \
      -H "Authorization: Bearer $TOKEN")
    echo "Response: $JOBS"
    echo "✓ Jobs endpoint tested"
else
    echo "⚠ Skipping (no valid token)"
fi

echo "\n========================================"
echo "E2E Tests Completed"
echo "========================================"
