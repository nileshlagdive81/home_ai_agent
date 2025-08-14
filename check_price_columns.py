#!/usr/bin/env python3
"""
Check price-related columns in the properties table
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database import get_db
from sqlalchemy import text

def check_price_columns():
    """Check all price-related columns in the properties table"""
    
    try:
        db = next(get_db())
        
        print("💰 Checking price-related columns in properties table...")
        print("=" * 60)
        
        # Get all columns from properties table
        columns_result = db.execute(text("SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'properties' ORDER BY ordinal_position"))
        
        price_columns = []
        all_columns = []
        
        for row in columns_result:
            column_name = row[0]
            data_type = row[1]
            nullable = row[2]
            
            all_columns.append(f"  - {column_name}: {data_type} ({nullable})")
            
            # Check if column is price-related
            if any(price_word in column_name.lower() for price_word in ['price', 'cost', 'amount', 'value', 'sell', 'buy', 'rent']):
                price_columns.append(f"  💰 {column_name}: {data_type} ({nullable})")
        
        print("📋 All columns in properties table:")
        print("-" * 40)
        for col in all_columns:
            print(col)
        
        print("\n💰 Price-related columns:")
        print("-" * 30)
        if price_columns:
            for col in price_columns:
                print(col)
        else:
            print("  No price-related columns found")
        
        # Check if there are any sample records
        print("\n📊 Sample data check:")
        print("-" * 25)
        try:
            sample_result = db.execute(text("SELECT COUNT(*) as total FROM properties"))
            total_count = sample_result.fetchone()[0]
            print(f"  Total properties: {total_count}")
            
            if total_count > 0:
                # Show a few sample records
                sample_data = db.execute(text("SELECT id, property_type, bhk_count, sell_price, status FROM properties LIMIT 3"))
                print("  Sample records:")
                for row in sample_data:
                    print(f"    - ID: {row[0][:8]}..., Type: {row[1]}, BHK: {row[2]}, Price: ₹{row[3]:,}, Status: {row[4]}")
            else:
                print("  No properties found in database")
                
        except Exception as e:
            print(f"  Error checking sample data: {e}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_price_columns()
