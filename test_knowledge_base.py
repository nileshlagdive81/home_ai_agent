#!/usr/bin/env python3
"""
Test script for Real Estate Knowledge Base
"""

import requests
import json

def test_knowledge_base():
    """Test the knowledge base API endpoints"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Real Estate Knowledge Base API")
    print("=" * 50)
    
    # Test 1: Get knowledge categories
    print("\n1️⃣ Testing GET /api/v1/knowledge/categories")
    try:
        response = requests.get(f"{base_url}/api/v1/knowledge/categories")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {data['total_categories']} categories:")
            for category in data['categories']:
                print(f"   • {category}")
        else:
            print(f"❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Get knowledge suggestions
    print("\n2️⃣ Testing GET /api/v1/knowledge/suggestions")
    try:
        response = requests.get(f"{base_url}/api/v1/knowledge/suggestions")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {data['total_suggestions']} suggestions:")
            for suggestion in data['suggestions']:
                print(f"   • {suggestion}")
        else:
            print(f"❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Test knowledge queries
    test_queries = [
        "What is carpet area?",
        "What is RERA?",
        "How to apply for home loan?",
        "What documents are needed for home loan?",
        "What is stamp duty?",
        "Is real estate a good investment?",
        "How to calculate rental yield?",
        "What is built up area?",
        "What is super built up area?",
        "What is BHK?"
    ]
    
    print("\n3️⃣ Testing Knowledge Queries")
    print("-" * 30)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        try:
            response = requests.post(
                f"{base_url}/api/v1/knowledge/query",
                data={"query": query}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    print(f"   ✅ Found answer in category: {data['category']}")
                    print(f"   📊 Confidence: {data['confidence']:.2f}")
                    # Show first 100 characters of answer
                    answer_preview = data['answer'].replace('<br>', ' ').replace('<strong>', '').replace('</strong>', '')[:100]
                    print(f"   💡 Answer preview: {answer_preview}...")
                else:
                    print(f"   ⚠️  No exact match found")
                    print(f"   💡 Suggestions: {len(data['suggestions'])} available")
            else:
                print(f"   ❌ Failed with status {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Knowledge Base Testing Complete!")

if __name__ == "__main__":
    test_knowledge_base()
