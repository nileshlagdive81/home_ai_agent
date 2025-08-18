-- Add floor plan URLs to sample properties
-- This script adds floor plan images to BHK configurations for testing

-- First, let's add floor plan URLs to some sample properties
-- We'll use sample images as floor plans for now

UPDATE properties 
SET floor_plan_url = 'images/Project Images/Sample Project Image.jpg'
WHERE bhk_count = 1.0 
LIMIT 2;

UPDATE properties 
SET floor_plan_url = 'images/Project Images/Sample Bedroom.jpg'
WHERE bhk_count = 2.0 
LIMIT 2;

UPDATE properties 
SET floor_plan_url = 'images/Project Images/sample kitchen.jpg'
WHERE bhk_count = 3.0 
LIMIT 2;

-- Add floor plan URLs to properties in specific projects
UPDATE properties 
SET floor_plan_url = 'images/Project Images/sample hall.jpg'
WHERE project_id IN (
    SELECT id FROM projects WHERE name ILIKE '%Lodha%'
) AND bhk_count = 1.0;

UPDATE properties 
SET floor_plan_url = 'images/Project Images/sample toilet.jpg'
WHERE project_id IN (
    SELECT id FROM projects WHERE name ILIKE '%Lodha%'
) AND bhk_count = 2.0;

UPDATE properties 
SET floor_plan_url = 'images/Project Images/sample balcony.jpg'
WHERE project_id IN (
    SELECT id FROM projects WHERE name ILIKE '%Lodha%'
) AND bhk_count = 3.0;

-- Verify the updates
SELECT 
    p.id,
    p.bhk_count,
    p.floor_plan_url,
    pr.name as project_name
FROM properties p
JOIN projects pr ON p.project_id = pr.id
WHERE p.floor_plan_url IS NOT NULL
ORDER BY pr.name, p.bhk_count;
