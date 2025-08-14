#!/usr/bin/env python3
"""
Test script for the NLP Engine
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from services.nlp_engine import RealEstateNLPEngine

def test_nlp_engine():
    """Test the NLP engine with various queries"""
    try:
        print("Initializing NLP Engine...")
        nlp_engine = RealEstateNLPEngine()
        print("✅ NLP Engine initialized successfully!")
        
        # Test queries
        test_queries = [
            "I want a 2BHK flat in Mumbai",
            "Show me properties near metro station",
            "What's the price of 3BHK in Bandra?",
            "Book a site visit for tomorrow",
            "Compare these two projects",
            "Properties under 50 lakhs in Pune",
            "Show me houses near good schools",
            "What amenities does this project have?",
            "Schedule a viewing for next week",
            "Find apartments near my office"
        ]
        
        print("\n" + "="*60)
        print("Testing NLP Engine with Real Estate Queries")
        print("="*60)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{i}. Query: {query}")
            print("-" * 50)
            
            try:
                # Process the query
                result = nlp_engine.process_query(query)
                print(f"Intent: {result.intent}")
                print(f"Confidence: {result.confidence:.2f}")
                
                if result.entities:
                    print("Entities:")
                    for entity in result.entities:
                        print(f"  - {entity.text} ({entity.label}) - Confidence: {entity.confidence:.2f}")
                else:
                    print("Entities: None detected")
                
                # Get search criteria
                criteria = nlp_engine.get_search_criteria(query)
                print(f"Search Criteria: {criteria['filters']}")
                
                # Get suggestions
                suggestions = nlp_engine.get_suggestions(query)
                if suggestions:
                    print(f"Suggestions: {', '.join(suggestions)}")
                
            except Exception as e:
                print(f"❌ Error processing query: {e}")
        
        print("\n" + "="*60)
        print("✅ NLP Engine testing completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error initializing NLP Engine: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_nlp_engine()
    if not success:
        sys.exit(1)
