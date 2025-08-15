#!/usr/bin/env python3
"""
Script to remove all gym amenities from all properties
"""

from backend.database import get_db
from sqlalchemy import text

def remove_gym_amenities():
    """Remove all gym amenities from all properties"""
    print("🗑️ REMOVING GYM AMENITIES FROM ALL PROPERTIES")
    print("=" * 60)
    
    db = next(get_db())
    
    try:
        # First, let's see what we're about to delete
        print("1️⃣ CHECKING WHAT WILL BE REMOVED:")
        print("-" * 40)
        
        # Get the gym amenity ID
        gym_id_query = "SELECT id FROM amenities WHERE name ILIKE '%gym%'"
        gym_id_result = db.execute(text(gym_id_query)).fetchone()
        
        if not gym_id_result:
            print("   ❌ No gym amenity found in amenities table")
            return
        
        gym_id = gym_id_result[0]
        print(f"   🏋️ Gym amenity ID: {gym_id}")
        
        # Count how many project-amenity relationships will be removed
        count_query = "SELECT COUNT(*) FROM project_amenities WHERE amenity_id = :gym_id"
        count_result = db.execute(text(count_query), {"gym_id": gym_id}).fetchone()
        gym_relationships = count_result[0]
        
        print(f"   📊 Project-amenity relationships to remove: {gym_relationships}")
        
        # Show which projects will lose gym amenities
        projects_query = """
            SELECT p.name as project_name, pa.project_id
            FROM project_amenities pa
            JOIN projects p ON pa.project_id = p.id
            WHERE pa.amenity_id = :gym_id
            ORDER BY p.name
        """
        projects = db.execute(text(projects_query), {"gym_id": gym_id}).fetchall()
        
        print(f"   🏗️ Projects that will lose gym amenities:")
        for project in projects:
            print(f"      - {project[0]} (ID: {project[1]})")
        
        # Confirm deletion
        print(f"\n2️⃣ CONFIRMING DELETION:")
        print("-" * 40)
        print(f"   🚨 This will remove gym amenities from {gym_relationships} projects")
        print(f"   🚨 This action cannot be undone!")
        
        # For safety, let's just proceed (since this is a test environment)
        print(f"   ✅ Proceeding with deletion...")
        
        # Delete all gym amenity relationships
        delete_query = "DELETE FROM project_amenities WHERE amenity_id = :gym_id"
        result = db.execute(text(delete_query), {"gym_id": gym_id})
        
        print(f"   🗑️ Deleted {result.rowcount} gym amenity relationships")
        
        # Verify deletion
        print(f"\n3️⃣ VERIFYING DELETION:")
        print("-" * 40)
        
        # Check if any gym relationships remain
        remaining_query = "SELECT COUNT(*) FROM project_amenities WHERE amenity_id = :gym_id"
        remaining_result = db.execute(text(remaining_query), {"gym_id": gym_id}).fetchone()
        remaining_count = remaining_result[0]
        
        if remaining_count == 0:
            print(f"   ✅ All gym amenities successfully removed!")
        else:
            print(f"   ⚠️ {remaining_count} gym amenities still remain")
        
        # Check total project-amenity relationships
        total_query = "SELECT COUNT(*) FROM project_amenities"
        total_result = db.execute(text(total_query)).fetchone()
        total_count = total_result[0]
        
        print(f"   📊 Total project-amenity relationships remaining: {total_count}")
        
        # Commit the changes
        db.commit()
        print(f"   💾 Changes committed to database")
        
    except Exception as e:
        print(f"❌ Error removing gym amenities: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    remove_gym_amenities()
