from fastapi import FastAPI, HTTPException, Depends, Query, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
import uvicorn
import os
import re
from dotenv import load_dotenv
from sqlalchemy.orm import Session

# Import our modules
from database import get_db, create_tables
from services.nlp_engine import RealEstateNLPEngine
from models import *

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Real Estate NLP API",
    description="AI-powered real estate search and booking system with natural language processing",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize NLP engine
nlp_engine = RealEstateNLPEngine()

@app.on_event("startup")
async def startup_event():
    """Initialize database and create tables on startup"""
    try:
        create_tables()
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Real Estate NLP API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "nlp_engine": "loaded"}

@app.post("/api/v1/search/nlp")
async def nlp_search(
    query: str = Form(..., description="Natural language search query"),
    db: Session = Depends(get_db)
):
    """
    Natural language search endpoint
    Processes natural language queries and returns relevant properties
    """
    try:
        # Process the query with NLP engine
        nlp_result = nlp_engine.process_query(query)
        
        # Get search criteria
        search_criteria = nlp_engine.get_search_criteria(query)
        
        # Log the search query for training (temporarily disabled)
        # search_query = SearchQuery(
        #     query_text=query,
        #     detected_intent=nlp_result.intent,
        #     extracted_entities=search_criteria["filters"],
        #     search_results_count=0  # Will be updated after search
        # )
        # db.add(search_query)
        # db.commit()
        
        # Build the complete SQL query using raw SQL for better control
        from sqlalchemy import text
        
        # Start building the WHERE conditions
        where_conditions = []
        query_params = {}
        
        # Apply location filter
        if "city" in search_criteria["filters"]:
            # City takes precedence over general location
            city = search_criteria["filters"]["city"]
            where_conditions.append("l.city ILIKE :city")
            query_params["city"] = f"%{city}%"
            print(f"✅ Applied city filter: {city}")
        elif "location" in search_criteria["filters"]:
            location = search_criteria["filters"]["location"]
            where_conditions.append("(l.city ILIKE :location OR l.locality ILIKE :location)")
            query_params["location"] = f"%{location}%"
            print(f"✅ Applied location filter: {location}")
        
        # Apply BHK filter
        if "bhk" in search_criteria["filters"]:
            bhk = search_criteria["filters"]["bhk"]
            bhk_operator = search_criteria["filters"].get("bhk_operator", "=")
            where_conditions.append(f"pr.bhk_count {bhk_operator} :bhk")
            query_params["bhk"] = bhk
            print(f"✅ Applied BHK filter: {bhk_operator} {bhk}")
        
        # Apply property type filter
        if "property_type" in search_criteria["filters"]:
            prop_type = search_criteria["filters"]["property_type"]
            where_conditions.append("pr.property_type ILIKE :property_type")
            query_params["property_type"] = f"%{prop_type}%"
            print(f"✅ Applied property type filter: {prop_type}")
        
        # Apply price filter
        if "price_range" in search_criteria["filters"]:
            price_operator = search_criteria["filters"].get("price_operator", "=")
            price_value = search_criteria["filters"].get("price_value")
            
            if price_value is not None:
                where_conditions.append(f"pr.sell_price {price_operator} :price_value")
                query_params["price_value"] = price_value
                print(f"✅ Applied price filter: {price_operator} ₹{price_value:,}")
            else:
                # Fallback to old pattern matching for backward compatibility
                price_text = search_criteria["filters"]["price_range"].lower()
                
                # Pattern for "under X crore/lakhs"
                under_match = re.search(r'under\s+(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)', price_text)
                if under_match:
                    max_price = float(under_match.group(1))
                    if 'lakh' in price_text:
                        max_price = max_price * 100000  # Convert lakhs to rupees
                    elif 'crore' in price_text or 'cr' in price_text:
                        max_price = max_price * 10000000  # Convert crores to rupees
                    
                    where_conditions.append("pr.sell_price < :max_price")
                    query_params["max_price"] = max_price
                    print(f"✅ Applied price filter: under ₹{max_price:,}")
                
                # Pattern for "above X crore/lakhs"
                above_match = re.search(r'above\s+(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)', price_text)
                if above_match:
                    min_price = float(above_match.group(1))
                    if 'lakh' in price_text:
                        min_price = min_price * 100000  # Convert lakhs to rupees
                    elif 'crore' in price_text or 'cr' in price_text:
                        min_price = min_price * 10000000  # Convert crores to rupees
                    
                    where_conditions.append("pr.sell_price > :min_price")
                    query_params["min_price"] = min_price
                    print(f"✅ Applied price filter: above ₹{min_price:,}")
                
                # Pattern for range "X-Y crore/lakhs"
                range_match = re.search(r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)', price_text)
                if range_match:
                    min_price = float(range_match.group(1))
                    max_price = float(range_match.group(2))
                    if 'lakh' in price_text:
                        min_price = min_price * 100000
                        max_price = max_price * 100000
                    elif 'crore' in price_text or 'cr' in price_text:
                        min_price = min_price * 10000000
                        max_price = max_price * 10000000
                    
                    where_conditions.append("pr.sell_price >= :min_price AND pr.sell_price <= :max_price")
                    query_params["min_price"] = min_price
                    query_params["max_price"] = max_price
                    print(f"✅ Applied price filter: ₹{min_price:,} - ₹{max_price:,}")
                
                # Pattern for "between X to Y crore/lakhs"
                between_match = re.search(r'between\s+(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|crore|crores)\s*to\s*(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|crore|crores)', price_text)
                if between_match:
                    min_price = float(between_match.group(1))
                    max_price = float(between_match.group(2))
                    if 'lakh' in price_text:
                        min_price = min_price * 100000
                        max_price = max_price * 100000
                    elif 'crore' in price_text or 'cr' in price_text:
                        min_price = min_price * 10000000
                        max_price = max_price * 10000000
                    
                    where_conditions.append("pr.sell_price >= :min_price AND pr.sell_price <= :max_price")
                    query_params["min_price"] = min_price
                    query_params["max_price"] = max_price
                    print(f"✅ Applied price filter: between ₹{min_price:,} - ₹{max_price:,}")
        
        # Apply carpet area filter
        if "carpet_area" in search_criteria["filters"]:
            area_operator = search_criteria["filters"].get("area_operator", "=")
            area_value = search_criteria["filters"].get("area_value")
            
            if area_value is not None:
                where_conditions.append(f"pr.carpet_area_sqft {area_operator} :area_value")
                query_params["area_value"] = area_value
                print(f"✅ Applied carpet area filter: {area_operator} {area_value} sqft")
        
        # Apply amenity filter
        amenity_name = None
        if "amenity" in search_criteria["filters"]:
            amenity_name = search_criteria["filters"]["amenity"]
        elif "amenities" in search_criteria["filters"] and search_criteria["filters"]["amenities"]:
            # Handle case where NLP engine returns amenities as a list
            amenity_name = search_criteria["filters"]["amenities"][0]  # Take first amenity
        
        # Apply nearby place filter (NEW ADDITION)
        nearby_place_filter = None
        if "nearby_place" in search_criteria["filters"]:
            nearby_place_filter = {
                "place_type": search_criteria["filters"]["nearby_place"],
                "distance": search_criteria["filters"]["nearby_distance"],
                "operator": search_criteria["filters"]["nearby_operator"]
            }
            print(f"✅ Applied nearby place filter: {nearby_place_filter['place_type']} {nearby_place_filter['operator']} {nearby_place_filter['distance']}km")
        
        # Build the WHERE clause for non-amenity filters
        where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
        
        # Build the complete SQL query with conditional JOIN for amenities and nearby places
        if amenity_name and nearby_place_filter:
            print(f"✅ Applying both amenity and nearby place filters")
            # Use direct JOIN with DISTINCT and nearby places
            sql_query = f"""
                SELECT DISTINCT ON (pr.id) pr.id, pr.bhk_count, pr.carpet_area_sqft, pr.sell_price, pr.floor_number,
                       pr.property_type, pr.facing, pr.status,
                       p.id as project_id, p.name as project_name, p.developer_id, p.project_status,
                       p.total_units, p.total_floors, p.possession_date, p.rera_number, p.description, p.project_type,
                       l.city, l.locality
                FROM properties pr
                JOIN projects p ON pr.project_id = p.id
                JOIN project_locations pl ON p.id = pl.project_id
                JOIN locations l ON pl.location_id = l.id
                JOIN project_amenities pa ON p.id = pa.project_id
                JOIN amenities a ON pa.amenity_id = a.id
                JOIN nearby_places np ON p.id = np.project_id
                WHERE a.name ILIKE :amenity_name
                AND np.place_type = :nearby_place_type
                AND np.distance_km {nearby_place_filter['operator']} :nearby_distance
                AND {where_clause}
                ORDER BY pr.id, pr.sell_price
                LIMIT 20
            """
            query_params["amenity_name"] = f"%{amenity_name}%"
            query_params["nearby_place_type"] = nearby_place_filter["place_type"]
            query_params["nearby_distance"] = nearby_place_filter["distance"]
            print(f"✅ Applied amenity + nearby place filters")
        elif amenity_name:
            print(f"✅ Applying amenity filter: {amenity_name}")
            # Use direct JOIN with DISTINCT to avoid duplicate properties
            sql_query = f"""
                SELECT DISTINCT ON (pr.id) pr.id, pr.bhk_count, pr.carpet_area_sqft, pr.sell_price, pr.floor_number,
                       pr.property_type, pr.facing, pr.status,
                       p.id as project_id, p.name as project_name, p.developer_id, p.project_status,
                       p.total_units, p.total_floors, p.possession_date, p.rera_number, p.description, p.project_type,
                       l.city, l.locality
                FROM properties pr
                JOIN projects p ON pr.project_id = p.id
                JOIN project_locations pl ON p.id = pl.project_id
                JOIN locations l ON pl.location_id = l.id
                JOIN project_amenities pa ON p.id = pa.project_id
                JOIN amenities a ON pa.amenity_id = a.id
                WHERE a.name ILIKE :amenity_name
                AND {where_clause}
                ORDER BY pr.id, pr.sell_price
                LIMIT 20
            """
            query_params["amenity_name"] = f"%{amenity_name}%"
            print(f"✅ Applied amenity filter with direct JOIN: {amenity_name}")
        elif nearby_place_filter:
            print(f"✅ Applying nearby place filter only")
            # Use nearby places filter without amenities
            sql_query = f"""
                SELECT DISTINCT ON (pr.id) pr.id, pr.bhk_count, pr.carpet_area_sqft, pr.sell_price, pr.floor_number,
                       pr.property_type, pr.facing, pr.status,
                       p.id as project_id, p.name as project_name, p.developer_id, p.project_status,
                       p.total_units, p.total_floors, p.possession_date, p.rera_number, p.description, p.project_type,
                       l.city, l.locality
                FROM properties pr
                JOIN projects p ON pr.project_id = p.id
                JOIN project_locations pl ON p.id = pl.project_id
                JOIN locations l ON pl.location_id = l.id
                JOIN nearby_places np ON p.id = np.project_id
                WHERE np.place_type = :nearby_place_type
                AND np.distance_km {nearby_place_filter['operator']} :nearby_distance
                AND {where_clause}
                ORDER BY pr.id, pr.sell_price
                LIMIT 20
            """
            query_params["nearby_place_type"] = nearby_place_filter["place_type"]
            query_params["nearby_distance"] = nearby_place_filter["distance"]
            print(f"✅ Applied nearby place filter only")
        else:
            # No amenity or nearby place filter - use simpler query
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
        
        # DETAILED LOGGING - Let's see exactly what's happening
        print("\n" + "="*80)
        print("🔍 DETAILED SQL DEBUGGING")
        print("="*80)
        print(f"📊 Total filters applied: {len(where_conditions)}")
        print(f"🔍 Where conditions array: {where_conditions}")
        print(f"🔍 Where clause (joined): {where_clause}")
        print(f"🔍 Query parameters: {query_params}")
        print(f"🔍 Parameter count: {len(query_params)}")
        print("\n🔍 COMPLETE SQL QUERY:")
        print("-" * 40)
        print(sql_query)
        print("-" * 40)
        
        try:
            # Execute the raw SQL query
            print(f"\n🚀 Executing SQL query...")
            query_results = db.execute(text(sql_query), query_params).fetchall()
            print(f"✅ SQL execution successful! Found {len(query_results)} results")
            
        except Exception as e:
            print(f"❌ SQL execution failed with error: {e}")
            print(f"❌ Error type: {type(e).__name__}")
            print(f"❌ Full error details: {str(e)}")
            # Return empty results if SQL fails
            query_results = []
        
        print("="*80)
        
        # Update search results count (temporarily disabled)
        # search_query.search_results_count = len(query_results)
        # db.commit()
        
        # Format results from raw SQL
        results = []
        for row in query_results:
            project_data = {
                "id": str(row[0]),  # pr.id
                "bhk_count": float(row[1]) if row[1] else None,  # pr.bhk_count
                "carpet_area_sqft": float(row[2]) if row[2] else None,  # pr.carpet_area_sqft
                "sell_price": float(row[3]) if row[3] else None,  # pr.sell_price
                "floor_number": row[4],  # pr.floor_number
                "property_type": row[5],  # pr.property_type
                "facing": row[6],  # pr.facing
                "status": row[7],  # pr.status
                "project": {
                    "id": str(row[8]),  # p.id
                    "name": row[9],  # p.name
                    "developer_id": str(row[10]) if row[10] else None,  # p.developer_id
                    "project_status": row[11],  # p.project_status
                    "total_units": row[12],  # p.total_units
                    "total_floors": row[13],  # p.total_floors
                    "possession_date": str(row[14]) if row[14] else None,  # p.possession_date
                    "rera_number": row[15],  # p.rera_number
                    "description": row[16],  # p.description
                    "project_type": row[17]  # p.project_type
                },
                "location": {
                    "city": row[18],  # l.city
                    "locality": row[19]  # l.locality
                }
            }
            results.append(project_data)
        
        # Final logging
        print(f"\n📊 FINAL RESULTS:")
        print(f"   - Raw SQL results: {len(query_results)} rows")
        print(f"   - Formatted results: {len(results)} properties")
        print(f"   - Results being returned: {len(results)}")
        print("="*80)
        
        return {
            "query": query,
            "intent": nlp_result.intent,
            "confidence": nlp_result.confidence,
            "extracted_entities": search_criteria["filters"],
            "results_count": len(results),
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@app.get("/api/v1/search/suggestions")
async def get_search_suggestions(
    partial_query: str = Query(..., description="Partial search query")
):
    """Get search suggestions based on partial query"""
    try:
        suggestions = nlp_engine.get_suggestions(partial_query)
        return {
            "query": partial_query,
            "suggestions": suggestions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting suggestions: {str(e)}")

@app.get("/api/v1/properties")
async def get_properties(
    city: Optional[str] = Query(None, description="Filter by city"),
    locality: Optional[str] = Query(None, description="Filter by locality"),
    bhk: Optional[int] = Query(None, description="Filter by BHK"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    project_status: Optional[str] = Query(None, description="Filter by project status"),
    limit: int = Query(20, description="Number of results to return"),
    offset: int = Query(0, description="Number of results to skip"),
    db: Session = Depends(get_db)
):
    """Get properties with filters"""
    try:
        query = db.query(Project).filter(Project.is_active == True)
        
        # Apply filters
        if city:
            query = query.join(Locality).join(City).filter(City.name.ilike(f"%{city}%"))
        
        if locality:
            query = query.join(Locality).filter(Locality.name.ilike(f"%{locality}%"))
        
        if bhk:
            query = query.join(PropertyUnit).filter(PropertyUnit.bhk == bhk)
        
        if project_status:
            query = query.filter(Project.project_status == project_status)
        
        # Apply price filters
        if min_price or max_price:
            query = query.join(PropertyUnit)
            if min_price:
                query = query.filter(PropertyUnit.total_price >= min_price)
            if max_price:
                query = query.filter(PropertyUnit.total_price <= max_price)
        
        # Get total count
        total_count = query.count()
        
        # Apply pagination
        projects = query.offset(offset).limit(limit).all()
        
        # Format results
        results = []
        for project in projects:
            project_data = {
                "id": project.id,
                "name": project.name,
                "developer_name": project.developer_name,
                "project_status": project.project_status,
                "total_units": project.total_units,
                "total_floors": project.total_floors,
                "possession_date": str(project.possession_date) if project.possession_date else None,
                "rera_number": project.rera_number,
                "description": project.description,
                "highlights": project.highlights,
                "locality": {
                    "name": project.locality.name,
                    "city": project.locality.city.name,
                    "state": project.locality.city.state
                } if project.locality else None,
                "property_type": project.property_type.name if project.property_type else None
            }
            results.append(project_data)
        
        return {
            "total_count": total_count,
            "limit": limit,
            "offset": offset,
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching properties: {str(e)}")

@app.get("/api/v1/cities")
async def get_cities(db: Session = Depends(get_db)):
    """Get all cities"""
    try:
        cities = db.query(City).filter(City.is_active == True).all()
        return [{"id": city.id, "name": city.name, "state": city.state} for city in cities]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching cities: {str(e)}")

@app.get("/api/v1/localities/{city_id}")
async def get_localities(city_id: int, db: Session = Depends(get_db)):
    """Get localities for a specific city"""
    try:
        localities = db.query(Locality).filter(
            Locality.city_id == city_id,
            Locality.is_active == True
        ).all()
        return [{"id": loc.id, "name": loc.name, "pincode": loc.pincode} for loc in localities]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching localities: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
