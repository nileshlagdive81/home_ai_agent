#!/usr/bin/env python3
"""
Script to test the backend API endpoint directly
"""

import requests
import json

def test_backend_api():
    """Test the backend API endpoint directly"""
    print("🧪 TESTING BACKEND API ENDPOINT")
    print("=" * 60)
    
    # Test the specific query
    query = "3 BHK apartments in Pune above 1.5 crores with gym, located within 3 km of metro station"
    
    print(f"1️⃣ SENDING QUERY: {query}")
    print("-" * 40)
    
    try:
        # Send request to backend
        response = requests.post(
            "http://localhost:8000/search",
            json={"query": query},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   📊 Response Status: {response.status_code}")
        print(f"   📊 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n2️⃣ RESPONSE DATA:")
            print("-" * 40)
            print(f"   📊 Response Type: {type(data)}")
            print(f"   📊 Response Keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            
            if isinstance(data, dict):
                if 'properties' in data:
                    properties = data['properties']
                    print(f"   📊 Properties Count: {len(properties)}")
                    print(f"   📊 Properties Type: {type(properties)}")
                    
                    if properties:
                        print(f"\n3️⃣ SAMPLE PROPERTIES:")
                        print("-" * 40)
                        for i, prop in enumerate(properties[:3]):  # Show first 3
                            print(f"   Property {i+1}:")
                            for key, value in prop.items():
                                print(f"      {key}: {value}")
                    else:
                        print("   ❌ No properties in response")
                else:
                    print(f"   📊 Full Response: {json.dumps(data, indent=2)}")
            else:
                print(f"   📊 Raw Response: {data}")
        else:
            print(f"   ❌ Error Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Connection Error: Backend server not running")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_backend_api()
