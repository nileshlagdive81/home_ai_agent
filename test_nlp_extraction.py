#!/usr/bin/env python3
"""
Script to test the updated NLP extraction
"""

from backend.services.nlp_engine import RealEstateNLPEngine

def test_nlp_extraction():
    """Test the updated NLP extraction"""
    print("🧪 TESTING UPDATED NLP EXTRACTION")
    print("=" * 60)
    
    # Initialize NLP engine
    nlp_engine = RealEstateNLPEngine()
    
    # Test the specific query
    query = "3 BHK apartments in Pune above 1.5 crores with gym, located within 3 km of metro station"
    
    print(f"1️⃣ TESTING QUERY: {query}")
    print("-" * 40)
    
    # Process the query
    intent_result = nlp_engine.process_query(query)
    search_criteria = nlp_engine.get_search_criteria(query)
    
    print(f"2️⃣ INTENT ANALYSIS:")
    print("-" * 40)
    print(f"   📊 Intent: {intent_result.intent}")
    print(f"   📊 Confidence: {intent_result.confidence}")
    print(f"   📊 Entities found: {len(intent_result.entities)}")
    
    print(f"\n3️⃣ EXTRACTED ENTITIES:")
    print("-" * 40)
    for i, entity in enumerate(intent_result.entities):
        print(f"   Entity {i+1}:")
        print(f"      Text: '{entity.text}'")
        print(f"      Label: {entity.label}")
        print(f"      Confidence: {entity.confidence}")
    
    print(f"\n4️⃣ SEARCH CRITERIA:")
    print("-" * 40)
    print(f"   📊 Intent: {search_criteria['intent']}")
    print(f"   📊 Confidence: {search_criteria['confidence']}")
    print(f"   📊 Filters: {search_criteria['filters']}")
    
    # Check specific filters
    filters = search_criteria['filters']
    print(f"\n5️⃣ SPECIFIC FILTERS:")
    print("-" * 40)
    
    if 'city' in filters:
        print(f"   ✅ City: {filters['city']}")
    else:
        print(f"   ❌ City: Not found")
    
    if 'bhk' in filters:
        print(f"   ✅ BHK: {filters['bhk']} {filters.get('bhk_operator', '=')}")
    else:
        print(f"   ❌ BHK: Not found")
    
    if 'price_value' in filters:
        print(f"   ✅ Price: {filters['price_operator']} ₹{filters['price_value']:,}")
    else:
        print(f"   ❌ Price: Not found")
    
    if 'amenities' in filters:
        print(f"   ✅ Amenities: {filters['amenities']}")
    else:
        print(f"   ❌ Amenities: Not found")
    
    if 'nearby_place' in filters:
        print(f"   ✅ Nearby Place: {filters['nearby_place']} {filters['nearby_operator']} {filters['nearby_distance']}km")
    else:
        print(f"   ❌ Nearby Place: Not found")

if __name__ == "__main__":
    test_nlp_extraction()
