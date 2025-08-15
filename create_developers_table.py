#!/usr/bin/env python3
"""
Script to create a simple developers table
"""

from backend.database import get_db, engine
from sqlalchemy import text

def create_developers_table():
    """Create a simple developers table"""
    print("🏗️ Creating developers table...")
    
    db = next(get_db())
    
    try:
        # Create developers table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS developers (
            id VARCHAR PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            description TEXT,
            established_year INTEGER,
            rera_number VARCHAR(50),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        
        db.execute(text(create_table_sql))
        
        # Insert a few sample developers
        insert_developers_sql = """
        INSERT INTO developers (id, name, description, established_year, rera_number) VALUES
        ('dev-001', 'Sample Developer 1', 'Leading real estate developer in Maharashtra', 1995, 'MH123456'),
        ('dev-002', 'Sample Developer 2', 'Premium property developer', 2000, 'MH234567'),
        ('dev-003', 'Sample Developer 3', 'Luxury home builder', 1998, 'MH345678')
        ON CONFLICT (id) DO NOTHING;
        """
        
        db.execute(text(insert_developers_sql))
        
        db.commit()
        print("✅ Developers table created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating developers table: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_developers_table()
