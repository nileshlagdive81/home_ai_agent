#!/usr/bin/env python3
"""
Check actual database structure to see existing columns
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database import get_db
from sqlalchemy import text

def check_database_structure():
    """Check what tables and columns actually exist in the database"""
    
    try:
        db = next(get_db())
        
        # Check what tables exist
        print("🔍 Checking database structure...")
        print("=" * 50)
        
        # List all tables
        tables_result = db.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name"))
        print("📋 Existing tables:")
        tables = [row[0] for row in tables_result]
        for table in tables:
            print(f"  - {table}")
        
        print()
        
        # Check properties table structure if it exists
        if 'properties' in tables:
            print("🏠 Properties table columns:")
            print("-" * 30)
            columns_result = db.execute(text("SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'properties' ORDER BY ordinal_position"))
            for row in columns_result:
                nullable = "NULL" if row[2] == "YES" else "NOT NULL"
                print(f"  - {row[0]}: {row[1]} ({nullable})")
        else:
            print("❌ Properties table does not exist")
            
        # Check projects table structure if it exists
        if 'projects' in tables:
            print("\n🏗️ Projects table columns:")
            print("-" * 30)
            columns_result = db.execute(text("SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'projects' ORDER BY ordinal_position"))
            for row in columns_result:
                nullable = "NULL" if row[2] == "YES" else "NOT NULL"
                print(f"  - {row[0]}: {row[1]} ({nullable})")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")

if __name__ == "__main__":
    check_database_structure()
