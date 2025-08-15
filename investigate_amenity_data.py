#!/usr/bin/env python3
"""
Script to investigate the actual data in amenity-related tables
"""

from backend.database import get_db
from sqlalchemy import text

def investigate_amenity_data():
    """Investigate the actual data in amenity-related tables"""
    print("🔍 INVESTIGATING AMENITY DATA")
    print("=" * 60)
    
    db = next(get_db())
    
    try:
        # 1. Check what amenities exist
        print("1️⃣ CHECKING AMENITIES TABLE:")
        print("-" * 30)
        
        amenities_query = "SELECT id, name FROM amenities ORDER BY name"
        amenities = db.execute(text(amenities_query)).fetchall()
        
        print(f"   📊 Total amenities: {len(amenities)}")
        for amenity in amenities:
            print(f"   - {amenity[1]} (ID: {amenity[0]})")
        
        # 2. Check what project_amenities exist
        print(f"\n2️⃣ CHECKING PROJECT_AMENITIES TABLE:")
        print("-" * 30)
        
        project_amenities_query = """
            SELECT pa.project_id, pa.amenity_id, a.name as amenity_name, p.name as project_name
            FROM project_amenities pa
            JOIN amenities a ON pa.amenity_id = a.id
            JOIN projects p ON pa.project_id = p.id
            ORDER BY p.name, a.name
        """
        project_amenities = db.execute(text(project_amenities_query)).fetchall()
        
        print(f"   📊 Total project-amenity relationships: {len(project_amenities)}")
        for pa in project_amenities:
            print(f"   - Project: {pa[3]} | Amenity: {pa[2]} (Project ID: {pa[0]}, Amenity ID: {pa[1]})")
        
        # 3. Check specifically for gym
        print(f"\n3️⃣ CHECKING FOR GYM SPECIFICALLY:")
        print("-" * 30)
        
        gym_query = """
            SELECT pa.project_id, pa.amenity_id, a.name as amenity_name, p.name as project_name
            FROM project_amenities pa
            JOIN amenities a ON pa.amenity_id = a.id
            JOIN projects p ON pa.project_id = p.id
            WHERE a.name ILIKE '%gym%'
            ORDER BY p.name
        """
        gym_results = db.execute(text(gym_query)).fetchall()
        
        print(f"   📊 Projects with gym: {len(gym_results)}")
        for gym in gym_results:
            print(f"   - Project: {gym[3]} (ID: {gym[0]}) | Amenity: {gym[2]} (ID: {gym[1]})")
        
        # 4. Check the exact EXISTS subquery that's failing
        print(f"\n4️⃣ TESTING THE EXACT EXISTS SUBQUERY:")
        print("-" * 30)
        
        # Test the EXISTS subquery for a specific project
        if gym_results:
            test_project_id = gym_results[0][0]  # Use first project with gym
            
            exists_query = """
                SELECT 1 FROM project_amenities pa
                JOIN amenities a ON pa.amenity_id = a.id
                WHERE pa.project_id = :project_id AND a.name ILIKE :amenity_name
            """
            
            exists_result = db.execute(text(exists_query), {
                "project_id": test_project_id,
                "amenity_name": "%gym%"
            }).fetchall()
            
            print(f"   🔍 Testing EXISTS for project ID {test_project_id}:")
            print(f"   📊 EXISTS result: {len(exists_result)} rows")
            print(f"   ✅ EXISTS subquery works: {'Yes' if exists_result else 'No'}")
        
        # 5. Check if the issue is with the main query structure
        print(f"\n5️⃣ TESTING MAIN QUERY STRUCTURE:")
        print("-" * 30)
        
        # Test a simple version of the main query with just the amenity filter
        simple_query = """
            SELECT COUNT(*) as count
            FROM properties pr
            JOIN projects p ON pr.project_id = p.id
            JOIN project_locations pl ON p.id = pl.project_id
            JOIN locations l ON pl.location_id = l.id
            WHERE EXISTS (
                SELECT 1 FROM project_amenities pa
                JOIN amenities a ON pa.amenity_id = a.id
                WHERE pa.project_id = p.id AND a.name ILIKE :amenity_name
            )
        """
        
        simple_result = db.execute(text(simple_query), {"amenity_name": "%gym%"}).fetchall()
        print(f"   🔍 Simple query with just amenity filter:")
        print(f"   📊 Results: {simple_result[0][0]} properties")
        
        # 6. Check if the issue is with the combination of filters
        print(f"\n6️⃣ TESTING FILTER COMBINATIONS:")
        print("-" * 30)
        
        # Test with location + amenity
        location_amenity_query = """
            SELECT COUNT(*) as count
            FROM properties pr
            JOIN projects p ON pr.project_id = p.id
            JOIN project_locations pl ON p.id = pl.project_id
            JOIN locations l ON pl.location_id = l.id
            WHERE (l.city ILIKE :location OR l.locality ILIKE :location)
            AND EXISTS (
                SELECT 1 FROM project_amenities pa
                JOIN amenities a ON pa.amenity_id = a.id
                WHERE pa.project_id = p.id AND a.name ILIKE :amenity_name
            )
        """
        
        location_amenity_result = db.execute(text(location_amenity_query), {
            "location": "%pune%",
            "amenity_name": "%gym%"
        }).fetchall()
        
        print(f"   🔍 Location + Amenity filter:")
        print(f"   📊 Results: {location_amenity_result[0][0]} properties")
        
        # Test with BHK + amenity
        bhk_amenity_query = """
            SELECT COUNT(*) as count
            FROM properties pr
            JOIN projects p ON pr.project_id = p.id
            JOIN project_locations pl ON p.id = pl.project_id
            JOIN locations l ON pl.location_id = l.id
            WHERE pr.bhk_count = :bhk
            AND EXISTS (
                SELECT 1 FROM project_amenities pa
                JOIN amenities a ON pa.amenity_id = a.id
                WHERE pa.project_id = p.id AND a.name ILIKE :amenity_name
            )
        """
        
        bhk_amenity_result = db.execute(text(bhk_amenity_query), {
            "bhk": 2.0,
            "amenity_name": "%gym%"
        }).fetchall()
        
        print(f"   🔍 BHK + Amenity filter:")
        print(f"   📊 Results: {bhk_amenity_result[0][0]} properties")
        
    except Exception as e:
        print(f"❌ Error investigating amenity data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    investigate_amenity_data()
