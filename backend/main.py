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
from backend.database import get_db, create_tables
from backend.services.nlp_engine import RealEstateNLPEngine
from backend.models import *

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
        
        # Build database query based on extracted criteria
        db_query = db.query(Property, Project, Location).join(Project).join(ProjectLocation).join(Location)
        
        # Apply filters based on extracted entities
        if "location" in search_criteria["filters"]:
            location = search_criteria["filters"]["location"]
            # Search in cities and localities
            db_query = db_query.filter(
                (Location.city.ilike(f"%{location}%")) | 
                (Location.locality.ilike(f"%{location}%"))
            )
            print(f"✅ Applied location filter: {location}")
        
        if "bhk" in search_criteria["filters"]:
            bhk = search_criteria["filters"]["bhk"]
            bhk_operator = search_criteria["filters"].get("bhk_operator", "=")
            
            # Apply BHK filter with operator
            if bhk_operator == "=":
                db_query = db_query.filter(Property.bhk_count == bhk)
            elif bhk_operator == ">":
                db_query = db_query.filter(Property.bhk_count > bhk)
            elif bhk_operator == "<":
                db_query = db_query.filter(Property.bhk_count < bhk)
            elif bhk_operator == ">=":
                db_query = db_query.filter(Property.bhk_count >= bhk)
            elif bhk_operator == "<=":
                db_query = db_query.filter(Property.bhk_count <= bhk)
            
            print(f"✅ Applied BHK filter: {bhk_operator} {bhk}")
        
        if "property_type" in search_criteria["filters"]:
            prop_type = search_criteria["filters"]["property_type"]
            db_query = db_query.filter(Property.property_type.ilike(f"%{prop_type}%"))
            print(f"✅ Applied property type filter: {prop_type}")
        
        # Apply price filters from NLP extraction with operators
        if "price_range" in search_criteria["filters"]:
            price_operator = search_criteria["filters"].get("price_operator", "=")
            price_value = search_criteria["filters"].get("price_value")
            
            if price_value is not None:
                # Apply price filter using the sell_price column from properties table
                if price_operator == "<":
                    db_query = db_query.filter(Property.sell_price < price_value)
                    print(f"✅ Applied price filter: < ₹{price_value:,} (using sell_price column)")
                elif price_operator == ">":
                    db_query = db_query.filter(Property.sell_price > price_value)
                    print(f"✅ Applied price filter: > ₹{price_value:,} (using sell_price column)")
                elif price_operator == "<=":
                    db_query = db_query.filter(Property.sell_price <= price_value)
                    print(f"✅ Applied price filter: <= ₹{price_value:,} (using sell_price column)")
                elif price_operator == ">=":
                    db_query = db_query.filter(Property.sell_price >= price_value)
                    print(f"✅ Applied price filter: >= ₹{price_value:,} (using sell_price column)")
                elif price_operator == "=":
                    db_query = db_query.filter(Property.sell_price == price_value)
                    print(f"✅ Applied price filter: = ₹{price_value:,} (using sell_price column)")
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
                    
                    db_query = db_query.filter(Property.sell_price < max_price)
                    print(f"✅ Applied price filter: under ₹{max_price:,} (using sell_price column)")
                
                # Pattern for "above X crore/lakhs"
                above_match = re.search(r'above\s+(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)', price_text)
                if above_match:
                    min_price = float(above_match.group(1))
                    if 'lakh' in price_text:
                        min_price = min_price * 100000  # Convert lakhs to rupees
                    elif 'crore' in price_text or 'cr' in price_text:
                        min_price = min_price * 10000000  # Convert crores to rupees
                    
                    db_query = db_query.filter(Property.sell_price > min_price)
                    print(f"✅ Applied price filter: above ₹{min_price:,} (using sell_price column)")
                
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
                    
                    db_query = db_query.filter(
                        Property.sell_price >= min_price,
                        Property.sell_price <= max_price
                    )
                    print(f"✅ Applied price filter: ₹{min_price:,} - ₹{max_price:,} (using sell_price column)")
                
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
                    
                    db_query = db_query.filter(
                        Property.sell_price >= min_price,
                        Property.sell_price <= max_price
                    )
                    print(f"✅ Applied price filter: between ₹{min_price:,} - ₹{max_price:,} (using sell_price column)")
        
        # Apply carpet area filters with operators
        if "carpet_area" in search_criteria["filters"]:
            area_operator = search_criteria["filters"].get("area_operator", "=")
            area_value = search_criteria["filters"].get("area_value")
            
            if area_value is not None:
                # Apply carpet area filter
                if area_operator == "<":
                    db_query = db_query.filter(Property.carpet_area_sqft < area_value)
                    print(f"✅ Applied carpet area filter: < {area_value} sqft")
                elif area_operator == ">":
                    db_query = db_query.filter(Property.carpet_area_sqft > area_value)
                    print(f"✅ Applied carpet area filter: > {area_value} sqft")
                elif area_operator == "<=":
                    db_query = db_query.filter(Property.carpet_area_sqft <= area_value)
                    print(f"✅ Applied carpet area filter: <= {area_value} sqft")
                elif area_operator == ">=":
                    db_query = db_query.filter(Property.carpet_area_sqft >= area_value)
                    print(f"✅ Applied carpet area filter: >= {area_value} sqft")
                elif area_operator == "=":
                    db_query = db_query.filter(Property.carpet_area_sqft == area_value)
                    print(f"✅ Applied carpet area filter: = {area_value} sqft")
        
        # Execute the query
        query_results = db_query.limit(20).all()
        
        # Update search results count (temporarily disabled)
        # search_query.search_results_count = len(query_results)
        # db.commit()
        
        # Format results
        results = []
        for property_item, project, location in query_results:
            project_data = {
                "id": str(property_item.id),
                "bhk_count": float(property_item.bhk_count) if property_item.bhk_count else None,
                "carpet_area_sqft": float(property_item.carpet_area_sqft) if property_item.carpet_area_sqft else None,
                "sell_price": float(property_item.sell_price) if property_item.sell_price else None,
                "floor_number": property_item.floor_number,
                "property_type": property_item.property_type,
                "facing": property_item.facing,
                "status": property_item.status,
                "project": {
                    "id": str(project.id),
                    "name": project.name,
                    "developer_id": str(project.developer_id) if project.developer_id else None,
                    "project_status": project.project_status,
                    "total_units": project.total_units,
                    "total_floors": project.total_floors,
                    "possession_date": str(project.possession_date) if project.possession_date else None,
                    "rera_number": project.rera_number,
                    "description": project.description,
                    "project_type": project.project_type
                } if project else None,
                "location": {
                    "city": location.city if location else None,
                    "locality": location.locality if location else None
                } if location else None
            }
            results.append(project_data)
        
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
