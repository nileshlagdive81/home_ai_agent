#!/usr/bin/env python3
import sys
import os
sys.path.append("backend")
from database import SessionLocal

print("🏠 VASTU NLP QUERY DEMONSTRATION")
print("=" * 60)

# 1. User Query
user_query = "Is Lodha Park property vastu compliant?"
print(f"👤 USER QUERY: {user_query}")
print()

# 2. NLP Intent Detection (Simulated)
print("🧠 NLP INTENT DETECTION:")
print("-" * 30)
detected_intent = "VASTU_COMPLIANCE_CHECK"
confidence_score = 0.95
print(f"Intent: {detected_intent}")
print(f"Confidence: {confidence_score}")
print()

# 3. NLP Entity Extraction (Simulated)
print("🔍 NLP ENTITY EXTRACTION:")
print("-" * 30)
extracted_entities = {
    "PROPERTY_ID": "Lodha Park",
    "PROPERTY_TYPE": "property",
    "INTENT": "vastu compliant"
}
print("Extracted Entities:")
for entity_type, value in extracted_entities.items():
    print(f"  {entity_type}: {value}")
print()

# 4. Generated SQL Query
print("🗄️ GENERATED SQL QUERY:")
print("-" * 30)
sql_query = """
SELECT 
    p.project_name,
    p.property_type,
    p.bhk_count,
    p.facing,
    va.overall_vastu_score,
    va.vastu_compliance_percentage,
    va.major_vastu_issues,
    va.minor_vastu_issues,
    va.vastu_recommendations,
    va.vastu_benefits
FROM properties p
JOIN projects pr ON p.project_id = pr.id
LEFT JOIN property_vastu_analysis va ON p.id = va.property_id
WHERE pr.project_name ILIKE '%Lodha%'
ORDER BY va.overall_vastu_score DESC NULLS LAST;
"""
print(sql_query.strip())
print()

# 5. Database Results
print("📊 DATABASE RESULTS:")
print("-" * 30)

db = SessionLocal()
try:
    # Execute the actual query
    results = db.execute(sql_query.strip()).fetchall()
    
    if results:
        print(f"✅ Found {len(results)} properties in Lodha Park")
        print()
        
        for i, result in enumerate(results, 1):
            print(f"🏠 PROPERTY {i}:")
            print(f"  Project: {result[0]}")
            print(f"  Type: {result[1]}")
            print(f"  BHK: {result[2]}")
            print(f"  Facing: {result[3]}")
            print(f"  Overall Vastu Score: {result[4] or 'Not Analyzed'}")
            print(f"  Compliance: {result[5] or 'Not Analyzed'}%")
            
            if result[6]:  # major issues
                print(f"  Major Issues: {result[6]}")
            if result[7]:  # minor issues
                print(f"  Minor Issues: {result[7]}")
            if result[8]:  # recommendations
                print(f"  Recommendations: {result[8]}")
            if result[9]:  # benefits
                print(f"  Benefits: {result[9]}")
            print()
    else:
        print("❌ No properties found for Lodha Park")
        print()
        
        # Check what projects exist
        projects = db.execute("SELECT project_name FROM projects").fetchall()
        print("Available projects:")
        for project in projects:
            print(f"  - {project[0]}")
        print()
        
        # Check if Vastu analysis exists
        vastu_count = db.execute("SELECT COUNT(*) FROM property_vastu_analysis").fetchone()[0]
        print(f"Total properties with Vastu analysis: {vastu_count}")
        
        if vastu_count > 0:
            print("\nSample Vastu analysis data:")
            sample = db.execute("""
                SELECT p.project_name, va.overall_vastu_score, va.vastu_compliance_percentage
                FROM property_vastu_analysis va
                JOIN properties p ON va.property_id = p.id
                LIMIT 3
            """).fetchall()
            
            for sample_data in sample:
                print(f"  {sample_data[0]}: Score {sample_data[1]}, Compliance {sample_data[2]}%")

except Exception as e:
    print(f"❌ Error executing query: {str(e)}")
finally:
    db.close()

print()
print("=" * 60)
print("🎯 QUERY ANALYSIS SUMMARY:")
print(f"• NLP Intent: {detected_intent}")
print(f"• Entities: {', '.join(extracted_entities.keys())}")
print(f"• Tables Used: properties, projects, property_vastu_analysis")
print(f"• Fields Retrieved: 10 Vastu-related fields")
print(f"• Data Available: {'Yes' if results else 'No'}")
