-- Mock Data for Project Details Tables
-- This data relates to existing projects and property units

-- 1. Room Specifications for existing BHK types
-- Using actual property IDs from the database
INSERT INTO room_specifications (property_id, room_name, room_type, length_feet, width_feet, area_sqft, direction, features) VALUES
-- For 1 BHK (Lodha Park)
('d6ad4288-4b05-4dbe-87fb-e21c6a7553d2', 'Master Bedroom', 'bedroom', 12.0, 10.0, 120.0, 'North-East', ARRAY['Built-in wardrobe', 'Garden view', 'Balcony access']),
('d6ad4288-4b05-4dbe-87fb-e21c6a7553d2', 'Living Room', 'living', 14.0, 12.0, 168.0, 'North', ARRAY['Garden view', 'Balcony access', 'TV unit space']),
('d6ad4288-4b05-4dbe-87fb-e21c6a7553d2', 'Kitchen', 'kitchen', 8.0, 6.0, 48.0, 'South-East', ARRAY['Modular kitchen', 'Granite countertop', 'Breakfast counter']),
('d6ad4288-4b05-4dbe-87fb-e21c6a7553d2', 'Bathroom', 'bathroom', 6.0, 5.0, 30.0, 'North-West', ARRAY['Geyser provision', 'Exhaust fan', 'Modern fittings']),
('d6ad4288-4b05-4dbe-87fb-e21c6a7553d2', 'Balcony', 'balcony', 8.0, 4.0, 32.0, 'North', ARRAY['Garden view', 'Drying area', 'Plant space']),

-- For 2.5 BHK (Lodha Park)
('b57bc857-ae7e-4d5d-80db-692c0647ec1d', 'Master Bedroom', 'bedroom', 14.0, 12.0, 168.0, 'North-East', ARRAY['Built-in wardrobe', 'Attached bathroom', 'Balcony access']),
('b57bc857-ae7e-4d5d-80db-692c0647ec1d', 'Second Bedroom', 'bedroom', 12.0, 10.0, 120.0, 'North-West', ARRAY['Built-in wardrobe', 'Window view', 'Study area']),
('b57bc857-ae7e-4d5d-80db-692c0647ec1d', 'Living Room', 'living', 16.0, 14.0, 224.0, 'North', ARRAY['Dining area', 'Balcony access', 'TV unit space']),
('b57bc857-ae7e-4d5d-80db-692c0647ec1d', 'Kitchen', 'kitchen', 10.0, 8.0, 80.0, 'South-East', ARRAY['Modular kitchen', 'Granite countertop', 'Breakfast counter', 'Utility area']),
('b57bc857-ae7e-4d5d-80db-692c0647ec1d', 'Master Bathroom', 'bathroom', 8.0, 6.0, 48.0, 'North-East', ARRAY['Geyser provision', 'Exhaust fan', 'Modern fittings', 'Shower area']),
('b57bc857-ae7e-4d5d-80db-692c0647ec1d', 'Second Bathroom', 'bathroom', 6.0, 5.0, 30.0, 'North-West', ARRAY['Geyser provision', 'Exhaust fan', 'Modern fittings']),
('b57bc857-ae7e-4d5d-80db-692c0647ec1d', 'Balcony', 'balcony', 10.0, 4.0, 40.0, 'North', ARRAY['Garden view', 'Drying area', 'Plant space']),

-- For 3.5 BHK (Lodha Park)
('a8f9c009-77ba-47c1-806e-89194f5b2349', 'Master Bedroom', 'bedroom', 16.0, 14.0, 224.0, 'North-East', ARRAY['Built-in wardrobe', 'Attached bathroom', 'Balcony access', 'Walk-in closet']),
('a8f9c009-77ba-47c1-806e-89194f5b2349', 'Second Bedroom', 'bedroom', 14.0, 12.0, 168.0, 'North-West', ARRAY['Built-in wardrobe', 'Window view', 'Study area']),
('a8f9c009-77ba-47c1-806e-89194f5b2349', 'Third Bedroom', 'bedroom', 12.0, 10.0, 120.0, 'South-West', ARRAY['Built-in wardrobe', 'Window view', 'Guest room setup']),
('a8f9c009-77ba-47c1-806e-89194f5b2349', 'Living Room', 'living', 18.0, 16.0, 288.0, 'North', ARRAY['Separate dining area', 'Balcony access', 'TV unit space', 'Entertainment area']),
('a8f9c009-77ba-47c1-806e-89194f5b2349', 'Kitchen', 'kitchen', 12.0, 10.0, 120.0, 'South-East', ARRAY['Modular kitchen', 'Granite countertop', 'Breakfast counter', 'Utility area', 'Store room']),
('a8f9c009-77ba-47c1-806e-89194f5b2349', 'Master Bathroom', 'bathroom', 10.0, 8.0, 80.0, 'North-East', ARRAY['Geyser provision', 'Exhaust fan', 'Modern fittings', 'Shower area', 'Jacuzzi']),
('a8f9c009-77ba-47c1-806e-89194f5b2349', 'Second Bathroom', 'bathroom', 8.0, 6.0, 48.0, 'North-West', ARRAY['Geyser provision', 'Exhaust fan', 'Modern fittings', 'Shower area']),
('a8f9c009-77ba-47c1-806e-89194f5b2349', 'Third Bathroom', 'bathroom', 6.0, 5.0, 30.0, 'South-West', ARRAY['Geyser provision', 'Exhaust fan', 'Modern fittings']),
('a8f9c009-77ba-47c1-806e-89194f5b2349', 'Balcony', 'balcony', 12.0, 4.0, 48.0, 'North', ARRAY['Garden view', 'Drying area', 'Plant space', 'Sitting area']);

-- 2. Project Construction Specifications
-- Using actual project IDs from the database
INSERT INTO project_construction_specs (project_id, structure_type, wall_material, flooring_material, ceiling_type, electrical_specs, plumbing_specs, paint_specs) VALUES
('0338932f-b499-4b51-8f0a-07f877364674', 'RCC Frame Structure', 'AAC Blocks', 'Vitrified Tiles', 'POP with Gypsum', 'Copper wiring, Modular switches, LED lighting', 'CPVC pipes, Premium fittings, Geyser provision', 'Asian Paints Royale, Weathershield exterior'),
('27d2efb5-f70c-461f-a6ab-c61d3582e3d3', 'RCC Frame Structure', 'AAC Blocks', 'Marble & Vitrified Tiles', 'POP with Gypsum', 'Copper wiring, Modular switches, LED lighting, Smart home ready', 'CPVC pipes, Premium fittings, Geyser provision, Water softener', 'Asian Paints Royale, Weathershield exterior, Textured finish'),
('d87e9c19-e101-4867-85d9-05b925bfa094', 'Steel Frame Structure', 'AAC Blocks', 'Premium Marble', 'Suspended Gypsum', 'Copper wiring, Modular switches, LED lighting, Smart home automation', 'CPVC pipes, Premium fittings, Geyser provision, Water softener, RO system', 'Asian Paints Royale, Weathershield exterior, Metallic finish');

-- 3. Project Environmental Features
INSERT INTO project_environmental_features (project_id, solar_water_heating, rainwater_harvesting, energy_efficient_lighting, waste_management_system, green_building_certification, water_conservation_features, energy_conservation_features) VALUES
('0338932f-b499-4b51-8f0a-07f877364674', TRUE, TRUE, TRUE, TRUE, 'IGBC Silver', 'Low-flow fixtures, Dual flush toilets, Water-efficient landscaping', 'LED lighting, Energy-efficient appliances, Natural ventilation'),
('27d2efb5-f70c-461f-a6ab-c61d3582e3d3', TRUE, TRUE, TRUE, TRUE, 'IGBC Gold', 'Low-flow fixtures, Dual flush toilets, Water-efficient landscaping, Grey water recycling', 'LED lighting, Energy-efficient appliances, Natural ventilation, Solar panels'),
('d87e9c19-e101-4867-85d9-05b925bfa094', TRUE, TRUE, TRUE, TRUE, 'LEED Platinum', 'Low-flow fixtures, Dual flush toilets, Water-efficient landscaping, Grey water recycling, Rainwater storage', 'LED lighting, Energy-efficient appliances, Natural ventilation, Solar panels, Wind turbines');

-- 4. Project Expert Reviews
INSERT INTO project_expert_reviews (project_id, location_rating, construction_quality_rating, investment_potential_rating, overall_rating, expert_name, review_date, review_summary, detailed_review) VALUES
('0338932f-b499-4b51-8f0a-07f877364674', 4.5, 4.2, 4.3, 4.3, 'Real Estate Expert Group', '2024-01-15', 'Excellent location with good connectivity and amenities. Construction quality meets standards.', 'This project offers great value for money with its strategic location near major transport hubs. The construction quality is consistent with market standards, and the amenities provided justify the pricing. Investment potential is good with expected appreciation of 8-10% annually.'),
('27d2efb5-f70c-461f-a6ab-c61d3582e3d3', 4.8, 4.6, 4.7, 4.7, 'Property Consultants India', '2024-01-20', 'Premium location with superior construction quality and excellent investment potential.', 'Located in one of the most sought-after areas, this project stands out for its premium construction quality and attention to detail. The developer has maintained high standards throughout, making it an excellent investment choice with expected returns of 12-15% annually.'),
('d87e9c19-e101-4867-85d9-05b925bfa094', 4.9, 4.8, 4.9, 4.9, 'Luxury Real Estate Advisors', '2024-01-25', 'Exceptional luxury project with world-class construction and outstanding investment value.', 'This is a landmark project that sets new standards in luxury living. The construction quality is exceptional, using premium materials and innovative techniques. The location is prime, and the investment potential is outstanding with expected returns of 15-20% annually.');

-- 5. Project Safety Features
INSERT INTO project_safety_features (project_id, cctv_surveillance, fire_alarm_system, access_control, fire_staircase, refuge_areas, fire_extinguishers, emergency_exits, security_personnel_count, monitoring_24_7, emergency_protocols) VALUES
('0338932f-b499-4b51-8f0a-07f877364674', TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, 4, 8, TRUE, '24/7 security monitoring with CCTV surveillance. Fire safety systems with automatic alarms and sprinklers. Emergency response protocols in place with trained personnel. Direct connectivity to local fire department and police stations.'),
('27d2efb5-f70c-461f-a6ab-c61d3582e3d3', TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, 6, 12, TRUE, 'Advanced security system with biometric access control. Comprehensive fire safety with automatic detection and suppression. Emergency response protocols with regular drills. 24/7 monitoring with backup systems.'),
('d87e9c19-e101-4867-85d9-05b925bfa094', TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, 8, 16, TRUE, 'State-of-the-art security with AI-powered surveillance. Advanced fire safety with multiple suppression systems. Comprehensive emergency protocols with regular training. 24/7 monitoring with redundant systems and backup power.');

-- 6. Project Milestones
INSERT INTO project_milestones (project_id, milestone_name, status, completion_date, planned_date, description, progress_percentage, sort_order) VALUES
-- Project 1 milestones (Lodha Park)
('0338932f-b499-4b51-8f0a-07f877364674', 'Foundation', 'completed', '2023-06-15', '2023-06-30', 'Foundation work completed with RCC structure', 100, 1),
('0338932f-b499-4b51-8f0a-07f877364674', 'Structure', 'completed', '2023-12-20', '2023-12-31', 'RCC frame structure completed up to top floor', 100, 2),
('0338932f-b499-4b51-8f0a-07f877364674', 'Interiors', 'in_progress', NULL, '2024-03-31', 'Interior finishing work in progress', 75, 3),
('0338932f-b499-4b51-8f0a-07f877364674', 'Handover', 'pending', NULL, '2024-06-30', 'Final handover to customers', 0, 4),

-- Project 2 milestones (Godrej Bayview)
('27d2efb5-f70c-461f-a6ab-c61d3582e3d3', 'Foundation', 'completed', '2023-07-01', '2023-07-15', 'Foundation work completed with premium materials', 100, 1),
('27d2efb5-f70c-461f-a6ab-c61d3582e3d3', 'Structure', 'completed', '2024-01-15', '2024-01-31', 'Steel frame structure completed', 100, 2),
('27d2efb5-f70c-461f-a6ab-c61d3582e3d3', 'Interiors', 'in_progress', NULL, '2024-04-30', 'Premium interior finishing in progress', 60, 3),
('27d2efb5-f70c-461f-a6ab-c61d3582e3d3', 'Handover', 'pending', NULL, '2024-08-31', 'Final handover to customers', 0, 4),

-- Project 3 milestones (Raheja Vivarea)
('d87e9c19-e101-4867-85d9-05b925bfa094', 'Foundation', 'completed', '2023-08-01', '2023-08-15', 'Premium foundation with advanced engineering', 100, 1),
('d87e9c19-e101-4867-85d9-05b925bfa094', 'Structure', 'completed', '2024-02-01', '2024-02-15', 'Luxury steel frame structure completed', 100, 2),
('d87e9c19-e101-4867-85d9-05b925bfa094', 'Interiors', 'in_progress', NULL, '2024-06-30', 'Luxury interior finishing in progress', 45, 3),
('d87e9c19-e101-4867-85d9-05b925bfa094', 'Handover', 'pending', NULL, '2024-12-31', 'Final luxury handover to customers', 0, 4);
