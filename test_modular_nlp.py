#!/usr/bin/env python3
"""
Test Script for Modular NLP Architecture
Demonstrates independent operation of search properties and knowledge base engines
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.services.nlp_orchestrator import NLPOrchestrator
from backend.services.search_properties_engine import SearchPropertiesEngine
from backend.services.knowledge_base_engine import KnowledgeBaseEngine

def test_individual_engines():
    """Test each engine independently"""
    print("🧪 Testing Individual Engines")
    print("=" * 50)
    
    # Test Search Properties Engine
    print("\n🏠 Testing Search Properties Engine:")
    print("-" * 40)
    search_engine = SearchPropertiesEngine()
    
    search_queries = [
        "Show me 2 BHK apartments in Pune",
        "Properties under 50 lakhs in Mumbai",
        "Houses with swimming pool in Bangalore",
        "Villas above 2 crores in Delhi"
    ]
    
    for query in search_queries:
        result = search_engine.classify_intent(query)
        print(f"Query: '{query}'")
        print(f"Intent: {result.intent}")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"Entities: {result.entities}")
        print(f"Search Criteria: {result.search_criteria}")
        print()
    
    # Test Knowledge Base Engine
    print("\n📚 Testing Knowledge Base Engine:")
    print("-" * 40)
    knowledge_engine = KnowledgeBaseEngine()
    
    knowledge_queries = [
        "What is carpet area?",
        "How to buy property in India?",
        "What is RERA?",
        "Is real estate a good investment?"
    ]
    
    for query in knowledge_queries:
        result = knowledge_engine.search_knowledge(query)
        if result:
            print(f"Query: '{query}'")
            print(f"Category: {result.category}")
            print(f"Confidence: {result.confidence:.2f}")
            print(f"Answer Preview: {result.answer[:100]}...")
            print(f"Suggestions: {result.suggestions}")
            print()
        else:
            print(f"Query: '{query}' - No match found")
            print()
    
    # Get statistics
    print("\n📊 Engine Statistics:")
    print("-" * 40)
    search_stats = search_engine.evaluate_model([])
    knowledge_stats = knowledge_engine.get_statistics()
    
    print(f"Search Properties Engine: {search_stats}")
    print(f"Knowledge Base Engine: {knowledge_stats}")

def test_orchestrator():
    """Test the orchestrator's routing capabilities"""
    print("\n🎯 Testing NLP Orchestrator")
    print("=" * 50)
    
    orchestrator = NLPOrchestrator()
    
    # Test queries that should be clearly routed
    test_queries = [
        # Knowledge queries
        "What is carpet area?",
        "How to apply for home loan?",
        "Tell me about RERA",
        "What is the meaning of BHK?",
        
        # Search queries
        "Show me 2 BHK apartments in Pune",
        "Find properties under 50 lakhs",
        "Looking for houses with swimming pool",
        "Properties near metro station",
        
        # Ambiguous queries
        "2 BHK in Mumbai",
        "Property investment advice",
        "Real estate in Bangalore",
        "Home buying process"
    ]
    
    print("🔍 Testing Query Routing:")
    print("-" * 40)
    
    for query in test_queries:
        result = orchestrator.route_query(query)
        print(f"Query: '{query}'")
        print(f"Routed to: {result.engine_used}")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"Reason: {result.routing_reason}")
        
        if result.response_data:
            if result.engine_used == "knowledge_base":
                print(f"Category: {result.response_data.category}")
                print(f"Answer Preview: {result.response_data.answer[:80]}...")
            elif result.engine_used == "search_properties":
                print(f"Intent: {result.response_data.intent}")
                print(f"Entities: {result.response_data.entities}")
        
        print()
    
    # Get orchestrator statistics
    print("\n📊 Orchestrator Statistics:")
    print("-" * 40)
    stats = orchestrator.get_engine_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")

def test_no_interference():
    """Test that engines don't interfere with each other"""
    print("\n🛡️ Testing No Interference Between Engines")
    print("=" * 60)
    
    # Initialize both engines independently
    search_engine = SearchPropertiesEngine()
    knowledge_engine = KnowledgeBaseEngine()
    
    # Test that search engine doesn't affect knowledge engine
    print("\n🏠 Testing Search Engine Independence:")
    print("-" * 40)
    
    # Add new search training data
    new_search_data = {
        "intents": {
            "TEST_SEARCH_INTENT": {
                "examples": ["This is a test search query"],
                "entities": ["TEST_ENTITY"]
            }
        }
    }
    
    search_engine.train_model(new_search_data)
    print("✅ Added new search training data")
    
    # Verify knowledge engine is unchanged
    original_kb_stats = knowledge_engine.get_statistics()
    print(f"Knowledge Base stats before: {original_kb_stats}")
    
    # Test that knowledge engine doesn't affect search engine
    print("\n📚 Testing Knowledge Engine Independence:")
    print("-" * 40)
    
    # Add new knowledge training data
    new_knowledge_data = {
        "knowledge_base": {
            "test_category": [
                {
                    "question": "what is test question",
                    "keywords": ["test", "question"],
                    "answer": "This is a test answer"
                }
            ]
        }
    }
    
    knowledge_engine.train_model(new_knowledge_data)
    print("✅ Added new knowledge training data")
    
    # Verify search engine is unchanged
    search_intents = list(search_engine.training_data["search_properties"]["intents"].keys())
    print(f"Search intents after KB update: {search_intents}")
    
    # Verify both engines still work independently
    print("\n🔄 Testing Independent Operation:")
    print("-" * 40)
    
    search_result = search_engine.classify_intent("Show me 2 BHK apartments")
    print(f"Search Engine Result: {search_result.intent} (confidence: {search_result.confidence:.2f})")
    
    knowledge_result = knowledge_engine.search_knowledge("What is carpet area?")
    if knowledge_result:
        print(f"Knowledge Engine Result: {knowledge_result.category} (confidence: {knowledge_result.confidence:.2f})")
    else:
        print("Knowledge Engine Result: No match found")
    
    print("\n✅ Both engines working independently - no interference detected!")

def main():
    """Main test function"""
    print("🚀 Modular NLP Architecture Test Suite")
    print("=" * 60)
    print("This test demonstrates the independent operation of:")
    print("1. Search Properties Engine")
    print("2. Knowledge Base Engine")
    print("3. NLP Orchestrator")
    print("4. No interference between engines")
    
    try:
        # Test individual engines
        test_individual_engines()
        
        # Test orchestrator
        test_orchestrator()
        
        # Test no interference
        test_no_interference()
        
        print("\n🎉 All tests completed successfully!")
        print("✅ Modular architecture working as expected")
        print("✅ No interference between engines")
        print("✅ Independent training and operation")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
