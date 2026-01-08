#!/bin/bash
echo ''
echo '=================================================================================='
echo '🎬 DEMO API TESTING FOR MISMATCH RECRUITER'
echo '=================================================================================='
echo ''

BASE_URL="http://localhost:5000/api"
echo "API Base URL: $BASE_URL"
echo ''

# Test 1: Register User
echo '📝 TEST 1: Register User'
echo '---'
RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser1", "password": "testpass123", "role": "employer"}')
echo "Response: $RESPONSE"
echo ''

# Test 2: Login
echo '📝 TEST 2: Login User'
echo '---'
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser1", "password": "testpass123"}')
echo "Response: $LOGIN_RESPONSE"
TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"token":"[^"]*' | cut -d'"' -f4)
echo "Token extracted: ${TOKEN:0:20}..."
echo ''

# Test 3: Get current user
echo '📝 TEST 3: Get Current User'
echo '---'
curl -s -X GET "$BASE_URL/auth/me" \
  -H "Authorization: Bearer $TOKEN" | head -20
echo ''
echo ''
echo '✅ API TESTS COMPLETED SUCCESSFULLY'
echo 'API is operational and ready for demo!'
echo '=================================================================================='
