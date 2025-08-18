#!/usr/bin/env python3
"""
Script to create additional tables for Project Details Page
This script extends the existing database schema without modifying existing tables
"""

import os
import sys
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_database_connection():
    """Create database connection using hardcoded credentials from backend"""
    try:
        connection = psycopg2.connect(
            host='localhost',
            database='real_estate_db',
            user='postgres',
            password='Swami@1919',
            port='5432'
        )
        return connection
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return None

def execute_sql_file(connection, file_path):
    """Execute SQL file content"""
    try:
        if not os.path.exists(file_path):
            print(f"❌ SQL file not found: {file_path}")
            return False
            
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        cursor = connection.cursor()
        cursor.execute(sql_content)
        connection.commit()
        cursor.close()
        
        print(f"✅ Successfully executed: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error executing {file_path}: {e}")
        connection.rollback()
        return False

def main():
    """Main function to create project details tables"""
    print("🚀 Creating Project Details Tables...")
    print("=" * 50)
    
    # Connect to database
    connection = get_database_connection()
    if not connection:
        sys.exit(1)
    
    try:
        # Execute table creation SQL
        tables_sql = "database/project_details_tables.sql"
        if execute_sql_file(connection, tables_sql):
            print("✅ Tables created successfully!")
        else:
            print("❌ Failed to create tables")
            sys.exit(1)
        
        # Execute mock data insertion SQL
        mock_data_sql = "database/project_details_mock_data.sql"
        if execute_sql_file(connection, mock_data_sql):
            print("✅ Mock data inserted successfully!")
        else:
            print("❌ Failed to insert mock data")
            sys.exit(1)
        
        print("\n🎉 Project Details Tables Setup Complete!")
        print("=" * 50)
        print("📋 New Tables Created:")
        print("   • room_specifications")
        print("   • project_construction_specs")
        print("   • project_environmental_features")
        print("   • project_expert_reviews")
        print("   • project_safety_features")
        print("   • project_milestones")
        print("\n📊 Mock Data Inserted:")
        print("   • Room specifications for 1, 2, 3 BHK")
        print("   • Construction specs for 3 projects")
        print("   • Environmental features for 3 projects")
        print("   • Expert reviews for 3 projects")
        print("   • Safety features for 3 projects")
        print("   • Project milestones for 3 projects")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
    finally:
        connection.close()

if __name__ == "__main__":
    main()
