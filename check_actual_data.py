#!/usr/bin/env python3
"""
Check actual data in the database to understand the data structure
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database import get_db
from sqlalchemy import text

def check_actual_data():
    """Check what data actually exists in the database"""
    
    try:
        db = next(get_db())
        
        print("🔍 Checking actual data in the database...")
        print("=" * 60)
        
        # Check properties table data
        print("🏠 Properties table data:")
        print("-" * 30)
        
        # Count total properties
        count_result = db.execute(text("SELECT COUNT(*) FROM properties"))
        total_properties = count_result.fetchone()[0]
        print(f"  Total properties: {total_properties}")
        
        # Check BHK distribution
        bhk_result = db.execute(text("SELECT bhk_count, COUNT(*) FROM properties WHERE bhk_count IS NOT NULL GROUP BY bhk_count ORDER BY bhk_count"))
        print("  BHK distribution:")
        for row in bhk_result:
            print(f"    - {row[0]} BHK: {row[1]} properties")
        
        # Check property types
        type_result = db.execute(text("SELECT property_type, COUNT(*) FROM properties WHERE property_type IS NOT NULL GROUP BY property_type ORDER BY COUNT(*) DESC"))
        print("  Property types:")
        for row in type_result:
            print(f"    - {row[0]}: {row[1]} properties")
        
        # Check price ranges
        price_result = db.execute(text("SELECT MIN(sell_price), MAX(sell_price), AVG(sell_price) FROM properties"))
        min_price, max_price, avg_price = price_result.fetchone()
        print(f"  Price range: ₹{min_price:,.0f} - ₹{max_price:,.0f}")
        print(f"  Average price: ₹{avg_price:,.0f}")
        
        # Check locations
        print("\n🌍 Location data:")
        print("-" * 20)
        
        # Check if project_locations table has data
        pl_count = db.execute(text("SELECT COUNT(*) FROM project_locations"))
        pl_total = pl_count.fetchone()[0]
        print(f"  Project-location mappings: {pl_total}")
        
        # Check if locations table has data
        loc_count = db.execute(text("SELECT COUNT(*) FROM locations"))
        loc_total = loc_count.fetchone()[0]
        print(f"  Total locations: {loc_total}")
        
        if loc_total > 0:
            # Show some sample locations
            loc_sample = db.execute(text("SELECT city, locality FROM locations LIMIT 5"))
            print("  Sample locations:")
            for row in loc_sample:
                print(f"    - {row[1]}, {row[0]}")
        
        # Check projects
        print("\n🏗️ Projects data:")
        print("-" * 20)
        proj_count = db.execute(text("SELECT COUNT(*) FROM projects"))
        proj_total = proj_count.fetchone()[0]
        print(f"  Total projects: {proj_total}")
        
        # Check if properties have project_id
        proj_prop_count = db.execute(text("SELECT COUNT(*) FROM properties WHERE project_id IS NOT NULL"))
        proj_prop_total = proj_prop_count.fetchone()[0]
        print(f"  Properties with project_id: {proj_prop_total}")
        
        # Check if properties have location info
        print("\n🔍 Checking why NLP query returned 0 results:")
        print("-" * 50)
        
        # Check properties with BHK = 2
        bhk2_count = db.execute(text("SELECT COUNT(*) FROM properties WHERE bhk_count = 2"))
        bhk2_total = bhk2_count.fetchone()[0]
        print(f"  Properties with 2 BHK: {bhk2_total}")
        
        # Check properties with apartment type
        apt_count = db.execute(text("SELECT COUNT(*) FROM properties WHERE property_type ILIKE '%apartment%'"))
        apt_total = apt_count.fetchone()[0]
        print(f"  Properties with 'apartment' type: {apt_total}")
        
        # Check properties under 1 crore
        under1cr_count = db.execute(text("SELECT COUNT(*) FROM properties WHERE sell_price <= 10000000"))
        under1cr_total = under1cr_count.fetchone()[0]
        print(f"  Properties under 1 crore: {under1cr_total}")
        
        # Check properties with all three conditions
        all_conditions = db.execute(text("""
            SELECT COUNT(*) FROM properties p
            WHERE p.bhk_count = 2 
            AND p.property_type ILIKE '%apartment%' 
            AND p.sell_price <= 10000000
        """))
        all_conditions_total = all_conditions.fetchone()[0]
        print(f"  Properties matching ALL conditions: {all_conditions_total}")
        
        # Check if the issue is with joins
        print("\n🔗 Checking join relationships:")
        print("-" * 35)
        
        # Check properties that can join with projects
        joinable_props = db.execute(text("""
            SELECT COUNT(*) FROM properties p
            JOIN projects pr ON p.project_id = pr.id
        """))
        joinable_count = joinable_props.fetchone()[0]
        print(f"  Properties that can join with projects: {joinable_count}")
        
        # Check if we can get location info
        if joinable_count > 0:
            location_joinable = db.execute(text("""
                SELECT COUNT(*) FROM properties p
                JOIN projects pr ON p.project_id = pr.id
                JOIN project_locations pl ON pr.id = pl.project_id
                JOIN locations l ON pl.location_id = l.id
            """))
            location_count = location_joinable.fetchone()[0]
            print(f"  Properties with full location info: {location_count}")
            
            if location_count > 0:
                # Check if any have Pune location
                pune_count = db.execute(text("""
                    SELECT COUNT(*) FROM properties p
                    JOIN projects pr ON p.project_id = pr.id
                    JOIN project_locations pl ON pr.id = pl.project_id
                    JOIN locations l ON pl.location_id = l.id
                    WHERE l.city ILIKE '%pune%' OR l.locality ILIKE '%pune%'
                """))
                pune_total = pune_count.fetchone()[0]
                print(f"  Properties in Pune: {pune_total}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_actual_data()
