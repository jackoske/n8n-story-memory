#!/usr/bin/env python3
"""
Simple test script to validate the memory API functionality
Run this after starting docker-compose to verify everything works
"""

import requests
import json

API_BASE = "http://localhost:8001"
API_KEY = "your-secret-api-key-here"  # Should match API_KEY in .env

# Headers with authentication
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_health():
    """Test if API is running"""
    try:
        response = requests.get(f"{API_BASE}/health")
        print(f"✅ Health Check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
        return False

def test_create_child():
    """Test creating a child profile"""
    child_data = {
        "name": "Alice",
        "age": 7,
        "reading_level": 2,
        "interests": ["dragons", "friendship", "adventure"]
    }
    
    try:
        response = requests.post(f"{API_BASE}/children", json=child_data, headers=headers)
        print(f"✅ Create Child: {response.status_code} - {response.json()}")
        return response.json().get("id") if response.status_code == 200 else None
    except Exception as e:
        print(f"❌ Create Child Failed: {e}")
        return None

def test_get_child(child_id):
    """Test getting child profile"""
    try:
        response = requests.get(f"{API_BASE}/children/{child_id}", headers=headers)
        print(f"✅ Get Child: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Get Child Failed: {e}")
        return False

def test_save_story(child_id):
    """Test saving a story"""
    story_data = {
        "child_id": child_id,
        "story_text": "Once upon a time, there was a friendly dragon named Spark who loved making new friends. One day, Spark met a little girl who was scared of dragons...",
        "difficulty": 2,
        "summary": "A friendly dragon named Spark makes friends with a scared little girl",
        "keywords": ["dragon", "friendship", "brave", "Spark"]
    }
    
    try:
        response = requests.post(f"{API_BASE}/stories", json=story_data, headers=headers)
        print(f"✅ Save Story: {response.status_code} - {response.json()}")
        return response.json().get("id") if response.status_code == 200 else None
    except Exception as e:
        print(f"❌ Save Story Failed: {e}")
        return None

def test_search_stories(child_id):
    """Test searching stories"""
    try:
        # Test keyword search
        response = requests.get(f"{API_BASE}/stories/search", params={
            "child_id": child_id,
            "query": "dragon friendship"
        }, headers=headers)
        print(f"✅ Search Stories: {response.status_code} - Found {len(response.json())} stories")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Search Stories Failed: {e}")
        return False

def test_save_feedback(story_id, child_id):
    """Test saving feedback"""
    feedback_data = {
        "story_id": story_id,
        "child_id": child_id,
        "rating": 5,
        "comprehension_score": 85
    }
    
    try:
        response = requests.post(f"{API_BASE}/feedback", json=feedback_data, headers=headers)
        print(f"✅ Save Feedback: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Save Feedback Failed: {e}")
        return False

def test_get_progress(child_id):
    """Test getting progress"""
    try:
        response = requests.get(f"{API_BASE}/progress/{child_id}", headers=headers)
        print(f"✅ Get Progress: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Get Progress Failed: {e}")
        return False

def run_all_tests():
    """Run complete test suite"""
    print("🚀 Starting API Tests...\n")
    
    # Test 1: Health check
    if not test_health():
        print("❌ API not running. Start with: docker-compose up -d")
        return
    
    # Test 2: Create child
    child_id = test_create_child()
    if not child_id:
        print("❌ Cannot continue without child ID")
        return
    
    # Test 3: Get child
    test_get_child(child_id)
    
    # Test 4: Save story
    story_id = test_save_story(child_id)
    if not story_id:
        print("❌ Cannot continue without story ID")
        return
    
    # Test 5: Search stories
    test_search_stories(child_id)
    
    # Test 6: Save feedback
    test_save_feedback(story_id, child_id)
    
    # Test 7: Get progress
    test_get_progress(child_id)
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    run_all_tests()