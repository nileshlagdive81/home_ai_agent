-- Real Estate Database Schema
-- This schema supports Indian real estate with comprehensive property details

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Cities table
CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    state VARCHAR(100) NOT NULL,
    country VARCHAR(50) DEFAULT 'India',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Localities table (areas within cities)
CREATE TABLE localities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    city_id INTEGER REFERENCES cities(id) ON DELETE CASCADE,
    pincode VARCHAR(10),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, city_id)
);

-- Property types table
CREATE TABLE property_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Amenities table
CREATE TABLE amenities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50) NOT NULL, -- 'basic', 'luxury', 'security', 'recreation'
    icon VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Nearby places categories
CREATE TABLE nearby_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    icon VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Nearby places table
CREATE TABLE nearby_places (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category_id INTEGER REFERENCES nearby_categories(id) ON DELETE CASCADE,
    locality_id INTEGER REFERENCES localities(id) ON DELETE CASCADE,
    distance_km DECIMAL(5,2),
    address TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Projects table (main property projects)
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    developer_name VARCHAR(200),
    locality_id INTEGER REFERENCES localities(id) ON DELETE CASCADE,
    property_type_id INTEGER REFERENCES property_types(id) ON DELETE CASCADE,
    total_units INTEGER,
    units_per_floor INTEGER,
    total_floors INTEGER,
    project_status VARCHAR(50) NOT NULL, -- 'planning', 'under_construction', 'ready_to_move', 'completed'
    possession_date DATE,
    rera_number VARCHAR(50),
    description TEXT,
    highlights TEXT[],
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Project amenities mapping
CREATE TABLE project_amenities (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    amenity_id INTEGER REFERENCES amenities(id) ON DELETE CASCADE,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, amenity_id)
);

-- Project nearby places mapping
CREATE TABLE project_nearby (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    nearby_place_id INTEGER REFERENCES nearby_places(id) ON DELETE CASCADE,
    distance_km DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, nearby_place_id)
);

-- Property units table (individual flats/houses)
CREATE TABLE property_units (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    unit_number VARCHAR(50),
    floor_number INTEGER,
    bhk INTEGER NOT NULL, -- 1, 2, 3, 4, 5+
    carpet_area_sqft DECIMAL(8,2),
    built_up_area_sqft DECIMAL(8,2),
    super_built_up_area_sqft DECIMAL(8,2),
    price_per_sqft DECIMAL(10,2),
    total_price DECIMAL(15,2),
    booking_amount DECIMAL(12,2),
    is_available BOOLEAN DEFAULT TRUE,
    is_booked BOOLEAN DEFAULT FALSE,
    is_sold BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Property images table
CREATE TABLE property_images (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    unit_id INTEGER REFERENCES property_units(id) ON DELETE SET NULL,
    image_url VARCHAR(500) NOT NULL,
    image_type VARCHAR(50), -- 'exterior', 'interior', 'floor_plan', 'amenity', 'location'
    is_primary BOOLEAN DEFAULT FALSE,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users table (agents, admins, customers)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    full_name VARCHAR(200) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'customer', -- 'admin', 'agent', 'customer'
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User authentication table
CREATE TABLE user_auth (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    password_hash VARCHAR(255) NOT NULL,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Property viewings/appointments table
CREATE TABLE property_viewings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    unit_id INTEGER REFERENCES property_units(id) ON DELETE SET NULL,
    viewing_date DATE NOT NULL,
    viewing_time TIME NOT NULL,
    status VARCHAR(20) DEFAULT 'scheduled', -- 'scheduled', 'confirmed', 'completed', 'cancelled'
    agent_notes TEXT,
    customer_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Search queries log (for NLP training)
CREATE TABLE search_queries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    query_text TEXT NOT NULL,
    detected_intent VARCHAR(100),
    extracted_entities JSONB,
    search_results_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_projects_locality ON projects(locality_id);
CREATE INDEX idx_projects_status ON projects(project_status);
CREATE INDEX idx_property_units_project ON property_units(project_id);
CREATE INDEX idx_property_units_bhk ON property_units(bhk);
CREATE INDEX idx_property_units_price ON property_units(total_price);
CREATE INDEX idx_localities_city ON localities(city_id);
CREATE INDEX idx_nearby_places_locality ON nearby_places(locality_id);
CREATE INDEX idx_search_queries_intent ON search_queries(detected_intent);
CREATE INDEX idx_search_queries_created ON search_queries(created_at);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply triggers to tables with updated_at
CREATE TRIGGER update_cities_updated_at BEFORE UPDATE ON cities FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_localities_updated_at BEFORE UPDATE ON localities FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_property_units_updated_at BEFORE UPDATE ON property_units FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_property_viewings_updated_at BEFORE UPDATE ON property_viewings FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_nearby_places_updated_at BEFORE UPDATE ON nearby_places FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
