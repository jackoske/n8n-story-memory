-- Storytelling AI Memory Database Schema
-- PostgreSQL with pgvector extension for semantic search

-- Enable pgvector extension for embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Children/User profiles
CREATE TABLE children (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INTEGER CHECK (age > 0 AND age < 18),
    reading_level INTEGER DEFAULT 1 CHECK (reading_level BETWEEN 1 AND 10),
    interests TEXT[], -- Array of interests like ['dragons', 'friendship', 'adventure']
    preferred_story_length VARCHAR(20) DEFAULT 'medium', -- short, medium, long
    personality_traits TEXT[], -- ['curious', 'brave', 'creative']
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Stories with memory and context
CREATE TABLE stories (
    id SERIAL PRIMARY KEY,
    child_id INTEGER REFERENCES children(id) ON DELETE CASCADE,
    title VARCHAR(200),
    story_text TEXT NOT NULL,
    difficulty_level INTEGER CHECK (difficulty_level BETWEEN 1 AND 10),
    story_type VARCHAR(50), -- 'original', 'continuation', 'remix'
    parent_story_id INTEGER REFERENCES stories(id), -- For continuations
    summary TEXT, -- Brief summary for context
    characters TEXT[], -- Main characters mentioned
    themes TEXT[], -- Story themes/topics
    keywords TEXT[], -- Searchable keywords
    word_count INTEGER,
    estimated_read_time INTEGER, -- in minutes
    story_embedding vector(1536), -- OpenAI embeddings for semantic search
    metadata JSONB, -- Flexible additional data
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Story interactions and feedback
CREATE TABLE story_interactions (
    id SERIAL PRIMARY KEY,
    story_id INTEGER REFERENCES stories(id) ON DELETE CASCADE,
    child_id INTEGER REFERENCES children(id) ON DELETE CASCADE,
    interaction_type VARCHAR(50), -- 'completed', 'liked', 'continued', 'skipped'
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    comprehension_score INTEGER CHECK (comprehension_score BETWEEN 0 AND 100),
    engagement_level VARCHAR(20), -- 'low', 'medium', 'high'
    feedback_text TEXT,
    time_spent INTEGER, -- seconds spent reading/listening
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Conversation context for multi-turn stories
CREATE TABLE story_conversations (
    id SERIAL PRIMARY KEY,
    child_id INTEGER REFERENCES children(id) ON DELETE CASCADE,
    conversation_id UUID DEFAULT gen_random_uuid(),
    story_id INTEGER REFERENCES stories(id),
    turn_number INTEGER,
    user_input TEXT,
    ai_response TEXT,
    context_data JSONB, -- Store conversation state
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Memory associations (for connecting related stories/themes)
CREATE TABLE memory_associations (
    id SERIAL PRIMARY KEY,
    child_id INTEGER REFERENCES children(id) ON DELETE CASCADE,
    source_story_id INTEGER REFERENCES stories(id) ON DELETE CASCADE,
    target_story_id INTEGER REFERENCES stories(id) ON DELETE CASCADE,
    association_type VARCHAR(50), -- 'similar_theme', 'character_reference', 'continuation'
    strength FLOAT DEFAULT 1.0, -- How strong the association is
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Progress tracking
CREATE TABLE reading_progress (
    id SERIAL PRIMARY KEY,
    child_id INTEGER REFERENCES children(id) ON DELETE CASCADE,
    date DATE DEFAULT CURRENT_DATE,
    stories_completed INTEGER DEFAULT 0,
    total_words_read INTEGER DEFAULT 0,
    average_comprehension FLOAT,
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    achievements TEXT[], -- Array of unlocked achievements
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(child_id, date)
);

-- Indexes for performance
CREATE INDEX idx_stories_child_id ON stories(child_id);
CREATE INDEX idx_stories_created_at ON stories(created_at);
CREATE INDEX idx_stories_difficulty ON stories(difficulty_level);
CREATE INDEX idx_stories_keywords ON stories USING GIN(keywords);
CREATE INDEX idx_stories_themes ON stories USING GIN(themes);
CREATE INDEX idx_stories_embedding ON stories USING ivfflat (story_embedding vector_cosine_ops);

CREATE INDEX idx_interactions_child_story ON story_interactions(child_id, story_id);
CREATE INDEX idx_interactions_type ON story_interactions(interaction_type);

CREATE INDEX idx_conversations_child_id ON story_conversations(child_id);
CREATE INDEX idx_conversations_conversation_id ON story_conversations(conversation_id);

CREATE INDEX idx_associations_child_id ON memory_associations(child_id);
CREATE INDEX idx_progress_child_date ON reading_progress(child_id, date);

-- Triggers for updating timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_children_updated_at BEFORE UPDATE ON children
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_progress_updated_at BEFORE UPDATE ON reading_progress
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();