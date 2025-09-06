#!/usr/bin/env python3
"""
Test the complete n8n workflow integration
Simulates how your frontend would call the storytelling workflow
"""

import requests
import json
import time

def test_n8n_workflow():
    """Test the complete storytelling workflow"""
    
    # First ensure our memory API is running
    try:
        health_response = requests.get("http://localhost:8000/health")
        if health_response.status_code != 200:
            print("❌ Memory API not running. Start with: docker-compose up -d")
            return
    except:
        print("❌ Cannot reach memory API at localhost:8000")
        return
    
    # Create a test child first (directly via API)
    child_data = {
        "name": "Emma",
        "age": 6,
        "reading_level": 2,
        "interests": ["unicorns", "magic", "friendship"]
    }
    
    child_response = requests.post("http://localhost:8000/children", json=child_data)
    if child_response.status_code != 200:
        print("❌ Failed to create test child")
        return
    
    child_id = child_response.json()["id"]
    print(f"✅ Created test child with ID: {child_id}")
    
    # Now test the n8n webhook (assuming you've imported the workflow)
    webhook_url = "http://localhost:5678/webhook/story-request"  # Adjust if different
    
    # Test story request
    story_request = {
        "child_id": child_id,
        "topic": "unicorn adventure",
        "request": "Tell me a story about a unicorn who learns to fly"
    }
    
    print(f"\n🔄 Sending story request to n8n webhook...")
    print(f"Request: {json.dumps(story_request, indent=2)}")
    
    try:
        # This would trigger your n8n workflow
        response = requests.post(webhook_url, json=story_request, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ n8n Workflow Success!")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
            # Verify story was saved to memory
            stories_response = requests.get(f"http://localhost:8000/stories/{child_id}")
            if stories_response.status_code == 200:
                stories = stories_response.json()
                print(f"✅ Found {len(stories)} stories in memory")
            
        else:
            print(f"❌ n8n Webhook failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectRefused:
        print("❌ Cannot reach n8n at localhost:5678")
        print("Make sure n8n is running and the webhook is active")
    except requests.exceptions.Timeout:
        print("❌ Request timed out - workflow might be taking too long")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_story_continuation(child_id):
    """Test continuing a previous story"""
    continuation_request = {
        "child_id": child_id,
        "topic": "unicorn adventure",
        "request": "continue the previous story"
    }
    
    webhook_url = "http://localhost:5678/webhook/story-request"
    
    print(f"\n🔄 Testing story continuation...")
    try:
        response = requests.post(webhook_url, json=continuation_request, timeout=30)
        if response.status_code == 200:
            print(f"✅ Story continuation successful!")
            result = response.json()
            print(f"New story starts with: {result.get('story', '')[:100]}...")
        else:
            print(f"❌ Continuation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 Testing n8n Storytelling Workflow Integration")
    print("Make sure both docker-compose and n8n workflow are running!\n")
    
    test_n8n_workflow()
    
    # Uncomment to test continuation after first story
    # print("\nWaiting 5 seconds before testing continuation...")  
    # time.sleep(5)
    # test_story_continuation(child_id)  # You'd need to pass the child_id