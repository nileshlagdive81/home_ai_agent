#!/usr/bin/env python3
"""
Script to clean all data from the database
"""

from backend.database import get_db, engine
from backend.models import Base, Location, Project, Property, ProjectLocation
from sqlalchemy import text, inspect

def clean_database():
    """Clean all data from the database"""
    print("🧹 Cleaning Database...")
    print("=" * 50)
    
    db = next(get_db())
    
    try:
        # Get table names using proper SQLAlchemy inspect
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        
        print(f"📋 Found {len(table_names)} tables:")
        for table in table_names:
            print(f"  • {table}")
        
        print(f"\n🗑️ Starting data cleanup...")
        
        # Clear data from tables in reverse dependency order
        tables_to_clear = [
            'properties',
            'project_amenities', 
            'project_locations',
            'projects',
            'locations',
            'amenities'
        ]
        
        for table in tables_to_clear:
            if table in table_names:
                try:
                    # Clear the table using proper SQLAlchemy text
                    db.execute(text(f"DELETE FROM {table}"))
                    print(f"  ✅ Cleared table: {table}")
                except Exception as e:
                    print(f"  ❌ Error clearing {table}: {e}")
        
        # Commit the changes
        db.commit()
        print(f"\n✅ Database cleanup completed successfully!")
        
        # Verify cleanup
        print(f"\n🔍 Verifying cleanup...")
        for table in tables_to_clear:
            if table in table_names:
                try:
                    result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    print(f"  • {table}: {count} records")
                except Exception as e:
                    print(f"  • {table}: Error checking count - {e}")
        
        print(f"\n🎉 Database is now clean and ready for fresh data!")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    clean_database()
