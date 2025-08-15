#!/usr/bin/env python3
"""
Script to check the structure of nearby_places table
"""

from backend.database import get_db
from sqlalchemy import text

def check_table_structure():
    """Check the structure of nearby_places table"""
    print("🔍 CHECKING NEARBY_PLACES TABLE STRUCTURE")
    print("=" * 60)
    
    db = next(get_db())
    
    try:
        # Check table structure
        structure_query = """
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'nearby_places'
            ORDER BY ordinal_position
        """
        
        columns = db.execute(text(structure_query)).fetchall()
        
        print("📊 TABLE STRUCTURE:")
        print("-" * 40)
        for column in columns:
            col_name, data_type, nullable, default_val = column
            print(f"   - {col_name}: {data_type} {'(NULL)' if nullable == 'YES' else '(NOT NULL)'}")
            if default_val:
                print(f"     Default: {default_val}")
        
        # Check sample data
        print(f"\n📊 SAMPLE DATA:")
        print("-" * 40)
        sample_query = "SELECT * FROM nearby_places LIMIT 5"
        sample_data = db.execute(text(sample_query)).fetchall()
        
        for row in sample_data:
            print(f"   {row}")
        
        # Check total count
        count_query = "SELECT COUNT(*) FROM nearby_places"
        total_count = db.execute(text(count_query)).fetchone()[0]
        print(f"\n📊 Total nearby places: {total_count}")
        
    except Exception as e:
        print(f"❌ Error checking table structure: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    check_table_structure()
