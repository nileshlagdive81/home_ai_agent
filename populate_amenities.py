#!/usr/bin/env python3
"""
Script to populate the amenities table with realistic amenities for residential properties
"""

from backend.database import get_db
from sqlalchemy import text
import uuid
from datetime import datetime

def populate_amenities():
    """Populate amenities table with realistic amenities"""
    print("🏗️ Populating amenities table...")
    db = next(get_db())
    current_time = datetime.now()
    
    try:
        # Insert realistic amenities data
        amenities_data = [
            # Basic Amenities
            {
                'id': str(uuid.uuid4()),
                'name': '24/7 Security',
                'category': 'Security',
                'description': 'Round the clock security with CCTV surveillance and security personnel',
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Power Backup',
                'category': 'Essential',
                'description': 'Uninterrupted power supply for common areas and elevators',
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Water Supply',
                'category': 'Essential',
                'description': '24/7 water supply with storage tanks',
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Lift Service',
                'category': 'Essential',
                'description': 'High-speed elevators with backup power',
                'created_at': current_time,
                'updated_at': current_time
            },
            
            # Recreational Amenities
            {
                'id': str(uuid.uuid4()),
                'name': 'Swimming Pool',
                'category': 'Recreation',
                'description': 'Olympic size swimming pool with changing rooms',
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Gymnasium',
                'category': 'Recreation',
                'description': 'Fully equipped gym with modern equipment and trainers',
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Children Play Area',
                'category': 'Recreation',
                'description': 'Safe and engaging play area for children',
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Garden',
                'category': 'Recreation',
                'description': 'Landscaped gardens with walking tracks',
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Party Hall',
                'category': 'Recreation',
                'description': 'Multi-purpose party hall for events and celebrations',
                'created_at': current_time,
                'updated_at': current_time
            },
            
            # Lifestyle Amenities
            {
                'id': str(uuid.uuid4()),
                'name': 'Clubhouse',
                'category': 'Lifestyle',
                'description': 'Exclusive clubhouse with indoor games and lounge area',
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Spa & Salon',
                'category': 'Lifestyle',
                'description': 'In-house spa and salon services',
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Restaurant',
                'category': 'Lifestyle',
                'description': 'Fine dining restaurant within the complex',
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Coffee Shop',
                'category': 'Lifestyle',
                'description': 'Casual coffee shop for residents',
                'created_at': current_time,
                'updated_at': current_time
            },
            
            # Convenience Amenities
            {
                'id': str(uuid.uuid4()),
                'name': 'Shopping Center',
                'category': 'Convenience',
                'description': 'Retail shops and convenience stores',
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'ATM',
                'category': 'Convenience',
                'description': 'ATM facility within the complex',
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Medical Center',
                'category': 'Convenience',
                'description': 'Basic medical facilities and pharmacy',
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Car Wash',
                'category': 'Convenience',
                'description': 'Automated car wash facility',
                'created_at': current_time,
                'updated_at': current_time
            },
            
            # Parking & Transport
            {
                'id': str(uuid.uuid4()),
                'name': 'Covered Parking',
                'category': 'Parking',
                'description': 'Covered parking spaces for residents',
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Visitor Parking',
                'category': 'Parking',
                'description': 'Dedicated parking for visitors',
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Shuttle Service',
                'category': 'Transport',
                'description': 'Regular shuttle service to nearby metro and bus stations',
                'created_at': current_time,
                'updated_at': current_time
            },
            
            # Technology Amenities
            {
                'id': str(uuid.uuid4()),
                'name': 'High-Speed Internet',
                'category': 'Technology',
                'description': 'Fiber optic internet connectivity',
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Smart Home Features',
                'category': 'Technology',
                'description': 'Smart lighting, security, and climate control',
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'App-Based Services',
                'category': 'Technology',
                'description': 'Mobile app for maintenance requests and payments',
                'created_at': current_time,
                'updated_at': current_time
            }
        ]
        
        for amenity_data in amenities_data:
            insert_sql = """
            INSERT INTO amenities (id, name, category, description, created_at, updated_at)
            VALUES (:id, :name, :category, :description, :created_at, :updated_at)
            """
            db.execute(text(insert_sql), amenity_data)
        
        db.commit()
        print(f"✅ Successfully populated amenities table with {len(amenities_data)} amenities!")
        
        # Show the inserted data by category
        result = db.execute(text("SELECT category, name FROM amenities ORDER BY category, name"))
        print("\n📋 Inserted amenities:")
        current_category = None
        for row in result:
            if current_category != row[0]:
                current_category = row[0]
                print(f"\n🏷️ {current_category}:")
            print(f"  - {row[1]}")
            
    except Exception as e:
        print(f"❌ Error populating amenities table: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    populate_amenities()
