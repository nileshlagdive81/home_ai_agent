#!/usr/bin/env python3
"""
Script to populate database with fresh, realistic data for Pune and Mumbai
"""

import uuid
import random
from datetime import datetime, timedelta
from backend.database import get_db
from backend.models import *

def populate_fresh_data():
    """Populate database with fresh, realistic data"""
    print("🌱 Populating Database with Fresh Data...")
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
                db.add(location)
                db.flush()
                created_locations[f"{city}_{loc_data['locality']}"] = location
                print(f"  ✅ Added: {loc_data['locality']}, {city}")
        
        # 2. Create amenities
        print("\n🎯 Creating amenities...")
        
        amenities_data = [
            # Basic amenities
            {"name": "24/7 Security", "category": "security"},
            {"name": "CCTV Surveillance", "category": "security"},
            {"name": "Intercom System", "category": "basic"},
            {"name": "Power Backup", "category": "basic"},
            {"name": "Water Supply", "category": "basic"},
            {"name": "Parking Space", "category": "basic"},
            {"name": "Lift", "category": "basic"},
            {"name": "Garden", "category": "recreation"},
            {"name": "Children's Play Area", "category": "recreation"},
            {"name": "Gym", "category": "recreation"},
            {"name": "Swimming Pool", "category": "recreation"},
            {"name": "Clubhouse", "category": "recreation"},
            {"name": "Party Hall", "category": "recreation"},
            {"name": "Indoor Games", "category": "recreation"},
            {"name": "Jogging Track", "category": "recreation"},
            {"name": "Cycling Track", "category": "recreation"},
            {"name": "Meditation Center", "category": "wellness"},
            {"name": "Yoga Studio", "category": "wellness"},
            {"name": "Spa", "category": "luxury"},
            {"name": "Concierge Service", "category": "luxury"},
            {"name": "Pet Park", "category": "recreation"},
            {"name": "Car Wash", "category": "basic"},
            {"name": "ATM", "category": "basic"},
            {"name": "Medical Center", "category": "basic"},
            {"name": "Day Care Center", "category": "basic"},
            {"name": "Library", "category": "recreation"},
            {"name": "Business Center", "category": "business"},
            {"name": "Conference Room", "category": "business"},
            {"name": "Guest Rooms", "category": "luxury"}
        ]
        
        created_amenities = {}
        for amenity_data in amenities_data:
            amenity = Amenity(
                id=str(uuid.uuid4()),
                name=amenity_data["name"],
                category=amenity_data["category"]
            )
            db.add(amenity)
            db.flush()
            created_amenities[amenity_data["name"]] = amenity
            print(f"  ✅ Added: {amenity_data['name']} ({amenity_data['category']})")
        
        # 3. Create nearby place categories
        print("\n🏢 Creating nearby place categories...")
        
        nearby_categories_data = [
            "Schools & Colleges", "Hospitals & Clinics", "Shopping Malls", "Metro Stations",
            "Railway Stations", "Bus Stands", "Airports", "Banks & ATMs", "Restaurants & Pubs",
            "Parks & Gardens", "Sports Facilities", "Religious Places", "Entertainment Centers"
        ]
        
        created_categories = {}
        for category_name in nearby_categories_data:
            category = NearbyCategory(
                id=str(uuid.uuid4()),
                name=category_name
            )
            db.add(category)
            db.flush()
            created_categories[category_name] = category
            print(f"  ✅ Added: {category_name}")
        
        # 4. Create nearby places
        print("\n🚇 Creating nearby places...")
        
        nearby_places_data = [
            # Schools & Colleges
            {"name": "Delhi Public School", "category": "Schools & Colleges", "distance_km": 1.2},
            {"name": "Symbiosis International University", "category": "Schools & Colleges", "distance_km": 2.5},
            {"name": "MIT World Peace University", "category": "Schools & Colleges", "distance_km": 3.0},
            {"name": "St. Mary's School", "category": "Schools & Colleges", "distance_km": 1.8},
            {"name": "Fergusson College", "category": "Schools & Colleges", "distance_km": 2.2},
            
            # Hospitals & Clinics
            {"name": "Sahyadri Hospital", "category": "Hospitals & Clinics", "distance_km": 1.5},
            {"name": "Ruby Hall Clinic", "category": "Hospitals & Clinics", "distance_km": 2.8},
            {"name": "Jehangir Hospital", "category": "Hospitals & Clinics", "distance_km": 3.2},
            {"name": "Apollo Hospital", "category": "Hospitals & Clinics", "distance_km": 4.0},
            {"name": "KEM Hospital", "category": "Hospitals & Clinics", "distance_km": 2.1},
            
            # Shopping Malls
            {"name": "Phoenix MarketCity", "category": "Shopping Malls", "distance_km": 2.0},
            {"name": "Seasons Mall", "category": "Shopping Malls", "distance_km": 1.8},
            {"name": "Amanora Mall", "category": "Shopping Malls", "distance_km": 3.5},
            {"name": "Westend Mall", "category": "Shopping Malls", "distance_km": 2.8},
            {"name": "Elpro Mall", "category": "Shopping Malls", "distance_km": 1.2},
            
            # Metro Stations
            {"name": "Vanaz Metro Station", "category": "Metro Stations", "distance_km": 0.8},
            {"name": "Deccan Metro Station", "category": "Metro Stations", "distance_km": 1.5},
            {"name": "Garware Metro Station", "category": "Metro Stations", "distance_km": 2.2},
            {"name": "Civil Court Metro Station", "category": "Metro Stations", "distance_km": 3.0},
            {"name": "Swargate Metro Station", "category": "Metro Stations", "distance_km": 4.2},
            
            # Railway Stations
            {"name": "Pune Junction", "category": "Railway Stations", "distance_km": 2.5},
            {"name": "Shivajinagar Station", "category": "Railway Stations", "distance_km": 1.8},
            {"name": "Khadki Station", "category": "Railway Stations", "distance_km": 3.5},
            {"name": "Dapodi Station", "category": "Railway Stations", "distance_km": 4.8},
            {"name": "Pimpri Station", "category": "Railway Stations", "distance_km": 6.2},
            
            # Restaurants & Pubs
            {"name": "The Urban Foundry", "category": "Restaurants & Pubs", "distance_km": 1.0},
            {"name": "Effingut Brewerkz", "category": "Restaurants & Pubs", "distance_km": 1.5},
            {"name": "The Beer Cafe", "category": "Restaurants & Pubs", "distance_km": 2.0},
            {"name": "Independence Brewing Co", "category": "Restaurants & Pubs", "distance_km": 2.8},
            {"name": "Doolally Taproom", "category": "Restaurants & Pubs", "distance_km": 3.2}
        ]
        
        created_nearby_places = {}
        for place_data in nearby_places_data:
            place = NearbyPlace(
                id=str(uuid.uuid4()),
                name=place_data["name"],
                category_id=created_categories[place_data["category"]].id,
                distance_km=place_data["distance_km"]
            )
            db.add(place)
            db.flush()
            created_nearby_places[place_data["name"]] = place
            print(f"  ✅ Added: {place_data['name']} ({place_data['distance_km']} km)")
        
        # 5. Create developers
        print("\n🏗️ Creating developers...")
        
        developers_data = [
            "Lodha Group", "Godrej Properties", "Mahindra Lifespaces", "Kolte Patil Developers",
            "Purvankara Limited", "Sobha Limited", "Prestige Group", "Brigade Group",
            "Pune Realty", "Mumbai Developers", "Urban Infrastructure", "Green Homes Ltd"
        ]
        
        created_developers = {}
        for dev_name in developers_data:
            developer = Developer(
                id=str(uuid.uuid4()),
                name=dev_name,
                description=f"Leading real estate developer in Maharashtra",
                established_year=random.randint(1990, 2010),
                rera_number=f"MH{random.randint(100000, 999999)}"
            )
            db.add(developer)
            db.flush()
            created_developers[dev_name] = developer
            print(f"  ✅ Added: {dev_name}")
        
        # 6. Create projects
        print("\n🏢 Creating projects...")
        
        project_types = ["Luxury Apartment", "Premium Apartment", "Green Apartment", "Smart Home", "Luxury Villa", "Townhouse"]
        project_statuses = ["Ready to Move", "Under Construction", "Pre-launch"]
        
        created_projects = {}
        project_counter = 1
        
        for city, locations in [("Pune", pune_locations), ("Mumbai", mumbai_locations)]:
            for loc_data in locations:
                for i in range(2):  # 2 projects per location
                    project_name = f"{random.choice(list(created_developers.keys()))} {random.choice(project_types)} {project_counter}"
                    
                    project = Project(
                        id=str(uuid.uuid4()),
                        name=project_name,
                        developer_id=random.choice(list(created_developers.values())).id,
                        description=f"Premium {random.choice(project_types).lower()} project in {loc_data['locality']}, {city}",
                        project_type=random.choice(project_types),
                        total_units=random.randint(100, 500),
                        units_per_floor=random.randint(4, 8),
                        total_floors=random.randint(15, 35),
                        project_status=random.choice(project_statuses),
                        rera_number=f"{city[:2].upper()}{random.randint(100000, 999999)}",
                        possession_date=datetime.now() + timedelta(days=random.randint(100, 800)),
                        completion_date=datetime.now() + timedelta(days=random.randint(50, 400))
                    )
                    db.add(project)
                    db.flush()
                    
                    # Create project location
                    project_location = ProjectLocation(
                        id=str(uuid.uuid4()),
                        project_id=project.id,
                        location_id=created_locations[f"{city}_{loc_data['locality']}"].id
                    )
                    db.add(project_location)
                    
                    # Add random amenities to project
                    project_amenities = random.sample(list(created_amenities.values()), random.randint(8, 15))
                    for amenity in project_amenities:
                        project_amenity = ProjectAmenity(
                            id=str(uuid.uuid4()),
                            project_id=project.id,
                            amenity_id=amenity.id
                        )
                        db.add(project_amenity)
                    
                    # Add random nearby places
                    project_nearby = random.sample(list(created_nearby_places.values()), random.randint(5, 10))
                    for nearby in project_nearby:
                        project_nearby_rel = ProjectNearby(
                            id=str(uuid.uuid4()),
                            project_id=project.id,
                            nearby_place_id=nearby.id
                        )
                        db.add(project_nearby_rel)
                    
                    created_projects[project_name] = project
                    print(f"  ✅ Added: {project_name} in {loc_data['locality']}, {city}")
                    project_counter += 1
        
        # 7. Create properties with realistic prices
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
                base_price = random.randint(min_price, max_price)
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
                db.add(property_unit)
                print(f"  ✅ Added: {bhk_count} BHK • {carpet_area} sqft • ₹{adjusted_price:,}")
                property_counter += 1
        
        # Commit all changes
        db.commit()
        print(f"\n🎉 Database population completed successfully!")
        print(f"📊 Created:")
        print(f"  • {len(created_locations)} locations")
        print(f"  • {len(created_amenities)} amenities")
        print(f"  • {len(created_categories)} nearby categories")
        print(f"  • {len(created_nearby_places)} nearby places")
        print(f"  • {len(created_developers)} developers")
        print(f"  • {len(created_projects)} projects")
        print(f"  • {property_counter - 1} properties")
        
    except Exception as e:
        print(f"❌ Error during population: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    populate_fresh_data()
