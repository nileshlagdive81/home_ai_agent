#!/usr/bin/env python3
"""
Script to check if nearby places are properly linked to projects
"""

from backend.database import get_db
from sqlalchemy import text

def check_nearby_linkage():
    """Check if nearby places are properly linked to projects"""
    print("🔍 CHECKING NEARBY PLACES LINKAGE TO PROJECTS")
    print("=" * 60)
    
    db = next(get_db())
    
    try:
        # Check 1: Direct nearby places query
        print("1️⃣ CHECK: Direct nearby places query")
        print("-" * 40)
        query1 = """
            SELECT COUNT(*) as count
            FROM nearby_places
            WHERE place_type = 'METRO STATION'
        """
        result1 = db.execute(text(query1)).fetchone()[0]
        print(f"   📊 Total metro stations in nearby_places: {result1}")
        
        # Check 2: Nearby places with project info
        print("\n2️⃣ CHECK: Nearby places with project info")
        print("-" * 40)
        query2 = """
            SELECT np.place_name, np.distance_km, p.name as project_name, l.locality
            FROM nearby_places np
            JOIN projects p ON np.project_id = p.id
            JOIN project_locations pl ON p.id = pl.project_id
            JOIN locations l ON pl.location_id = l.id
            WHERE np.place_type = 'METRO STATION'
            AND l.city ILIKE '%pune%'
            ORDER BY np.distance_km
        """
        metro_stations = db.execute(text(query2)).fetchall()
        print(f"   📊 Metro stations in Pune projects:")
        for metro in metro_stations:
            print(f"      - {metro[0]} at {metro[1]}km - {metro[2]} in {metro[3]}")
        
        # Check 3: Projects that should have metro stations
        print("\n3️⃣ CHECK: Projects that should have metro stations")
        print("-" * 40)
        query3 = """
            SELECT DISTINCT p.name as project_name, l.locality
            FROM projects p
            JOIN project_locations pl ON p.id = pl.project_id
            JOIN locations l ON pl.location_id = l.id
            WHERE l.city ILIKE '%pune%'
            ORDER BY p.name, l.locality
        """
        pune_projects = db.execute(text(query3)).fetchall()
        print(f"   📊 All Pune projects:")
        for project in pune_projects:
            print(f"      - {project[0]} in {project[1]}")
        
        # Check 4: Check if nearby places exist for specific projects
        print("\n4️⃣ CHECK: Check if nearby places exist for specific projects")
        print("-" * 40)
        query4 = """
            SELECT p.name as project_name, l.locality, COUNT(np.id) as nearby_count
            FROM projects p
            JOIN project_locations pl ON p.id = pl.project_id
            JOIN locations l ON pl.location_id = l.id
            LEFT JOIN nearby_places np ON p.id = np.project_id
            WHERE l.city ILIKE '%pune%'
            GROUP BY p.id, p.name, l.locality
            ORDER BY p.name, l.locality
        """
        project_nearby_counts = db.execute(text(query4)).fetchall()
        print(f"   📊 Nearby places count per project:")
        for project in project_nearby_counts:
            print(f"      - {project[0]} in {project[1]}: {project[2]} nearby places")
        
        # Check 5: Check if the issue is with project_id in nearby_places
        print("\n5️⃣ CHECK: Check nearby_places table structure")
        print("-" * 40)
        query5 = """
            SELECT np.project_id, np.place_type, np.place_name, np.distance_km
            FROM nearby_places np
            WHERE np.place_type = 'METRO STATION'
            LIMIT 5
        """
        nearby_sample = db.execute(text(query5)).fetchall()
        print(f"   📊 Sample nearby places data:")
        for place in nearby_sample:
            print(f"      - Project ID: {place[0]}, Type: {place[1]}, Name: {place[2]}, Distance: {place[3]}km")
        
    except Exception as e:
        print(f"❌ Error checking nearby linkage: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    check_nearby_linkage()
