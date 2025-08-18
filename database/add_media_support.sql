-- Add media support to Real Estate database
-- This script adds video support and floor plan support

-- 1. Add video_url field to projects table
ALTER TABLE projects ADD COLUMN IF NOT EXISTS video_url VARCHAR(500);

-- 2. Add floor_plan_url field to properties table
ALTER TABLE properties ADD COLUMN IF NOT EXISTS floor_plan_url VARCHAR(500);

-- 3. Create project_media table for storing images and videos
CREATE TABLE IF NOT EXISTS project_media (
    id VARCHAR PRIMARY KEY,  -- UUID as string
    project_id VARCHAR NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    property_id VARCHAR REFERENCES properties(id) ON DELETE SET NULL,
    
    -- Media file information
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL, -- Relative path from project root
    file_type VARCHAR(20) NOT NULL, -- 'image' or 'video'
    mime_type VARCHAR(100), -- e.g., 'image/jpeg', 'video/mp4'
    file_size_bytes INTEGER,
    
    -- Media categorization
    media_category VARCHAR(50) NOT NULL, -- 'exterior', 'interior', 'floor_plan', 'amenity', 'location', 'video_tour'
    is_primary BOOLEAN DEFAULT FALSE, -- Primary image for project
    is_featured BOOLEAN DEFAULT FALSE, -- Featured in listings
    
    -- Display properties
    alt_text VARCHAR(255), -- Alt text for accessibility
    caption TEXT, -- Optional caption
    sort_order INTEGER DEFAULT 0, -- For ordering in galleries
    
    -- Metadata
    width INTEGER, -- For images/videos
    height INTEGER, -- For images/videos
    duration_seconds INTEGER, -- For videos
    
    -- Status and tracking
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_project_media_project_id ON project_media(project_id);
CREATE INDEX IF NOT EXISTS idx_project_media_property_id ON project_media(property_id);
CREATE INDEX IF NOT EXISTS idx_project_media_category ON project_media(media_category);
CREATE INDEX IF NOT EXISTS idx_project_media_type ON project_media(file_type);
CREATE INDEX IF NOT EXISTS idx_project_media_primary ON project_media(is_primary);
CREATE INDEX IF NOT EXISTS idx_project_media_sort ON project_media(sort_order);

-- Create unique constraint for primary media per project
CREATE UNIQUE INDEX IF NOT EXISTS idx_project_media_primary_unique ON project_media(project_id) WHERE is_primary = TRUE;

-- Insert sample media data for Lodha Park project
-- First, let's find the Lodha Park project ID
DO $$
DECLARE
    lodha_project_id VARCHAR;
BEGIN
    -- Get the Lodha Park project ID
    SELECT id INTO lodha_project_id FROM projects WHERE name ILIKE '%Lodha Park%' LIMIT 1;
    
    IF lodha_project_id IS NOT NULL THEN
        -- Insert sample images for Lodha Park
        INSERT INTO project_media (id, project_id, file_name, file_path, file_type, mime_type, media_category, is_primary, alt_text, sort_order) VALUES
        (gen_random_uuid()::VARCHAR, lodha_project_id, 'lodha-park-main.jpg', 'images/Project Images/Sample Project Image.jpg', 'image', 'image/jpeg', 'exterior', TRUE, 'Lodha Park - Main View', 1),
        (gen_random_uuid()::VARCHAR, lodha_project_id, 'lodha-park-bedroom.jpg', 'images/Project Images/Sample Bedroom.jpg', 'image', 'image/jpeg', 'interior', FALSE, 'Lodha Park - Bedroom', 2),
        (gen_random_uuid()::VARCHAR, lodha_project_id, 'lodha-park-kitchen.jpg', 'images/Project Images/sample kitchen.jpg', 'image', 'image/jpeg', 'interior', FALSE, 'Lodha Park - Kitchen', 3),
        (gen_random_uuid()::VARCHAR, lodha_project_id, 'lodha-park-hall.jpg', 'images/Project Images/sample hall.jpg', 'image', 'image/jpeg', 'interior', FALSE, 'Lodha Park - Living Hall', 4),
        (gen_random_uuid()::VARCHAR, lodha_project_id, 'lodha-park-bathroom.jpg', 'images/Project Images/sample toilet.jpg', 'image', 'image/jpeg', 'interior', FALSE, 'Lodha Park - Bathroom', 5),
        (gen_random_uuid()::VARCHAR, lodha_project_id, 'lodha-park-balcony.jpg', 'images/Project Images/sample balcony.jpg', 'image', 'image/jpeg', 'interior', FALSE, 'Lodha Park - Balcony', 6);
        
        -- Insert sample video for Lodha Park
        INSERT INTO project_media (id, project_id, file_name, file_path, file_type, mime_type, media_category, is_primary, alt_text, sort_order) VALUES
        (gen_random_uuid()::VARCHAR, lodha_project_id, 'lodha-park-video.mp4', 'images/Project Videos/Projevct Vides.mp4', 'video', 'video/mp4', 'video_tour', FALSE, 'Lodha Park - Project Video Tour', 7);
        
        -- Update Lodha Park project with video URL
        UPDATE projects SET video_url = 'images/Project Videos/Projevct Vides.mp4' WHERE id = lodha_project_id;
        
        RAISE NOTICE 'Inserted media data for Lodha Park project ID: %', lodha_project_id;
    ELSE
        RAISE NOTICE 'Lodha Park project not found';
    END IF;
END $$;

-- Insert sample floor plan data for BHK configurations
-- This will be populated when properties are created with floor plan URLs
