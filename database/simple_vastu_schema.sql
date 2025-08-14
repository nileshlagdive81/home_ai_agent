-- Simple Vastu Schema - Room Direction Analysis Only
-- Focuses only on room placement by direction for basic Vastu compliance

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Vastu Directions Table (8 directions)
CREATE TABLE IF NOT EXISTS vastu_directions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    direction_name VARCHAR(50) NOT NULL, -- North, South, East, West, NE, NW, SE, SW
    ruling_deity VARCHAR(100), -- Kuber, Yama, Indra, Varun, etc.
    element VARCHAR(50), -- Earth, Water, Fire, Air
    best_for TEXT, -- What this direction is best for
    avoid_for TEXT, -- What to avoid in this direction
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vastu Room Types Table (Basic rooms)
CREATE TABLE IF NOT EXISTS vastu_room_types (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    room_name VARCHAR(100) NOT NULL, -- Hall, Kitchen, Pooja Room, Bathroom, etc.
    best_direction VARCHAR(50), -- Best direction for this room
    avoid_direction VARCHAR(50), -- Direction to avoid for this room
    vastu_benefits TEXT, -- Benefits of proper placement
    vastu_issues TEXT, -- Issues if placed incorrectly
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Property Room Vastu Analysis Table (Simple room analysis)
CREATE TABLE IF NOT EXISTS property_room_vastu (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    property_id UUID REFERENCES properties(id),
    room_type VARCHAR(100) NOT NULL, -- Hall, Kitchen, Pooja Room, Bathroom
    room_direction VARCHAR(50) NOT NULL, -- North, South, East, West, etc.
    vastu_score INTEGER CHECK (vastu_score >= 1 AND vastu_score <= 10), -- 1-10 score
    is_ideal_placement BOOLEAN DEFAULT FALSE, -- True if room is in best direction
    vastu_status VARCHAR(50), -- Excellent, Good, Fair, Poor
    recommendations TEXT, -- Simple recommendations
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert basic Vastu directions
INSERT INTO vastu_directions (direction_name, ruling_deity, element, best_for, avoid_for) VALUES
('North', 'Kuber (Wealth)', 'Water', 'Business, Water bodies, Main entrance', 'Kitchen, Fire place'),
('South', 'Yama (Justice)', 'Earth', 'Storage, Heavy items, Master bedroom', 'Main entrance, Living area'),
('East', 'Indra (Power)', 'Air', 'Main entrance, Living room, Study', 'Kitchen, Bathroom'),
('West', 'Varun (Water)', 'Water', 'Bedroom, Study room, Storage', 'Main entrance, Kitchen'),
('North-East', 'Ishanya (Knowledge)', 'Space', 'Prayer room, Study, Water tank', 'Kitchen, Bathroom, Storage'),
('South-East', 'Agni (Fire)', 'Fire', 'Kitchen, Fire place, Generator', 'Prayer room, Bedroom'),
('South-West', 'Nairutya (Stability)', 'Earth', 'Master bedroom, Storage, Heavy items', 'Kitchen, Prayer room'),
('North-West', 'Vayu (Air)', 'Air', 'Guest bedroom, Storage, Garage', 'Prayer room, Main entrance');

-- Insert basic room types with Vastu guidelines
INSERT INTO vastu_room_types (room_name, best_direction, avoid_direction, vastu_benefits, vastu_issues) VALUES
('Hall/Living Room', 'North, East, North-East', 'South-West, South', 'Family harmony, Positive energy, Good communication', 'Family conflicts, Negative energy, Communication issues'),
('Kitchen', 'South-East', 'North-East, North', 'Good health, Prosperity, Family harmony', 'Health issues, Financial problems, Family conflicts'),
('Pooja Room', 'North-East', 'South-West, South-East', 'Spiritual growth, Peace of mind, Positive energy', 'Spiritual obstacles, Mental stress, Negative energy'),
('Master Bedroom', 'South-West', 'North-East, North', 'Stability, Good sleep, Relationship harmony', 'Sleep issues, Relationship problems, Instability'),
('Bathroom', 'North-West, South', 'North-East, East', 'Good health, Proper waste elimination', 'Health issues, Energy drainage'),
('Study Room', 'North-East, East', 'South-West, South', 'Concentration, Knowledge gain, Success', 'Lack of focus, Learning difficulties'),
('Storage Room', 'South-West, South', 'North-East, East', 'Proper organization, Stability', 'Clutter, Disorganization'),
('Dining Room', 'West, North-West', 'South-East, South', 'Good digestion, Family bonding', 'Digestive issues, Family conflicts');

-- Create indexes for performance
CREATE INDEX idx_property_room_vastu_property_id ON property_room_vastu(property_id);
CREATE INDEX idx_property_room_vastu_room_type ON property_room_vastu(room_type);
CREATE INDEX idx_property_room_vastu_direction ON property_room_vastu(room_direction);
CREATE INDEX idx_vastu_directions_name ON vastu_directions(direction_name);
CREATE INDEX idx_vastu_room_types_name ON vastu_room_types(room_name);
