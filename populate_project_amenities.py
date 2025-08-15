#!/usr/bin/env python3
"""
Script to populate the project_amenities table to link projects with their amenities
"""

from backend.database import get_db
from sqlalchemy import text
import uuid
from datetime import datetime
import random

def populate_project_amenities():
    """Populate project_amenities table to link projects with amenities"""
    print("🏗️ Populating project_amenities table...")
    db = next(get_db())
    current_time = datetime.now()
    
    try:
        # Get project IDs
        proj_result = db.execute(text("SELECT id, name FROM projects"))
        projects = [(row[0], row[1]) for row in proj_result]
        
        # Get amenity IDs
        amenity_result = db.execute(text("SELECT id, name, category FROM amenities"))
        amenities = [(row[0], row[1], row[2]) for row in amenity_result]
        
        print(f"📋 Found {len(projects)} projects and {len(amenities)} amenities")
        
        # Define project-amenity mappings based on project type and realistic scenarios
        project_amenity_mappings = []
        
        for project_id, project_name in projects:
            # All projects get essential amenities
            essential_amenities = ['24/7 Security', 'Power Backup', 'Water Supply', 'Lift Service']
            
            # Premium projects get more amenities
            if 'Luxury' in project_name or 'Premium' in project_name or 'Godrej' in project_name or 'Lodha' in project_name:
                additional_amenities = [
                    'Swimming Pool', 'Gymnasium', 'Children Play Area', 'Garden', 'Party Hall',
                    'Clubhouse', 'Spa & Salon', 'Restaurant', 'Coffee Shop', 'Shopping Center',
                    'ATM', 'Medical Center', 'Car Wash', 'Covered Parking', 'Visitor Parking',
                    'High-Speed Internet', 'Smart Home Features', 'App-Based Services'
                ]
            else:
                # Mid-range projects get moderate amenities
                additional_amenities = [
                    'Gymnasium', 'Children Play Area', 'Garden', 'Clubhouse',
                    'Shopping Center', 'ATM', 'Covered Parking', 'High-Speed Internet'
                ]
            
            # Combine essential and additional amenities
            all_amenities = essential_amenities + additional_amenities
            
            # Add some random amenities for variety
            available_random_amenities = [a for a in amenities if a[1] not in all_amenities]
            if available_random_amenities:
                num_random = min(random.randint(2, 5), len(available_random_amenities))
                random_amenities = random.sample(available_random_amenities, num_random)
                all_amenities.extend([a[1] for a in random_amenities])
            
            # Create mappings for each amenity
            for amenity_name in all_amenities:
                # Find amenity ID
                amenity_id = None
                for a_id, a_name, a_category in amenities:
                    if a_name == amenity_name:
                        amenity_id = a_id
                        break
                
                if amenity_id:
                    # Determine if included in maintenance (essential amenities usually are)
                    included_in_maintenance = amenity_name in essential_amenities
                    
                    project_amenity_mappings.append({
                        'id': str(uuid.uuid4()),
                        'project_id': project_id,
                        'amenity_id': amenity_id,
                        'available': True,
                        'included_in_maintenance': included_in_maintenance,
                        'created_at': current_time,
                        'updated_at': current_time
                    })
        
        # Insert project-amenity mappings
        for mapping in project_amenity_mappings:
            insert_sql = """
            INSERT INTO project_amenities (id, project_id, amenity_id, available, 
                                         included_in_maintenance, created_at, updated_at)
            VALUES (:id, :project_id, :amenity_id, :available, 
                   :included_in_maintenance, :created_at, :updated_at)
            """
            db.execute(text(insert_sql), mapping)
        
        db.commit()
        print(f"✅ Successfully populated project_amenities table with {len(project_amenity_mappings)} mappings!")
        
        # Show the inserted data by project
        result = db.execute(text("""
            SELECT p.name as project_name, a.name as amenity_name, a.category,
                   pa.included_in_maintenance
            FROM project_amenities pa 
            JOIN projects p ON pa.project_id = p.id 
            JOIN amenities a ON pa.amenity_id = a.id 
            ORDER BY p.name, a.category, a.name
        """))
        print("\n📋 Project Amenities:")
        current_project = None
        for row in result:
            if current_project != row[0]:
                current_project = row[0]
                print(f"\n🏢 {current_project}:")
            maintenance_icon = "💰" if row[3] else "💳"
            print(f"  - {row[1]} ({row[2]}) {maintenance_icon}")
            
    except Exception as e:
        print(f"❌ Error populating project_amenities table: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    populate_project_amenities()
