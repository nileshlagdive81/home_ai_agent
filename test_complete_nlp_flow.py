#!/usr/bin/env python3
"""
Complete NLP Flow Test - Shows NLP processing, SQL generation, and data retrieval
Uses the ACTUAL database structure with properties table and sell_price column
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.services.nlp_engine import RealEstateNLPEngine
from backend.database import get_db
from sqlalchemy import text
import json

def test_complete_nlp_flow():
    """Test the complete NLP flow from query to data using actual database structure"""
    
    query = "2 BHK apartments under 1 crore in Pune"
    print(f"🔍 Testing Complete NLP Flow for: '{query}'")
    print("=" * 80)
    
    # Step 1: Initialize NLP Engine
    try:
        nlp_engine = RealEstateNLPEngine()
        print("✅ NLP Engine initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize NLP Engine: {e}")
        return
    
    # Step 2: Process Query with NLP Engine
    print(f"\n📝 Step 1: NLP Query Processing")
    print("-" * 50)
    
    # Extract entities
    entities = nlp_engine.extract_entities(query)
    print("   📊 Extracted Entities:")
    for entity in entities:
        print(f"      - {entity.text} ({entity.label}) - Confidence: {entity.confidence}")
    
    # Get search criteria
    criteria = nlp_engine.get_search_criteria(query)
    print(f"\n   🎯 Search Criteria: {json.dumps(criteria['filters'], indent=6)}")
    
    # Step 3: Show Intent Classification
    print(f"\n🧠 Step 2: Intent Classification")
    print("-" * 50)
    
    intent_result = nlp_engine.process_query(query)
    print(f"   🎯 Detected Intent: {intent_result.intent}")
    print(f"   📊 Confidence Score: {intent_result.confidence:.2f}")
    
    # Step 4: Show SQL Query Construction
    print(f"\n🗄️ Step 3: SQL Query Construction")
    print("-" * 50)
    
    # Build the SQL query step by step using ACTUAL database structure
    base_query = "SELECT p.*, pr.name as project_name, pr.developer_id, l.city, l.locality FROM properties p"
    print(f"   📋 Base Query: {base_query}")
    
    sql_parts = [base_query]
    
    # Location filter - join with projects and locations
    if "location" in criteria["filters"]:
        location = criteria["filters"]["location"]
        location_join = """
        JOIN projects pr ON p.project_id = pr.id
        JOIN project_locations pl ON pr.id = pl.project_id
        JOIN locations l ON pl.location_id = l.id"""
        location_filter = f"WHERE (l.city ILIKE '%{location}%' OR l.locality ILIKE '%{location}%')"
        sql_parts.append(location_join)
        sql_parts.append(location_filter)
        print(f"   🌍 Location Filter: {location}")
    else:
        # If no location, still need to join for project info
        sql_parts.append("JOIN projects pr ON p.project_id = pr.id")
        sql_parts.append("JOIN project_locations pl ON pr.id = pl.project_id")
        sql_parts.append("JOIN locations l ON pl.location_id = l.id")
        sql_parts.append("WHERE 1=1")
    
    # BHK filter
    if "bhk" in criteria["filters"]:
        bhk = criteria["filters"]["bhk"]
        bhk_filter = f"AND p.bhk_count = {bhk}"
        sql_parts.append(bhk_filter)
        print(f"   🏠 BHK Filter: {bhk}")
    
    # Property type filter
    if "property_type" in criteria["filters"]:
        prop_type = criteria["filters"]["property_type"]
        prop_type_filter = f"AND p.property_type ILIKE '%{prop_type}%'"
        sql_parts.append(prop_type_filter)
        print(f"   🏢 Property Type Filter: {prop_type}")
    
    # Price filter using the ACTUAL sell_price column
    if "price_range" in criteria["filters"]:
        price_text = criteria["filters"]["price_range"].lower()
        import re
        
        # Pattern for "under X crore/lakhs"
        under_match = re.search(r'under\s+(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)', price_text)
        if under_match:
            max_price = float(under_match.group(1))
            if 'lakh' in price_text:
                max_price = max_price * 100000  # Convert lakhs to rupees
            elif 'crore' in price_text or 'cr' in price_text:
                max_price = max_price * 10000000  # Convert crores to rupees
            
            price_filter = f"AND p.sell_price <= {max_price}"
            sql_parts.append(price_filter)
            print(f"   💰 Price Filter: under ₹{max_price:,} (using sell_price column)")
    
    # Construct final SQL
    final_sql = " ".join(sql_parts)
    print(f"\n   🗄️ Final SQL Query:")
    print(f"   {final_sql}")
    
    # Step 5: Execute Query and Show Results
    print(f"\n📊 Step 4: Data Retrieval")
    print("-" * 50)
    
    try:
        # Get database session
        db = next(get_db())
        
        # Build and execute the query using raw SQL for demonstration
        sql_query = final_sql + " LIMIT 20"
        print(f"   🔍 Executing: {sql_query}")
        
        result = db.execute(text(sql_query))
        properties = result.fetchall()
        
        print(f"\n   📈 Query Results:")
        print(f"   Total properties found: {len(properties)}")
        
        if properties:
            print(f"\n   🏠 Property Details:")
            for i, prop in enumerate(properties[:5], 1):  # Show first 5
                print(f"   {i}. Property ID: {prop[0][:8]}...")
                print(f"      🏢 Type: {prop[2] if prop[2] else 'Not specified'}")
                print(f"      🏠 BHK: {prop[3] if prop[3] else 'Not specified'}")
                print(f"      💰 Price: ₹{prop[11]:,}" if prop[11] else "Price not available")
                print(f"      📍 Location: {prop[14] if prop[14] else 'N/A'}, {prop[13] if prop[13] else 'N/A'}")
                print(f"      🏗️ Project: {prop[12] if prop[12] else 'Not specified'}")
                print()
        else:
            print("   ❌ No properties found matching the criteria")
        
        db.close()
        
    except Exception as e:
        print(f"   ❌ Database error: {e}")
    
    # Step 6: Summary
    print(f"\n📋 Step 5: Summary")
    print("-" * 50)
    print(f"   🔍 Original Query: '{query}'")
    print(f"   🎯 Detected Intent: {intent_result.intent}")
    print(f"   📊 Confidence: {intent_result.confidence:.2f}")
    print(f"   🗄️ SQL Filters Applied: {len(sql_parts) - 1}")  # -1 for base query
    print(f"   📈 Results Found: {len(properties) if 'properties' in locals() else 'N/A'}")
    print(f"   💰 Price Filter Applied: Using 'sell_price' column (existing database structure)")
    
    print(f"\n✅ Complete NLP Flow Test Completed!")

if __name__ == "__main__":
    test_complete_nlp_flow()
