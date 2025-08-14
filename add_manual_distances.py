#!/usr/bin/env python3
"""
Simple script to manually add distance data
No internet required - just type in the distances you know
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database import get_db
from sqlalchemy import text

def show_existing_data():
    """Show existing landmarks and distances"""
    
    db = next(get_db())
    
    try:
        print("📊 EXISTING DISTANCE DATA:")
        print("=" * 50)
        
        # Show landmarks
        landmarks = db.execute(text("""
            SELECT np.name, nc.name as category, l.city, l.name as locality, np.distance_km
            FROM nearby_places np
            JOIN nearby_categories nc ON np.category_id = nc.id
            JOIN localities l ON np.locality_id = l.id
            ORDER BY l.city, l.name, np.distance_km
        """)).fetchall()
        
        if landmarks:
            current_city = ""
            for landmark in landmarks:
                name, category, city, locality, distance = landmark
                if city != current_city:
                    print(f"\n🌆 {city}:")
                    current_city = city
                print(f"  • {name} ({category}): {distance} km - {locality}")
        else:
            print("  No landmarks found. Let's add some!")
        
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

def add_landmark_manually():
    """Manually add a new landmark with distance"""
    
    db = next(get_db())
    
    try:
        print("🏛️  ADD NEW LANDMARK:")
        print("-" * 30)
        
        # Get available categories
        categories = db.execute(text("SELECT id, name FROM nearby_categories ORDER BY name")).fetchall()
        print("Available categories:")
        for i, (cat_id, cat_name) in enumerate(categories, 1):
            print(f"  {i}. {cat_name}")
        
        # Get available localities
        localities = db.execute(text("SELECT id, name, city FROM localities ORDER BY city, name")).fetchall()
        print("\nAvailable localities:")
        for i, (loc_id, loc_name, city) in enumerate(localities, 1):
            print(f"  {i}. {city} - {loc_name}")
        
        print("\nEnter landmark details:")
        
        # Get landmark name
        landmark_name = input("Landmark name (e.g., NMV School): ").strip()
        if not landmark_name:
            print("❌ Landmark name is required")
            return
        
        # Get category
        try:
            cat_choice = int(input(f"Choose category (1-{len(categories)}): ")) - 1
            if 0 <= cat_choice < len(categories):
                category_id = categories[cat_choice][0]
                category_name = categories[cat_choice][1]
            else:
                print("❌ Invalid category choice")
                return
        except ValueError:
            print("❌ Please enter a valid number")
            return
        
        # Get locality
        try:
            loc_choice = int(input(f"Choose locality (1-{len(localities)}): ")) - 1
            if 0 <= loc_choice < len(localities):
                locality_id = localities[loc_choice][0]
                locality_name = localities[loc_choice][1]
                city_name = localities[loc_choice][2]
            else:
                print("❌ Invalid locality choice")
                return
        except ValueError:
            print("❌ Please enter a valid number")
            return
        
        # Get distance
        try:
            distance = float(input("Distance in kilometers (e.g., 3.5): "))
            if distance <= 0:
                print("❌ Distance must be positive")
                return
        except ValueError:
            print("❌ Please enter a valid distance")
            return
        
        # Get address (optional)
        address = input("Address (optional): ").strip()
        if not address:
            address = f"Near {locality_name}, {city_name}"
        
        # Check if landmark already exists
        existing = db.execute(
            text("SELECT id FROM nearby_places WHERE name = :name AND locality_id = :locality_id"),
            {"name": landmark_name, "locality_id": locality_id}
        ).fetchone()
        
        if existing:
            print(f"❌ Landmark '{landmark_name}' already exists in {locality_name}")
            return
        
        # Insert new landmark
        db.execute(
            text("""
                INSERT INTO nearby_places (name, category_id, locality_id, distance_km, address) 
                VALUES (:name, :category_id, :locality_id, :distance, :address)
            """),
            {
                "name": landmark_name,
                "category_id": category_id,
                "locality_id": locality_id,
                "distance": distance,
                "address": address
            }
        )
        
        db.commit()
        print(f"✅ Successfully added: {landmark_name} ({category_name}) - {distance} km from {locality_name}, {city_name}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

def add_project_distance():
    """Add distance from a project to a landmark"""
    
    db = next(get_db())
    
    try:
        print("🏢 ADD PROJECT TO LANDMARK DISTANCE:")
        print("-" * 40)
        
        # Get available projects
        projects = db.execute(text("SELECT id, name, locality_id FROM projects ORDER BY name")).fetchall()
        if not projects:
            print("❌ No projects found. Please add projects first.")
            return
        
        print("Available projects:")
        for i, (proj_id, proj_name, proj_loc_id) in enumerate(projects, 1):
            print(f"  {i}. {proj_name}")
        
        # Get available landmarks
        landmarks = db.execute(text("""
            SELECT np.id, np.name, nc.name as category, l.city, l.name as locality
            FROM nearby_places np
            JOIN nearby_categories nc ON np.category_id = nc.id
            JOIN localities l ON np.locality_id = l.id
            ORDER BY l.city, l.name, np.name
        """)).fetchall()
        
        if not landmarks:
            print("❌ No landmarks found. Please add landmarks first.")
            return
        
        print("\nAvailable landmarks:")
        for i, (land_id, land_name, land_cat, land_city, land_loc) in enumerate(landmarks, 1):
            print(f"  {i}. {land_name} ({land_cat}) - {land_loc}, {land_city}")
        
        print("\nEnter project-landmark distance:")
        
        # Get project
        try:
            proj_choice = int(input(f"Choose project (1-{len(projects)}): ")) - 1
            if 0 <= proj_choice < len(projects):
                project_id = projects[proj_choice][0]
                project_name = projects[proj_choice][1]
            else:
                print("❌ Invalid project choice")
                return
        except ValueError:
            print("❌ Please enter a valid number")
            return
        
        # Get landmark
        try:
            land_choice = int(input(f"Choose landmark (1-{len(landmarks)}): ")) - 1
            if 0 <= land_choice < len(landmarks):
                landmark_id = landmarks[land_choice][0]
                landmark_name = landmarks[land_choice][1]
                landmark_cat = landmarks[land_choice][2]
            else:
                print("❌ Invalid landmark choice")
                return
        except ValueError:
            print("❌ Please enter a valid number")
            return
        
        # Get distance
        try:
            distance = float(input("Distance in kilometers (e.g., 2.5): "))
            if distance <= 0:
                print("❌ Distance must be positive")
                return
        except ValueError:
            print("❌ Please enter a valid distance")
            return
        
        # Check if project-landmark distance already exists
        existing = db.execute(
            text("SELECT id FROM project_nearby WHERE project_id = :project_id AND nearby_place_id = :landmark_id"),
            {"project_id": project_id, "landmark_id": landmark_id}
        ).fetchone()
        
        if existing:
            print(f"❌ Distance from {project_name} to {landmark_name} already exists")
            return
        
        # Insert new project-landmark distance
        db.execute(
            text("""
                INSERT INTO project_nearby (project_id, nearby_place_id, distance_km) 
                VALUES (:project_id, :landmark_id, :distance)
            """),
            {
                "project_id": project_id,
                "landmark_id": landmark_id,
                "distance": distance
            }
        )
        
        db.commit()
        print(f"✅ Successfully added: {project_name} → {landmark_name} ({landmark_cat}): {distance} km")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Main menu for manual distance management"""
    
    while True:
        print("\n🗺️  MANUAL DISTANCE MANAGEMENT")
        print("=" * 40)
        print("1. View existing distance data")
        print("2. Add new landmark with distance")
        print("3. Add project to landmark distance")
        print("4. Exit")
        print("-" * 40)
        
        choice = input("Choose option (1-4): ").strip()
        
        if choice == "1":
            show_existing_data()
        elif choice == "2":
            add_landmark_manually()
        elif choice == "3":
            add_project_distance()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main()
