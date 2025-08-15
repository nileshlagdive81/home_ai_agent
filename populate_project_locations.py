#!/usr/bin/env python3
"""
Script to populate the project_locations table to link projects with their locations
"""

from backend.database import get_db
from sqlalchemy import text
import uuid
from datetime import datetime

def populate_project_locations():
    """Populate project_locations table to link projects with locations"""
    print("🏗️ Populating project_locations table...")
    db = next(get_db())
    current_time = datetime.now()
    
    try:
        # Get project IDs and names
        proj_result = db.execute(text("SELECT id, name FROM projects"))
        projects = [(row[0], row[1]) for row in proj_result]
        
        # Get location IDs, cities, and localities
        loc_result = db.execute(text("SELECT id, city, locality FROM locations"))
        locations = [(row[0], row[1], row[2]) for row in loc_result]
        
        print(f"📋 Found {len(projects)} projects and {len(locations)} locations")
        
        # Define project-location mappings based on realistic scenarios
        project_location_mappings = [
            # Mumbai Projects
            ('Lodha Park', 'Mumbai', 'Bandra West'),
            ('Lodha Park', 'Mumbai', 'Juhu'),
            ('Godrej Bayview', 'Mumbai', 'Worli'),
            ('Godrej Bayview', 'Mumbai', 'Lower Parel'),
            ('Raheja Vivarea', 'Mumbai', 'Andheri West'),
            ('Raheja Vivarea', 'Mumbai', 'Powai'),
            ('Prestige Seawoods', 'Mumbai', 'Thane West'),
            ('Prestige Seawoods', 'Mumbai', 'Navi Mumbai'),
            
            # Pune Projects
            ('Kolte Patil Life Republic', 'Pune', 'Hinjewadi'),
            ('Kolte Patil Life Republic', 'Pune', 'Wakad'),
            ('Kolte Patil Westend', 'Pune', 'Baner'),
            ('Kolte Patil Westend', 'Pune', 'Aundh'),
            ('Lodha Belmondo', 'Pune', 'Koregaon Park'),
            ('Lodha Belmondo', 'Pune', 'Kalyani Nagar'),
            ('Godrej Emerald', 'Pune', 'Viman Nagar'),
            ('Godrej Emerald', 'Pune', 'Kharadi'),
            ('Godrej Emerald', 'Pune', 'Magarpatta City'),
            ('Kolte Patil Life Republic', 'Pune', 'Hadapsar')
        ]
        
        # Insert project-location mappings
        inserted_count = 0
        for project_name, city, locality in project_location_mappings:
            # Find project ID
            project_id = None
            for proj_id, proj_name in projects:
                if proj_name == project_name:
                    project_id = proj_id
                    break
            
            # Find location ID
            location_id = None
            for loc_id, loc_city, loc_locality in locations:
                if loc_city == city and loc_locality == locality:
                    location_id = loc_id
                    break
            
            if project_id and location_id:
                insert_sql = """
                INSERT INTO project_locations (id, project_id, location_id, created_at, updated_at)
                VALUES (:id, :project_id, :location_id, :created_at, :updated_at)
                """
                db.execute(text(insert_sql), {
                    'id': str(uuid.uuid4()),
                    'project_id': project_id,
                    'location_id': location_id,
                    'created_at': current_time,
                    'updated_at': current_time
                })
                inserted_count += 1
            else:
                print(f"⚠️ Could not find mapping for {project_name} in {city}, {locality}")
        
        db.commit()
        print(f"✅ Successfully populated project_locations table with {inserted_count} mappings!")
        
        # Show the inserted data
        result = db.execute(text("""
            SELECT p.name as project_name, l.city, l.locality 
            FROM project_locations pl 
            JOIN projects p ON pl.project_id = p.id 
            JOIN locations l ON pl.location_id = l.id 
            ORDER BY p.name, l.city, l.locality
        """))
        print("\n📋 Project-Location Mappings:")
        current_project = None
        for row in result:
            if current_project != row[0]:
                current_project = row[0]
                print(f"\n🏢 {current_project}:")
            print(f"  - {row[1]}, {row[2]}")
            
    except Exception as e:
        print(f"❌ Error populating project_locations table: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    populate_project_locations()
