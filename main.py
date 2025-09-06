from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
import asyncpg
import os
from dotenv import load_dotenv
import openai
import numpy as np

load_dotenv()

app = FastAPI(title="Storytelling Memory API", version="1.0.0")

# Security
security = HTTPBearer()
API_KEY = os.getenv("API_KEY", "your-secret-api-key-here")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return True

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/storydb")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Pydantic models
class Child(BaseModel):
    name: str
    age: int
    reading_level: int = 1
    interests: List[str] = []

class Story(BaseModel):
    child_id: int
    story_text: str
    difficulty: int
    summary: str
    keywords: List[str]

class Feedback(BaseModel):
    story_id: int
    child_id: int
    rating: int
    comprehension_score: int

class StorySearch(BaseModel):
    child_id: int
    query: Optional[str] = None
    keywords: Optional[List[str]] = None

# Database connection pool
async def get_db():
    return await asyncpg.connect(DATABASE_URL)

# Helper functions
async def get_embedding(text: str):
    """Generate embedding for semantic search"""
    try:
        response = await openai.embeddings.acreate(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

# API Endpoints

@app.post("/children")
async def create_child(child: Child, _: bool = Depends(verify_token)):
    """Create a new child profile"""
    conn = await get_db()
    try:
        query = """
            INSERT INTO children (name, age, reading_level, interests) 
            VALUES ($1, $2, $3, $4) RETURNING id
        """
        child_id = await conn.fetchval(
            query, child.name, child.age, child.reading_level, child.interests
        )
        return {"id": child_id, "message": "Child profile created"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await conn.close()

@app.get("/children/{child_id}")
async def get_child(child_id: int, _: bool = Depends(verify_token)):
    """Get child profile"""
    conn = await get_db()
    try:
        query = "SELECT * FROM children WHERE id = $1"
        child = await conn.fetchrow(query, child_id)
        if not child:
            raise HTTPException(status_code=404, detail="Child not found")
        return dict(child)
    finally:
        await conn.close()

@app.post("/stories")
async def save_story(story: Story, _: bool = Depends(verify_token)):
    """Save a new story with embedding"""
    conn = await get_db()
    try:
        # Generate embedding for the story
        embedding_text = f"{story.summary} {' '.join(story.keywords)}"
        embedding = await get_embedding(embedding_text)
        
        query = """
            INSERT INTO stories (child_id, story_text, difficulty, summary, keywords, embedding) 
            VALUES ($1, $2, $3, $4, $5, $6) RETURNING id
        """
        story_id = await conn.fetchval(
            query, story.child_id, story.story_text, story.difficulty, 
            story.summary, story.keywords, embedding
        )
        return {"id": story_id, "message": "Story saved"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await conn.close()

@app.get("/stories/{child_id}")
async def get_child_stories(child_id: int, limit: int = 10, _: bool = Depends(verify_token)):
    """Get all stories for a child"""
    conn = await get_db()
    try:
        query = """
            SELECT id, story_text, difficulty, summary, keywords, created_at 
            FROM stories WHERE child_id = $1 
            ORDER BY created_at DESC LIMIT $2
        """
        stories = await conn.fetch(query, child_id, limit)
        return [dict(story) for story in stories]
    finally:
        await conn.close()

@app.get("/stories/latest/{child_id}")
async def get_latest_story(child_id: int, _: bool = Depends(verify_token)):
    """Get the latest story for a child"""
    conn = await get_db()
    try:
        query = """
            SELECT * FROM stories WHERE child_id = $1 
            ORDER BY created_at DESC LIMIT 1
        """
        story = await conn.fetchrow(query, child_id)
        if not story:
            raise HTTPException(status_code=404, detail="No stories found")
        return dict(story)
    finally:
        await conn.close()

@app.get("/stories/search")
async def search_stories(child_id: int, query: Optional[str] = None, limit: int = 5, _: bool = Depends(verify_token)):
    """Search stories by keywords or semantic similarity"""
    conn = await get_db()
    try:
        if query:
            # Semantic search using embeddings
            query_embedding = await get_embedding(query)
            if query_embedding:
                search_query = """
                    SELECT *, embedding <=> $1 as similarity 
                    FROM stories WHERE child_id = $2 
                    ORDER BY similarity LIMIT $3
                """
                stories = await conn.fetch(search_query, query_embedding, child_id, limit)
            else:
                # Fallback to keyword search
                search_query = """
                    SELECT * FROM stories WHERE child_id = $1 
                    AND (keywords && $2 OR summary ILIKE $3)
                    ORDER BY created_at DESC LIMIT $4
                """
                keywords = [query]
                like_query = f"%{query}%"
                stories = await conn.fetch(search_query, child_id, keywords, like_query, limit)
        else:
            # Return recent stories
            search_query = """
                SELECT * FROM stories WHERE child_id = $1 
                ORDER BY created_at DESC LIMIT $2
            """
            stories = await conn.fetch(search_query, child_id, limit)
        
        return [dict(story) for story in stories]
    finally:
        await conn.close()

@app.post("/feedback")
async def save_feedback(feedback: Feedback, _: bool = Depends(verify_token)):
    """Save story feedback and update reading level"""
    conn = await get_db()
    try:
        # Save feedback
        feedback_query = """
            INSERT INTO feedback (story_id, child_id, rating, comprehension_score) 
            VALUES ($1, $2, $3, $4) RETURNING id
        """
        feedback_id = await conn.fetchval(
            feedback_query, feedback.story_id, feedback.child_id, 
            feedback.rating, feedback.comprehension_score
        )
        
        # Update reading level if comprehension is high
        if feedback.comprehension_score > 80:
            update_query = """
                UPDATE children SET reading_level = reading_level + 1 
                WHERE id = $1 AND reading_level < 10
            """
            await conn.execute(update_query, feedback.child_id)
        
        return {"id": feedback_id, "message": "Feedback saved"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await conn.close()

@app.get("/progress/{child_id}")
async def get_progress(child_id: int, _: bool = Depends(verify_token)):
    """Get reading progress summary"""
    conn = await get_db()
    try:
        # Get child info
        child_query = "SELECT * FROM children WHERE id = $1"
        child = await conn.fetchrow(child_query, child_id)
        
        # Get story count and average feedback
        stats_query = """
            SELECT 
                COUNT(s.id) as story_count,
                AVG(f.rating) as avg_rating,
                AVG(f.comprehension_score) as avg_comprehension
            FROM stories s
            LEFT JOIN feedback f ON s.id = f.story_id
            WHERE s.child_id = $1
        """
        stats = await conn.fetchrow(stats_query, child_id)
        
        return {
            "child": dict(child) if child else None,
            "stats": dict(stats) if stats else None
        }
    finally:
        await conn.close()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)