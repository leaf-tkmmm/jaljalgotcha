#!/bin/bash

# Test the /api/combinations endpoint with various parameters
# Make the script executable with: chmod +x test-api.sh

# Set the API base URL - change if deployed to a different host
API_BASE="https://jaljalgotcha.onrender.com:5000"

echo "===== Testing /api/combinations endpoint ====="

# Test 1: Basic request with duration in minutes
echo -e "\n\nTest 1: Basic request with duration in minutes (5 minutes)"
curl -G "${API_BASE}/api/combinations" \
  --data-urlencode "duration=5" \
  -s | jq .

# Test 2: With HH:MM:SS format
echo -e "\n\nTest 2: With HH:MM:SS format (00:10:30)"
curl -G "${API_BASE}/api/combinations" \
  --data-urlencode "duration=00:10:30" \
  -s | jq .


