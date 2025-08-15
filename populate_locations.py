#!/usr/bin/env python3
"""
Script to populate the locations table with realistic data for Pune and Mumbai
"""

from backend.database import get_db
from sqlalchemy import text
import uuid
from datetime import datetime

def populate_locations():
    """Populate locations table with realistic data for Pune and Mumbai"""
    print("🏗️ Populating locations table...")
    db = next(get_db())
    current_time = datetime.now()
    
    try:
        # Insert realistic location data for Pune and Mumbai
        locations_data = [
            # Mumbai Locations
            {
                'id': str(uuid.uuid4()),
                'locality': 'Bandra West',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'pincode': '400050',
                'area': 'Premium',
                'metro_available': True,
                'airport_distance_km': 8.5,
                'railway_station_distance_km': 2.0,
                'bus_stand_distance_km': 0.5,
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'locality': 'Juhu',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'pincode': '400049',
                'area': 'Premium',
                'metro_available': False,
                'airport_distance_km': 6.0,
                'railway_station_distance_km': 3.5,
                'bus_stand_distance_km': 0.8,
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'locality': 'Andheri West',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'pincode': '400058',
                'area': 'Mid-Range',
                'metro_available': True,
                'airport_distance_km': 4.0,
                'railway_station_distance_km': 1.5,
                'bus_stand_distance_km': 0.3,
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'locality': 'Powai',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'pincode': '400076',
                'area': 'Mid-Range',
                'metro_available': False,
                'airport_distance_km': 12.0,
                'railway_station_distance_km': 4.0,
                'bus_stand_distance_km': 1.2,
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'locality': 'Thane West',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'pincode': '400601',
                'area': 'Affordable',
                'metro_available': True,
                'airport_distance_km': 25.0,
                'railway_station_distance_km': 2.5,
                'bus_stand_distance_km': 0.8,
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'locality': 'Navi Mumbai',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'pincode': '400706',
                'area': 'Affordable',
                'metro_available': True,
                'airport_distance_km': 18.0,
                'railway_station_distance_km': 3.0,
                'bus_stand_distance_km': 1.0,
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'locality': 'Worli',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'pincode': '400018',
                'area': 'Premium',
                'metro_available': True,
                'airport_distance_km': 15.0,
                'railway_station_distance_km': 4.5,
                'bus_stand_distance_km': 1.5,
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'locality': 'Lower Parel',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'pincode': '400013',
                'area': 'Premium',
                'metro_available': True,
                'airport_distance_km': 16.0,
                'railway_station_distance_km': 3.8,
                'bus_stand_distance_km': 1.2,
                'created_at': current_time,
                'updated_at': current_time
            },
            
            # Pune Locations
            {
                'id': str(uuid.uuid4()),
                'locality': 'Koregaon Park',
                'city': 'Pune',
                'state': 'Maharashtra',
                'pincode': '411001',
                'area': 'Premium',
                'metro_available': False,
                'airport_distance_km': 12.0,
                'railway_station_distance_km': 2.5,
                'bus_stand_distance_km': 0.8,
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'locality': 'Kalyani Nagar',
                'city': 'Pune',
                'state': 'Maharashtra',
                'pincode': '411006',
                'area': 'Premium',
                'metro_available': False,
                'airport_distance_km': 10.0,
                'railway_station_distance_km': 3.0,
                'bus_stand_distance_km': 1.0,
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'locality': 'Viman Nagar',
                'city': 'Pune',
                'state': 'Maharashtra',
                'pincode': '411014',
                'area': 'Mid-Range',
                'metro_available': False,
                'airport_distance_km': 8.0,
                'railway_station_distance_km': 4.5,
                'bus_stand_distance_km': 1.5,
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'locality': 'Hinjewadi',
                'city': 'Pune',
                'state': 'Maharashtra',
                'pincode': '411057',
                'area': 'Mid-Range',
                'metro_available': False,
                'airport_distance_km': 20.0,
                'railway_station_distance_km': 8.0,
                'bus_stand_distance_km': 2.0,
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'locality': 'Wakad',
                'city': 'Pune',
                'state': 'Maharashtra',
                'pincode': '411057',
                'area': 'Affordable',
                'metro_available': False,
                'airport_distance_km': 22.0,
                'railway_station_distance_km': 9.0,
                'bus_stand_distance_km': 2.5,
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'locality': 'Baner',
                'city': 'Pune',
                'state': 'Maharashtra',
                'pincode': '411045',
                'area': 'Mid-Range',
                'metro_available': False,
                'airport_distance_km': 15.0,
                'railway_station_distance_km': 6.0,
                'bus_stand_distance_km': 1.8,
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'locality': 'Aundh',
                'city': 'Pune',
                'state': 'Maharashtra',
                'pincode': '411007',
                'area': 'Mid-Range',
                'metro_available': False,
                'airport_distance_km': 18.0,
                'railway_station_distance_km': 7.0,
                'bus_stand_distance_km': 2.2,
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'locality': 'Hadapsar',
                'city': 'Pune',
                'state': 'Maharashtra',
                'pincode': '411028',
                'area': 'Affordable',
                'metro_available': False,
                'airport_distance_km': 25.0,
                'railway_station_distance_km': 10.0,
                'bus_stand_distance_km': 3.0,
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'locality': 'Kharadi',
                'city': 'Pune',
                'state': 'Maharashtra',
                'pincode': '411014',
                'area': 'Mid-Range',
                'metro_available': False,
                'airport_distance_km': 20.0,
                'railway_station_distance_km': 8.5,
                'bus_stand_distance_km': 2.8,
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'locality': 'Magarpatta City',
                'city': 'Pune',
                'state': 'Maharashtra',
                'pincode': '411028',
                'area': 'Premium',
                'metro_available': False,
                'airport_distance_km': 18.0,
                'railway_station_distance_km': 7.5,
                'bus_stand_distance_km': 2.0,
                'created_at': current_time,
                'updated_at': current_time
            }
        ]
        
        for loc_data in locations_data:
            insert_sql = """
            INSERT INTO locations (id, locality, city, state, pincode, area, metro_available, 
                                 airport_distance_km, railway_station_distance_km, bus_stand_distance_km, 
                                 created_at, updated_at)
            VALUES (:id, :locality, :city, :state, :pincode, :area, :metro_available,
                   :airport_distance_km, :railway_station_distance_km, :bus_stand_distance_km,
                   :created_at, :updated_at)
            """
            db.execute(text(insert_sql), loc_data)
        
        db.commit()
        print(f"✅ Successfully populated locations table with {len(locations_data)} locations!")
        
        # Show the inserted data by city
        result = db.execute(text("SELECT city, locality, area FROM locations ORDER BY city, area"))
        print("\n📋 Inserted locations:")
        current_city = None
        for row in result:
            if current_city != row[0]:
                current_city = row[0]
                print(f"\n🏙️ {current_city}:")
            print(f"  - {row[1]} ({row[2]})")
            
    except Exception as e:
        print(f"❌ Error populating locations table: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    populate_locations()
