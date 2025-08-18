-- Additional Tables for Project Details Page
-- These tables extend the existing schema without modifying existing tables

-- 1. Room Specifications for existing BHK types
CREATE TABLE IF NOT EXISTS room_specifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID REFERENCES properties(id) ON DELETE CASCADE,
    room_name VARCHAR(100) NOT NULL, -- Master Bedroom, Living Room, Kitchen, etc.
    room_type VARCHAR(50) NOT NULL, -- bedroom, living, kitchen, bathroom, balcony
    length_feet DECIMAL(5,2),
    width_feet DECIMAL(5,2),
    area_sqft DECIMAL(8,2),
    direction VARCHAR(50), -- North, South, East, West, NE, NW, SE, SW
    features TEXT[], -- Built-in wardrobe, garden view, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Project Construction Specifications
CREATE TABLE IF NOT EXISTS project_construction_specs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    structure_type VARCHAR(100), -- RCC frame, steel frame, etc.
    wall_material VARCHAR(100), -- AAC blocks, bricks, etc.
    flooring_material VARCHAR(100), -- Vitrified tiles, marble, etc.
    ceiling_type VARCHAR(100), -- POP, gypsum, etc.
    electrical_specs TEXT, -- Wiring, switches, etc.
    plumbing_specs TEXT, -- Pipes, fittings, etc.
    paint_specs TEXT, -- Interior/exterior paint types
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Project Environmental Features
CREATE TABLE IF NOT EXISTS project_environmental_features (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    solar_water_heating BOOLEAN DEFAULT FALSE,
    rainwater_harvesting BOOLEAN DEFAULT FALSE,
    energy_efficient_lighting BOOLEAN DEFAULT FALSE,
    waste_management_system BOOLEAN DEFAULT FALSE,
    green_building_certification VARCHAR(100), -- LEED, IGBC, etc.
    water_conservation_features TEXT,
    energy_conservation_features TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Project Expert Reviews
CREATE TABLE IF NOT EXISTS project_expert_reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    location_rating DECIMAL(3,1), -- 4.8/5
    construction_quality_rating DECIMAL(3,1),
    investment_potential_rating DECIMAL(3,1),
    overall_rating DECIMAL(3,1),
    expert_name VARCHAR(200),
    review_date DATE,
    review_summary TEXT,
    detailed_review TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Project Safety Features
CREATE TABLE IF NOT EXISTS project_safety_features (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    cctv_surveillance BOOLEAN DEFAULT FALSE,
    fire_alarm_system BOOLEAN DEFAULT FALSE,
    access_control BOOLEAN DEFAULT FALSE,
    fire_staircase BOOLEAN DEFAULT FALSE,
    refuge_areas BOOLEAN DEFAULT FALSE,
    fire_extinguishers BOOLEAN DEFAULT FALSE,
    emergency_exits INTEGER,
    security_personnel_count INTEGER,
    monitoring_24_7 BOOLEAN DEFAULT FALSE,
    emergency_protocols TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Project Milestones
CREATE TABLE IF NOT EXISTS project_milestones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    milestone_name VARCHAR(100) NOT NULL, -- Foundation, Structure, Interiors, etc.
    status VARCHAR(50) NOT NULL, -- completed, in_progress, pending
    completion_date DATE,
    planned_date DATE,
    description TEXT,
    progress_percentage INTEGER, -- 0-100
    sort_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_room_specs_property ON room_specifications(property_id);
CREATE INDEX idx_construction_specs_project ON project_construction_specs(project_id);
CREATE INDEX idx_environmental_features_project ON project_environmental_features(project_id);
CREATE INDEX idx_expert_reviews_project ON project_expert_reviews(project_id);
CREATE INDEX idx_safety_features_project ON project_safety_features(project_id);
CREATE INDEX idx_milestones_project ON project_milestones(project_id);
CREATE INDEX idx_milestones_sort_order ON project_milestones(sort_order);

-- Note: updated_at triggers not created as the function doesn't exist in this database
-- The tables will still work without the automatic timestamp updates
