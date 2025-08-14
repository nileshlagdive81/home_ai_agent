-- Create media storage table for projects (images and videos)
CREATE TABLE project_media (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    property_id UUID REFERENCES properties(id) ON DELETE SET NULL,
    
    -- Media file information
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL, -- Relative path from project root
    file_type VARCHAR(20) NOT NULL, -- 'image' or 'video'
    mime_type VARCHAR(100), -- e.g., 'image/jpeg', 'video/mp4'
    file_size_bytes BIGINT,
    
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
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_project_media_project_id ON project_media(project_id);
CREATE INDEX idx_project_media_property_id ON project_media(property_id);
CREATE INDEX idx_project_media_category ON project_media(media_category);
CREATE INDEX idx_project_media_type ON project_media(file_type);
CREATE INDEX idx_project_media_primary ON project_media(is_primary);
CREATE INDEX idx_project_media_sort ON project_media(sort_order);

-- Create unique constraint for primary media per project
CREATE UNIQUE INDEX idx_project_media_primary_unique ON project_media(project_id) WHERE is_primary = TRUE;

-- Add trigger for updated_at
CREATE TRIGGER update_project_media_updated_at 
    BEFORE UPDATE ON project_media 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data for existing projects
INSERT INTO project_media (project_id, file_name, file_path, file_type, mime_type, media_category, is_primary, alt_text, sort_order)
SELECT 
    p.id,
    'project-' || p.id || '-main.jpg',
    'images/projects/' || LOWER(REPLACE(p.name, ' ', '-')) || '/main.jpg',
    'image',
    'image/jpeg',
    'exterior',
    TRUE,
    p.name || ' - Main View',
    1
FROM projects p
WHERE p.project_status IN ('Ready to Move', 'Under Construction', 'New Launch')
LIMIT 5;

-- Add media count to projects view (optional)
CREATE OR REPLACE VIEW projects_with_media AS
SELECT 
    p.*,
    COUNT(pm.id) as total_media_count,
    COUNT(CASE WHEN pm.file_type = 'image' THEN 1 END) as image_count,
    COUNT(CASE WHEN pm.file_type = 'video' THEN 1 END) as video_count,
    MAX(CASE WHEN pm.is_primary = TRUE THEN pm.file_path END) as primary_image_path
FROM projects p
LEFT JOIN project_media pm ON p.id = pm.project_id AND pm.is_active = TRUE
GROUP BY p.id, p.name, p.developer_id, p.description, p.project_type, p.total_units, 
         p.units_per_floor, p.total_floors, p.project_status, p.rera_number, 
         p.possession_date, p.completion_date, p.created_at, p.updated_at;
