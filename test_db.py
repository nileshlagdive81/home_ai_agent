#!/usr/bin/env python3
"""
Test script to verify database connection and create tables
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from database import create_tables, engine
from models import *

def test_database():
    """Test database connection and create tables"""
    try:
        print("Testing database connection...")
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ Database connection successful!")
        
        print("Creating tables...")
        create_tables()
        print("✅ Tables created successfully!")
        
        # Verify tables were created
        with engine.connect() as conn:
            result = conn.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            tables = [row[0] for row in result]
            print(f"✅ Tables created: {', '.join(tables)}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_database()
    if success:
        print("\n🎉 Database setup completed successfully!")
    else:
        print("\n💥 Database setup failed!")
        sys.exit(1)
