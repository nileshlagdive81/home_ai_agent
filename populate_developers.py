#!/usr/bin/env python3
"""
Script to populate the developers table with realistic data
"""

from backend.database import get_db
from sqlalchemy import text
import uuid
from datetime import datetime

def populate_developers():
    """Populate developers table with realistic data"""
    print("🏗️ Populating developers table...")
    db = next(get_db())
    current_time = datetime.now()
    
    try:
        # Insert realistic developer data
        developers_data = [
            {
                'id': str(uuid.uuid4()),
                'name': 'Lodha Group',
                'company_name': 'Lodha Group',
                'experience_years': 35,
                'completed_projects': 150,
                'turnover': 15000.00,
                'contact_number': '+91-22-6656-6000',
                'email': 'info@lodhagroup.com',
                'office_address': 'Lodha Excelus, Apollo Bunder, Mumbai, Maharashtra 400001',
                'reputation_rating': 4.8,
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Godrej Properties',
                'company_name': 'Godrej Properties Limited',
                'experience_years': 25,
                'completed_projects': 120,
                'turnover': 12000.00,
                'contact_number': '+91-22-6796-0000',
                'email': 'connect@godrejproperties.com',
                'office_address': 'Godrej One, Pirojshanagar, Vikhroli, Mumbai, Maharashtra 400079',
                'reputation_rating': 4.7,
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Kolte Patil Developers',
                'company_name': 'Kolte Patil Developers Limited',
                'experience_years': 30,
                'completed_projects': 80,
                'turnover': 8000.00,
                'contact_number': '+91-20-6601-8000',
                'email': 'info@koltepatil.com',
                'office_address': 'Kolte Patil House, 1st Floor, 1-7-62/1, Shivaji Nagar, Pune, Maharashtra 411005',
                'reputation_rating': 4.6,
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'K Raheja Corp',
                'company_name': 'K Raheja Corp',
                'experience_years': 40,
                'completed_projects': 200,
                'turnover': 20000.00,
                'contact_number': '+91-22-6656-7000',
                'email': 'info@kraheja.com',
                'office_address': 'Raheja Centre, Free Press Journal Marg, Nariman Point, Mumbai, Maharashtra 400021',
                'reputation_rating': 4.9,
                'created_at': current_time,
                'updated_at': current_time
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Prestige Group',
                'company_name': 'Prestige Group',
                'experience_years': 35,
                'completed_projects': 180,
                'turnover': 18000.00,
                'contact_number': '+91-80-4179-9999',
                'email': 'info@prestigegroup.com',
                'office_address': 'Prestige Centre Point, 7, Cunningham Road, Bengaluru, Karnataka 560052',
                'reputation_rating': 4.7,
                'created_at': current_time,
                'updated_at': current_time
            }
        ]
        
        for dev_data in developers_data:
            insert_sql = """
            INSERT INTO developers (id, name, company_name, experience_years, completed_projects, 
                                 turnover, contact_number, email, office_address, reputation_rating, 
                                 created_at, updated_at)
            VALUES (:id, :name, :company_name, :experience_years, :completed_projects,
                   :turnover, :contact_number, :email, :office_address, :reputation_rating,
                   :created_at, :updated_at)
            """
            db.execute(text(insert_sql), dev_data)
        
        db.commit()
        print(f"✅ Successfully populated developers table with {len(developers_data)} developers!")
        
        # Show the inserted data
        result = db.execute(text("SELECT id, name, company_name, experience_years FROM developers"))
        print("\n📋 Inserted developers:")
        for row in result:
            print(f"  - {row[1]} ({row[2]}) - {row[3]} years experience")
            
    except Exception as e:
        print(f"❌ Error populating developers table: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    populate_developers()
