#!/usr/bin/env python3
"""
Script to check nearby places for Pune projects
"""

from backend.database import get_db
from sqlalchemy import text

def check_pune_nearby():
    """Check nearby places for Pune projects"""
    print("🔍 CHECKING NEARBY PLACES FOR PUNE PROJECTS")
    print("=" * 60)
    
    db = next(get_db())
    
    try:
        # Get all nearby places for Pune projects
        nearby_query = """
            SELECT DISTINCT np.place_name, np.place_type, np.distance_km, np.walking_distance,
                   p.name as project_name, l.locality, l.city
            FROM nearby_places np
            JOIN projects p ON np.project_id = p.id
            JOIN project_locations pl ON p.id = pl.project_id
            JOIN locations l ON pl.location_id = l.id
            WHERE l.city ILIKE '%pune%'
            ORDER BY np.place_type, np.place_name, np.distance_km
        """
        
        nearby_places = db.execute(text(nearby_query)).fetchall()
        
        print(f"📊 Total nearby places for Pune projects: {len(nearby_places)}")
        print("\n🏗️ NEARBY PLACES BY TYPE:")
        print("-" * 50)
        
        # Group by place type
        place_types = {}
        for place in nearby_places:
            place_type = place[1]  # np.place_type
            if place_type not in place_types:
                place_types[place_type] = []
            place_types[place_type].append(place)
        
        for place_type, places in place_types.items():
            print(f"\n📍 {place_type.upper()}:")
            print(f"   📊 Count: {len(places)}")
            for place in places:
                place_name, _, distance, walking, project, locality, city = place
                walking_text = "🚶 Walking distance" if walking else "🚗 Driving distance"
                print(f"   - {place_name} ({distance}km) - {walking_text} - {project} in {locality}")
        
        # Show unique place names for complex queries
        print(f"\n🔍 UNIQUE PLACE NAMES FOR COMPLEX QUERIES:")
        print("-" * 50)
        unique_places = set()
        for place in nearby_places:
            unique_places.add(place[0])  # place_name
        
        for place_name in sorted(unique_places):
            print(f"   - {place_name}")
        
        # Show distance ranges
        distances = [float(place[2]) for place in nearby_places if place[2]]
        if distances:
            print(f"\n📏 DISTANCE RANGES:")
            print(f"   - Min: {min(distances)} km")
            print(f"   - Max: {max(distances)} km")
            print(f"   - Average: {sum(distances)/len(distances):.1f} km")
        
        # Show walking distance options
        walking_count = sum(1 for place in nearby_places if place[3])  # walking_distance
        print(f"\n🚶 WALKING DISTANCE OPTIONS:")
        print(f"   - Walking distance places: {walking_count}")
        print(f"   - Driving distance places: {len(nearby_places) - walking_count}")
        
    except Exception as e:
        print(f"❌ Error checking nearby places: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    check_pune_nearby()
