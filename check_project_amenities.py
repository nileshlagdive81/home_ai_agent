#!/usr/bin/env python3
"""
Script to check the current state of project_amenities table
"""

from backend.database import get_db
from sqlalchemy import text

def check_project_amenities():
    """Check the current state of project_amenities table"""
    print("🔍 CHECKING PROJECT_AMENITIES TABLE")
    print("=" * 60)
    
    db = next(get_db())
    
    try:
        # Check total count
        count_query = "SELECT COUNT(*) FROM project_amenities"
        total_count = db.execute(text(count_query)).fetchone()[0]
        print(f"📊 Total project-amenity relationships: {total_count}")
        
        # Check what amenities are linked to projects
        amenity_count_query = """
            SELECT a.name as amenity_name, COUNT(*) as project_count
            FROM project_amenities pa
            JOIN amenities a ON pa.amenity_id = a.id
            GROUP BY a.name
            ORDER BY project_count DESC
        """
        amenity_counts = db.execute(text(amenity_count_query)).fetchall()
        
        print(f"\n📊 AMENITY DISTRIBUTION:")
        print("-" * 40)
        for amenity_name, project_count in amenity_counts:
            print(f"   {amenity_name}: {project_count} projects")
        
        # Check specifically for gym
        gym_query = """
            SELECT pa.project_id, pa.amenity_id, a.name as amenity_name, p.name as project_name
            FROM project_amenities pa
            JOIN amenities a ON pa.amenity_id = a.id
            JOIN projects p ON pa.project_id = p.id
            WHERE a.name ILIKE '%gym%'
            ORDER BY p.name
        """
        gym_results = db.execute(text(gym_query)).fetchall()
        
        print(f"\n🏋️ GYM AMENITIES FOUND:")
        print("-" * 30)
        print(f"   📊 Total projects with gym: {len(gym_results)}")
        for gym in gym_results:
            print(f"   - Project: {gym[3]} (ID: {gym[0]}) | Amenity: {gym[2]} (ID: {gym[1]})")
        
        # Check if there are any properties in Pune with gym
        pune_gym_query = """
            SELECT COUNT(DISTINCT pr.id) as property_count
            FROM properties pr
            JOIN projects p ON pr.project_id = p.id
            JOIN project_locations pl ON p.id = pl.project_id
            JOIN locations l ON pl.location_id = l.id
            JOIN project_amenities pa ON p.id = pa.project_id
            JOIN amenities a ON pa.amenity_id = a.id
            WHERE l.city ILIKE '%pune%'
            AND a.name ILIKE '%gym%'
        """
        pune_gym_count = db.execute(text(pune_gym_query)).fetchone()[0]
        
        print(f"\n🏠 PUNE PROPERTIES WITH GYM:")
        print("-" * 30)
        print(f"   📊 Properties in Pune with gym: {pune_gym_count}")
        
        # Check if there are any 2 BHK properties in Pune with gym
        pune_2bhk_gym_query = """
            SELECT COUNT(DISTINCT pr.id) as property_count
            FROM properties pr
            JOIN projects p ON pr.project_id = p.id
            JOIN project_locations pl ON p.id = pl.project_id
            JOIN locations l ON pl.location_id = l.id
            JOIN project_amenities pa ON p.id = pa.project_id
            JOIN amenities a ON pa.amenity_id = a.id
            WHERE l.city ILIKE '%pune%'
            AND pr.bhk_count = 2
            AND a.name ILIKE '%gym%'
        """
        pune_2bhk_gym_count = db.execute(text(pune_2bhk_gym_query)).fetchone()[0]
        
        print(f"   📊 2 BHK Properties in Pune with gym: {pune_2bhk_gym_count}")
        
        # Check if there are any 2 BHK properties in Pune with gym under 1.5 cr
        pune_2bhk_gym_price_query = """
            SELECT COUNT(DISTINCT pr.id) as property_count
            FROM properties pr
            JOIN projects p ON pr.project_id = p.id
            JOIN project_locations pl ON p.id = pl.project_id
            JOIN locations l ON pl.location_id = l.id
            JOIN project_amenities pa ON p.id = pa.project_id
            JOIN amenities a ON pa.amenity_id = a.id
            WHERE l.city ILIKE '%pune%'
            AND pr.bhk_count = 2
            AND pr.sell_price < 15000000
            AND a.name ILIKE '%gym%'
        """
        pune_2bhk_gym_price_count = db.execute(text(pune_2bhk_gym_price_query)).fetchone()[0]
        
        print(f"   📊 2 BHK Properties in Pune with gym under 1.5 cr: {pune_2bhk_gym_price_count}")
        
    except Exception as e:
        print(f"❌ Error checking project_amenities: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    check_project_amenities()
