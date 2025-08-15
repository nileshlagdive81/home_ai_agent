#!/usr/bin/env python3
"""
Script to check the current nearby places data structure and linkage
"""

from backend.database import get_db
from sqlalchemy import text

def check_nearby_data():
    """Check the current nearby places data structure and linkage"""
    print("🔍 CHECKING NEARBY PLACES DATA")
    print("=" * 60)
    
    db = next(get_db())
    
    try:
        # Check table structure
        print("1️⃣ TABLE STRUCTURE:")
        print("-" * 40)
        
        # Check nearby_places table columns
        columns_query = """
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'nearby_places'
            ORDER BY ordinal_position
        """
        columns = db.execute(text(columns_query)).fetchall()
        print(f"   📊 nearby_places table columns:")
        for col in columns:
            print(f"      - {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'})")
        
        # Check project_amenities table columns (for comparison)
        print(f"\n   📊 project_amenities table columns:")
        amenity_columns_query = """
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'project_amenities'
            ORDER BY ordinal_position
        """
        amenity_columns = db.execute(text(amenity_columns_query)).fetchall()
        for col in amenity_columns:
            print(f"      - {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'})")
        
        # Check data counts
        print(f"\n2️⃣ DATA COUNTS:")
        print("-" * 40)
        
        count_queries = [
            ("nearby_places", "SELECT COUNT(*) FROM nearby_places"),
            ("projects", "SELECT COUNT(*) FROM projects"),
            ("project_amenities", "SELECT COUNT(*) FROM project_amenities"),
            ("amenities", "SELECT COUNT(*) FROM amenities")
        ]
        
        for table_name, query in count_queries:
            count = db.execute(text(query)).fetchone()[0]
            print(f"   📊 {table_name}: {count} records")
        
        # Check nearby places data
        print(f"\n3️⃣ NEARBY PLACES DATA:")
        print("-" * 40)
        
        nearby_query = """
            SELECT np.id, np.place_type, np.place_name, np.distance_km, 
                   np.project_id, p.name as project_name
            FROM nearby_places np
            LEFT JOIN projects p ON np.project_id = p.id
            ORDER BY np.place_type, np.distance_km
            LIMIT 10
        """
        nearby_data = db.execute(text(nearby_query)).fetchall()
        
        if nearby_data:
            print(f"   📊 Sample nearby places:")
            for place in nearby_data:
                print(f"      - {place[1]}: {place[2]} at {place[3]}km -> Project: {place[5] or 'NULL'}")
        else:
            print("   ❌ No nearby places data found")
        
        # Check metro stations specifically
        print(f"\n4️⃣ METRO STATIONS:")
        print("-" * 40)
        
        metro_query = """
            SELECT COUNT(*) as count
            FROM nearby_places
            WHERE place_type = 'METRO STATION'
        """
        metro_count = db.execute(text(metro_query)).fetchone()[0]
        print(f"   📊 Metro stations: {metro_count}")
        
        if metro_count > 0:
            metro_details_query = """
                SELECT np.place_name, np.distance_km, p.name as project_name
                FROM nearby_places np
                LEFT JOIN projects p ON np.project_id = p.id
                WHERE np.place_type = 'METRO STATION'
                ORDER BY np.distance_km
                LIMIT 5
            """
            metro_details = db.execute(text(metro_details_query)).fetchall()
            print(f"   📊 Sample metro stations:")
            for metro in metro_details:
                print(f"      - {metro[0]} at {metro[1]}km -> {metro[2] or 'NULL'}")
        
        # Check project linkage
        print(f"\n5️⃣ PROJECT LINKAGE:")
        print("-" * 40)
        
        linkage_query = """
            SELECT COUNT(*) as count
            FROM nearby_places np
            JOIN projects p ON np.project_id = p.id
        """
        linked_count = db.execute(text(linkage_query)).fetchone()[0]
        print(f"   📊 Nearby places linked to projects: {linked_count}")
        
        unlinked_query = """
            SELECT COUNT(*) as count
            FROM nearby_places np
            LEFT JOIN projects p ON np.project_id = p.id
            WHERE p.id IS NULL
        """
        unlinked_count = db.execute(text(unlinked_query)).fetchone()[0]
        print(f"   📊 Nearby places NOT linked to projects: {unlinked_count}")
        
    except Exception as e:
        print(f"❌ Error checking nearby data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    check_nearby_data()
