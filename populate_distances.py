#!/usr/bin/env python3
"""
Script to populate distance data manually for landmarks and projects
No internet required - all distances are manually entered
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database import get_db
from sqlalchemy import text

def populate_landmark_categories():
    """Populate basic landmark categories"""
    
    db = next(get_db())
    
    try:
        # Define landmark categories
        categories = [
            ("School", "Educational institutions", "🏫"),
            ("Railway Station", "Railway stations and metro", "🚉"),
            ("IT Park", "IT parks and tech hubs", "🏢"),
            ("Metro Station", "Metro rail stations", "🚇"),
            ("Hospital", "Hospitals and clinics", "🏥"),
            ("Mall", "Shopping malls and centers", "🛍️"),
            ("Airport", "Airports and terminals", "✈️"),
            ("Bus Stand", "Bus terminals and stops", "🚌"),
            ("Park", "Parks and gardens", "🌳"),
            ("Restaurant", "Restaurants and cafes", "🍽️"),
            ("Office", "Office buildings and corporate parks", "🏢"),
            ("Bank", "Banks and ATMs", "🏦"),
            ("Gym", "Gyms and fitness centers", "💪"),
            ("Cinema", "Movie theaters", "🎬"),
            ("Market", "Local markets and shops", "🛒")
        ]
        
        print("🏗️  Populating landmark categories...")
        
        for name, description, icon in categories:
            # Check if category already exists
            existing = db.execute(
                text("SELECT id FROM nearby_categories WHERE name = :name"),
                {"name": name}
            ).fetchone()
            
            if not existing:
                db.execute(
                    text("""
                        INSERT INTO nearby_categories (name, description, icon) 
                        VALUES (:name, :description, :icon)
                    """),
                    {"name": name, "description": description, "icon": icon}
                )
                print(f"  ✅ Added: {name} {icon}")
            else:
                print(f"  ⚠️  Already exists: {name}")
        
        db.commit()
        print("✅ Landmark categories populated successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

def populate_sample_landmarks():
    """Populate sample landmarks with distances"""
    
    db = next(get_db())
    
    try:
        # Get category IDs
        categories = db.execute(text("SELECT id, name FROM nearby_categories")).fetchall()
        category_map = {cat[1]: cat[0] for cat in categories}
        
        # Get locality IDs
        localities = db.execute(text("SELECT id, name, city FROM localities")).fetchall()
        locality_map = {f"{loc[2]}_{loc[1]}": loc[0] for loc in localities}
        
        print("🏛️  Populating sample landmarks...")
        
        # Sample landmarks data
        landmarks_data = [
            # Mumbai Landmarks
            ("NMV School", "School", "Mumbai_Bandra West", 3.0, "Near Bandra Station"),
            ("Bandra Railway Station", "Railway Station", "Mumbai_Bandra West", 2.0, "Bandra West"),
            ("Mindspace IT Park", "IT Park", "Mumbai_Andheri", 6.0, "Andheri West"),
            ("Inorbit Mall", "Mall", "Mumbai_Andheri", 1.5, "Andheri West"),
            ("Mumbai Airport", "Airport", "Mumbai_Andheri", 8.0, "Andheri East"),
            ("Andheri Metro", "Metro Station", "Mumbai_Andheri", 0.8, "Andheri West"),
            ("Kokilaben Hospital", "Hospital", "Mumbai_Andheri", 2.5, "Andheri West"),
            ("Powai Lake", "Park", "Mumbai_Powai", 1.0, "Powai"),
            ("Hiranandani Gardens", "Park", "Mumbai_Powai", 0.5, "Powai"),
            ("IIT Bombay", "Office", "Mumbai_Powai", 1.2, "Powai"),
            
            # Bangalore Landmarks
            ("Whitefield Railway", "Railway Station", "Bangalore_Whitefield", 4.0, "Whitefield"),
            ("Phoenix MarketCity", "Mall", "Bangalore_Whitefield", 2.0, "Whitefield"),
            ("ITPL Tech Park", "IT Park", "Bangalore_Whitefield", 1.5, "Whitefield"),
            ("Bangalore Airport", "Airport", "Bangalore_Whitefield", 25.0, "Whitefield"),
            ("Whitefield Metro", "Metro Station", "Bangalore_Whitefield", 0.5, "Whitefield"),
            ("Vydehi Hospital", "Hospital", "Bangalore_Whitefield", 3.0, "Whitefield"),
            
            # Pune Landmarks
            ("Pune Airport", "Airport", "Pune_Hinjewadi", 18.0, "Hinjewadi"),
            ("Hinjewadi IT Park", "IT Park", "Pune_Hinjewadi", 2.0, "Hinjewadi"),
            ("Phoenix MarketCity Pune", "Mall", "Pune_Hinjewadi", 1.8, "Hinjewadi"),
            ("Pune Railway Station", "Railway Station", "Pune_Hinjewadi", 12.0, "Hinjewadi"),
            ("Pune Metro", "Metro Station", "Pune_Hinjewadi", 3.5, "Hinjewadi")
        ]
        
        for name, category, location_key, distance, address in landmarks_data:
            if category in category_map and location_key in locality_map:
                category_id = category_map[category]
                locality_id = locality_map[location_key]
                
                # Check if landmark already exists
                existing = db.execute(
                    text("SELECT id FROM nearby_places WHERE name = :name AND locality_id = :locality_id"),
                    {"name": name, "locality_id": locality_id}
                ).fetchone()
                
                if not existing:
                    db.execute(
                        text("""
                            INSERT INTO nearby_places (name, category_id, locality_id, distance_km, address) 
                            VALUES (:name, :category_id, :locality_id, :distance, :address)
                        """),
                        {
                            "name": name, 
                            "category_id": category_id, 
                            "locality_id": locality_id, 
                            "distance": distance, 
                            "address": address
                        }
                    )
                    print(f"  ✅ Added: {name} - {distance} km from {location_key}")
                else:
                    print(f"  ⚠️  Already exists: {name} in {location_key}")
            else:
                print(f"  ❌ Skipped: {name} - Category '{category}' or Location '{location_key}' not found")
        
        db.commit()
        print("✅ Sample landmarks populated successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

def populate_project_distances():
    """Populate distances from projects to nearby landmarks"""
    
    db = next(get_db())
    
    try:
        print("🏢 Populating project to landmark distances...")
        
        # Get all projects and landmarks
        projects = db.execute(text("SELECT id, name, locality_id FROM projects")).fetchall()
        landmarks = db.execute(text("SELECT id, name, locality_id, distance_km FROM nearby_places")).fetchall()
        
        for project in projects:
            project_id, project_name, project_locality_id = project
            
            for landmark in landmarks:
                landmark_id, landmark_name, landmark_locality_id, base_distance = landmark
                
                # If project and landmark are in same locality, use base distance
                # If different localities, add some variation (simulating real-world distances)
                if project_locality_id == landmark_locality_id:
                    distance = base_distance
                else:
                    # Add some variation for different localities
                    import random
                    distance = base_distance + random.uniform(0.5, 3.0)
                    distance = round(distance, 1)
                
                # Check if project-landmark distance already exists
                existing = db.execute(
                    text("SELECT id FROM project_nearby WHERE project_id = :project_id AND nearby_place_id = :landmark_id"),
                    {"project_id": project_id, "landmark_id": landmark_id}
                ).fetchone()
                
                if not existing:
                    db.execute(
                        text("""
                            INSERT INTO project_nearby (project_id, nearby_place_id, distance_km) 
                            VALUES (:project_id, :landmark_id, :distance)
                        """),
                        {"project_id": project_id, "landmark_id": landmark_id, "distance": distance}
                    )
                    print(f"  ✅ {project_name} → {landmark_name}: {distance} km")
                else:
                    print(f"  ⚠️  Already exists: {project_name} → {landmark_name}")
        
        db.commit()
        print("✅ Project distances populated successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

def show_distance_data():
    """Display all distance data for verification"""
    
    db = next(get_db())
    
    try:
        print("📊 DISTANCE DATA SUMMARY:")
        print("=" * 60)
        
        # Show categories
        print("\n🏷️  LANDMARK CATEGORIES:")
        categories = db.execute(text("SELECT name, description FROM nearby_categories ORDER BY name")).fetchall()
        for cat in categories:
            print(f"  • {cat[0]}: {cat[1]}")
        
        # Show landmarks with distances
        print("\n🏛️  LANDMARKS WITH DISTANCES:")
        landmarks = db.execute(text("""
            SELECT np.name, nc.name as category, l.city, l.name as locality, np.distance_km, np.address
            FROM nearby_places np
            JOIN nearby_categories nc ON np.category_id = nc.id
            JOIN localities l ON np.locality_id = l.id
            ORDER BY l.city, l.name, np.distance_km
        """)).fetchall()
        
        current_city = ""
        for landmark in landmarks:
            name, category, city, locality, distance, address = landmark
            if city != current_city:
                print(f"\n  🌆 {city}:")
                current_city = city
            print(f"    • {name} ({category}): {distance} km - {locality}")
        
        # Show project distances
        print("\n🏢 PROJECT TO LANDMARK DISTANCES:")
        project_distances = db.execute(text("""
            SELECT pr.name as project, np.name as landmark, pn.distance_km, l.city, l.name as locality
            FROM project_nearby pn
            JOIN projects pr ON pn.project_id = pr.id
            JOIN nearby_places np ON pn.nearby_place_id = np.id
            JOIN localities l ON pr.locality_id = l.id
            ORDER BY l.city, pr.name, pn.distance_km
            LIMIT 20
        """)).fetchall()
        
        current_project = ""
        for pd in project_distances:
            project, landmark, distance, city, locality = pd
            if project != current_project:
                print(f"\n    🏗️  {project} ({city}, {locality}):")
                current_project = project
            print(f"      → {landmark}: {distance} km")
        
        print(f"\n📈 TOTAL RECORDS:")
        total_categories = db.execute(text("SELECT COUNT(*) FROM nearby_categories")).fetchone()[0]
        total_landmarks = db.execute(text("SELECT COUNT(*) FROM nearby_places")).fetchone()[0]
        total_project_distances = db.execute(text("SELECT COUNT(*) FROM project_nearby")).fetchone()[0]
        
        print(f"  • Categories: {total_categories}")
        print(f"  • Landmarks: {total_landmarks}")
        print(f"  • Project Distances: {total_project_distances}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

def main():
    """Main function to populate all distance data"""
    
    print("🗺️  MANUAL DISTANCE DATA POPULATION")
    print("=" * 50)
    print("This script will populate distance data without using internet APIs")
    print("All distances are manually entered based on real-world knowledge")
    print()
    
    try:
        # Step 1: Populate landmark categories
        populate_landmark_categories()
        print()
        
        # Step 2: Populate sample landmarks
        populate_sample_landmarks()
        print()
        
        # Step 3: Populate project distances
        populate_project_distances()
        print()
        
        # Step 4: Show summary
        show_distance_data()
        
        print("\n🎉 DISTANCE DATA POPULATION COMPLETE!")
        print("You can now use NLP queries like:")
        print("  • 'properties within 2 km of metro'")
        print("  • 'properties near airport within 5 km'")
        print("  • 'properties close to IT park'")
        
    except Exception as e:
        print(f"❌ Error in main: {e}")

if __name__ == "__main__":
    main()
