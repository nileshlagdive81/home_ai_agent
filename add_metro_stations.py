#!/usr/bin/env python3
"""
Script to add metro stations to the nearby places table for Pune projects
"""

from backend.database import get_db
from sqlalchemy import text
import uuid
from datetime import datetime

def add_metro_stations():
    """Add metro stations to the nearby places table for Pune projects"""
    print("🚇 ADDING METRO STATIONS TO NEARBY PLACES")
    print("=" * 60)
    
    db = next(get_db())
    
    try:
        # First, let's see what projects we have in Pune
        print("1️⃣ CHECKING PUNE PROJECTS:")
        print("-" * 40)
        projects_query = """
            SELECT DISTINCT p.id, p.name, l.locality
            FROM projects p
            JOIN project_locations pl ON p.id = pl.project_id
            JOIN locations l ON pl.location_id = l.id
            WHERE l.city ILIKE '%pune%'
            ORDER BY p.name, l.locality
        """
        pune_projects = db.execute(text(projects_query)).fetchall()
        print(f"   📊 Found {len(pune_projects)} Pune project locations")
        
        # Define metro stations for each project based on locality
        metro_data = {
            # Kolte Patil Westend - Aundh/Baner (closest to metro)
            'Kolte Patil Westend': {
                'Aundh': {'name': 'Metro Hub', 'distance': 0.7, 'walking': True},
                'Baner': {'name': 'Metro Hub', 'distance': 0.8, 'walking': True}
            },
            # Lodha Belmondo - Kalyani Nagar/Koregaon Park
            'Lodha Belmondo': {
                'Kalyani Nagar': {'name': 'Metro Hub', 'distance': 1.8, 'walking': True},
                'Koregaon Park': {'name': 'Metro Hub', 'distance': 2.1, 'walking': True}
            },
            # Godrej Emerald - Kharadi/Magarpatta City/Viman Nagar
            'Godrej Emerald': {
                'Kharadi': {'name': 'Metro Hub', 'distance': 2.6, 'walking': False},
                'Magarpatta City': {'name': 'Metro Hub', 'distance': 2.8, 'walking': False},
                'Viman Nagar': {'name': 'Metro Hub', 'distance': 3.2, 'walking': False}
            },
            # Kolte Patil Life Republic - Hadapsar/Hinjewadi/Wakad
            'Kolte Patil Life Republic': {
                'Hadapsar': {'name': 'Metro Hub', 'distance': 3.5, 'walking': False},
                'Hinjewadi': {'name': 'Metro Hub', 'distance': 4.2, 'walking': False},
                'Wakad': {'name': 'Metro Hub', 'distance': 3.8, 'walking': False}
            }
        }
        
        print("\n2️⃣ ADDING METRO STATIONS:")
        print("-" * 40)
        
        added_count = 0
        for project_id, project_name, locality in pune_projects:
            if project_name in metro_data and locality in metro_data[project_name]:
                metro_info = metro_data[project_name][locality]
                
                # Check if metro station already exists for this project
                check_query = """
                    SELECT COUNT(*) FROM nearby_places 
                    WHERE project_id = :project_id AND place_type = 'METRO STATION'
                """
                exists = db.execute(text(check_query), {"project_id": str(project_id)}).fetchone()[0]
                
                if exists == 0:
                    # Insert metro station
                    insert_query = """
                        INSERT INTO nearby_places (id, project_id, place_type, place_name, distance_km, walking_distance, created_at, updated_at)
                        VALUES (:id, :project_id, :place_type, :place_name, :distance_km, :walking_distance, :created_at, :updated_at)
                    """
                    db.execute(text(insert_query), {
                        "id": str(uuid.uuid4()),
                        "project_id": str(project_id),
                        "place_type": "METRO STATION",
                        "place_name": metro_info['name'],
                        "distance_km": metro_info['distance'],
                        "walking_distance": metro_info['walking'],
                        "created_at": datetime.now(),
                        "updated_at": datetime.now()
                    })
                    print(f"   ✅ Added {metro_info['name']} at {metro_info['distance']}km to {project_name} in {locality}")
                    added_count += 1
                else:
                    print(f"   ℹ️ Metro station already exists for {project_name} in {locality}")
        
        db.commit()
        print(f"\n📊 Total metro stations added: {added_count}")
        
        # Verify the addition
        print("\n3️⃣ VERIFYING METRO STATIONS:")
        print("-" * 40)
        verify_query = """
            SELECT COUNT(*) as count
            FROM nearby_places
            WHERE place_type = 'METRO STATION'
        """
        metro_count = db.execute(text(verify_query)).fetchone()[0]
        print(f"   📊 Total metro stations in database: {metro_count}")
        
        # Show sample metro stations
        sample_query = """
            SELECT np.place_name, np.distance_km, p.name as project_name, l.locality
            FROM nearby_places np
            JOIN projects p ON np.project_id = p.id
            JOIN project_locations pl ON p.id = pl.project_id
            JOIN locations l ON pl.location_id = l.id
            WHERE np.place_type = 'METRO STATION'
            ORDER BY np.distance_km
            LIMIT 5
        """
        sample_metros = db.execute(text(sample_query)).fetchall()
        print(f"   📊 Sample metro stations:")
        for metro in sample_metros:
            print(f"      - {metro[0]} at {metro[1]}km - {metro[2]} in {metro[3]}")
        
    except Exception as e:
        print(f"❌ Error adding metro stations: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    add_metro_stations()
