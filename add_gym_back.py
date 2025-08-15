#!/usr/bin/env python3
"""
Script to add gym amenities back to a few projects for testing
"""

from backend.database import get_db
from sqlalchemy import text
import uuid
from datetime import datetime

def add_gym_back():
    """Add gym amenities back to a few projects for testing"""
    print("🏋️ ADDING GYM AMENITIES BACK FOR TESTING")
    print("=" * 60)
    
    db = next(get_db())
    
    try:
        # Get the gym amenity ID
        gym_id_query = "SELECT id FROM amenities WHERE name ILIKE '%gym%'"
        gym_id_result = db.execute(text(gym_id_query)).fetchone()
        
        if not gym_id_result:
            print("   ❌ No gym amenity found in amenities table")
            return
        
        gym_id = gym_id_result[0]
        print(f"   🏋️ Gym amenity ID: {gym_id}")
        
        # Get a few projects to add gym to
        projects_query = """
            SELECT id, name FROM projects 
            ORDER BY name 
            LIMIT 3
        """
        projects = db.execute(text(projects_query)).fetchall()
        
        print(f"\n📊 Adding gym to {len(projects)} projects:")
        print("-" * 40)
        
        for project in projects:
            project_id = project[0]
            project_name = project[1]
            
            # Check if this project already has gym
            existing_query = """
                SELECT COUNT(*) FROM project_amenities 
                WHERE project_id = :project_id AND amenity_id = :gym_id
            """
            existing_result = db.execute(text(existing_query), {
                "project_id": project_id,
                "gym_id": gym_id
            }).fetchone()
            
            if existing_result[0] > 0:
                print(f"   ⚠️ {project_name} already has gym")
                continue
            
            # Add gym amenity to this project
            insert_query = """
                INSERT INTO project_amenities (id, project_id, amenity_id, created_at, updated_at)
                VALUES (:id, :project_id, :amenity_id, :created_at, :updated_at)
            """
            
            new_id = str(uuid.uuid4())
            now = datetime.utcnow()
            
            db.execute(text(insert_query), {
                "id": new_id,
                "project_id": project_id,
                "amenity_id": gym_id,
                "created_at": now,
                "updated_at": now
            })
            
            print(f"   ✅ Added gym to {project_name}")
        
        # Verify the additions
        print(f"\n🔍 VERIFYING ADDITIONS:")
        print("-" * 30)
        
        # Count total gym relationships
        count_query = "SELECT COUNT(*) FROM project_amenities WHERE amenity_id = :gym_id"
        count_result = db.execute(text(count_query), {"gym_id": gym_id}).fetchone()
        total_gym = count_result[0]
        
        print(f"   📊 Total projects with gym: {total_gym}")
        
        # Show which projects now have gym
        projects_with_gym_query = """
            SELECT p.name as project_name
            FROM project_amenities pa
            JOIN projects p ON pa.project_id = p.id
            WHERE pa.amenity_id = :gym_id
            ORDER BY p.name
        """
        projects_with_gym = db.execute(text(projects_with_gym_query), {"gym_id": gym_id}).fetchall()
        
        print(f"   🏗️ Projects with gym:")
        for project in projects_with_gym:
            print(f"      - {project[0]}")
        
        # Commit the changes
        db.commit()
        print(f"\n💾 Changes committed to database")
        
    except Exception as e:
        print(f"❌ Error adding gym amenities: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    add_gym_back()
