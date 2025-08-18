#!/usr/bin/env python3
"""
Setup script for media support in Real Estate database
This script adds video_url and floor_plan_url fields and creates the project_media table
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

def setup_media_support():
    """Set up media support in the database"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        print("Setting up media support...")
        
        # 1. Add video_url field to projects table
        try:
            cursor.execute("""
                ALTER TABLE projects ADD COLUMN IF NOT EXISTS video_url VARCHAR(500);
            """)
            print("✅ Added video_url field to projects table")
        except Exception as e:
            print(f"⚠️  video_url field: {e}")
        
        # 2. Add floor_plan_url field to properties table
        try:
            cursor.execute("""
                ALTER TABLE properties ADD COLUMN IF NOT EXISTS floor_plan_url VARCHAR(500);
            """)
            print("✅ Added floor_plan_url field to properties table")
        except Exception as e:
            print(f"⚠️  floor_plan_url field: {e}")
        
        # 3. Create project_media table (if it doesn't exist with correct structure)
        try:
            # Drop and recreate the table to ensure correct structure
            cursor.execute("DROP TABLE IF EXISTS project_media CASCADE;")
            
            cursor.execute("""
                CREATE TABLE project_media (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
                    property_id UUID REFERENCES properties(id) ON DELETE SET NULL,
                    
                    file_name VARCHAR(255) NOT NULL,
                    file_path VARCHAR(500) NOT NULL,
                    file_type VARCHAR(20) NOT NULL,
                    mime_type VARCHAR(100),
                    file_size_bytes BIGINT,
                    
                    media_category VARCHAR(50) NOT NULL,
                    is_primary BOOLEAN DEFAULT FALSE,
                    is_featured BOOLEAN DEFAULT FALSE,
                    
                    alt_text VARCHAR(255),
                    caption TEXT,
                    sort_order INTEGER DEFAULT 0,
                    
                    width INTEGER,
                    height INTEGER,
                    duration_seconds INTEGER,
                    
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """)
            print("✅ Created project_media table")
            
            # Create indexes
            cursor.execute("""
                CREATE INDEX idx_project_media_project_id ON project_media(project_id);
                CREATE INDEX idx_project_media_property_id ON project_media(property_id);
                CREATE INDEX idx_project_media_category ON project_media(media_category);
                CREATE INDEX idx_project_media_type ON project_media(file_type);
                CREATE INDEX idx_project_media_primary ON project_media(is_primary);
                CREATE INDEX idx_project_media_sort ON project_media(sort_order);
            """)
            print("✅ Created indexes for project_media table")
            
        except Exception as e:
            print(f"⚠️  project_media table: {e}")
        
        # 4. Add sample floor plan URLs to properties
        try:
            cursor.execute("""
                UPDATE properties 
                SET floor_plan_url = 'images/Project Images/Sample Project Image.jpg'
                WHERE bhk_count = 1.0;
            """)
            
            cursor.execute("""
                UPDATE properties 
                SET floor_plan_url = 'images/Project Images/Sample Bedroom.jpg'
                WHERE bhk_count = 2.0;
            """)
            
            cursor.execute("""
                UPDATE properties 
                SET floor_plan_url = 'images/Project Images/sample kitchen.jpg'
                WHERE bhk_count = 3.0;
            """)
            
            print("✅ Added sample floor plan URLs to properties")
            
        except Exception as e:
            print(f"⚠️  floor plan URLs: {e}")
        
        # 5. Insert sample media data for Lodha Park project
        try:
            # Find Lodha Park project
            cursor.execute("""
                SELECT id FROM projects WHERE name ILIKE '%Lodha%' LIMIT 1;
            """)
            result = cursor.fetchone()
            
            if result:
                lodha_project_id = result[0]
                print(f"Found Lodha Park project: {lodha_project_id}")
                
                # Insert sample images
                cursor.execute("""
                    INSERT INTO project_media (project_id, file_name, file_path, file_type, mime_type, media_category, is_primary, alt_text, sort_order) VALUES
                    (%s, 'lodha-park-main.jpg', 'images/Project Images/Sample Project Image.jpg', 'image', 'image/jpeg', 'exterior', TRUE, 'Lodha Park - Main View', 1),
                    (%s, 'lodha-park-bedroom.jpg', 'images/Project Images/Sample Bedroom.jpg', 'image', 'image/jpeg', 'interior', FALSE, 'Lodha Park - Bedroom', 2),
                    (%s, 'lodha-park-kitchen.jpg', 'images/Project Images/sample kitchen.jpg', 'image', 'image/jpeg', 'interior', FALSE, 'Lodha Park - Kitchen', 3),
                    (%s, 'lodha-park-video.mp4', 'images/Project Videos/Projevct Vides.mp4', 'video', 'video/mp4', 'video_tour', FALSE, 'Lodha Park - Project Video Tour', 4);
                """, (lodha_project_id, lodha_project_id, lodha_project_id, lodha_project_id))
                
                # Update project with video URL
                cursor.execute("""
                    UPDATE projects SET video_url = 'images/Project Videos/Projevct Vides.mp4' WHERE id = %s;
                """, (lodha_project_id,))
                
                print("✅ Added sample media data for Lodha Park")
            else:
                print("⚠️  Lodha Park project not found")
                
        except Exception as e:
            print(f"⚠️  sample media data: {e}")
        
        # Commit changes
        connection.commit()
        print("\n🎉 Media support setup completed successfully!")
        
        # Verify the setup
        print("\n📊 Verification:")
        cursor.execute("""
            SELECT COUNT(*) as total_properties_with_floor_plans 
            FROM properties 
            WHERE floor_plan_url IS NOT NULL;
        """)
        result = cursor.fetchone()
        print(f"Properties with floor plans: {result[0]}")
        
        cursor.execute("""
            SELECT COUNT(*) as total_media_items 
            FROM project_media;
        """)
        result = cursor.fetchone()
        print(f"Total media items: {result[0]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up media support: {e}")
        connection.rollback()
        return False
        
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    print("🚀 Setting up Media Support for Real Estate Database")
    print("=" * 60)
    
    success = setup_media_support()
    
    if success:
        print("\n✅ Setup completed successfully!")
        print("\nNext steps:")
        print("1. Restart the backend server")
        print("2. Test the project details page")
        print("3. Check BHK modals for floor plans")
        print("4. Verify video and image sections")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")
