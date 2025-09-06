# Storytelling Memory API Documentation

## Authentication
All endpoints (except `/health`) require Bearer token authentication:
```
API_KEY=your-secret-api-key-here
```

Include in headers:
```
Authorization: Bearer your-secret-api-key-here
Content-Type: application/json
```

## Base URL
```
https://jackskehan.tech/storyAPI
```

---

## Endpoints

### Health Check
**GET** `/health`
- **Description:** Check if API is running
- **Authentication:** None required
- **Response:** `{"status": "healthy"}`

---

### Child Management

**POST** `/children`
- **Description:** Create a new child profile
- **Authentication:** Required
- **Body:**
```json
{
  "name": "Alice",
  "age": 7,
  "reading_level": 2,
  "interests": ["dragons", "friendship", "adventure"]
}
```
- **Response:** `{"id": 1, "message": "Child profile created"}`

**GET** `/children/{child_id}`
- **Description:** Get child profile by ID
- **Authentication:** Required
- **Response:** Child profile with ID, name, age, reading_level, interests, created_at

---

### Story Management

**POST** `/stories`
- **Description:** Save a new story with AI-generated embedding
- **Authentication:** Required
- **Body:**
```json
{
  "child_id": 1,
  "story_text": "Once upon a time...",
  "difficulty": 2,
  "summary": "A brief summary",
  "keywords": ["adventure", "friendship"]
}
```
- **Response:** `{"id": 1, "message": "Story saved"}`

**GET** `/stories/{child_id}`
- **Description:** Get all stories for a child (default limit: 10)
- **Authentication:** Required
- **Query Params:** `?limit=10` (optional)
- **Response:** Array of story objects

**GET** `/stories/latest/{child_id}`
- **Description:** Get the most recent story for a child
- **Authentication:** Required
- **Response:** Single story object

**GET** `/stories/search`
- **Description:** Search stories by keywords or semantic similarity
- **Authentication:** Required
- **Query Params:** 
  - `child_id` (required)
  - `query` (optional) - search term
  - `limit` (optional, default: 5)
- **Response:** Array of matching stories

---

### Feedback & Progress

**POST** `/feedback`
- **Description:** Save story feedback and update child's reading level
- **Authentication:** Required
- **Body:**
```json
{
  "story_id": 1,
  "child_id": 1,
  "rating": 5,
  "comprehension_score": 85
}
```
- **Response:** `{"id": 1, "message": "Feedback saved"}`

**GET** `/progress/{child_id}`
- **Description:** Get reading progress summary for a child
- **Authentication:** Required
- **Response:**
```json
{
  "child": {...},
  "stats": {
    "story_count": 5,
    "avg_rating": 4.2,
    "avg_comprehension": 78.5
  }
}
```

---

## Example Usage

### Python
```python
import requests

headers = {
    "Authorization": "Bearer your-secret-api-key-here",
    "Content-Type": "application/json"
}

# Create child
response = requests.post(
    "https://jackskehan.tech/storyAPI/children",
    json={"name": "Alice", "age": 7, "reading_level": 2, "interests": ["dragons"]},
    headers=headers
)
child_id = response.json()["id"]

# Save story
response = requests.post(
    "https://jackskehan.tech/storyAPI/stories",
    json={
        "child_id": child_id,
        "story_text": "Once upon a time...",
        "difficulty": 2,
        "summary": "Adventure story",
        "keywords": ["adventure", "magic"]
    },
    headers=headers
)
```

### cURL
```bash
# Health check (no auth needed)
curl https://jackskehan.tech/storyAPI/health

# Create child (with auth)
curl -X POST https://jackskehan.tech/storyAPI/children \
  -H "Authorization: Bearer your-secret-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "age": 7, "reading_level": 2, "interests": ["dragons"]}'

# Get stories
curl -X GET "https://jackskehan.tech/storyAPI/stories/1?limit=5" \
  -H "Authorization: Bearer your-secret-api-key-here"
```

---

## Error Responses

**401 Unauthorized**
```json
{"detail": "Invalid API key"}
```

**400 Bad Request**
```json
{"detail": "Error description"}
```

**422 Unprocessable Entity**
```json
{"detail": "Validation error details"}
```