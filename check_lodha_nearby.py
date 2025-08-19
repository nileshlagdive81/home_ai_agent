#!/usr/bin/env python3
"""
Script to check which properties have nearby places data, specifically Lodha projects
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from database import get_db
from models import Project, NearbyPlace

def check_lodha_nearby_places():
    """Check nearby places data for Lodha projects"""
    try:
        db = next(get_db())
        
        # Find all Lodha projects
        lodha_projects = db.query(Project).filter(Project.name.ilike('%Lodha%')).all()
        
        print("=" * 60)
        print("LODHA PROJECTS NEARBY PLACES VERIFICATION")
        print("=" * 60)
        
        if not lodha_projects:
            print("❌ No Lodha projects found in the database")
            return
        
        print(f"✅ Found {len(lodha_projects)} Lodha project(s):")
        for project in lodha_projects:
            print(f"  - {project.name} (ID: {project.id})")
        
        print("\n" + "=" * 60)
        print("NEARBY PLACES DATA FOR LODHA PROJECTS")
        print("=" * 60)
        
        total_places = 0
        for project in lodha_projects:
            print(f"\n🏢 {project.name}:")
            
            # Get nearby places for this project
            nearby_places = db.query(NearbyPlace).filter(
                NearbyPlace.project_id == project.id
            ).order_by(NearbyPlace.place_type, NearbyPlace.distance_km).all()
            
            if not nearby_places:
                print("  ❌ No nearby places data found")
                continue
            
            print(f"  ✅ Found {len(nearby_places)} nearby places:")
            total_places += len(nearby_places)
            
            # Group by place type
            places_by_type = {}
            for place in nearby_places:
                place_type = place.place_type
                if place_type not in places_by_type:
                    places_by_type[place_type] = []
                places_by_type[place_type].append(place)
            
            # Display grouped by category
            for place_type, places in places_by_type.items():
                print(f"    📍 {place_type}:")
                for place in places:
                    walking_badge = "🚶‍♂️" if place.walking_distance else ""
                    print(f"      - {place.place_name}: {place.distance_km}km {walking_badge}")
        
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Total Lodha Projects: {len(lodha_projects)}")
        print(f"Total Nearby Places: {total_places}")
        
        if total_places > 0:
            print("✅ Lodha projects have nearby places data!")
        else:
            print("❌ Lodha projects need nearby places data!")
        
        # Also check all projects with nearby places
        print("\n" + "=" * 60)
        print("ALL PROJECTS WITH NEARBY PLACES DATA")
        print("=" * 60)
        
        all_projects_with_places = db.query(Project).join(NearbyPlace).distinct().all()
        print(f"Total projects with nearby places: {len(all_projects_with_places)}")
        
        for project in all_projects_with_places:
            place_count = db.query(NearbyPlace).filter(
                NearbyPlace.project_id == project.id
            ).count()
            print(f"  - {project.name}: {place_count} places")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    check_lodha_nearby_places()
