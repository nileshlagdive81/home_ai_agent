#!/usr/bin/env python3
"""
Test script to demonstrate field-specific queries and intent classification
"""

import json
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.nlp_engine import RealEstateNLPEngine

def load_training_data(file_path: str):
    """Load training data from JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def test_field_queries():
    """Test field-specific queries with the NLP engine"""
    
    # Load training data
    training_data = load_training_data("field_training_data.json")
    
    # Initialize NLP engine
    try:
        nlp_engine = RealEstateNLPEngine()
        print("✅ NLP Engine initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing NLP Engine: {e}")
        return
    
    print("\n" + "="*80)
    print("🧪 Testing Field-Specific Queries for Real Estate Projects")
    print("="*80)
    
    # Test Project Fields
    print("\n🏗️ PROJECT FIELDS:")
    print("-" * 50)
    
    project_fields = training_data["project_fields"]
    for field_name, field_data in project_fields.items():
        print(f"\n📋 Field: {field_name.replace('_', ' ').title()}")
        print(f"   Intent: {field_data['intent']}")
        print(f"   Entities: {', '.join(field_data['entities'])}")
        
        # Test first example query
        test_query = field_data["examples"][0]
        print(f"   Test Query: {test_query}")
        
        try:
            result = nlp_engine.process_query(test_query)
            print(f"   Detected Intent: {result.intent}")
            print(f"   Confidence: {result.confidence:.2f}")
            
            if result.entities:
                print(f"   Extracted Entities: {[f'{e.text}({e.label})' for e in result.entities]}")
            else:
                print(f"   Extracted Entities: None")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test Property Unit Fields
    print("\n🏠 PROPERTY UNIT FIELDS:")
    print("-" * 50)
    
    unit_fields = training_data["property_unit_fields"]
    for field_name, field_data in unit_fields.items():
        print(f"\n📋 Field: {field_name.replace('_', ' ').title()}")
        print(f"   Intent: {field_data['intent']}")
        print(f"   Entities: {', '.join(field_data['entities'])}")
        
        # Test first example query
        test_query = field_data["examples"][0]
        print(f"   Test Query: {test_query}")
        
        try:
            result = nlp_engine.process_query(test_query)
            print(f"   Detected Intent: {result.intent}")
            print(f"   Confidence: {result.confidence:.2f}")
            
            if result.entities:
                print(f"   Extracted Entities: {[f'{e.text}({e.label})' for e in result.entities]}")
            else:
                print(f"   Extracted Entities: None")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test Amenity Fields
    print("\n🏊 AMENITY FIELDS:")
    print("-" * 50)
    
    amenity_fields = training_data["amenity_fields"]
    for field_name, field_data in amenity_fields.items():
        print(f"\n📋 Field: {field_name.replace('_', ' ').title()}")
        print(f"   Intent: {field_data['intent']}")
        print(f"   Entities: {', '.join(field_data['entities'])}")
        
        # Test first example query
        test_query = field_data["examples"][0]
        print(f"   Test Query: {test_query}")
        
        try:
            result = nlp_engine.process_query(test_query)
            print(f"   Detected Intent: {result.intent}")
            print(f"   Confidence: {result.confidence:.2f}")
            
            if result.entities:
                print(f"   Extracted Entities: {[f'{e.text}({e.label})' for e in result.entities]}")
            else:
                print(f"   Extracted Entities: None")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test Nearby Places
    print("\n📍 NEARBY PLACES:")
    print("-" * 50)
    
    nearby_places = training_data["nearby_places"]
    for place_name, place_data in nearby_places.items():
        print(f"\n📋 Place: {place_name.replace('_', ' ').title()}")
        print(f"   Intent: {place_data['intent']}")
        print(f"   Entities: {', '.join(place_data['entities'])}")
        
        # Test first example query
        test_query = place_data["examples"][0]
        print(f"   Test Query: {test_query}")
        
        try:
            result = nlp_engine.process_query(test_query)
            print(f"   Detected Intent: {result.intent}")
            print(f"   Confidence: {result.confidence:.2f}")
            
            if result.entities:
                print(f"   Extracted Entities: {[f'{e.text}({e.label})' for e in result.entities]}")
            else:
                print(f"   Extracted Entities: None")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test Simple Search Queries
    print("\n🔍 SIMPLE SEARCH QUERIES:")
    print("-" * 50)
    
    search_queries = training_data["simple_search_queries"]
    for search_type, search_data in search_queries.items():
        print(f"\n📋 Search Type: {search_type.replace('_', ' ').title()}")
        print(f"   Intent: {search_data['intent']}")
        print(f"   Entities: {', '.join(search_data['entities'])}")
        
        # Test first example query
        test_query = search_data["examples"][0]
        print(f"   Test Query: {test_query}")
        
        try:
            result = nlp_engine.process_query(test_query)
            print(f"   Detected Intent: {result.intent}")
            print(f"   Confidence: {result.confidence:.2f}")
            
            if result.entities:
                print(f"   Extracted Entities: {[f'{e.text}({e.label})' for e in result.entities]}")
            else:
                print(f"   Extracted Entities: None")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "="*80)
    print("✅ Field-specific query testing completed!")
    print("="*80)

def test_custom_queries():
    """Test some custom queries to show the system's capabilities"""
    
    try:
        nlp_engine = RealEstateNLPEngine()
        print("\n🧪 Testing Custom Queries:")
        print("-" * 50)
        
        custom_queries = [
            "What is the name of Luxury Heights project?",
            "Who developed Green Valley?",
            "How many floors does Tech Park Residences have?",
            "What is the RERA number for Heritage Gardens?",
            "When can I move into Luxury Heights?",
            "What amenities does Green Valley offer?",
            "How far is the metro from Tech Park Residences?",
            "What is the carpet area of 2BHK in Luxury Heights?",
            "How much does a 3BHK flat cost in Tech Park?",
            "Is there a hospital near Heritage Gardens?"
        ]
        
        for i, query in enumerate(custom_queries, 1):
            print(f"\n{i}. Query: {query}")
            try:
                result = nlp_engine.process_query(query)
                print(f"   Intent: {result.intent}")
                print(f"   Confidence: {result.confidence:.2f}")
                
                if result.entities:
                    print(f"   Entities: {[f'{e.text}({e.label})' for e in result.entities]}")
                else:
                    print(f"   Entities: None")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
    except Exception as e:
        print(f"❌ Error testing custom queries: {e}")

if __name__ == "__main__":
    print("🚀 Starting Field-Specific Query Testing...")
    
    # Test field queries
    test_field_queries()
    
    # Test custom queries
    test_custom_queries()
    
    print("\n🎉 All testing completed!")
