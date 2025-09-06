-- Simple 3-table schema for storytelling AI memory

-- Enable vector extension for embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Children profiles
CREATE TABLE children (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    age INT,
    reading_level INT DEFAULT 1,
    interests TEXT[],
    created_at TIMESTAMP DEFAULT NOW()
);

-- Stories with memory
CREATE TABLE stories (
    id SERIAL PRIMARY KEY,
    child_id INT REFERENCES children(id),
    story_text TEXT NOT NULL,
    difficulty INT,
    summary TEXT,
    keywords TEXT[],
    created_at TIMESTAMP DEFAULT NOW(),
    embedding vector(1536)  -- Optional: for semantic search
);

-- Feedback and progress
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    story_id INT REFERENCES stories(id),
    child_id INT REFERENCES children(id),
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comprehension_score INT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_stories_child_id ON stories(child_id);
CREATE INDEX idx_stories_keywords ON stories USING GIN(keywords);
CREATE INDEX idx_feedback_child_id ON feedback(child_id);