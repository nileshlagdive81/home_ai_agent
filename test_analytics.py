#!/usr/bin/env python3
"""
Test Analytics Script - Debug Version
"""

import sys
import os

print("🔍 DEBUGGING ANALYTICS SCRIPT")
print("=" * 40)

# Add backend to path
print("1. Adding backend to path...")
sys.path.append("backend")
print(f"   Python path: {sys.path[-1]}")

try:
    print("2. Importing database...")
    from database import SessionLocal
    print("   ✅ Database imported successfully")
    
    print("3. Importing models...")
    from models import Property, Project
    print("   ✅ Models imported successfully")
    
    print("4. Importing SQLAlchemy...")
    from sqlalchemy import text
    print("   ✅ SQLAlchemy imported successfully")
    
    print("5. Creating database session...")
    db = SessionLocal()
    print("   ✅ Database session created")
    
    print("6. Querying properties...")
    properties = db.query(Property).limit(5).all()
    print(f"   ✅ Found {len(properties)} properties")
    
    if properties:
        print("7. Testing property access...")
        prop = properties[0]
        print(f"   ✅ Property: {prop.project.project_name} {prop.bhk_count}BHK")
        print(f"   ✅ Price: {prop.price_crores} crores")
        print(f"   ✅ Area: {prop.carpet_area_sqft} sqft")
    
    print("8. Closing database session...")
    db.close()
    print("   ✅ Database session closed")
    
    print("\n🎉 All imports and database operations successful!")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()

