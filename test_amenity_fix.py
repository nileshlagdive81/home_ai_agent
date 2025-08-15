#!/usr/bin/env python3
"""
Script to test if the amenity filter is now working correctly
"""

import requests
import json

def test_amenity_fix():
    """Test if the amenity filter is now working correctly"""
    print("🧪 TESTING AMENITY FILTER FIX")
    print("=" * 50)
    
    # Test the exact query that should return 3 properties
    test_query = "2 BHK apartments in Pune under 1.5 crores with gym"
    
    print(f"🔍 Testing query: '{test_query}'")
    
    try:
        # Make request to the backend
        response = requests.post(
            "http://localhost:8000/api/v1/search/nlp",
            data={"query": test_query}
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ Backend response received")
            print(f"📊 Results count: {result.get('results_count', 0)}")
            print(f"🎯 Intent: {result.get('intent', 'Unknown')}")
            print(f"🔍 Extracted entities: {json.dumps(result.get('extracted_entities', {}), indent=2)}")
            
            # Show the actual results
            results = result.get('results', [])
            print(f"\n🏠 Properties returned:")
            
            if results:
                for i, prop in enumerate(results, 1):
                    project_name = prop.get('project', {}).get('name', 'Unknown')
                    locality = prop.get('location', {}).get('locality', 'Unknown')
                    city = prop.get('location', {}).get('city', 'Unknown')
                    price = prop.get('sell_price', 0)
                    bhk = prop.get('bhk_count', 0)
                    
                    price_lakhs = price / 100000 if price else 0
                    print(f"   {i}. {project_name} | {locality} ({city}) | {bhk} BHK | ₹{price_lakhs:.1f}L")
            else:
                print("   No properties returned")
                
            # Check if this matches what we expect
            expected_count = 3
            actual_count = result.get('results_count', 0)
            
            if actual_count == expected_count:
                print(f"\n🎉 SUCCESS! Amenity filter is now working correctly!")
                print(f"✅ Backend returned {actual_count} properties as expected!")
            else:
                print(f"\n⚠️ Backend returned {actual_count} properties (expected {expected_count})")
                print("🔍 The amenity filter is still not working correctly")
                
        else:
            print(f"❌ Backend error: {response.status_code}")
            print(f"Error details: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on localhost:8000")
    except Exception as e:
        print(f"❌ Error testing backend: {e}")

if __name__ == "__main__":
    test_amenity_fix()
