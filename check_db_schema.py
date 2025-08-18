#!/usr/bin/env python3
"""
Check database schema to understand column types and table structure
"""

import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_connection():
    """Get database connection"""
    try:
        connection = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'real_estate_db'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'Swami@1919'),
            port=os.getenv('DB_PORT', '5432')
        )
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def check_schema():
    """Check the database schema"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        print("🔍 Checking Database Schema")
        print("=" * 50)
        
        # Check projects table
        print("\n📋 Projects table:")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'projects' 
            ORDER BY ordinal_position;
        """)
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'})")
        
        # Check properties table
        print("\n📋 Properties table:")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'properties' 
            ORDER BY ordinal_position;
        """)
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'})")
        
        # Check if project_media table exists
        print("\n📋 Project_media table:")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = 'project_media';
        """)
        result = cursor.fetchone()
        if result:
            print("  ✅ Table exists")
            cursor.execute("""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = 'project_media' 
                ORDER BY ordinal_position;
            """)
            columns = cursor.fetchall()
            for col in columns:
                print(f"  {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'})")
        else:
            print("  ❌ Table does not exist")
        
        # Check sample data
        print("\n📊 Sample Data:")
        cursor.execute("SELECT COUNT(*) FROM projects;")
        result = cursor.fetchone()
        print(f"  Projects: {result[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM properties;")
        result = cursor.fetchone()
        print(f"  Properties: {result[0]}")
        
        # Check for Lodha Park project
        cursor.execute("SELECT id, name FROM projects WHERE name ILIKE '%Lodha%';")
        result = cursor.fetchone()
        if result:
            print(f"  Lodha Park project: {result[0]} - {result[1]}")
        else:
            print("  Lodha Park project: Not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking schema: {e}")
        return False
        
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    check_schema()
