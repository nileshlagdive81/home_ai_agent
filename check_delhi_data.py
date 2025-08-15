#!/usr/bin/env python3
"""
Script to examine current Delhi data structure
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from database import get_db
from models import Location, Project, Property, Amenity, ProjectAmenity, ProjectLocation

def check_delhi_data():
    """Check current Delhi data structure"""
    
    db = next(get_db())
    
    print("🔍 Examining Delhi Data Structure:")
    print("=" * 60)
    
    try:
        # Check Delhi locations
        delhi_locations = db.query(Location).filter(Location.city.ilike('%Delhi%')).all()
        print(f"\n📍 Delhi Locations Found: {len(delhi_locations)}")
        for loc in delhi_locations:
            print(f"  - City: {loc.city}, Locality: {loc.locality}, Area: {loc.area}")
        
        # Check Delhi projects
        delhi_projects = db.query(Project).join(ProjectLocation).join(Location).filter(Location.city.ilike('%Delhi%')).all()
        print(f"\n🏢 Delhi Projects Found: {len(delhi_projects)}")
        for proj in delhi_projects[:5]:  # Show first 5
            print(f"  - Project: {proj.name}")
        
        # Check Delhi properties
        delhi_properties = db.query(Property).join(Project).join(ProjectLocation).join(Location).filter(Location.city.ilike('%Delhi%')).all()
        print(f"\n🏠 Delhi Properties Found: {len(delhi_properties)}")
        
        # Check amenities for Delhi projects
        delhi_amenities = db.query(Amenity).join(ProjectAmenity).join(Project).join(ProjectLocation).join(Location).filter(Location.city.ilike('%Delhi%')).distinct().all()
        print(f"\n🎯 Amenities for Delhi Projects: {len(delhi_amenities)}")
        for amenity in delhi_amenities:
            print(f"  - {amenity.name}")
        
        # Check nearby places for Delhi projects (if table exists)
        try:
            from models.nearby_place import NearbyPlace
            delhi_nearby = db.query(NearbyPlace).join(Project).join(ProjectLocation).join(Location).filter(Location.city.ilike('%Delhi%')).distinct().all()
            print(f"\n🚇 Nearby Places for Delhi Projects: {len(delhi_nearby)}")
            for nearby in delhi_nearby[:10]:  # Show first 10
                print(f"  - {nearby.name} ({nearby.category}) - {nearby.distance_km}km")
        except ImportError:
            print(f"\n🚇 Nearby Places table not available in current models")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_delhi_data()
