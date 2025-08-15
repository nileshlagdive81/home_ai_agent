#!/usr/bin/env python3
"""
Script to show a comprehensive summary of all the data that has been populated in the database
"""

from backend.database import get_db
from sqlalchemy import text

def show_database_summary():
    """Show comprehensive summary of all database data"""
    print("🏗️ DATABASE POPULATION SUMMARY")
    print("=" * 50)
    
    db = next(get_db())
    
    try:
        # 1. Developers Summary
        print("\n👥 DEVELOPERS:")
        result = db.execute(text("SELECT name, company_name, experience_years, completed_projects FROM developers ORDER BY name"))
        for row in result:
            print(f"  - {row[0]} ({row[1]}) - {row[2]} years exp, {row[3]} projects")
        
        # 2. Locations Summary
        print("\n📍 LOCATIONS:")
        result = db.execute(text("SELECT city, COUNT(*) as count FROM locations GROUP BY city ORDER BY city"))
        for row in result:
            print(f"  - {row[0]}: {row[1]} localities")
        
        # 3. Projects Summary
        print("\n🏢 PROJECTS:")
        result = db.execute(text("""
            SELECT p.name, p.project_type, p.project_status, p.total_units, 
                   d.name as developer, l.city, l.locality
            FROM projects p 
            JOIN developers d ON p.developer_id = d.id
            JOIN project_locations pl ON p.id = pl.project_id
            JOIN locations l ON pl.location_id = l.id
            ORDER BY p.name
        """))
        current_project = None
        for row in result:
            if current_project != row[0]:
                current_project = row[0]
                print(f"\n  🏢 {row[0]} ({row[1]}) - {row[2]}")
                print(f"    Developer: {row[4]}")
                print(f"    Units: {row[3]}")
                print(f"    Location: {row[5]}, {row[6]}")
            else:
                print(f"    Additional Location: {row[5]}, {row[6]}")
        
        # 4. Properties Summary
        print("\n🏠 PROPERTIES:")
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
        total_properties = 0
        for row in result:
            avg_price = int(row[2]) if row[2] else 0
            min_price = int(row[3]) if row[3] else 0
            max_price = int(row[4]) if row[4] else 0
            total_properties += row[1]
            print(f"  🏢 {row[0]}: {row[1]} properties")
            print(f"    💰 Price Range: ₹{min_price:,} - ₹{max_price:,}")
            print(f"    📊 Average Price: ₹{avg_price:,}")
        print(f"\n  📊 TOTAL PROPERTIES: {total_properties}")
        
        # 5. Amenities Summary
        print("\n🏷️ AMENITIES:")
        result = db.execute(text("SELECT category, COUNT(*) as count FROM amenities GROUP BY category ORDER BY category"))
        for row in result:
            print(f"  - {row[0]}: {row[1]} amenities")
        
        # 6. Project Amenities Summary
        print("\n🔗 PROJECT AMENITIES:")
        result = db.execute(text("""
            SELECT p.name as project_name, COUNT(pa.id) as amenity_count
            FROM projects p 
            JOIN project_amenities pa ON p.id = pa.project_id 
            GROUP BY p.id, p.name 
            ORDER BY p.name
        """))
        for row in result:
            print(f"  - {row[0]}: {row[1]} amenities")
        
        # 7. Nearby Places Summary
        print("\n🚶 NEARBY PLACES:")
        result = db.execute(text("""
            SELECT p.name as project_name, COUNT(np.id) as place_count
            FROM projects p 
            JOIN nearby_places np ON p.id = np.project_id 
            GROUP BY p.id, p.name 
            ORDER BY p.name
        """))
        for row in result:
            print(f"  - {row[0]}: {row[1]} nearby places")
        
        # 8. Sample Queries that can be tested
        print("\n🔍 SAMPLE QUERIES YOU CAN TEST:")
        print("  📍 Location-based queries:")
        print("    - 'Show me properties in Pune'")
        print("    - 'Properties in Mumbai Bandra West'")
        print("    - 'Houses near Hinjewadi'")
        
        print("\n  🏠 Property type queries:")
        print("    - 'Show me 2 BHK apartments'")
        print("    - '3 BHK properties under 2 crores'")
        print("    - '1 BHK flats in Pune'")
        
        print("\n  💰 Price-based queries:")
        print("    - 'Properties under 1 crore'")
        print("    - 'Houses between 1-2 crores'")
        print("    - 'Luxury properties above 2 crores'")
        
        print("\n  🏢 Project-based queries:")
        print("    - 'Properties in Lodha Park'")
        print("    - 'Show me Godrej projects'")
        print("    - 'Kolte Patil properties'")
        
        print("\n  🚶 Nearby amenities queries:")
        print("    - 'Properties near metro station'")
        print("    - 'Houses near schools'")
        print("    - 'Properties near hospitals'")
        
        print("\n  🏷️ Amenity-based queries:")
        print("    - 'Properties with swimming pool'")
        print("    - 'Houses with gym facilities'")
        print("    - 'Properties with smart home features'")
        
        print("\n  🔄 Status-based queries:")
        print("    - 'Available properties'")
        print("    - 'Ready to move houses'")
        print("    - 'Under construction projects'")
        
        print("\n  📊 Complex queries:")
        print("    - '2 BHK apartments in Pune under 1.5 crores with gym'")
        print("    - 'Luxury properties in Mumbai near metro with swimming pool'")
        print("    - '3 BHK houses in Kolte Patil projects with garden'")
        
        print("\n  📍 Distance-based queries:")
        print("    - 'Properties within 1 km of metro'")
        print("    - 'Houses near railway station'")
        print("    - 'Properties near shopping malls'")
        
        print("\n  🏗️ Developer-based queries:")
        print("    - 'Lodha Group properties'")
        print("    - 'Godrej projects in Mumbai'")
        print("    - 'Kolte Patil developments in Pune'")
        
        print("\n  🎯 Combined filters:")
        print("    - '2-3 BHK apartments in Pune under 2 crores with swimming pool'")
        print("    - 'Luxury properties in Mumbai near beach with gym and spa'")
        print("    - 'Ready to move 3 BHK in Kolte Patil projects near metro'")
        
    except Exception as e:
        print(f"❌ Error showing database summary: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    show_database_summary()
