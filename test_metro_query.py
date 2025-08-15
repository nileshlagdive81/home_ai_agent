#!/usr/bin/env python3
"""
Script to test the metro query after adding metro stations
"""

from backend.database import get_db
from sqlalchemy import text

def test_metro_query():
    """Test the metro query after adding metro stations"""
    print("🧪 TESTING: 3 BHK apartments in Pune above 1.5 crores with gym, located within 3 km of metro station")
    print("=" * 80)
    
    db = next(get_db())
    
    try:
        # Test the working query with 3km constraint
        print("1️⃣ TESTING: Final query with 3km metro constraint")
        print("-" * 40)
        query = """
            SELECT COUNT(*) as count
            FROM properties pr
            JOIN projects p ON pr.project_id = p.id
            JOIN project_locations pl ON p.id = pl.project_id
            JOIN locations l ON pl.location_id = l.id
            JOIN project_amenities pa ON p.id = pa.project_id
            JOIN amenities a ON pa.amenity_id = a.id
            JOIN nearby_places np ON p.id = np.project_id
            WHERE l.city ILIKE '%pune%' 
            AND pr.bhk_count = 3 
            AND pr.sell_price > 15000000
            AND a.name ILIKE '%gym%'
            AND np.place_type = 'METRO STATION'
            AND np.distance_km <= 3.0
        """
        result = db.execute(text(query)).fetchone()[0]
        print(f"   📊 3 BHK in Pune above 1.5 cr with gym near metro (≤3km): {result} properties")
        
        # Show the actual properties
        print("\n2️⃣ SHOWING: Properties that match the criteria")
        print("-" * 40)
        properties_query = """
            SELECT pr.id, pr.bhk_count, pr.sell_price, p.name as project_name, l.locality, np.distance_km
            FROM properties pr
            JOIN projects p ON pr.project_id = p.id
            JOIN project_locations pl ON p.id = pl.project_id
            JOIN locations l ON pl.location_id = l.id
            JOIN project_amenities pa ON p.id = pa.project_id
            JOIN amenities a ON pa.amenity_id = a.id
            JOIN nearby_places np ON p.id = np.project_id
            WHERE l.city ILIKE '%pune%' 
            AND pr.bhk_count = 3 
            AND pr.sell_price > 15000000
            AND a.name ILIKE '%gym%'
            AND np.place_type = 'METRO STATION'
            AND np.distance_km <= 3.0
            ORDER BY np.distance_km
        """
        properties = db.execute(text(properties_query)).fetchall()
        print(f"   📊 Properties found:")
        for prop in properties:
            price_cr = prop[2] / 10000000
            print(f"      - {prop[3]} in {prop[4]}: {prop[1]} BHK, ₹{price_cr:.1f} cr, Metro at {prop[5]}km")
        
        # Test with EXISTS subquery (alternative approach)
        print("\n3️⃣ TESTING: Alternative EXISTS subquery approach")
        print("-" * 40)
        exists_query = """
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
            AND a.name ILIKE '%gym%'
            AND EXISTS (
                SELECT 1 FROM nearby_places np
                WHERE np.project_id = p.id 
                AND np.place_type = 'METRO STATION'
                AND np.distance_km <= 3.0
            )
        """
        exists_result = db.execute(text(exists_query)).fetchone()[0]
        print(f"   📊 Using EXISTS subquery: {exists_result} properties")
        
    except Exception as e:
        print(f"❌ Error testing metro query: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    test_metro_query()
