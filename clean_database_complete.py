#!/usr/bin/env python3
"""
Script to completely clean all data from the database
"""

from backend.database import get_db, engine
from sqlalchemy import text, inspect

def clean_database_complete():
    """Clean all data from the database respecting foreign key constraints"""
    print("🧹 Complete Database Cleanup...")
    print("=" * 50)
    
    db = next(get_db())
    
    try:
        # Get table names using proper SQLAlchemy inspect
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        
        print(f"📋 Found {len(table_names)} tables:")
        for table in table_names:
            print(f"  • {table}")
        
        print(f"\n🗑️ Starting complete data cleanup...")
        
        # Clear data from tables in correct dependency order
        # Start with tables that have foreign keys to other tables
        tables_to_clear = [
            'property_price_history',
            'property_room_vastu',
            'roi_analysis',
            'search_results',
            'user_queries',
            'investment_analysis',
            'market_reports',
            'project_media',
            'project_nearby',
            'properties',
            'project_amenities', 
            'project_locations',
            'bhk_room_mapping',
            'projects',
            'locations',
            'amenities',
            'developers',
            'nearby_places',
            'financial_details',
            'room_vastu_guidelines',
            'vastu_directions',
            'nearby_categories',
            'bhk_types'
        ]
        
        # First, disable foreign key checks if possible
        try:
            db.execute(text("SET session_replication_role = replica;"))
            print("  ✅ Disabled foreign key checks")
        except:
            print("  ⚠️ Could not disable foreign key checks, will clear in order")
        
        for table in tables_to_clear:
            if table in table_names:
                try:
                    # Clear the table using proper SQLAlchemy text
                    result = db.execute(text(f"DELETE FROM {table}"))
                    deleted_count = result.rowcount
                    print(f"  ✅ Cleared table: {table} ({deleted_count} records)")
                except Exception as e:
                    print(f"  ❌ Error clearing {table}: {e}")
                    # Try to continue with other tables
        
        # Re-enable foreign key checks
        try:
            db.execute(text("SET session_replication_role = DEFAULT;"))
            print("  ✅ Re-enabled foreign key checks")
        except:
            pass
        
        # Commit the changes
        db.commit()
        print(f"\n✅ Database cleanup completed!")
        
        # Verify cleanup
        print(f"\n🔍 Verifying cleanup...")
        total_records = 0
        for table in tables_to_clear:
            if table in table_names:
                try:
                    result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    total_records += count
                    print(f"  • {table}: {count} records")
                except Exception as e:
                    print(f"  • {table}: Error checking count - {e}")
        
        print(f"\n📊 Total records remaining: {total_records}")
        
        if total_records == 0:
            print(f"\n🎉 Database is completely clean and ready for fresh data!")
        else:
            print(f"\n⚠️ Some data remains. You may need to manually clear remaining records.")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    clean_database_complete()
