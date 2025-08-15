#!/usr/bin/env python3
"""
Script to populate the projects table with realistic project data for Pune and Mumbai
"""

from backend.database import get_db
from sqlalchemy import text
import uuid
from datetime import datetime, date, timedelta
import random

def populate_projects():
    """Populate projects table with realistic project data"""
    print("🏗️ Populating projects table...")
    db = next(get_db())
    current_time = datetime.now()
    
    try:
        # Get developer IDs
        dev_result = db.execute(text("SELECT id FROM developers"))
        developer_ids = [row[0] for row in dev_result]
        
        # Get location IDs
        loc_result = db.execute(text("SELECT id, city, locality FROM locations"))
        location_data = [(row[0], row[1], row[2]) for row in loc_result]
        
        print(f"📋 Found {len(developer_ids)} developers and {len(location_data)} locations")
        
        # Insert realistic project data
        projects_data = [
            # Mumbai Projects
            {
                'id': str(uuid.uuid4()),
                'name': 'Lodha Park',
                'developer_id': developer_ids[0],  # Lodha Group
                'description': 'Luxury residential project with world-class amenities in the heart of Mumbai',
                'project_type': 'Residential',
                'total_units': 450,
                'units_per_floor': 8,
                'total_floors': 45,
                'project_status': 'Ready to Move',
                'rera_number': 'MahaRERA/A51234/2023',
                'possession_date': date(2024, 6, 15),
                'completion_date': date(2024, 6, 15),
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Godrej Bayview',
                'developer_id': developer_ids[1],  # Godrej Properties
                'description': 'Premium waterfront residential project with panoramic sea views',
                'project_type': 'Residential',
                'total_units': 320,
                'units_per_floor': 6,
                'total_floors': 38,
                'project_status': 'Under Construction',
                'rera_number': 'MahaRERA/A51235/2023',
                'possession_date': date(2025, 12, 31),
                'completion_date': date(2025, 12, 31),
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Raheja Vivarea',
                'developer_id': developer_ids[3],  # K Raheja Corp
                'description': 'Modern residential complex with smart home features and green living',
                'project_type': 'Residential',
                'total_units': 280,
                'units_per_floor': 7,
                'total_floors': 35,
                'project_status': 'Ready to Move',
                'rera_number': 'MahaRERA/A51236/2023',
                'possession_date': date(2024, 3, 20),
                'completion_date': date(2024, 3, 20),
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Prestige Seawoods',
                'developer_id': developer_ids[4],  # Prestige Group
                'description': 'Luxury residential project with premium amenities and sea views',
                'project_type': 'Residential',
                'total_units': 180,
                'units_per_floor': 5,
                'total_floors': 28,
                'project_status': 'Under Construction',
                'rera_number': 'MahaRERA/A51237/2023',
                'possession_date': date(2026, 6, 30),
                'completion_date': date(2026, 6, 30),
                'created_at': current_time,
                'updated_at': current_time
            },
            
            # Pune Projects
            {
                'id': str(uuid.uuid4()),
                'name': 'Kolte Patil Life Republic',
                'developer_id': developer_ids[2],  # Kolte Patil Developers
                'description': 'Integrated township with residential, commercial, and recreational facilities',
                'project_type': 'Residential',
                'total_units': 650,
                'units_per_floor': 10,
                'total_floors': 42,
                'project_status': 'Ready to Move',
                'rera_number': 'MahaRERA/A51238/2023',
                'possession_date': date(2024, 1, 15),
                'completion_date': date(2024, 1, 15),
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Kolte Patil Westend',
                'developer_id': developer_ids[2],  # Kolte Patil Developers
                'description': 'Premium residential project with modern amenities and green spaces',
                'project_type': 'Residential',
                'total_units': 420,
                'units_per_floor': 8,
                'total_floors': 35,
                'project_status': 'Under Construction',
                'rera_number': 'MahaRERA/A51239/2023',
                'possession_date': date(2025, 9, 30),
                'completion_date': date(2025, 9, 30),
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Lodha Belmondo',
                'developer_id': developer_ids[0],  # Lodha Group
                'description': 'Luxury residential project with premium amenities and golf course views',
                'project_type': 'Residential',
                'total_units': 380,
                'units_per_floor': 6,
                'total_floors': 32,
                'project_status': 'Ready to Move',
                'rera_number': 'MahaRERA/A51240/2023',
                'possession_date': date(2024, 8, 20),
                'completion_date': date(2024, 8, 20),
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Godrej Emerald',
                'developer_id': developer_ids[1],  # Godrej Properties
                'description': 'Green residential project with sustainable living features',
                'project_type': 'Residential',
                'total_units': 290,
                'units_per_floor': 7,
                'total_floors': 25,
                'project_status': 'Under Construction',
                'rera_number': 'MahaRERA/A51241/2023',
                'possession_date': date(2026, 3, 15),
                'completion_date': date(2026, 3, 15),
                'created_at': current_time,
                'updated_at': current_time
            }
        ]
        
        for project_data in projects_data:
            insert_sql = """
            INSERT INTO projects (id, name, developer_id, description, project_type, total_units, 
                                units_per_floor, total_floors, project_status, rera_number, 
                                possession_date, completion_date, created_at, updated_at)
            VALUES (:id, :name, :developer_id, :description, :project_type, :total_units,
                   :units_per_floor, :total_floors, :project_status, :rera_number,
                   :possession_date, :completion_date, :created_at, :updated_at)
            """
            db.execute(text(insert_sql), project_data)
        
        db.commit()
        print(f"✅ Successfully populated projects table with {len(projects_data)} projects!")
        
        # Show the inserted data
        result = db.execute(text("SELECT p.name, p.project_type, p.project_status, p.total_units, d.name as developer FROM projects p JOIN developers d ON p.developer_id = d.id ORDER BY p.name"))
        print("\n📋 Inserted projects:")
        for row in result:
            print(f"  - {row[0]} ({row[1]}) - {row[2]} - {row[3]} units by {row[4]}")
            
    except Exception as e:
        print(f"❌ Error populating projects table: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    populate_projects()
