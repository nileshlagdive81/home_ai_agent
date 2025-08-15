#!/usr/bin/env python3
"""
Test script to test the search endpoint
"""

import requests
import json

def test_search():
    """Test the search endpoint with the complex query"""
    
    url = "http://localhost:8000/api/v1/search/nlp"
    
    # Test the complex query
    query = "2 BHK apartments under 2.5 Crs and with Gym and carpet area less than 1300"
    
    payload = {
        "query": query
    }
    
    print("Testing Search Endpoint:")
    print("=" * 60)
    print(f"Query: '{query}'")
    print(f"URL: {url}")
    print("-" * 40)
    
    try:
        response = requests.post(url, data=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search successful!")
            print(f"Results count: {len(data.get('results', []))}")
            
            # Show first few results
            results = data.get('results', [])
            for i, result in enumerate(results[:3]):  # Show first 3 results
                print(f"\nResult {i+1}:")
                print(f"  BHK: {result.get('bhk_count')}")
                print(f"  Price: ₹{result.get('sell_price', 0):,}")
                print(f"  Area: {result.get('carpet_area_sqft')} sqft")
                print(f"  City: {result.get('location', {}).get('city', 'N/A')}")
                print(f"  Locality: {result.get('location', {}).get('locality', 'N/A')}")
                
        else:
            print(f"❌ Search failed: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the backend is running on port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_search()
