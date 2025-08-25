from fastapi import FastAPI, HTTPException, Depends, Query, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
import uvicorn
import os
import re
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy import or_

# Import our modules
from database import get_db, create_tables
from services.nlp_engine import RealEstateNLPEngine
from services.knowledge_base import RealEstateKnowledgeBase
from models import Base, Amenity, ProjectAmenity, Project, ProjectLocation, Property, Location
from models.project import Project
from models.property import Property
from models.location import Location
from models.amenity import Amenity
from models.project_amenity import ProjectAmenity
from models.project_media import ProjectMedia
from models.room_specification import RoomSpecification
from models.project_construction_spec import ProjectConstructionSpec
from models.project_environmental_feature import ProjectEnvironmentalFeature
from models.project_expert_review import ProjectExpertReview
from models.project_safety_feature import ProjectSafetyFeature
from models.project_milestone import ProjectMilestone
from models.nearby_place import NearbyPlace
from models.room_specification import RoomSpecification

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

# Initialize NLP engine and knowledge base
nlp_engine = RealEstateNLPEngine()
knowledge_base = RealEstateKnowledgeBase()

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
        
        # Globally exclude sold properties (case-insensitive match on 'sold')
        from sqlalchemy import func
        db_query = db_query.filter(
            (Property.status.is_(None)) | (~func.lower(Property.status).like('%sold%'))
        )
        
        # Apply filters based on extracted entities
        if "location" in search_criteria["filters"]:
            location = search_criteria["filters"]["location"]
            # Search in cities and localities
            db_query = db_query.filter(
                (Location.city.ilike(f"%{location}%")) | 
                (Location.locality.ilike(f"%{location}%"))
            )
            print(f"✅ Applied location filter: {location}")
        
        # Apply project-level status filters inferred from query text
        try:
            from sqlalchemy import func
            qlower = (query or "").lower()
            project_status_filter_applied = False
            if "ready to move" in qlower or "ready-to-move" in qlower or "ready to occupy" in qlower:
                db_query = db_query.filter(func.lower(Project.project_status).like('%ready%move%'))
                project_status_filter_applied = True
                print("✅ Applied project status filter: Ready to move")
            elif "under construction" in qlower or "under-construction" in qlower or "uc" in qlower:
                db_query = db_query.filter(func.lower(Project.project_status).like('%under%construction%'))
                project_status_filter_applied = True
                print("✅ Applied project status filter: Under construction")
            elif "completed" in qlower or "ready" in qlower and "move" not in qlower:
                # Broad 'completed' catch; avoid double-catching ready-to-move which includes 'ready'
                db_query = db_query.filter(func.lower(Project.project_status).like('%completed%'))
                project_status_filter_applied = True
                print("✅ Applied project status filter: Completed")
            
            # Note: If needed, extend with more status phrases and mappings
            if not project_status_filter_applied:
                print("ℹ️  No explicit project status phrase detected in query")
        except Exception as _e:
            # Don't fail search if status parsing fails
            print(f"⚠️ Skipped project status filter due to error: {_e}")

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
            # Skip generic property type filters that are too broad
            generic_types = ['flat', 'apartment', 'house', 'property', 'residential']
            if prop_type.lower() in generic_types:
                print(f"⚠️ Skipped generic property_type filter '{prop_type}' (too broad, would exclude valid properties)")
            # Only apply property_type filter if it's not a BHK-related property_type
            # (since BHK is already handled by the bhk filter above)
            elif not any(bhk_term in prop_type.lower() for bhk_term in ['bhk', 'bedroom', 'bed']):
                db_query = db_query.filter(Property.property_type.ilike(f"%{prop_type}%"))
                print(f"✅ Applied property type filter: {prop_type}")
            else:
                print(f"⚠️ Skipped property_type filter '{prop_type}' as it's BHK-related (handled by BHK filter)")
        
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
                elif area_operator == "BETWEEN":
                    # Handle range queries like "1000-1500"
                    if isinstance(area_value, str) and "-" in str(area_value):
                        try:
                            min_area, max_area = map(int, str(area_value).split("-"))
                            db_query = db_query.filter(
                                Property.carpet_area_sqft >= min_area,
                                Property.carpet_area_sqft <= max_area
                            )
                            print(f"✅ Applied carpet area filter: BETWEEN {min_area} - {max_area} sqft")
                        except ValueError:
                            print(f"⚠️ Invalid area range format: {area_value}")
                    else:
                        # Fallback to equals if range parsing fails
                        db_query = db_query.filter(Property.carpet_area_sqft == area_value)
                        print(f"✅ Applied carpet area filter: = {area_value} sqft (fallback)")
        
        # Apply amenities filters
        if "amenities" in search_criteria["filters"]:
            amenities_list = search_criteria["filters"]["amenities"]
            if amenities_list:
                # Join with project_amenities and amenities tables to filter by amenities
                db_query = db_query.join(ProjectAmenity, Property.project_id == ProjectAmenity.project_id)
                db_query = db_query.join(Amenity, ProjectAmenity.amenity_id == Amenity.id)
                
                # Filter by amenities (case-insensitive)
                amenity_filters = []
                for amenity in amenities_list:
                    amenity_filters.append(Amenity.name.ilike(f"%{amenity}%"))
                
                if amenity_filters:
                    db_query = db_query.filter(or_(*amenity_filters))
                    print(f"✅ Applied amenities filter: {', '.join(amenities_list)}")
        
        # Apply nearby place filters
        nearby_place_info = None
        if "nearby_place" in search_criteria["filters"]:
            nearby_place_info = search_criteria["filters"]["nearby_place"]
        elif "nearby_place" in search_criteria:
            nearby_place_info = search_criteria["nearby_place"]
        
        if nearby_place_info:
            place_type = nearby_place_info.get("place_type")
            place_name = nearby_place_info.get("place_name")  # Get specific place name if available
            distance_km = nearby_place_info.get("distance_km")
            distance_operator = nearby_place_info.get("distance_operator", "<=")
            
            if place_type:
                # Join with nearby_places table to filter by nearby places
                db_query = db_query.join(NearbyPlace, Property.project_id == NearbyPlace.project_id)
                
                # Apply nearby place filter with specific name if available
                if place_name:
                    # Filter by specific place name (exact match or partial match)
                    if distance_km is not None:
                        # Apply both place type and name with distance
                        if distance_operator == "<=":
                            db_query = db_query.filter(
                                NearbyPlace.place_type.ilike(f"%{place_type}%"),
                                NearbyPlace.place_name.ilike(f"%{place_name}%"),
                                NearbyPlace.distance_km <= distance_km
                            )
                        elif distance_operator == "<":
                            db_query = db_query.filter(
                                NearbyPlace.place_type.ilike(f"%{place_type}%"),
                                NearbyPlace.place_name.ilike(f"%{place_name}%"),
                                NearbyPlace.distance_km < distance_km
                            )
                        elif distance_operator == "=":
                            db_query = db_query.filter(
                                NearbyPlace.place_type.ilike(f"%{place_type}%"),
                                NearbyPlace.place_name.ilike(f"%{place_name}%"),
                                NearbyPlace.distance_km == distance_km
                            )
                        print(f"✅ Applied specific nearby place filter: '{place_name}' ({place_type}) within {distance_km}km ({distance_operator})")
                    else:
                        # Apply place type and name without distance constraint
                        db_query = db_query.filter(
                            NearbyPlace.place_type.ilike(f"%{place_type}%"),
                            NearbyPlace.place_name.ilike(f"%{place_name}%")
                        )
                        print(f"✅ Applied specific nearby place filter: '{place_name}' ({place_type})")
                else:
                    # Generic place type filtering (no specific name)
                    if distance_km is not None:
                        if distance_operator == "<=":
                            db_query = db_query.filter(
                                NearbyPlace.place_type.ilike(f"%{place_type}%"),
                                NearbyPlace.distance_km <= distance_km
                            )
                        elif distance_operator == "<":
                            db_query = db_query.filter(
                                NearbyPlace.place_type.ilike(f"%{place_type}%"),
                                NearbyPlace.distance_km < distance_km
                            )
                        elif distance_operator == "=":
                            db_query = db_query.filter(
                                NearbyPlace.place_type.ilike(f"%{place_type}%"),
                                NearbyPlace.distance_km == distance_km
                            )
                        print(f"✅ Applied generic nearby place filter: {place_type} within {distance_km}km ({distance_operator})")
                    else:
                        # Just place type without distance
                        db_query = db_query.filter(
                            NearbyPlace.place_type.ilike(f"%{place_type}%")
                        )
                        print(f"✅ Applied generic nearby place filter: {place_type}")
        
        # Additional intelligent parsing for special queries
        try:
            qlower_full = (query or "").lower()
            # 1) "within X km of <place>" → use NearbyPlace with distance
            import re as _re
            within_match = _re.search(r"within\s+(\d+(?:\.\d+)?)\s*k?m?s?\s+of\s+([^,\.;]+)", qlower_full)
            if within_match:
                dist_val = float(within_match.group(1))
                place_text = within_match.group(2).strip()
                # Use EXISTS subquery to avoid duplicate joins
                from sqlalchemy import exists
                nearby_exists = exists().where(
                    and_(
                        NearbyPlace.project_id == Project.id,
                        NearbyPlace.distance_km <= dist_val,
                        or_(
                            NearbyPlace.place_type.ilike(f"%{place_text}%"),
                            NearbyPlace.place_name.ilike(f"%{place_text}%")
                        )
                    )
                )
                db_query = db_query.filter(nearby_exists)
                print(f"✅ Applied nearby distance filter: within {dist_val} km of '{place_text}'")

                # Additionally, apply BHK filter if query contains an explicit BHK number
                bhk_match = _re.search(r"(\d+)\s*bhk", qlower_full)
                if bhk_match:
                    bhk_val = int(bhk_match.group(1))
                    db_query = db_query.filter(Property.bhk_count == bhk_val)
                    print(f"✅ Applied BHK filter from query: {bhk_val} BHK")

            # 2) "with N balconies" → properties having at least N balcony room specs
            balc_match = _re.search(r"(\d+)\s+balcon(?:y|ies)", qlower_full)
            if balc_match:
                min_balconies = int(balc_match.group(1))
                from sqlalchemy import select, literal_column
                # Subquery: property_ids having at least N balconies
                balc_subq = (
                    db.query(RoomSpecification.property_id.label("prop_id"))
                    .filter(func.lower(RoomSpecification.room_type) == 'balcony')
                    .group_by(RoomSpecification.property_id)
                    .having(func.count(RoomSpecification.id) >= min_balconies)
                    .subquery()
                )
                db_query = db_query.filter(Property.id.in_(select(balc_subq.c.prop_id)))
                print(f"✅ Applied balconies filter: >= {min_balconies} balconies")

            # 3) "garden view" → any room_specifications.features contains 'garden view'
            if 'garden view' in qlower_full:
                # Subquery using Postgres unnest to do case-insensitive contains
                garden_subq = (
                    db.query(RoomSpecification.property_id.label("prop_id"))
                    .filter(
                        text("EXISTS (SELECT 1 FROM unnest(room_specifications.features) f WHERE lower(f) like '%garden view%')")
                    )
                    .group_by(RoomSpecification.property_id)
                    .subquery()
                )
                db_query = db_query.filter(Property.id.in_(select(garden_subq.c.prop_id)))
                print("✅ Applied feature filter: Garden View")
        except Exception as _parse_e:
            print(f"⚠️ Skipped special query parsing due to error: {_parse_e}")

        # Execute the query
        query_results = db_query.limit(20).all()
        
        # Update search results count (temporarily disabled)
        # search_query.search_results_count = len(query_results)
        # db.commit()
        
        # Format results
        results = []
        for property_item, project, location in query_results:
            # Calculate price per sqft
            price_per_sqft = None
            if property_item.sell_price and property_item.carpet_area_sqft and property_item.carpet_area_sqft > 0:
                price_per_sqft = property_item.sell_price / property_item.carpet_area_sqft
            
            # Get primary image and media count for the project
            primary_media = db.query(ProjectMedia).filter(
                ProjectMedia.project_id == project.id,
                ProjectMedia.is_primary == True,
                ProjectMedia.is_active == True
            ).first()
            
            total_media_count = db.query(ProjectMedia).filter(
                ProjectMedia.project_id == project.id,
                ProjectMedia.is_active == True
            ).count()
            
            project_data = {
                "id": str(property_item.id),
                "bhk_count": float(property_item.bhk_count) if property_item.bhk_count else None,
                "carpet_area_sqft": float(property_item.carpet_area_sqft) if property_item.carpet_area_sqft else None,
                "sell_price": float(property_item.sell_price) if property_item.sell_price else None,
                "price_per_sqft": float(price_per_sqft) if price_per_sqft else None,
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
                } if location else None,
                "media": {
                    "primary_image": primary_media.file_path if primary_media else None,
                    "total_count": total_media_count
                } if primary_media or total_media_count > 0 else None
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
        query = db.query(Project)
        
        # Apply filters
        if city:
            query = query.join(ProjectLocation).join(Location).filter(Location.city.ilike(f"%{city}%"))
        
        if locality:
            query = query.join(ProjectLocation).join(Location).filter(Location.locality.ilike(f"%{locality}%"))
        
        if bhk:
            # Note: BHK filtering would need to be implemented differently
            # since PropertyUnit is not available in the current schema
            pass
        
        if project_status:
            query = query.filter(Project.project_status == project_status)
        
        # Apply price filters
        if min_price or max_price:
            # Note: Price filtering would need to be implemented differently
            # since PropertyUnit is not available in the current schema
            pass
        
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
                "project_status": project.project_status,
                "total_units": project.total_units,
                "total_floors": project.total_floors,
                "possession_date": str(project.possession_date) if project.possession_date else None,
                "rera_number": project.rera_number,
                "description": project.description,
                "project_type": project.project_type
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

@app.post("/api/v1/knowledge/query")
async def knowledge_query(
    query: str = Form(..., description="Knowledge query about real estate"),
):
    """
    Knowledge base query endpoint
    Processes knowledge queries and returns relevant information
    """
    try:
        # Search the knowledge base
        result = knowledge_base.search_knowledge(query)
        
        if result:
            return {
                "success": True,
                "query": query,
                "category": result["category"],
                "question": result["question"],
                "answer": result["answer"],
                "confidence": result["confidence"]
            }
        else:
            return {
                "success": False,
                "query": query,
                "message": "I couldn't find specific information about that. Try asking about real estate terms, processes, legal aspects, or investment topics.",
                "suggestions": knowledge_base.get_suggested_questions()
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing knowledge query: {str(e)}")

@app.get("/api/v1/knowledge/categories")
async def get_knowledge_categories():
    """Get available knowledge base categories"""
    try:
        categories = knowledge_base.get_knowledge_categories()
        return {
            "success": True,
            "categories": categories,
            "total_categories": len(categories)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching knowledge categories: {str(e)}")

@app.get("/api/v1/knowledge/suggestions")
async def get_knowledge_suggestions(category: Optional[str] = Query(None, description="Category to get suggestions for")):
    """Get suggested knowledge questions"""
    try:
        suggestions = knowledge_base.get_suggested_questions(category)
        return {
            "success": True,
            "category": category,
            "suggestions": suggestions,
            "total_suggestions": len(suggestions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching knowledge suggestions: {str(e)}")

@app.get("/api/v1/projects/{project_id}/amenities")
async def get_project_amenities(project_id: str, db: Session = Depends(get_db)):
    """Get amenities for a specific project"""
    try:
        # For now, return default amenities since there's a database schema mismatch
        # TODO: Fix the database schema to match the models
        default_amenities = [
            {"id": "1", "name": "Swimming Pool", "category": "basic", "icon": "🏊", "is_available": True},
            {"id": "2", "name": "Gym", "category": "basic", "icon": "💪", "is_available": True},
            {"id": "3", "name": "Garden", "category": "basic", "icon": "🌳", "is_available": True},
            {"id": "4", "name": "Security", "category": "basic", "icon": "🛡️", "is_available": True},
            {"id": "5", "name": "Lift", "category": "basic", "icon": "🛗", "is_available": True},
            {"id": "6", "name": "Parking", "category": "basic", "icon": "🚗", "is_available": True},
            {"id": "7", "name": "Concierge", "category": "basic", "icon": "🔔", "is_available": True},
            {"id": "8", "name": "Spa", "category": "luxury", "icon": "🧖", "is_available": True},
            {"id": "9", "name": "Theater", "category": "luxury", "icon": "🎭", "is_available": True},
            {"id": "10", "name": "Kids Play Area", "category": "basic", "icon": "🎠", "is_available": True}
        ]
        
        return {
            "success": True,
            "project_id": project_id,
            "amenities": default_amenities,
            "total_amenities": len(default_amenities)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching project amenities: {str(e)}")

@app.get("/api/v1/projects/{project_id}/property-configurations")
async def get_project_property_configurations(project_id: str, db: Session = Depends(get_db)):
    """Get all property configurations (BHK types) for a specific project with floor plans"""
    try:
        # Query properties for the given project
        from sqlalchemy import func
        properties = db.query(Property).filter(
            Property.project_id == project_id,
            (Property.status.is_(None)) | (~func.lower(Property.status).like('%sold%'))
        ).order_by(Property.bhk_count).all()
        
        # Format results
        configurations = []
        for prop in properties:
            config = {
                "id": str(prop.id),
                "bhk_count": float(prop.bhk_count) if prop.bhk_count else None,
                "carpet_area_sqft": float(prop.carpet_area_sqft) if prop.carpet_area_sqft else None,
                "super_builtup_area_sqft": float(prop.super_builtup_area_sqft) if prop.super_builtup_area_sqft else None,
                "sell_price": float(prop.sell_price) if prop.sell_price else None,
                "floor_plan_url": prop.floor_plan_url,
                "property_type": prop.property_type,
                "facing": prop.facing,
                "status": prop.status,
                "floor_number": prop.floor_number
            }
            configurations.append(config)
        
        return {
            "success": True,
            "project_id": project_id,
            "configurations": configurations,
            "total_configurations": len(configurations)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching property configurations: {str(e)}")

@app.get("/api/v1/projects/{project_id}/nearby-places")
async def get_project_nearby_places(project_id: str, db: Session = Depends(get_db)):
    """Get nearby places for a specific project with distances"""
    try:
        # Query nearby places for the given project
        nearby_places = db.query(NearbyPlace).filter(
            NearbyPlace.project_id == project_id
        ).order_by(NearbyPlace.place_type, NearbyPlace.distance_km).all()
        
        # Group by place type for better organization
        places_by_category = {}
        for place in nearby_places:
            category = place.place_type
            if category not in places_by_category:
                places_by_category[category] = []
            
            places_by_category[category].append({
                "id": str(place.id),
                "place_name": place.place_name,
                "distance_km": float(place.distance_km),
                "walking_distance": place.walking_distance,
                "created_at": str(place.created_at),
                "updated_at": str(place.updated_at)
            })
        
        return {
            "success": True,
            "project_id": project_id,
            "nearby_places": places_by_category,
            "total_categories": len(places_by_category),
            "total_places": len(nearby_places)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching nearby places: {str(e)}")

@app.get("/api/v1/projects/{project_id}/media")
async def get_project_media(project_id: str, db: Session = Depends(get_db)):
    """Get media (images and videos) for a specific project"""
    try:
        # Query the database for actual project media
        project_media = db.query(ProjectMedia).filter(
            ProjectMedia.project_id == project_id,
            ProjectMedia.is_active == True
        ).order_by(ProjectMedia.sort_order, ProjectMedia.created_at).all()
        
        # Convert SQLAlchemy objects to dictionaries
        media_list = []
        for media in project_media:
            media_dict = {
                "id": str(media.id),
                "file_name": media.file_name,
                "file_path": media.file_path,
                "file_type": media.file_type,
                "mime_type": media.mime_type,
                "media_category": media.media_category,
                "is_primary": media.is_primary,
                "alt_text": media.alt_text,
                "sort_order": media.sort_order,
                "width": media.width,
                "height": media.height,
                "duration_seconds": media.duration_seconds,
                "caption": media.caption
            }
            media_list.append(media_dict)
        
        return {
            "success": True,
            "project_id": project_id,
            "media": media_list,
            "total_media": len(media_list)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching project media: {str(e)}")

@app.get("/api/v1/search/nearby")
async def search_by_nearby_places(
    place_type: str = Query(..., description="Type of nearby place (e.g., hospital, school, mall)"),
    distance_km: float = Query(..., description="Maximum distance in kilometers"),
    city: str = Query(None, description="City to search in"),
    db: Session = Depends(get_db)
):
    """Search properties based on nearby places within specified distance"""
    try:
        # Build the query to find projects with nearby places
        query = db.query(Project).join(NearbyPlace).filter(
            NearbyPlace.place_type.ilike(f"%{place_type}%"),
            NearbyPlace.distance_km <= distance_km
        )
        
        # Add city filter if specified
        if city:
            query = query.join(ProjectLocation).join(Location).filter(
                Location.city.ilike(f"%{city}%")
            )
        
        # Get projects with nearby places
        projects = query.distinct().all()
        
        # Get properties for these projects, excluding sold
        from sqlalchemy import func
        project_ids = [str(project.id) for project in projects]
        properties = db.query(Property).filter(
            Property.project_id.in_(project_ids),
            (Property.status.is_(None)) | (~func.lower(Property.status).like('%sold%'))
        ).all()
        
        # Format results with nearby place information
        results = []
        for prop in properties:
            # Get nearby places for this property's project
            nearby_places = db.query(NearbyPlace).filter(
                NearbyPlace.project_id == prop.project_id,
                NearbyPlace.place_type.ilike(f"%{place_type}%"),
                NearbyPlace.distance_km <= distance_km
            ).all()
            
            # Get project and location info
            project = db.query(Project).filter(Project.id == prop.project_id).first()
            project_location = db.query(ProjectLocation).filter(ProjectLocation.project_id == prop.project_id).first()
            location = None
            if project_location:
                location = db.query(Location).filter(Location.id == project_location.location_id).first()
            
            result = {
                "id": str(prop.id),
                "project_id": str(prop.project_id),
                "project_name": project.name if project else None,
                "property_type": prop.property_type,
                "bhk_count": float(prop.bhk_count) if prop.bhk_count else None,
                "carpet_area_sqft": float(prop.carpet_area_sqft) if prop.carpet_area_sqft else None,
                "super_builtup_area_sqft": float(prop.super_builtup_area_sqft) if prop.super_builtup_area_sqft else None,
                "sell_price": float(prop.sell_price) if prop.sell_price else None,
                "floor_plan_url": prop.floor_plan_url,
                "facing": prop.facing,
                "status": prop.status,
                "floor_number": prop.floor_number,
                "city": location.city if location else None,
                "locality": location.locality if location else None,
                "nearby_places": [
                    {
                        "place_name": place.place_name,
                        "place_type": place.place_type,
                        "distance_km": float(place.distance_km),
                        "walking_distance": place.walking_distance
                    }
                    for place in nearby_places
                ]
            }
            results.append(result)
        
        return {
            "success": True,
            "query": {
                "place_type": place_type,
                "max_distance_km": distance_km,
                "city": city
            },
            "results": results,
            "total_results": len(results)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching by nearby places: {str(e)}")

@app.get("/api/v1/cities")
async def get_cities(db: Session = Depends(get_db)):
    """Get all cities"""
    try:
        # Query cities from the Location table
        cities = db.query(Location.city).distinct().filter(Location.city.isnot(None)).all()
        return [{"name": city[0]} for city in cities if city[0]]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching cities: {str(e)}")

@app.get("/api/v1/localities/{city_name}")
async def get_localities(city_name: str, db: Session = Depends(get_db)):
    """Get localities for a specific city"""
    try:
        # Query localities from the Location table for a specific city
        localities = db.query(Location.locality).filter(
            Location.city == city_name,
            Location.locality.isnot(None)
        ).distinct().all()
        
        return [{"name": locality[0]} for locality in localities if locality[0]]
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
