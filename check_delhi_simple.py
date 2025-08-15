#!/usr/bin/env python3
"""
Simple script to examine current Delhi data structure
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from database import get_db
from models import Location, Project, Property, Amenity, ProjectAmenity, ProjectLocation

def check_delhi_data_simple():
    """Check current Delhi data structure with simple queries"""
    
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
        for proj in delhi_projects:
            print(f"  - Project: {proj.name}")
        
        # Check Delhi properties
        delhi_properties = db.query(Property).join(Project).join(ProjectLocation).join(Location).filter(Location.city.ilike('%Delhi%')).all()
        print(f"\n🏠 Delhi Properties Found: {len(delhi_properties)}")
        
        # Check amenities for Delhi projects (simpler approach)
        print(f"\n🎯 Checking Amenities for Delhi Projects:")
        for proj in delhi_projects:
            print(f"  Project: {proj.name}")
            # Get amenities for this project
            project_amenities = db.query(ProjectAmenity).filter(ProjectAmenity.project_id == proj.id).all()
            if project_amenities:
                for pa in project_amenities:
                    amenity = db.query(Amenity).filter(Amenity.id == pa.amenity_id).first()
                    if amenity:
                        print(f"    - {amenity.name} ({amenity.category})")
            else:
                print(f"    - No amenities found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_delhi_data_simple()
