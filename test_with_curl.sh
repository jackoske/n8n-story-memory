#!/bin/bash
# Simple curl-based testing for the memory API
# Run this after starting docker-compose up -d

API_BASE="http://localhost:8000"
echo "🚀 Testing Memory API with curl..."

# Test 1: Health Check
echo -e "\n1️⃣ Health Check:"
curl -s "$API_BASE/health" | jq '.'

# Test 2: Create Child
echo -e "\n2️⃣ Create Child:"
CHILD_RESPONSE=$(curl -s -X POST "$API_BASE/children" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bob", 
    "age": 8, 
    "reading_level": 3,
    "interests": ["pirates", "treasure", "ocean"]
  }')
echo $CHILD_RESPONSE | jq '.'
CHILD_ID=$(echo $CHILD_RESPONSE | jq -r '.id')

# Test 3: Get Child
echo -e "\n3️⃣ Get Child Profile:"
curl -s "$API_BASE/children/$CHILD_ID" | jq '.'

# Test 4: Save Story
echo -e "\n4️⃣ Save Story:"
STORY_RESPONSE=$(curl -s -X POST "$API_BASE/stories" \
  -H "Content-Type: application/json" \
  -d "{
    \"child_id\": $CHILD_ID,
    \"story_text\": \"Captain Bob sailed the seven seas looking for treasure. His ship was fast and his crew was brave...\",
    \"difficulty\": 3,
    \"summary\": \"Captain Bob searches for treasure with his brave crew\",
    \"keywords\": [\"pirates\", \"treasure\", \"ship\", \"adventure\"]
  }")
echo $STORY_RESPONSE | jq '.'
STORY_ID=$(echo $STORY_RESPONSE | jq -r '.id')

# Test 5: Search Stories  
echo -e "\n5️⃣ Search Stories:"
curl -s "$API_BASE/stories/search?child_id=$CHILD_ID&query=treasure" | jq '.'

# Test 6: Get Latest Story
echo -e "\n6️⃣ Get Latest Story:"
curl -s "$API_BASE/stories/latest/$CHILD_ID" | jq '.'

# Test 7: Save Feedback
echo -e "\n7️⃣ Save Feedback:"
curl -s -X POST "$API_BASE/feedback" \
  -H "Content-Type: application/json" \
  -d "{
    \"story_id\": $STORY_ID,
    \"child_id\": $CHILD_ID,
    \"rating\": 4,
    \"comprehension_score\": 90
  }" | jq '.'

# Test 8: Get Progress
echo -e "\n8️⃣ Get Progress:"
curl -s "$API_BASE/progress/$CHILD_ID" | jq '.'

echo -e "\n✅ All tests completed!"