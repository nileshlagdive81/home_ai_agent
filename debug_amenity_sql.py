#!/usr/bin/env python3
"""
Script to debug the amenity filter SQL generation step by step
"""

from backend.database import get_db
from sqlalchemy import text

def debug_amenity_sql():
    """Debug the amenity filter SQL generation step by step"""
    print("🔍 DEBUGGING AMENITY FILTER SQL GENERATION")
    print("=" * 60)
    
    db = next(get_db())
    
    try:
        # Simulate the exact same logic from the backend
        print("1️⃣ SIMULATING BACKEND LOGIC")
        
        # Start building the WHERE conditions (same as backend)
        where_conditions = []
        query_params = {}
        
        # Apply location filter (same as backend)
        location = "pune"
        where_conditions.append("(l.city ILIKE :location OR l.locality ILIKE :location)")
        query_params["location"] = f"%{location}%"
        print(f"   ✅ Location filter: {location}")
        
        # Apply BHK filter (same as backend)
        bhk = 2.0
        bhk_operator = "="
        where_conditions.append(f"pr.bhk_count {bhk_operator} :bhk")
        query_params["bhk"] = bhk
        print(f"   ✅ BHK filter: {bhk_operator} {bhk}")
        
        # Apply property type filter (same as backend)
        prop_type = "apartment"
        where_conditions.append("pr.property_type ILIKE :property_type")
        query_params["property_type"] = f"%{prop_type}%"
        print(f"   ✅ Property type filter: {prop_type}")
        
        # Apply price filter (same as backend)
        price_value = 15000000.0
        where_conditions.append(f"pr.sell_price < :price_value")
        query_params["price_value"] = price_value
        print(f"   ✅ Price filter: < ₹{price_value:,}")
        
        # Apply amenity filter (same as backend)
        amenity_name = "gym"
        print(f"   ✅ Amenity filter: {amenity_name}")
        
        # Use the EXACT same approach as the backend
        where_conditions.append("""
            EXISTS (
                SELECT 1 FROM project_amenities pa
                JOIN amenities a ON pa.amenity_id = a.id
                WHERE pa.project_id = p.id AND a.name ILIKE :amenity_name
            )
        """)
        query_params["amenity_name"] = f"%{amenity_name}%"
        
        print(f"\n2️⃣ WHERE CONDITIONS BUILT:")
        print(f"   📊 Total conditions: {len(where_conditions)}")
        for i, condition in enumerate(where_conditions, 1):
            print(f"   {i}. {condition.strip()}")
        
        print(f"\n3️⃣ QUERY PARAMETERS:")
        for key, value in query_params.items():
            print(f"   {key}: {value}")
        
        # Build the complete SQL query (same as backend)
        where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
        
        sql_query = f"""
            SELECT pr.id, pr.bhk_count, pr.carpet_area_sqft, pr.sell_price, pr.floor_number,
                   pr.property_type, pr.facing, pr.status,
                   p.id as project_id, p.name as project_name, p.developer_id, p.project_status,
                   p.total_units, p.total_floors, p.possession_date, p.rera_number, p.description, p.project_type,
                   l.city, l.locality
            FROM properties pr
            JOIN projects p ON pr.project_id = p.id
            JOIN project_locations pl ON p.id = pl.project_id
            JOIN locations l ON pl.location_id = l.id
            WHERE {where_clause}
            ORDER BY pr.sell_price
            LIMIT 20
        """
        
        print(f"\n4️⃣ FINAL SQL QUERY:")
        print("-" * 50)
        print(sql_query)
        print("-" * 50)
        
        print(f"\n5️⃣ EXECUTING SQL QUERY...")
        try:
            query_results = db.execute(text(sql_query), query_params).fetchall()
            print(f"   ✅ SQL execution successful!")
            print(f"   📊 Results found: {len(query_results)}")
            
            if query_results:
                print(f"\n6️⃣ SAMPLE RESULTS:")
                for i, row in enumerate(query_results[:3], 1):
                    project_name = row[9]  # p.name
                    locality = row[19]      # l.locality
                    city = row[18]          # l.city
                    price = row[3]          # pr.sell_price
                    bhk = row[1]            # pr.bhk_count
                    
                    price_lakhs = price / 100000 if price else 0
                    print(f"   {i}. {project_name} | {locality} ({city}) | {bhk} BHK | ₹{price_lakhs:.1f}L")
            else:
                print(f"   ❌ No results found!")
                
                # Let's debug why no results
                print(f"\n7️⃣ DEBUGGING NO RESULTS:")
                
                # Test without amenity filter
                print(f"   🔍 Testing WITHOUT amenity filter...")
                where_conditions_no_amenity = where_conditions[:-1]  # Remove amenity filter
                where_clause_no_amenity = " AND ".join(where_conditions_no_amenity)
                
                sql_query_no_amenity = f"""
                    SELECT pr.id, pr.bhk_count, pr.carpet_area_sqft, pr.sell_price, pr.floor_number,
                           pr.property_type, pr.facing, pr.status,
                           p.id as project_id, p.name as project_name, p.developer_id, p.project_status,
                           p.total_units, p.total_floors, p.possession_date, p.rera_number, p.description, p.project_type,
                           l.city, l.locality
                    FROM properties pr
                    JOIN projects p ON pr.project_id = p.id
                    JOIN project_locations pl ON p.id = pl.project_id
                    JOIN locations l ON pl.location_id = l.id
                    WHERE {where_clause_no_amenity}
                    ORDER BY pr.sell_price
                    LIMIT 20
                """
                
                # Remove amenity parameter
                params_no_amenity = {k: v for k, v in query_params.items() if k != "amenity_name"}
                
                print(f"   🔍 SQL without amenity filter:")
                print(f"   {sql_query_no_amenity}")
                
                result_no_amenity = db.execute(text(sql_query_no_amenity), params_no_amenity).fetchall()
                print(f"   📊 Results without amenity filter: {len(result_no_amenity)}")
                
                if result_no_amenity:
                    print(f"   ✅ Found properties without amenity filter!")
                    print(f"   🔍 This means the amenity filter is the problem!")
                else:
                    print(f"   ❌ Still no results even without amenity filter!")
                    print(f"   🔍 The problem is in the basic query structure!")
                
        except Exception as e:
            print(f"   ❌ SQL execution failed: {e}")
            print(f"   🔍 Error type: {type(e).__name__}")
            
    except Exception as e:
        print(f"❌ Error in debugging: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    debug_amenity_sql()
