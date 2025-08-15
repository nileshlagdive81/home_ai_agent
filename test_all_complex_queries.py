import requests
import json

def test_complex_queries():
    """Test all complex queries to verify NLP and backend are working"""
    
    base_url = "http://localhost:8000/api/v1/search/nlp"
    
    # Test queries that should work
    test_queries = [
        {
            "query": "Show me 3 BHK in Pune under 2.5 Crs with Gym and Metro station within 3 kms",
            "expected_features": ["3 BHK", "Pune", "under 2.5 cr", "gym", "metro station within 3km"]
        },
        {
            "query": "2 BHK apartments in Pune under 1.5 crores with gym",
            "expected_features": ["2 BHK", "Pune", "under 1.5 cr", "gym"]
        },
        {
            "query": "3 BHK luxury apartments in Pune above 1.5 crores with swimming pool",
            "expected_features": ["3 BHK", "Pune", "above 1.5 cr", "swimming pool"]
        },
        {
            "query": "Properties in Mumbai with 2 BHK and parking",
            "expected_features": ["Mumbai", "2 BHK", "parking"]
        },
        {
            "query": "1 BHK flats in Pune near metro station within 2 km",
            "expected_features": ["1 BHK", "Pune", "metro station within 2km"]
        }
    ]
    
    print("🧪 TESTING ALL COMPLEX QUERIES")
    print("=" * 60)
    
    for i, test_case in enumerate(test_queries, 1):
        print(f"\n{i}️⃣ Testing: {test_case['query']}")
        print("-" * 50)
        
        try:
            response = requests.post(
                base_url,
                data={"query": test_case['query']},
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: Success")
                print(f"📊 Properties found: {len(data.get('results', []))}")
                print(f"🎯 Intent: {data.get('intent')}")
                print(f"🔍 Extracted entities: {json.dumps(data.get('extracted_entities', {}), indent=2)}")
                
                # Check if expected features were extracted
                extracted = data.get('extracted_entities', {})
                for feature in test_case['expected_features']:
                    if any(feature.lower() in str(value).lower() for value in extracted.values()):
                        print(f"✅ Found: {feature}")
                    else:
                        print(f"❌ Missing: {feature}")
                        
            else:
                print(f"❌ Status: Error {response.status_code}")
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        print()

if __name__ == "__main__":
    test_complex_queries()
