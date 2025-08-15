#!/usr/bin/env python3
"""
Script to update Delhi data with more variety
"""

import sys
import os
import uuid
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from database import get_db
from models import Location, Project, Property, Amenity, ProjectAmenity, ProjectLocation

def update_delhi_data():
    """Update Delhi data with more variety"""
    
    db = next(get_db())
    
    print("🔄 Updating Delhi Data with More Variety:")
    print("=" * 60)
    
    try:
        # 1. Add more Delhi localities
        print("\n📍 Adding more Delhi localities...")
        
        new_localities = [
            {"city": "Delhi", "locality": "Connaught Place", "area": "Central Delhi", "pincode": "110001", "state": "Delhi"},
            {"city": "Delhi", "locality": "Khan Market", "area": "South Delhi", "pincode": "110003", "state": "Delhi"},
            {"city": "Delhi", "locality": "Hauz Khas", "area": "South Delhi", "pincode": "110016", "state": "Delhi"},
            {"city": "Delhi", "locality": "Dwarka", "area": "South West Delhi", "pincode": "110075", "state": "Delhi"},
            {"city": "Delhi", "locality": "Rohini", "area": "North West Delhi", "pincode": "110085", "state": "Delhi"},
            {"city": "Delhi", "locality": "Pitampura", "area": "North West Delhi", "pincode": "110034", "state": "Delhi"},
            {"city": "Delhi", "locality": "Janakpuri", "area": "West Delhi", "pincode": "110058", "state": "Delhi"},
            {"city": "Delhi", "locality": "Rajouri Garden", "area": "West Delhi", "pincode": "110027", "state": "Delhi"},
            {"city": "Delhi", "locality": "Lajpat Nagar", "area": "South Delhi", "pincode": "110024", "state": "Delhi"},
            {"city": "Delhi", "locality": "Greater Kailash", "area": "South Delhi", "pincode": "110048", "state": "Delhi"}
        ]
        
        for loc_data in new_localities:
            # Check if location already exists
            existing = db.query(Location).filter(
                Location.city == loc_data["city"],
                Location.locality == loc_data["locality"]
            ).first()
            
            if not existing:
                new_location = Location(
                    id=str(uuid.uuid4()),
                    city=loc_data["city"],
                    locality=loc_data["locality"],
                    area=loc_data["area"],
                    pincode=loc_data["pincode"],
                    state=loc_data["state"],
                    metro_available=True,
                    airport_distance_km=15.0,
                    railway_station_distance_km=5.0,
                    bus_stand_distance_km=2.0
                )
                db.add(new_location)
                print(f"  ✅ Added: {loc_data['locality']}, {loc_data['area']}")
            else:
                print(f"  ⚠️ Already exists: {loc_data['locality']}")
        
        # 2. Add more amenities
        print("\n🎯 Adding more amenities...")
        
        new_amenities = [
            {"name": "Swimming Pool", "category": "recreation"},
            {"name": "Tennis Court", "category": "recreation"},
            {"name": "Squash Court", "category": "recreation"},
            {"name": "Badminton Court", "category": "recreation"},
            {"name": "Indoor Games Room", "category": "recreation"},
            {"name": "Party Hall", "category": "recreation"},
            {"name": "Conference Room", "category": "business"},
            {"name": "Business Center", "category": "business"},
            {"name": "ATM", "category": "basic"},
            {"name": "Bank", "category": "basic"},
            {"name": "Post Office", "category": "basic"},
            {"name": "Medical Center", "category": "basic"},
            {"name": "Pharmacy", "category": "basic"},
            {"name": "Day Care Center", "category": "basic"},
            {"name": "Pet Park", "category": "recreation"},
            {"name": "Cycling Track", "category": "recreation"},
            {"name": "Jogging Track", "category": "recreation"},
            {"name": "Meditation Center", "category": "recreation"},
            {"name": "Yoga Studio", "category": "recreation"},
            {"name": "Spa", "category": "luxury"}
        ]
        
        for amenity_data in new_amenities:
            existing = db.query(Amenity).filter(Amenity.name == amenity_data["name"]).first()
            if not existing:
                new_amenity = Amenity(
                    id=str(uuid.uuid4()),
                    name=amenity_data["name"],
                    category=amenity_data["category"]
                )
                db.add(new_amenity)
                print(f"  ✅ Added: {amenity_data['name']} ({amenity_data['category']})")
            else:
                print(f"  ⚠️ Already exists: {amenity_data['name']}")
        
        # 3. Create new Delhi projects with different localities
        print("\n🏢 Creating new Delhi projects...")
        
        new_projects = [
            {
                "name": "Lodha Luxury Residences",
                "locality": "Connaught Place",
                "project_type": "Luxury Apartment",
                "total_units": 150,
                "total_floors": 25,
                "project_status": "Under Construction"
            },
            {
                "name": "Godrej Green Homes",
                "locality": "Dwarka",
                "project_type": "Green Apartment",
                "total_units": 200,
                "total_floors": 20,
                "project_status": "Ready to Move"
            },
            {
                "name": "Sobha Dream Gardens",
                "locality": "Hauz Khas",
                "project_type": "Premium Villa",
                "total_units": 50,
                "total_floors": 3,
                "project_status": "Under Construction"
            },
            {
                "name": "Prestige Lake Ridge",
                "locality": "Rohini",
                "project_type": "Apartment",
                "total_units": 300,
                "total_floors": 18,
                "project_status": "Ready to Move"
            },
            {
                "name": "Brigade Lakefront",
                "locality": "Janakpuri",
                "project_type": "Luxury Apartment",
                "total_units": 180,
                "total_floors": 22,
                "project_status": "Under Construction"
            }
        ]
        
        for proj_data in new_projects:
            # Get the location for this project
            location = db.query(Location).filter(
                Location.city == "Delhi",
                Location.locality == proj_data["locality"]
            ).first()
            
            if location:
                # Create project
                new_project = Project(
                    id=str(uuid.uuid4()),
                    name=proj_data["name"],
                    project_type=proj_data["project_type"],
                    total_units=proj_data["total_units"],
                    total_floors=proj_data["total_floors"],
                    project_status=proj_data["project_status"],
                    rera_number=f"DL{uuid.uuid4().hex[:8].upper()}",
                    description=f"Premium {proj_data['project_type']} project in {proj_data['locality']}, Delhi"
                )
                db.add(new_project)
                db.flush()  # Get the ID
                
                # Create project location
                project_location = ProjectLocation(
                    id=str(uuid.uuid4()),
                    project_id=new_project.id,
                    location_id=location.id
                )
                db.add(project_location)
                
                print(f"  ✅ Added: {proj_data['name']} in {proj_data['locality']}")
                
                # Add random amenities to this project
                import random
                all_amenities = db.query(Amenity).all()
                project_amenities = random.sample(all_amenities, min(8, len(all_amenities)))
                
                for amenity in project_amenities:
                    project_amenity = ProjectAmenity(
                        id=str(uuid.uuid4()),
                        project_id=new_project.id,
                        amenity_id=amenity.id
                    )
                    db.add(project_amenity)
                
                print(f"    - Added {len(project_amenities)} amenities")
                
                # Create some sample properties
                for i in range(5):  # Create 5 sample properties
                    property_unit = Property(
                        id=str(uuid.uuid4()),
                        project_id=new_project.id,
                        property_type="Apartment",
                        bhk_count=random.choice([1.0, 2.0, 3.0, 4.0]),
                        carpet_area_sqft=random.randint(800, 2500),
                        sell_price=random.randint(5000000, 25000000),  # 50L to 2.5Cr
                        status="Available"
                    )
                    db.add(property_unit)
                
                print(f"    - Added 5 sample properties")
            else:
                print(f"  ❌ Location not found: {proj_data['locality']}")
        
        # Commit all changes
        db.commit()
        print(f"\n✅ Successfully updated Delhi data!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    update_delhi_data()
