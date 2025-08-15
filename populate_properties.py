#!/usr/bin/env python3
"""
Script to populate the properties table with realistic property data for all projects
"""

from backend.database import get_db
from sqlalchemy import text
import uuid
from datetime import datetime
import random

def populate_properties():
    """Populate properties table with realistic property data"""
    print("🏗️ Populating properties table...")
    db = next(get_db())
    current_time = datetime.now()
    
    try:
        # Get project IDs and names
        proj_result = db.execute(text("SELECT id, name FROM projects"))
        projects = [(row[0], row[1]) for row in proj_result]
        
        print(f"📋 Found {len(projects)} projects")
        
        # Define property data
        properties_data = []
        
        for project_id, project_name in projects:
            # Determine number of properties based on project size
            if 'Life Republic' in project_name:  # Large project
                num_properties = random.randint(80, 120)
            elif 'Luxury' in project_name or 'Premium' in project_name:
                num_properties = random.randint(40, 80)
            else:
                num_properties = random.randint(20, 50)
            
            print(f"🏢 {project_name}: Generating {num_properties} properties")
            
            # Generate properties for this project
            for i in range(num_properties):
                # Property type
                property_types = ['Apartment', 'Flat', 'Penthouse', 'Studio']
                property_type = random.choice(property_types)
                
                # BHK count (1-4 BHK)
                bhk_options = [1, 1.5, 2, 2.5, 3, 3.5, 4]
                bhk_count = random.choice(bhk_options)
                
                # Carpet area based on BHK
                if bhk_count == 1:
                    carpet_area = random.randint(400, 800)
                elif bhk_count == 1.5:
                    carpet_area = random.randint(600, 1000)
                elif bhk_count == 2:
                    carpet_area = random.randint(800, 1200)
                elif bhk_count == 2.5:
                    carpet_area = random.randint(1000, 1400)
                elif bhk_count == 3:
                    carpet_area = random.randint(1200, 1800)
                elif bhk_count == 3.5:
                    carpet_area = random.randint(1400, 2000)
                else:  # 4 BHK
                    carpet_area = random.randint(1800, 2500)
                
                # Super built-up area (usually 20-30% more than carpet area)
                super_builtup_multiplier = random.uniform(1.2, 1.3)
                super_builtup_area = int(carpet_area * super_builtup_multiplier)
                
                # Floor number (1-50, with more properties on lower floors)
                floor_weights = [0.4, 0.3, 0.2, 0.1]  # 40% on 1-10, 30% on 11-20, etc.
                floor_range = random.choices([(1, 10), (11, 20), (21, 35), (36, 50)], weights=floor_weights)[0]
                floor_number = random.randint(floor_range[0], floor_range[1])
                
                # Facing
                facing_options = ['North', 'South', 'East', 'West', 'North-East', 'North-West', 'South-East', 'South-West']
                facing = random.choice(facing_options)
                
                # Status
                status_options = ['Available', 'Booked', 'Sold', 'Under Construction']
                status = random.choice(status_options)
                
                # Price calculation based on area, BHK, and project type
                base_price_per_sqft = 8000  # Base price per sqft
                
                # Adjust price based on project type
                if 'Luxury' in project_name or 'Premium' in project_name:
                    base_price_per_sqft = random.randint(12000, 18000)
                elif 'Godrej' in project_name or 'Lodha' in project_name:
                    base_price_per_sqft = random.randint(10000, 15000)
                else:
                    base_price_per_sqft = random.randint(8000, 12000)
                
                # Adjust price based on BHK
                bhk_multiplier = 1.0
                if bhk_count >= 3:
                    bhk_multiplier = 1.2
                elif bhk_count >= 2:
                    bhk_multiplier = 1.1
                
                # Adjust price based on floor
                floor_multiplier = 1.0
                if floor_number > 20:
                    floor_multiplier = 1.15
                elif floor_number > 10:
                    floor_multiplier = 1.08
                
                # Calculate final price
                price_per_sqft = base_price_per_sqft * bhk_multiplier * floor_multiplier
                sell_price = int(carpet_area * price_per_sqft)
                
                # Ensure price is within the specified range (50 lakhs to 3 crores)
                min_price = 5000000  # 50 lakhs
                max_price = 30000000  # 3 crores
                
                if sell_price < min_price:
                    sell_price = min_price
                elif sell_price > max_price:
                    sell_price = max_price
                
                properties_data.append({
                    'id': str(uuid.uuid4()),
                    'project_id': project_id,
                    'property_type': property_type,
                    'bhk_count': bhk_count,
                    'carpet_area_sqft': carpet_area,
                    'super_builtup_area_sqft': super_builtup_area,
                    'floor_number': floor_number,
                    'facing': facing,
                    'status': status,
                    'sell_price': sell_price,
                    'created_at': current_time,
                    'updated_at': current_time
                })
        
        # Insert properties data
        for property_data in properties_data:
            insert_sql = """
            INSERT INTO properties (id, project_id, property_type, bhk_count, 
                                  carpet_area_sqft, super_builtup_area_sqft, 
                                  floor_number, facing, status, sell_price, 
                                  created_at, updated_at)
            VALUES (:id, :project_id, :property_type, :bhk_count, 
                   :carpet_area_sqft, :super_builtup_area_sqft, 
                   :floor_number, :facing, :status, :sell_price, 
                   :created_at, :updated_at)
            """
            db.execute(text(insert_sql), property_data)
        
        db.commit()
        print(f"✅ Successfully populated properties table with {len(properties_data)} properties!")
        
        # Show summary by project
        result = db.execute(text("""
            SELECT p.name as project_name, 
                   COUNT(prop.id) as property_count,
                   AVG(prop.sell_price) as avg_price,
                   MIN(prop.sell_price) as min_price,
                   MAX(prop.sell_price) as max_price
            FROM projects p 
            LEFT JOIN properties prop ON p.id = prop.project_id 
            GROUP BY p.id, p.name 
            ORDER BY p.name
        """))
        print("\n📋 Properties Summary by Project:")
        for row in result:
            avg_price = int(row[2]) if row[2] else 0
            min_price = int(row[3]) if row[3] else 0
            max_price = int(row[4]) if row[4] else 0
            print(f"🏢 {row[0]}: {row[1]} properties")
            print(f"   💰 Price Range: ₹{min_price:,} - ₹{max_price:,}")
            print(f"   📊 Average Price: ₹{avg_price:,}")
            print()
            
    except Exception as e:
        print(f"❌ Error populating properties table: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    populate_properties()
