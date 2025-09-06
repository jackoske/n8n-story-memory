# Storytelling AI Memory System for n8n

A simple 3-table memory database that integrates with n8n workflows for adaptive children's storytelling.

## Quick Start

1. **Set up environment:**

   ```bash
   cp .env.example .env
   # Add your OpenAI API key to .env
   ```

2. **Start the system:**

   ```bash
   docker-compose up -d
   ```

3. **Access services:**
   - Memory API: http://localhost:8000
   - Database: localhost:5432

## API Endpoints

### Child Management

- `POST /children` - Create child profile
- `GET /children/{id}` - Get child profile

### Story Memory

- `POST /stories` - Save story with embedding
- `GET /stories/{child_id}` - Get all child's stories
- `GET /stories/latest/{child_id}` - Get latest story
- `GET /stories/search?child_id=1&query=dragons` - Search stories

### Feedback & Progress

- `POST /feedback` - Save story feedback
- `GET /progress/{child_id}` - Get reading progress

## n8n Workflow Integration

### Example: Story Generation with Memory

1. **Webhook Trigger** - Receives story request
2. **Get Child Profile** - Fetch child's interests/reading level
3. **Search Past Stories** - Find related previous stories
4. **Generate Story** - OpenAI creates new story with context
5. **Save to Memory** - Store story with embedding
6. **Respond** - Return story to user

### Example Request:

```json
{
  "child_id": 1,
  "topic": "dragons and friendship",
  "request": "continue the adventure"
}
```

### Example Response:

```json
{
  "story": "Once upon a time, Luna the dragon...",
  "story_id": 42,
  "difficulty": 3
}
```

## Database Schema

**children**: `id, name, age, reading_level, interests[]`
**stories**: `id, child_id, story_text, difficulty, summary, keywords[], embedding`
**feedback**: `id, story_id, child_id, rating, comprehension_score`

## Memory Features

- **Semantic Search**: Find similar stories using OpenAI embeddings
- **Keyword Matching**: Search by themes, characters, topics
- **Adaptive Difficulty**: Auto-adjust reading level based on comprehension
- **Story Continuity**: Connect new stories to past adventures

## Development

```bash
# API only
uvicorn main:app --reload

# Database migrations
docker exec -it n8n_postgres_1 psql -U storyuser -d storydb -f /docker-entrypoint-initdb.d/init.sql

# View logs
docker-compose logs -f memory-api
```

