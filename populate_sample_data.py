#!/usr/bin/env python3
"""
Script to populate the database with sample real estate data
"""

import sys
import os
from datetime import date, time
from decimal import Decimal

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from database import SessionLocal, engine
from models import *

def populate_sample_data():
    """Populate database with sample data"""
    db = SessionLocal()
    
    try:
        print("🚀 Starting to populate database with sample data...")
        
        # Create Cities
        print("📍 Creating cities...")
        cities = [
            City(name="Mumbai", state="Maharashtra"),
            City(name="Delhi", state="Delhi"),
            City(name="Bangalore", state="Karnataka"),
            City(name="Pune", state="Maharashtra"),
            City(name="Hyderabad", state="Telangana")
        ]
        
        for city in cities:
            db.add(city)
        db.commit()
        
        # Create Localities
        print("🏘️ Creating localities...")
        localities = [
            Locality(name="Bandra West", city_id=1, pincode="400050"),
            Locality(name="Andheri West", city_id=1, pincode="400058"),
            Locality(name="Powai", city_id=1, pincode="400076"),
            Locality(name="Whitefield", city_id=3, pincode="560066"),
            Locality(name="Electronic City", city_id=3, pincode="560100"),
            Locality(name="Baner", city_id=4, pincode="411045"),
            Locality(name="Hinjewadi", city_id=4, pincode="411057"),
            Locality(name="Jubilee Hills", city_id=5, pincode="500033"),
            Locality(name="Gachibowli", city_id=5, pincode="500032")
        ]
        
        for locality in localities:
            db.add(locality)
        db.commit()
        
        # Create Property Types
        print("🏠 Creating property types...")
        property_types = [
            PropertyType(name="Apartment", description="Multi-story residential building"),
            PropertyType(name="Villa", description="Independent house with garden"),
            PropertyType(name="Penthouse", description="Luxury apartment on top floor"),
            PropertyType(name="Studio", description="Compact single-room apartment")
        ]
        
        for prop_type in property_types:
            db.add(prop_type)
        db.commit()
        
        # Create Amenities
        print("🏊 Creating amenities...")
        amenities = [
            Amenity(name="Swimming Pool", category="luxury", icon="🏊"),
            Amenity(name="Gym", category="luxury", icon="💪"),
            Amenity(name="Garden", category="luxury", icon="🌳"),
            Amenity(name="Parking", category="basic", icon="🚗"),
            Amenity(name="Lift", category="basic", icon="🛗"),
            Amenity(name="Security", category="security", icon="🔒"),
            Amenity(name="CCTV", category="security", icon="📹"),
            Amenity(name="Clubhouse", category="recreation", icon="🏠"),
            Amenity(name="Playground", category="recreation", icon="🎯"),
            Amenity(name="Power Backup", category="basic", icon="⚡")
        ]
        
        for amenity in amenities:
            db.add(amenity)
        db.commit()
        
        # Create Nearby Categories
        print("📍 Creating nearby place categories...")
        nearby_categories = [
            NearbyCategory(name="Transportation", description="Metro, Railway, Bus", icon="🚇"),
            NearbyCategory(name="Healthcare", description="Hospitals, Clinics", icon="🏥"),
            NearbyCategory(name="Education", description="Schools, Colleges", icon="🎓"),
            NearbyCategory(name="Shopping", description="Malls, Markets", icon="🛍️"),
            NearbyCategory(name="Entertainment", description="Cinemas, Parks", icon="🎬")
        ]
        
        for category in nearby_categories:
            db.add(category)
        db.commit()
        
        # Create Nearby Places
        print("🏢 Creating nearby places...")
        nearby_places = [
            NearbyPlace(name="Bandra Metro Station", category_id=1, locality_id=1, distance_km=0.5),
            NearbyPlace(name="Andheri Railway Station", category_id=1, locality_id=2, distance_km=0.8),
            NearbyPlace(name="Hiranandani Hospital", category_id=2, locality_id=3, distance_km=1.2),
            NearbyPlace(name="Whitefield Metro", category_id=1, locality_id=4, distance_km=0.3),
            NearbyPlace(name="International School", category_id=3, locality_id=4, distance_km=0.7),
            NearbyPlace(name="Phoenix MarketCity", category_id=4, locality_id=5, distance_km=1.0),
            NearbyPlace(name="Central Park", category_id=5, locality_id=6, distance_km=0.6)
        ]
        
        for place in nearby_places:
            db.add(place)
        db.commit()
        
        # Create Projects
        print("🏗️ Creating projects...")
        projects = [
            Project(
                name="Luxury Heights",
                developer_name="Premium Developers Ltd",
                locality_id=1,
                property_type_id=1,
                total_units=120,
                units_per_floor=4,
                total_floors=30,
                project_status="ready_to_move",
                possession_date=date(2024, 6, 1),
                rera_number="MahaRERA/A51234/2020",
                description="Premium luxury apartments in the heart of Bandra West",
                highlights=["Sea View", "Premium Amenities", "Prime Location"]
            ),
            Project(
                name="Green Valley",
                developer_name="Eco Homes Pvt Ltd",
                locality_id=3,
                property_type_id=2,
                total_units=50,
                units_per_floor=2,
                total_floors=25,
                project_status="under_construction",
                possession_date=date(2025, 12, 1),
                rera_number="MahaRERA/A51235/2021",
                description="Eco-friendly villas with modern amenities",
                highlights=["Eco-Friendly", "Large Gardens", "Modern Design"]
            ),
            Project(
                name="Tech Park Residences",
                developer_name="Smart City Developers",
                locality_id=4,
                property_type_id=1,
                total_units=200,
                units_per_floor=6,
                total_floors=35,
                project_status="ready_to_move",
                possession_date=date(2024, 3, 1),
                rera_number="KarRERA/A51236/2019",
                description="Modern apartments near IT hub",
                highlights=["Near IT Park", "Smart Home Features", "Community Living"]
            ),
            Project(
                name="Heritage Gardens",
                developer_name="Classic Builders",
                locality_id=6,
                property_type_id=1,
                total_units=80,
                units_per_floor=3,
                total_floors=28,
                project_status="planning",
                possession_date=date(2026, 6, 1),
                rera_number="MahaRERA/A51237/2022",
                description="Heritage-inspired apartments with modern comforts",
                highlights=["Heritage Design", "Large Balconies", "Premium Location"]
            )
        ]
        
        for project in projects:
            db.add(project)
        db.commit()
        
        # Create Property Units
        print("🏠 Creating property units...")
        property_units = [
            PropertyUnit(
                project_id=1,
                unit_number="A-101",
                floor_number=1,
                bhk=2,
                carpet_area_sqft=Decimal("1200.00"),
                built_up_area_sqft=Decimal("1400.00"),
                super_built_up_area_sqft=Decimal("1600.00"),
                price_per_sqft=Decimal("25000.00"),
                total_price=Decimal("40000000.00"),
                booking_amount=Decimal("2000000.00")
            ),
            PropertyUnit(
                project_id=1,
                unit_number="A-102",
                floor_number=1,
                bhk=3,
                carpet_area_sqft=Decimal("1800.00"),
                built_up_area_sqft=Decimal("2100.00"),
                super_built_up_area_sqft=Decimal("2400.00"),
                price_per_sqft=Decimal("25000.00"),
                total_price=Decimal("60000000.00"),
                booking_amount=Decimal("3000000.00")
            ),
            PropertyUnit(
                project_id=2,
                unit_number="V-001",
                floor_number=1,
                bhk=4,
                carpet_area_sqft=Decimal("3000.00"),
                built_up_area_sqft=Decimal("3500.00"),
                super_built_up_area_sqft=Decimal("4000.00"),
                price_per_sqft=Decimal("18000.00"),
                total_price=Decimal("72000000.00"),
                booking_amount=Decimal("3600000.00")
            ),
            PropertyUnit(
                project_id=3,
                unit_number="T-201",
                floor_number=2,
                bhk=2,
                carpet_area_sqft=Decimal("1100.00"),
                built_up_area_sqft=Decimal("1300.00"),
                super_built_up_area_sqft=Decimal("1500.00"),
                price_per_sqft=Decimal("12000.00"),
                total_price=Decimal("18000000.00"),
                booking_amount=Decimal("900000.00")
            )
        ]
        
        for unit in property_units:
            db.add(unit)
        db.commit()
        
        # Create Project Amenities
        print("🏊 Creating project amenities...")
        project_amenities = [
            ProjectAmenity(project_id=1, amenity_id=1),  # Swimming Pool
            ProjectAmenity(project_id=1, amenity_id=2),  # Gym
            ProjectAmenity(project_id=1, amenity_id=3),  # Garden
            ProjectAmenity(project_id=1, amenity_id=4),  # Parking
            ProjectAmenity(project_id=1, amenity_id=5),  # Lift
            ProjectAmenity(project_id=1, amenity_id=6),  # Security
            ProjectAmenity(project_id=2, amenity_id=3),  # Garden
            ProjectAmenity(project_id=2, amenity_id=4),  # Parking
            ProjectAmenity(project_id=2, amenity_id=6),  # Security
            ProjectAmenity(project_id=2, amenity_id=7),  # CCTV
            ProjectAmenity(project_id=3, amenity_id=1),  # Swimming Pool
            ProjectAmenity(project_id=3, amenity_id=2),  # Gym
            ProjectAmenity(project_id=3, amenity_id=4),  # Parking
            ProjectAmenity(project_id=3, amenity_id=5),  # Lift
            ProjectAmenity(project_id=3, amenity_id=6),  # Security
        ]
        
        for project_amenity in project_amenities:
            db.add(project_amenity)
        db.commit()
        
        # Create Project Nearby Places
        print("📍 Creating project nearby places...")
        project_nearby = [
            ProjectNearby(project_id=1, nearby_place_id=1, distance_km=Decimal("0.5")),
            ProjectNearby(project_id=2, nearby_place_id=3, distance_km=Decimal("1.2")),
            ProjectNearby(project_id=3, nearby_place_id=4, distance_km=Decimal("0.3")),
            ProjectNearby(project_id=3, nearby_place_id=5, distance_km=Decimal("0.7")),
            ProjectNearby(project_id=4, nearby_place_id=7, distance_km=Decimal("0.6"))
        ]
        
        for project_nearby_place in project_nearby:
            db.add(project_nearby_place)
        db.commit()
        
        # Create Users
        print("👥 Creating users...")
        users = [
            User(
                username="admin",
                email="admin@realestate.com",
                phone="9876543210",
                full_name="System Administrator",
                role="admin"
            ),
            User(
                username="agent1",
                email="agent1@realestate.com",
                phone="9876543211",
                full_name="John Smith",
                role="agent"
            ),
            User(
                username="customer1",
                email="customer1@email.com",
                phone="9876543212",
                full_name="Alice Johnson",
                role="customer"
            )
        ]
        
        for user in users:
            db.add(user)
        db.commit()
        
        print("✅ Sample data populated successfully!")
        print(f"📊 Created: {len(cities)} cities, {len(localities)} localities, {len(projects)} projects")
        print(f"🏠 Created: {len(property_units)} property units, {len(amenities)} amenities")
        print(f"👥 Created: {len(users)} users")
        
    except Exception as e:
        print(f"❌ Error populating sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    populate_sample_data()
