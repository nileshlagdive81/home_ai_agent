#!/usr/bin/env python3
"""
Test script to verify price extraction from NLP engine
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.services.nlp_engine import RealEstateNLPEngine

def test_price_extraction():
    """Test price extraction from various queries"""
    
    # Initialize NLP engine
    try:
        nlp_engine = RealEstateNLPEngine()
        print("✅ NLP Engine initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize NLP Engine: {e}")
        return
    
    # Test queries with price information
    test_queries = [
        "2 BHK apartments under 1 crore in Pune",
        "3 BHK villa under 2 crores in Mumbai",
        "1 BHK flat under 50 lakhs in Bangalore",
        "4 BHK penthouse above 3 crores in Delhi",
        "2.5 BHK apartment between 80 lakhs to 1.2 crores in Chennai",
        "Studio apartment under 30 lakhs in Hyderabad",
        "Villa over 5 crores in Goa",
        "2 BHK flat less than 75 lakhs in Pune"
    ]
    
    print("\n🔍 Testing Price Extraction:")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        
        # Extract entities
        entities = nlp_engine.extract_entities(query)
        
        # Show extracted entities
        print("   📊 Extracted Entities:")
        for entity in entities:
            print(f"      - {entity.text} ({entity.label}) - Confidence: {entity.confidence}")
        
        # Get search criteria
        criteria = nlp_engine.get_search_criteria(query)
        print(f"   🎯 Search Criteria: {criteria['filters']}")
        
        # Check if price was extracted
        if 'price_range' in criteria['filters']:
            print(f"   💰 Price Filter: {criteria['filters']['price_range']}")
        else:
            print("   ❌ No price filter extracted")

if __name__ == "__main__":
    test_price_extraction()
