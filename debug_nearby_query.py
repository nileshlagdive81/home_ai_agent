#!/usr/bin/env python3
"""
Script to debug the specific query step by step
"""

from backend.database import get_db
from sqlalchemy import text

def debug_nearby_query():
    """Debug the specific query step by step"""
    print("🔍 DEBUGGING: 3 BHK apartments in Pune above 1.5 crores with swimming pool and gym, located within 1 km of metro station")
    print("=" * 80)
    
    db = next(get_db())
    
    try:
        # Step 1: Basic 3 BHK in Pune
        print("1️⃣ STEP: 3 BHK in Pune")
        print("-" * 40)
        query1 = """
            SELECT COUNT(*) as count
            FROM properties pr
            JOIN projects p ON pr.project_id = p.id
            JOIN project_locations pl ON p.id = pl.project_id
            JOIN locations l ON pl.location_id = l.id
            WHERE l.city ILIKE '%pune%' AND pr.bhk_count = 3
        """
        result1 = db.execute(text(query1)).fetchone()[0]
        print(f"   📊 3 BHK in Pune: {result1} properties")
        
        # Step 2: Add price filter
        print("\n2️⃣ STEP: Add price filter (> 1.5 crores)")
        print("-" * 40)
        query2 = """
            SELECT COUNT(*) as count
            FROM properties pr
            JOIN projects p ON pr.project_id = p.id
            JOIN project_locations pl ON p.id = pl.project_id
            JOIN locations l ON pl.location_id = l.id
            WHERE l.city ILIKE '%pune%' AND pr.bhk_count = 3 AND pr.sell_price > 15000000
        """
        result2 = db.execute(text(query2)).fetchone()[0]
        print(f"   📊 3 BHK in Pune above 1.5 cr: {result2} properties")
        
        # Step 3: Add swimming pool amenity
        print("\n3️⃣ STEP: Add swimming pool amenity")
        print("-" * 40)
        query3 = """
            SELECT COUNT(*) as count
            FROM properties pr
            JOIN projects p ON pr.project_id = p.id
            JOIN project_locations pl ON p.id = pl.project_id
            JOIN locations l ON pl.location_id = l.id
            JOIN project_amenities pa ON p.id = pa.project_id
            JOIN amenities a ON pa.amenity_id = a.id
            WHERE l.city ILIKE '%pune%' 
            AND pr.bhk_count = 3 
            AND pr.sell_price > 15000000
            AND a.name ILIKE '%swimming%'
        """
        result3 = db.execute(text(query3)).fetchone()[0]
        print(f"   📊 3 BHK in Pune above 1.5 cr with swimming pool: {result3} properties")
        
        # Step 4: Add gym amenity
        print("\n4️⃣ STEP: Add gym amenity")
        print("-" * 40)
        query4 = """
            SELECT COUNT(*) as count
            FROM properties pr
            JOIN projects p ON pr.project_id = p.id
            JOIN project_locations pl ON p.id = pl.project_id
            JOIN locations l ON pl.location_id = l.id
            JOIN project_amenities pa ON p.id = pa.project_id
            JOIN amenities a ON pa.amenity_id = a.id
            WHERE l.city ILIKE '%pune%' 
            AND pr.bhk_count = 3 
            AND pr.sell_price > 15000000
            AND a.name ILIKE '%swimming%'
            AND EXISTS (
                SELECT 1 FROM project_amenities pa2
                JOIN amenities a2 ON pa2.amenity_id = a2.id
                WHERE pa2.project_id = p.id AND a2.name ILIKE '%gym%'
            )
        """
        result4 = db.execute(text(query4)).fetchone()[0]
        print(f"   📊 3 BHK in Pune above 1.5 cr with swimming pool AND gym: {result4} properties")
        
        # Step 5: Check what projects have both amenities
        print("\n5️⃣ STEP: Check projects with both amenities")
        print("-" * 40)
        query5 = """
            SELECT DISTINCT p.name as project_name, l.locality
            FROM projects p
            JOIN project_locations pl ON p.id = pl.project_id
            JOIN locations l ON pl.location_id = l.id
            JOIN project_amenities pa1 ON p.id = pa1.project_id
            JOIN amenities a1 ON pa1.amenity_id = a1.id
            JOIN project_amenities pa2 ON p.id = pa2.project_id
            JOIN amenities a2 ON pa2.amenity_id = a2.id
            WHERE l.city ILIKE '%pune%'
            AND a1.name ILIKE '%swimming%'
            AND a2.name ILIKE '%gym%'
            ORDER BY p.name, l.locality
        """
        projects_with_both = db.execute(text(query5)).fetchall()
        print(f"   📊 Projects with both swimming pool and gym:")
        for project in projects_with_both:
            print(f"      - {project[0]} in {project[1]}")
        
        # Step 6: Check nearby places for these projects
        print("\n6️⃣ STEP: Check nearby places for projects with both amenities")
        print("-" * 40)
        if projects_with_both:
            project_names = [f"'{p[0]}'" for p in projects_with_both]
            project_list = ", ".join(project_names)
            
            query6 = f"""
                SELECT p.name as project_name, l.locality, np.place_type, np.place_name, np.distance_km
                FROM projects p
                JOIN project_locations pl ON p.id = pl.project_id
                JOIN locations l ON pl.location_id = l.id
                JOIN nearby_places np ON p.id = np.project_id
                WHERE p.name IN ({project_list})
                AND np.place_type = 'METRO STATION'
                ORDER BY p.name, np.distance_km
            """
            nearby_metro = db.execute(text(query6)).fetchall()
            print(f"   📊 Metro stations near projects with both amenities:")
            for metro in nearby_metro:
                print(f"      - {metro[0]} in {metro[1]}: {metro[3]} at {metro[4]}km")
        
        # Step 7: Final query with all constraints
        print("\n7️⃣ STEP: Final query with all constraints")
        print("-" * 40)
        query7 = """
            SELECT COUNT(*) as count
            FROM properties pr
            JOIN projects p ON pr.project_id = p.id
            JOIN project_locations pl ON p.id = pl.project_id
            JOIN locations l ON pl.location_id = l.id
            JOIN project_amenities pa1 ON p.id = pa1.project_id
            JOIN amenities a1 ON pa1.amenity_id = a1.id
            JOIN project_amenities pa2 ON p.id = pa2.project_id
            JOIN amenities a2 ON pa2.amenity_id = a2.id
            JOIN nearby_places np ON p.id = np.project_id
            WHERE l.city ILIKE '%pune%' 
            AND pr.bhk_count = 3 
            AND pr.sell_price > 15000000
            AND a1.name ILIKE '%swimming%'
            AND a2.name ILIKE '%gym%'
            AND np.place_type = 'METRO STATION'
            AND np.distance_km <= 1.0
        """
        result7 = db.execute(text(query7)).fetchone()[0]
        print(f"   📊 Final result with all constraints: {result7} properties")
        
        # Step 8: Show what properties exist without nearby constraint
        print("\n8️⃣ STEP: Properties without nearby constraint")
        print("-" * 40)
        query8 = """
            SELECT pr.id, pr.bhk_count, pr.sell_price, p.name as project_name, l.locality
            FROM properties pr
            JOIN projects p ON pr.project_id = p.id
            JOIN project_locations pl ON p.id = pl.project_id
            JOIN locations l ON pl.location_id = l.id
            JOIN project_amenities pa1 ON p.id = pa1.project_id
            JOIN amenities a1 ON pa1.amenity_id = a1.id
            JOIN project_amenities pa2 ON p.id = pa2.project_id
            JOIN amenities a2 ON pa2.amenity_id = a2.id
            WHERE l.city ILIKE '%pune%' 
            AND pr.bhk_count = 3 
            AND pr.sell_price > 15000000
            AND a1.name ILIKE '%swimming%'
            AND a2.name ILIKE '%gym%'
            LIMIT 5
        """
        properties_without_nearby = db.execute(text(query8)).fetchall()
        print(f"   📊 Sample properties with both amenities (without nearby constraint):")
        for prop in properties_without_nearby:
            price_cr = prop[2] / 10000000
            print(f"      - ID: {prop[0]}, {prop[1]} BHK, ₹{price_cr:.1f} cr, {prop[3]} in {prop[4]}")
        
    except Exception as e:
        print(f"❌ Error debugging query: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    debug_nearby_query()
