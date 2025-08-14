-- 🗺️ MANUAL DISTANCE DATA POPULATION
-- Run this script to add sample distance data without internet APIs
-- All distances are manually entered based on real-world knowledge

-- Step 1: Insert landmark categories (if not exists)
INSERT INTO nearby_categories (name, description, icon) VALUES
('School', 'Educational institutions', '🏫'),
('Railway Station', 'Railway stations and metro', '🚉'),
('IT Park', 'IT parks and tech hubs', '🏢'),
('Metro Station', 'Metro rail stations', '🚇'),
('Hospital', 'Hospitals and clinics', '🏥'),
('Mall', 'Shopping malls and centers', '🛍️'),
('Airport', 'Airports and terminals', '✈️'),
('Bus Stand', 'Bus terminals and stops', '🚌'),
('Park', 'Parks and gardens', '🌳'),
('Restaurant', 'Restaurants and cafes', '🍽️'),
('Office', 'Office buildings and corporate parks', '🏢'),
('Bank', 'Banks and ATMs', '🏦'),
('Gym', 'Gyms and fitness centers', '💪'),
('Cinema', 'Movie theaters', '🎬'),
('Market', 'Local markets and shops', '🛒')
ON CONFLICT (name) DO NOTHING;

-- Step 2: Insert sample landmarks with distances
-- Note: You'll need to update the locality_id values based on your actual data

-- Mumbai Landmarks
INSERT INTO nearby_places (name, category_id, locality_id, distance_km, address) VALUES
('NMV School', (SELECT id FROM nearby_categories WHERE name = 'School'), 
 (SELECT id FROM localities WHERE name = 'Bandra West' AND city_id = (SELECT id FROM cities WHERE name = 'Mumbai')), 
 3.0, 'Near Bandra Station'),
 
('Bandra Railway Station', (SELECT id FROM nearby_categories WHERE name = 'Railway Station'), 
 (SELECT id FROM localities WHERE name = 'Bandra West' AND city_id = (SELECT id FROM cities WHERE name = 'Mumbai')), 
 2.0, 'Bandra West'),
 
('Mindspace IT Park', (SELECT id FROM nearby_categories WHERE name = 'IT Park'), 
 (SELECT id FROM localities WHERE name = 'Andheri' AND city_id = (SELECT id FROM cities WHERE name = 'Mumbai')), 
 6.0, 'Andheri West'),
 
('Inorbit Mall', (SELECT id FROM nearby_categories WHERE name = 'Mall'), 
 (SELECT id FROM localities WHERE name = 'Andheri' AND city_id = (SELECT id FROM cities WHERE name = 'Mumbai')), 
 1.5, 'Andheri West'),
 
('Mumbai Airport', (SELECT id FROM nearby_categories WHERE name = 'Airport'), 
 (SELECT id FROM localities WHERE name = 'Andheri' AND city_id = (SELECT id FROM cities WHERE name = 'Mumbai')), 
 8.0, 'Andheri East'),
 
('Andheri Metro', (SELECT id FROM nearby_categories WHERE name = 'Metro Station'), 
 (SELECT id FROM localities WHERE name = 'Andheri' AND city_id = (SELECT id FROM cities WHERE name = 'Mumbai')), 
 0.8, 'Andheri West'),
 
('Kokilaben Hospital', (SELECT id FROM nearby_categories WHERE name = 'Hospital'), 
 (SELECT id FROM localities WHERE name = 'Andheri' AND city_id = (SELECT id FROM cities WHERE name = 'Mumbai')), 
 2.5, 'Andheri West'),
 
('Powai Lake', (SELECT id FROM nearby_categories WHERE name = 'Park'), 
 (SELECT id FROM localities WHERE name = 'Powai' AND city_id = (SELECT id FROM cities WHERE name = 'Mumbai')), 
 1.0, 'Powai'),
 
('Hiranandani Gardens', (SELECT id FROM nearby_categories WHERE name = 'Park'), 
 (SELECT id FROM localities WHERE name = 'Powai' AND city_id = (SELECT id FROM cities WHERE name = 'Mumbai')), 
 0.5, 'Powai'),
 
('IIT Bombay', (SELECT id FROM nearby_categories WHERE name = 'Office'), 
 (SELECT id FROM localities WHERE name = 'Powai' AND city_id = (SELECT id FROM cities WHERE name = 'Mumbai')), 
 1.2, 'Powai')

ON CONFLICT (name, locality_id) DO NOTHING;

-- Bangalore Landmarks
INSERT INTO nearby_places (name, category_id, locality_id, distance_km, address) VALUES
('Whitefield Railway', (SELECT id FROM nearby_categories WHERE name = 'Railway Station'), 
 (SELECT id FROM localities WHERE name = 'Whitefield' AND city_id = (SELECT id FROM cities WHERE name = 'Bangalore')), 
 4.0, 'Whitefield'),
 
('Phoenix MarketCity', (SELECT id FROM nearby_categories WHERE name = 'Mall'), 
 (SELECT id FROM localities WHERE name = 'Whitefield' AND city_id = (SELECT id FROM cities WHERE name = 'Bangalore')), 
 2.0, 'Whitefield'),
 
('ITPL Tech Park', (SELECT id FROM nearby_categories WHERE name = 'IT Park'), 
 (SELECT id FROM localities WHERE name = 'Whitefield' AND city_id = (SELECT id FROM cities WHERE name = 'Bangalore')), 
 1.5, 'Whitefield'),
 
('Bangalore Airport', (SELECT id FROM nearby_categories WHERE name = 'Airport'), 
 (SELECT id FROM localities WHERE name = 'Whitefield' AND city_id = (SELECT id FROM cities WHERE name = 'Bangalore')), 
 25.0, 'Whitefield'),
 
('Whitefield Metro', (SELECT id FROM nearby_categories WHERE name = 'Metro Station'), 
 (SELECT id FROM localities WHERE name = 'Whitefield' AND city_id = (SELECT id FROM cities WHERE name = 'Bangalore')), 
 0.5, 'Whitefield'),
 
('Vydehi Hospital', (SELECT id FROM nearby_categories WHERE name = 'Hospital'), 
 (SELECT id FROM localities WHERE name = 'Whitefield' AND city_id = (SELECT id FROM cities WHERE name = 'Bangalore')), 
 3.0, 'Whitefield')

ON CONFLICT (name, locality_id) DO NOTHING;

-- Pune Landmarks
INSERT INTO nearby_places (name, category_id, locality_id, distance_km, address) VALUES
('Pune Airport', (SELECT id FROM nearby_categories WHERE name = 'Airport'), 
 (SELECT id FROM localities WHERE name = 'Hinjewadi' AND city_id = (SELECT id FROM cities WHERE name = 'Pune')), 
 18.0, 'Hinjewadi'),
 
('Hinjewadi IT Park', (SELECT id FROM nearby_categories WHERE name = 'IT Park'), 
 (SELECT id FROM localities WHERE name = 'Hinjewadi' AND city_id = (SELECT id FROM cities WHERE name = 'Pune')), 
 2.0, 'Hinjewadi'),
 
('Phoenix MarketCity Pune', (SELECT id FROM nearby_categories WHERE name = 'Mall'), 
 (SELECT id FROM localities WHERE name = 'Hinjewadi' AND city_id = (SELECT id FROM cities WHERE name = 'Pune')), 
 1.8, 'Hinjewadi'),
 
('Pune Railway Station', (SELECT id FROM nearby_categories WHERE name = 'Railway Station'), 
 (SELECT id FROM localities WHERE name = 'Hinjewadi' AND city_id = (SELECT id FROM cities WHERE name = 'Pune')), 
 12.0, 'Hinjewadi'),
 
('Pune Metro', (SELECT id FROM nearby_categories WHERE name = 'Metro Station'), 
 (SELECT id FROM localities WHERE name = 'Hinjewadi' AND city_id = (SELECT id FROM cities WHERE name = 'Pune')), 
 3.5, 'Hinjewadi')

ON CONFLICT (name, locality_id) DO NOTHING;

-- Step 3: Insert project to landmark distances
-- Note: You'll need to update the project_id values based on your actual data

-- Example: Lodha Park project distances
INSERT INTO project_nearby (project_id, nearby_place_id, distance_km) VALUES
-- Replace 'Lodha Park' with your actual project name
((SELECT id FROM projects WHERE name LIKE '%Lodha%' LIMIT 1), 
 (SELECT id FROM nearby_places WHERE name = 'NMV School'), 3.2),
 
((SELECT id FROM projects WHERE name LIKE '%Lodha%' LIMIT 1), 
 (SELECT id FROM nearby_places WHERE name = 'Bandra Railway Station'), 2.1),
 
((SELECT id FROM projects WHERE name LIKE '%Lodha%' LIMIT 1), 
 (SELECT id FROM nearby_places WHERE name = 'Mindspace IT Park'), 6.5),
 
((SELECT id FROM projects WHERE name LIKE '%Lodha%' LIMIT 1), 
 (SELECT id FROM nearby_places WHERE name = 'Inorbit Mall'), 1.8),
 
((SELECT id FROM projects WHERE name LIKE '%Lodha%' LIMIT 1), 
 (SELECT id FROM nearby_places WHERE name = 'Mumbai Airport'), 8.2)

ON CONFLICT (project_id, nearby_place_id) DO NOTHING;

-- Example: Hiranandani Gardens project distances
INSERT INTO project_nearby (project_id, nearby_place_id, distance_km) VALUES
-- Replace 'Hiranandani Gardens' with your actual project name
((SELECT id FROM projects WHERE name LIKE '%Hiranandani%' LIMIT 1), 
 (SELECT id FROM nearby_places WHERE name = 'Powai Lake'), 0.3),
 
((SELECT id FROM projects WHERE name LIKE '%Hiranandani%' LIMIT 1), 
 (SELECT id FROM nearby_places WHERE name = 'Hiranandani Gardens'), 0.1),
 
((SELECT id FROM projects WHERE name LIKE '%Hiranandani%' LIMIT 1), 
 (SELECT id FROM nearby_places WHERE name = 'IIT Bombay'), 1.0),
 
((SELECT id FROM projects WHERE name LIKE '%Hiranandani%' LIMIT 1), 
 (SELECT id FROM nearby_places WHERE name = 'Mumbai Airport'), 12.5)

ON CONFLICT (project_id, nearby_place_id) DO NOTHING;

-- Step 4: Verify the data
SELECT 'Landmark Categories' as info, COUNT(*) as count FROM nearby_categories
UNION ALL
SELECT 'Landmarks', COUNT(*) FROM nearby_places
UNION ALL
SELECT 'Project Distances', COUNT(*) FROM project_nearby;

-- Step 5: Show sample distance data
SELECT 
    np.name as landmark,
    nc.name as category,
    l.city,
    l.name as locality,
    np.distance_km,
    np.address
FROM nearby_places np
JOIN nearby_categories nc ON np.category_id = nc.id
JOIN localities l ON np.locality_id = l.id
ORDER BY l.city, l.name, np.distance_km
LIMIT 20;
