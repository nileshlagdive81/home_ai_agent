#!/usr/bin/env python3
"""
Minimal script to populate database with basic data for Pune and Mumbai
"""

import uuid
import random
from datetime import datetime
from backend.database import get_db
from backend.models import *

def populate_minimal_data():
    """Populate database with minimal data"""
    print("🌱 Populating Database with Minimal Data...")
    print("=" * 60)
    
    db = next(get_db())
    
    try:
        # 1. Create cities and locations
        print("\n📍 Creating cities and locations...")
        
        # Pune locations with realistic areas
        pune_locations = [
            {"locality": "Baner", "area": "West Pune", "pincode": "411045", "metro": True, "airport": 12.0, "railway": 8.0, "bus": 2.0},
            {"locality": "Hinjewadi", "area": "West Pune", "pincode": "411057", "metro": False, "airport": 18.0, "railway": 12.0, "bus": 1.5},
            {"locality": "Wakad", "area": "West Pune", "pincode": "411057", "metro": False, "airport": 20.0, "railway": 15.0, "bus": 2.0},
            {"locality": "Koregaon Park", "area": "Central Pune", "pincode": "411001", "metro": True, "airport": 8.0, "railway": 3.0, "bus": 1.0},
            {"locality": "Kalyani Nagar", "area": "Central Pune", "pincode": "411006", "metro": True, "airport": 10.0, "railway": 5.0, "bus": 1.5},
            {"locality": "Viman Nagar", "area": "East Pune", "pincode": "411014", "metro": True, "airport": 5.0, "railway": 8.0, "bus": 2.0},
            {"locality": "Hadapsar", "area": "South Pune", "pincode": "411028", "metro": True, "airport": 15.0, "railway": 10.0, "bus": 1.0},
            {"locality": "Magarpatta", "area": "South Pune", "pincode": "411028", "metro": True, "airport": 12.0, "railway": 8.0, "bus": 1.5}
        ]
        
        # Mumbai locations with realistic areas
        mumbai_locations = [
            {"locality": "Bandra West", "area": "Western Suburbs", "pincode": "400050", "metro": True, "airport": 8.0, "railway": 2.0, "bus": 1.0},
            {"locality": "Andheri West", "area": "Western Suburbs", "pincode": "400058", "metro": True, "airport": 5.0, "railway": 1.5, "bus": 1.0},
            {"locality": "Powai", "area": "Central Suburbs", "pincode": "400076", "metro": False, "airport": 12.0, "railway": 8.0, "bus": 2.0},
            {"locality": "Thane West", "area": "Thane", "pincode": "400601", "metro": True, "airport": 25.0, "railway": 3.0, "bus": 2.0},
            {"locality": "Navi Mumbai", "area": "Navi Mumbai", "pincode": "400701", "metro": True, "airport": 35.0, "railway": 5.0, "bus": 3.0},
            {"locality": "Worli", "area": "South Mumbai", "pincode": "400018", "metro": True, "airport": 15.0, "railway": 4.0, "bus": 1.5},
            {"locality": "Lower Parel", "area": "Central Mumbai", "pincode": "400013", "metro": True, "airport": 18.0, "railway": 3.0, "bus": 1.0},
            {"locality": "Chembur", "area": "Central Suburbs", "pincode": "400071", "metro": False, "airport": 12.0, "railway": 6.0, "bus": 2.0}
        ]
        
        # Create locations
        created_locations = {}
        current_time = datetime.now()
        for city_data in [("Pune", pune_locations), ("Mumbai", mumbai_locations)]:
            city, locations = city_data
            for loc_data in locations:
                location = Location(
                    id=str(uuid.uuid4()),
                    city=city,
                    locality=loc_data["locality"],
                    area=loc_data["area"],
                    pincode=loc_data["pincode"],
                    state="Maharashtra",
                    metro_available=loc_data["metro"],
                    airport_distance_km=loc_data["airport"],
                    railway_station_distance_km=loc_data["railway"],
                    bus_stand_distance_km=loc_data["bus"]
                )
                # Explicitly set timestamps
                location.created_at = current_time
                location.updated_at = current_time
                
                db.add(location)
                db.flush()
                created_locations[f"{city}_{loc_data['locality']}"] = location
                print(f"  ✅ Added: {loc_data['locality']}, {city}")
        
        # 2. Create simple projects (without developer reference)
        print("\n🏢 Creating simple projects...")
        
        project_types = ["Luxury Apartment", "Premium Apartment", "Green Apartment", "Smart Home", "Luxury Villa", "Townhouse"]
        project_statuses = ["Ready to Move", "Under Construction", "Pre-launch"]
        
        created_projects = {}
        project_counter = 1
        
        for city, locations in [("Pune", pune_locations), ("Mumbai", mumbai_locations)]:
            for loc_data in locations:
                for i in range(2):  # 2 projects per location
                    project_name = f"Project {project_counter} - {loc_data['locality']}"
                    
                    # Create a simple project without developer reference
                    project = Project(
                        id=str(uuid.uuid4()),
                        name=project_name,
                        developer_id=None,  # Set to NULL
                        description=f"Premium project in {loc_data['locality']}, {city}",
                        project_type=random.choice(project_types),
                        total_units=random.randint(100, 500),
                        units_per_floor=random.randint(4, 8),
                        total_floors=random.randint(15, 35),
                        project_status=random.choice(project_statuses),
                        rera_number=f"{city[:2].upper()}{random.randint(100000, 999999)}",
                        possession_date=current_time.date(),
                        completion_date=current_time.date()
                    )
                    # Explicitly set timestamps
                    project.created_at = current_time
                    project.updated_at = current_time
                    
                    db.add(project)
                    db.flush()
                    
                    # Create project location
                    project_location = ProjectLocation(
                        id=str(uuid.uuid4()),
                        project_id=project.id,
                        location_id=created_locations[f"{city}_{loc_data['locality']}"].id
                    )
                    # Explicitly set timestamps
                    project_location.created_at = current_time
                    project_location.updated_at = current_time
                    
                    db.add(project_location)
                    
                    created_projects[project_name] = project
                    print(f"  ✅ Added: {project_name} in {loc_data['locality']}, {city}")
                    project_counter += 1
        
        # 3. Create properties with realistic prices
        print("\n🏠 Creating properties with realistic prices...")
        
        # Price ranges: 50 lakhs to 3 crores
        min_price = 5000000  # 50 lakhs
        max_price = 30000000  # 3 crores
        
        property_counter = 1
        for project in created_projects.values():
            # Create 10-20 properties per project
            num_properties = random.randint(10, 20)
            for i in range(num_properties):
                # Realistic price calculation
                bhk_count = random.choice([1, 2, 3, 4])
                
                # Price per sqft varies by BHK and location
                price_per_sqft = random.randint(8000, 25000)  # 8K to 25K per sqft
                carpet_area = random.randint(600, 2500)  # 600 to 2500 sqft
                
                # Adjust price based on BHK and area
                adjusted_price = int(price_per_sqft * carpet_area * (1 + (bhk_count - 1) * 0.1))
                
                property_unit = Property(
                    id=str(uuid.uuid4()),
                    project_id=project.id,
                    property_type=f"{bhk_count} BHK",
                    bhk_count=bhk_count,
                    carpet_area_sqft=carpet_area,
                    super_builtup_area_sqft=int(carpet_area * 1.25),
                    floor_number=random.randint(1, 35),
                    facing=random.choice(["North", "South", "East", "West", "North-East", "North-West", "South-East", "South-West"]),
                    status=random.choice(["Available", "Sold", "Reserved", "Under Construction"]),
                    sell_price=adjusted_price
                )
                # Explicitly set timestamps
                property_unit.created_at = current_time
                property_unit.updated_at = current_time
                
                db.add(property_unit)
                print(f"  ✅ Added: {bhk_count} BHK • {carpet_area} sqft • ₹{adjusted_price:,}")
                property_counter += 1
        
        # Commit all changes
        db.commit()
        print(f"\n🎉 Database population completed successfully!")
        print(f"📊 Created:")
        print(f"  • {len(created_locations)} locations")
        print(f"  • {len(created_projects)} projects")
        print(f"  • {property_counter - 1} properties")
        
        print(f"\n💡 Sample Queries You Can Test:")
        print(f"  • '2 BHK in Baner, Pune'")
        print(f"  • 'Properties under 1 crore in Mumbai'")
        print(f"  • '3 BHK apartments in Koregaon Park'")
        print(f"  • 'Luxury properties in Bandra West'")
        print(f"  • 'Properties between 1-2 crores in Hinjewadi'")
        print(f"  • '4 BHK villas in Wakad'")
        print(f"  • 'Ready to move properties in Pune'")
        print(f"  • 'Metro connected properties in Mumbai'")
        
        print(f"\n🔍 Complex Queries You Can Test:")
        print(f"  • 'Properties in Pune with metro access under 2 crores'")
        print(f"  • '3-4 BHK apartments in Mumbai between 1.5-3 crores'")
        print(f"  • 'Ready to move properties in Baner or Hinjewadi'")
        print(f"  • 'Properties near airport (within 10km) in Pune'")
        print(f"  • 'Luxury apartments in South Mumbai above 2 crores'")
        print(f"  • 'Green apartments in West Pune with 2-3 BHK'")
        print(f"  • 'Properties in Thane or Navi Mumbai under 1 crore'")
        print(f"  • 'Smart homes in Central Pune with metro connectivity'")
        
    except Exception as e:
        print(f"❌ Error during population: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    populate_minimal_data()
