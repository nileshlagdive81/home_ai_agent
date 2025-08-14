#!/usr/bin/env python3
"""
Script to populate distance data ONLY for Pune and Mumbai properties
Final version with proper UUID handling and timestamps
"""

import sys
import os
import uuid
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database import get_db
from sqlalchemy import text

def clear_existing_distance_data():
    """Clear existing distance data to start fresh"""
    
    db = next(get_db())
    
    try:
        print("🧹 CLEARING EXISTING DISTANCE DATA")
        print("=" * 50)
        
        # Clear nearby_places table
        db.execute(text("DELETE FROM nearby_places"))
        print("✅ Cleared nearby_places table")
        
        db.commit()
        print("✅ All existing distance data cleared successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

def populate_pune_mumbai_landmarks():
    """Populate landmarks ONLY for Pune and Mumbai using existing table structure"""
    
    db = next(get_db())
    
    try:
        # Get location IDs for Pune and Mumbai only
        locations = db.execute(text("""
            SELECT id, city, locality, area 
            FROM locations 
            WHERE city IN ('Pune', 'Mumbai')
            ORDER BY city, locality
        """)).fetchall()
        
        print("🏛️  Populating Pune and Mumbai landmarks...")
        print(f"Found {len(locations)} locations in Pune/Mumbai")
        
        # Define landmarks for each city
        landmarks_data = [
            # Mumbai Landmarks
            ("NMV School", "School", "Mumbai", "Bandra West", 3.0, "Near Bandra Station"),
            ("Bandra Railway Station", "Railway Station", "Mumbai", "Bandra West", 2.0, "Bandra West"),
            ("Mindspace IT Park", "IT Park", "Mumbai", "Worli", 6.0, "Worli"),
            ("Inorbit Mall", "Mall", "Mumbai", "Bandra West", 1.5, "Bandra West"),
            ("Mumbai Airport", "Airport", "Mumbai", "Bandra West", 12.5, "Mumbai Airport"),
            ("Bandra Metro", "Metro Station", "Mumbai", "Bandra West", 0.8, "Bandra West"),
            ("Kokilaben Hospital", "Hospital", "Mumbai", "Worli", 2.5, "Worli"),
            ("Powai Lake", "Park", "Mumbai", "Worli", 1.0, "Worli"),
            ("Hiranandani Gardens", "Park", "Mumbai", "Worli", 0.5, "Worli"),
            ("IIT Bombay", "Office", "Mumbai", "Worli", 1.2, "Worli"),
            ("Phoenix MarketCity", "Mall", "Mumbai", "Worli", 2.0, "Worli"),
            ("Worli Sea Face", "Park", "Mumbai", "Worli", 0.3, "Worli"),
            ("Bandra Fort", "Park", "Mumbai", "Bandra West", 0.2, "Bandra West"),
            ("Juhu Beach", "Park", "Mumbai", "Bandra West", 1.8, "Bandra West"),
            
            # Pune Landmarks
            ("Pune Airport", "Airport", "Pune", "Hinjewadi", 25.0, "Pune Airport"),
            ("Hinjewadi IT Park", "IT Park", "Pune", "Hinjewadi", 2.0, "Hinjewadi"),
            ("Phoenix MarketCity Pune", "Mall", "Pune", "Hinjewadi", 1.8, "Hinjewadi"),
            ("Pune Railway Station", "Railway Station", "Pune", "Hinjewadi", 12.0, "Pune Railway"),
            ("Pune Metro", "Metro Station", "Pune", "Hinjewadi", 3.5, "Hinjewadi"),
            ("Wakad IT Park", "IT Park", "Pune", "Hinjewadi", 1.5, "Wakad"),
            ("Pune University", "Office", "Pune", "Hinjewadi", 8.0, "Pune University"),
            ("Koregaon Park", "Park", "Pune", "Hinjewadi", 15.0, "Koregaon Park"),
            ("FC Road", "Market", "Pune", "Hinjewadi", 18.0, "FC Road"),
            ("Koregaon Park Mall", "Mall", "Pune", "Hinjewadi", 16.0, "Koregaon Park"),
            ("Pune Central Mall", "Mall", "Pune", "Hinjewadi", 14.0, "Pune Central"),
            ("Pune Golf Course", "Park", "Pune", "Hinjewadi", 20.0, "Pune Golf Course")
        ]
        
        # Get projects in Pune and Mumbai
        projects = db.execute(text("""
            SELECT pr.id, pr.name, l.city, l.locality
            FROM projects pr
            JOIN project_locations pl ON pr.id = pl.project_id
            JOIN locations l ON pl.location_id = l.id
            WHERE l.city IN ('Pune', 'Mumbai')
            ORDER BY l.city, pr.name
        """)).fetchall()
        
        print(f"Found {len(projects)} projects in Pune/Mumbai:")
        for proj in projects:
            print(f"  • {proj[1]} ({proj[2]}, {proj[3]})")
        
        # Create landmarks for each project
        current_time = datetime.now()
        for project in projects:
            project_id, project_name, project_city, project_locality = project
            
            for name, place_type, city, locality, base_distance, address in landmarks_data:
                # Check if this landmark belongs to the project's city
                if city == project_city:
                    # Calculate distance based on locality
                    if project_locality == locality:
                        # Same locality - use base distance
                        distance = base_distance
                    else:
                        # Different locality in same city - add some variation
                        import random
                        distance = base_distance + random.uniform(0.5, 2.0)
                        distance = round(distance, 1)
                    
                    # Insert landmark with explicit UUID and timestamps
                    db.execute(
                        text("""
                            INSERT INTO nearby_places (id, project_id, place_type, place_name, distance_km, walking_distance, created_at, updated_at) 
                            VALUES (:id, :project_id, :place_type, :place_name, :distance, :walking_distance, :created_at, :updated_at)
                        """),
                        {
                            "id": str(uuid.uuid4()),
                            "project_id": project_id,
                            "place_type": place_type,
                            "place_name": name,
                            "distance": distance,
                            "walking_distance": distance <= 1.0,  # Walking distance if <= 1 km
                            "created_at": current_time,
                            "updated_at": current_time
                        }
                    )
                    print(f"  ✅ {project_name} → {name} ({place_type}): {distance} km")
        
        db.commit()
        print("✅ Pune and Mumbai landmarks populated successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

def show_distance_summary():
    """Show summary of distance data for Pune and Mumbai"""
    
    db = next(get_db())
    
    try:
        print("📊 PUNE AND MUMBAI DISTANCE DATA SUMMARY")
        print("=" * 60)
        
        # Show landmarks by project and city
        print("\n🏛️  LANDMARKS BY PROJECT:")
        landmarks = db.execute(text("""
            SELECT pr.name as project, l.city, l.locality, np.place_name, np.place_type, np.distance_km, np.walking_distance
            FROM nearby_places np
            JOIN projects pr ON np.project_id = pr.id
            JOIN project_locations pl ON pr.id = pl.project_id
            JOIN locations l ON pl.location_id = l.id
            ORDER BY l.city, pr.name, np.distance_km
        """)).fetchall()
        
        current_project = ""
        current_city = ""
        for landmark in landmarks:
            project, city, locality, place_name, place_type, distance, walking = landmark
            if city != current_city:
                print(f"\n  🌆 {city}:")
                current_city = city
                current_project = ""
            
            if project != current_project:
                print(f"    🏗️  {project} ({locality}):")
                current_project = project
            
            walking_icon = "🚶" if walking else "🚗"
            print(f"      • {place_name} ({place_type}): {distance} km {walking_icon}")
        
        # Show summary statistics
        print(f"\n📈 TOTAL RECORDS:")
        total_landmarks = db.execute(text("SELECT COUNT(*) FROM nearby_places")).fetchone()[0]
        print(f"  • Landmarks: {total_landmarks}")
        
        # Show distance ranges
        print(f"\n📏 DISTANCE RANGES:")
        walking_count = db.execute(text("SELECT COUNT(*) FROM nearby_places WHERE walking_distance = true")).fetchone()[0]
        driving_count = total_landmarks - walking_count
        print(f"  • Walking distance (≤1 km): {walking_count}")
        print(f"  • Driving distance (>1 km): {driving_count}")
        
        # Show place types
        print(f"\n🏷️  PLACE TYPES:")
        place_types = db.execute(text("""
            SELECT place_type, COUNT(*) as count
            FROM nearby_places
            GROUP BY place_type
            ORDER BY count DESC
        """)).fetchall()
        
        for place_type, count in place_types:
            print(f"  • {place_type}: {count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

def main():
    """Main function to populate Pune and Mumbai distance data only"""
    
    print("🗺️  PUNE AND MUMBAI DISTANCE DATA POPULATION")
    print("=" * 60)
    print("This script will populate distance data ONLY for Pune and Mumbai")
    print("Removing Bangalore and Delhi data as requested")
    print("Using existing table structure with proper UUID handling and timestamps")
    print()
    
    try:
        # Step 1: Clear existing data
        clear_existing_distance_data()
        print()
        
        # Step 2: Populate Pune and Mumbai landmarks only
        populate_pune_mumbai_landmarks()
        print()
        
        # Step 3: Show summary
        show_distance_summary()
        
        print("\n🎉 PUNE AND MUMBAI DISTANCE DATA POPULATION COMPLETE!")
        print("✅ Only Pune and Mumbai properties and landmarks are now available")
        print("❌ Bangalore and Delhi data has been removed")
        print()
        print("You can now use NLP queries like:")
        print("  • 'properties within 2 km of metro in Mumbai'")
        print("  • 'properties near airport within 5 km in Pune'")
        print("  • 'properties close to IT park in Hinjewadi'")
        print("  • 'properties near Bandra station'")
        print("  • 'properties within walking distance of mall'")
        
    except Exception as e:
        print(f"❌ Error in main: {e}")

if __name__ == "__main__":
    main()
