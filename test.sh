#!/bin/bash
API_BASE="https://jaljalgotcha.onrender.com"
# API_BASE="http://localhost:5000"

echo "Test: 5分指定"
curl -G "${API_BASE}/api/combinations" \
  --data-urlencode "duration=5" \
  -s | jq .

echo "Test: HH:MM:SS指定"
curl -G "${API_BASE}/api/combinations" \
  --data-urlencode "duration=00:10:30" \
  -s | jq .
