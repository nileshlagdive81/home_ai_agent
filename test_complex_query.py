#!/usr/bin/env python3
"""
Script to test complex queries step by step
"""

import requests
import json

def test_complex_query():
    url = "http://localhost:8000/api/v1/search/nlp"
    
    # Test the complex query
    query = "Show me 3 BHK in Pune under 2.5 Crs with Gym and Metro station within 3 kms"
    
    print(f"Testing query: {query}")
    print("=" * 60)
    
    try:
        response = requests.post(
            url,
            data={"query": query},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Properties found: {len(data.get('properties', []))}")
            print(f"Full response: {json.dumps(data, indent=2)}")
        else:
            print(f"Error response: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_complex_query()
