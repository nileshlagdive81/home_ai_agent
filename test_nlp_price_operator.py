#!/usr/bin/env python3
"""
Test script to debug NLP price operator extraction
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from services.nlp_engine import RealEstateNLPEngine

def test_price_operators():
    """Test various price queries to see how operators are extracted"""
    
    # Initialize NLP engine
    nlp_engine = RealEstateNLPEngine()
    
    # Test queries
    test_queries = [
        "2 BHK apartments under 1 crore in Pune",
        "3 BHK houses above 50 lakhs",
        "Properties under 1 Cr in Mumbai",
        "Flats below 2 crore",
        "Houses less than 1.5 cr",
        "Apartments over 75 lakhs",
        "Properties above 2 crore",
        "2 BHK exactly 1 crore",
        "3 BHK = 1.5 crore"
    ]
    
    print("Testing NLP Price Operator Extraction:")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        print("-" * 40)
        
        try:
            # Process the query
            intent_result = nlp_engine.process_query(query)
            print(f"Intent: {intent_result.intent} (confidence: {intent_result.confidence:.2f})")
            
            # Extract search criteria
            criteria = nlp_engine.get_search_criteria(query)
            print(f"Search Criteria: {criteria['filters']}")
            
            # Show detailed entity information
            print("Entities:")
            for entity in intent_result.entities:
                if entity.label == "PRICE":
                    print(f"  PRICE: '{entity.text}' -> Operator: {entity.context.get('operator', 'N/A')}, Value: {entity.context.get('value', 'N/A')}")
                else:
                    print(f"  {entity.label}: '{entity.text}' -> {entity.context}")
                    
        except Exception as e:
            print(f"❌ Error processing query: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_price_operators()
