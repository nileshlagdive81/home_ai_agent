#!/usr/bin/env python3
"""
Script to populate the nearby_places table with realistic nearby places for each project
"""

from backend.database import get_db
from sqlalchemy import text
import uuid
from datetime import datetime
import random

def populate_nearby_places():
    """Populate nearby_places table with realistic nearby places"""
    print("🏗️ Populating nearby_places table...")
    db = next(get_db())
    current_time = datetime.now()
    
    try:
        # Get project IDs
        proj_result = db.execute(text("SELECT id, name FROM projects"))
        projects = [(row[0], row[1]) for row in proj_result]
        
        print(f"📋 Found {len(projects)} projects")
        
        # Define nearby places data for each project
        nearby_places_data = []
        
        for project_id, project_name in projects:
            # Generate 5-8 nearby places for each project
            num_places = random.randint(5, 8)
            
            # Define place types and names
            place_types = [
                'School', 'Hospital', 'Railway Station', 'Metro Station', 'Bus Stand',
                'Mall', 'Market', 'Restaurant', 'Bank', 'ATM', 'Pharmacy', 'Gym',
                'Park', 'Cinema', 'Shopping Center', 'Medical Store', 'Petrol Pump',
                'Post Office', 'Police Station', 'Fire Station'
            ]
            
            place_names = [
                'Central School', 'City Hospital', 'Main Railway Station', 'Metro Hub',
                'Central Bus Stand', 'Mega Mall', 'Local Market', 'Food Court',
                'State Bank', 'ATM Center', 'Medical Center', 'Fitness Zone',
                'Central Park', 'Multiplex', 'Shopping Complex', 'Health Store',
                'Fuel Station', 'Post Office', 'Police Station', 'Fire Station'
            ]
            
            # Select random places for this project
            selected_places = random.sample(list(zip(place_types, place_names)), num_places)
            
            for place_type, place_name in selected_places:
                # Generate realistic distance (0.5 to 3.0 km)
                distance = round(random.uniform(0.5, 3.0), 1)
                # Walking distance if less than 1.5 km
                walking_distance = distance <= 1.5
                
                nearby_places_data.append({
                    'id': str(uuid.uuid4()),
                    'project_id': project_id,
                    'place_type': place_type,
                    'place_name': place_name,
                    'distance_km': distance,
                    'walking_distance': walking_distance,
                    'created_at': current_time,
                    'updated_at': current_time
                })
        
        # Insert nearby places data
        for place_data in nearby_places_data:
            insert_sql = """
            INSERT INTO nearby_places (id, project_id, place_type, place_name, 
                                     distance_km, walking_distance, created_at, updated_at)
            VALUES (:id, :project_id, :place_type, :place_name, 
                   :distance_km, :walking_distance, :created_at, :updated_at)
            """
            db.execute(text(insert_sql), place_data)
        
        db.commit()
        print(f"✅ Successfully populated nearby_places table with {len(nearby_places_data)} places!")
        
        # Show the inserted data by project
        result = db.execute(text("""
            SELECT p.name as project_name, np.place_type, np.place_name, 
                   np.distance_km, np.walking_distance
            FROM nearby_places np 
            JOIN projects p ON np.project_id = p.id 
            ORDER BY p.name, np.distance_km
        """))
        print("\n📋 Nearby Places by Project:")
        current_project = None
        for row in result:
            if current_project != row[0]:
                current_project = row[0]
                print(f"\n🏢 {current_project}:")
            walking_icon = "🚶" if row[4] else "🚗"
            print(f"  - {row[1]}: {row[2]} ({row[3]} km) {walking_icon}")
            
    except Exception as e:
        print(f"❌ Error populating nearby_places table: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    populate_nearby_places()
