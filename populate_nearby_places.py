#!/usr/bin/env python3
"""
Populate Nearby Places Data
Adds realistic nearby places (hospitals, schools, malls, etc.) to all projects
"""

import sys
import os
import uuid
from decimal import Decimal

# Add backend to path
sys.path.append("backend")

try:
    from database import SessionLocal
    from models import Project, NearbyPlace, NearbyCategory
    print("✅ Database connection established")
except ImportError as e:
    print(f"❌ Error importing database: {e}")
    sys.exit(1)

def create_nearby_categories(db):
    """Create nearby place categories if they don't exist"""
    categories = [
        {"name": "Hospital", "description": "Medical facilities and hospitals", "icon": "🏥"},
        {"name": "School", "description": "Educational institutions", "icon": "🏫"},
        {"name": "College", "description": "Higher education institutions", "icon": "🎓"},
        {"name": "Mall", "description": "Shopping malls and retail centers", "icon": "🛍️"},
        {"name": "Market", "description": "Local markets and grocery stores", "icon": "🛒"},
        {"name": "Metro Station", "description": "Public transportation", "icon": "🚇"},
        {"name": "Bus Stop", "description": "Public bus transportation", "icon": "🚌"},
        {"name": "Railway Station", "description": "Train stations", "icon": "🚉"},
        {"name": "Airport", "description": "Airports and aviation facilities", "icon": "✈️"},
        {"name": "Park", "description": "Public parks and recreational areas", "icon": "🌳"},
        {"name": "Gym", "description": "Fitness centers and gyms", "icon": "💪"},
        {"name": "Restaurant", "description": "Restaurants and food outlets", "icon": "🍽️"},
        {"name": "Bank", "description": "Banks and financial institutions", "icon": "🏦"},
        {"name": "Post Office", "description": "Postal services", "icon": "📮"},
        {"name": "Police Station", "description": "Law enforcement", "icon": "👮"},
        {"name": "Fire Station", "description": "Emergency services", "icon": "🚒"},
        {"name": "Temple", "description": "Religious places", "icon": "🕍"},
        {"name": "Cinema", "description": "Movie theaters", "icon": "🎬"},
        {"name": "Library", "description": "Public libraries", "icon": "📚"},
        {"name": "Sports Complex", "description": "Sports facilities", "icon": "⚽"}
    ]
    
    print("🏷️  Creating nearby place categories...")
    for cat_data in categories:
        existing = db.query(NearbyCategory).filter(NearbyCategory.name == cat_data["name"]).first()
        if not existing:
            category = NearbyCategory(
                id=str(uuid.uuid4()),
                name=cat_data["name"],
                description=cat_data["description"],
                icon=cat_data["icon"]
            )
            db.add(category)
            print(f"  ✅ Created category: {cat_data['name']} {cat_data['icon']}")
    
    db.commit()
    print(f"✅ Created {len(categories)} nearby place categories")

def generate_nearby_places_for_project(project, project_index):
    """Generate realistic nearby places for a project based on its location"""
    nearby_places = []
    
    # Base nearby places that most projects would have
    base_places = [
        {"type": "Hospital", "names": ["City Hospital", "General Hospital", "Medical Center"], "base_distance": 2.5},
        {"type": "School", "names": ["Public School", "Primary School", "Elementary School"], "base_distance": 1.2},
        {"type": "Market", "names": ["Local Market", "Grocery Store", "Supermarket"], "base_distance": 0.8},
        {"type": "Bus Stop", "names": ["Bus Stop", "Transport Hub"], "base_distance": 0.5},
        {"type": "Bank", "names": ["State Bank", "National Bank", "Local Bank"], "base_distance": 1.5},
        {"type": "Restaurant", "names": ["Local Restaurant", "Food Court", "Cafe"], "base_distance": 0.7},
        {"type": "Park", "names": ["City Park", "Children's Park", "Recreation Area"], "base_distance": 1.0}
    ]
    
    # Additional places based on project type and location
    if "luxury" in project.name.lower() or "premium" in project.name.lower():
        additional_places = [
            {"type": "Mall", "names": ["Premium Mall", "Luxury Shopping Center"], "base_distance": 3.0},
            {"type": "Gym", "names": ["Fitness Center", "Health Club"], "base_distance": 1.8},
            {"type": "Cinema", "names": ["Multiplex", "Movie Theater"], "base_distance": 2.2}
        ]
        base_places.extend(additional_places)
    
    if "residential" in project.project_type.lower():
        additional_places = [
            {"type": "College", "names": ["Engineering College", "Arts College"], "base_distance": 4.0},
            {"type": "Sports Complex", "names": ["Sports Center", "Fitness Complex"], "base_distance": 2.5}
        ]
        base_places.extend(additional_places)
    
    # Generate nearby places with realistic variations
    for place_data in base_places:
        # Add some variation based on project index to make it realistic
        variation = (project_index % 5) * 0.3
        distance = place_data["base_distance"] + variation
        
        # Ensure distance is within reasonable bounds
        distance = max(0.3, min(8.0, distance))
        
        # Select a random name from the available options
        import random
        place_name = random.choice(place_data["names"])
        
        # Add project-specific identifier
        place_name = f"{place_name} - {project.name.split()[0]}"
        
        nearby_place = NearbyPlace(
            id=str(uuid.uuid4()),
            project_id=project.id,
            place_type=place_data["type"],
            place_name=place_name,
            distance_km=Decimal(str(round(distance, 2))),
            walking_distance=(distance <= 1.5)  # Walking distance if within 1.5km
        )
        nearby_places.append(nearby_place)
    
    return nearby_places

def populate_nearby_places():
    """Main function to populate nearby places for all projects"""
    db = SessionLocal()
    
    try:
        # Create categories first
        create_nearby_categories(db)
        
        # Get all projects
        projects = db.query(Project).all()
        print(f"\n🏗️  Found {len(projects)} projects to populate with nearby places")
        
        if not projects:
            print("❌ No projects found in database")
            return
        
        total_places_created = 0
        
        for i, project in enumerate(projects):
            print(f"\n📍 Processing project {i+1}/{len(projects)}: {project.name}")
            
            # Check if project already has nearby places
            existing_places = db.query(NearbyPlace).filter(NearbyPlace.project_id == project.id).count()
            if existing_places > 0:
                print(f"  ℹ️  Project already has {existing_places} nearby places, skipping")
                continue
            
            # Generate nearby places for this project
            nearby_places = generate_nearby_places_for_project(project, i)
            
            # Add to database
            for place in nearby_places:
                db.add(place)
            
            db.commit()
            print(f"  ✅ Added {len(nearby_places)} nearby places")
            total_places_created += len(nearby_places)
        
        print(f"\n🎉 Successfully populated nearby places!")
        print(f"📊 Summary:")
        print(f"  - Projects processed: {len(projects)}")
        print(f"  - Total nearby places created: {total_places_created}")
        print(f"  - Average places per project: {total_places_created/len(projects):.1f}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()
    
    return True

if __name__ == "__main__":
    success = populate_nearby_places()
    sys.exit(0 if success else 1)
