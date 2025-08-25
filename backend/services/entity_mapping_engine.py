import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class EntityType(Enum):
    """Types of entities in the system"""
    PROPERTY_TYPE = "property_type"
    LOCATION = "location"
    PRICE_RANGE = "price_range"
    AMENITY = "amenity"
    BHK = "bhk"
    STATUS = "status"
    BUILDER = "builder"

@dataclass
class EntityMapping:
    """Entity mapping structure with 2 child levels max"""
    primary_value: str
    synonyms: List[str]
    child_levels: Dict[str, List[str]]
    metadata: Dict[str, Any]

class EntityMappingEngine:
    """Engine for managing entity mappings and auto-expansion"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.entity_mappings = self._initialize_entity_mappings()
        self.reverse_mappings = self._build_reverse_mappings()
    
    def _initialize_entity_mappings(self) -> Dict[str, Dict[str, EntityMapping]]:
        """Initialize comprehensive entity mappings"""
        return {
            EntityType.PROPERTY_TYPE.value: {
                "apartment": EntityMapping(
                    primary_value="Apartment",
                    synonyms=["Flat", "Unit", "Ghar", "Apartment", "Residential Unit"],
                    child_levels={
                        "category": ["Residential", "Commercial", "Mixed Use"],
                        "style": ["Modern", "Traditional", "Contemporary", "Luxury"]
                    },
                    metadata={
                        "description": "Multi-unit residential building",
                        "typical_size": "500-2000 sq ft",
                        "ownership": "Freehold/Leasehold"
                    }
                ),
                "villa": EntityMapping(
                    primary_value="Villa",
                    synonyms=["Independent House", "Bungalow", "Ghar", "Villa", "House"],
                    child_levels={
                        "type": ["Independent", "Row House", "Semi-Detached", "Duplex"],
                        "style": ["Modern", "Traditional", "Contemporary", "Luxury"]
                    },
                    metadata={
                        "description": "Independent residential unit",
                        "typical_size": "1500-5000 sq ft",
                        "ownership": "Freehold"
                    }
                ),
                "plot": EntityMapping(
                    primary_value="Plot",
                    synonyms=["Land", "Plot", "Jameen", "Land Plot", "Empty Plot"],
                    child_levels={
                        "usage": ["Residential", "Commercial", "Agricultural", "Mixed"],
                        "approval": ["Approved", "Unapproved", "Under Process"]
                    },
                    metadata={
                        "description": "Empty land for construction",
                        "typical_size": "1000-10000 sq ft",
                        "ownership": "Freehold"
                    }
                )
            },
            
            EntityType.BHK.value: {
                "1bhk": EntityMapping(
                    primary_value="1 BHK",
                    synonyms=["1 BHK", "1 Bedroom", "1 Bedroom Hall Kitchen", "Ek BHK", "One BHK"],
                    child_levels={
                        "size": ["Compact", "Standard", "Large"],
                        "type": ["Apartment", "Villa", "Row House"]
                    },
                    metadata={
                        "description": "One bedroom with hall and kitchen",
                        "typical_size": "400-800 sq ft",
                        "suitable_for": "Single person, couple"
                    }
                ),
                "2bhk": EntityMapping(
                    primary_value="2 BHK",
                    synonyms=["2 BHK", "2 Bedroom", "2 Bedroom Hall Kitchen", "Do BHK", "Two BHK"],
                    child_levels={
                        "size": ["Compact", "Standard", "Large", "Premium"],
                        "type": ["Apartment", "Villa", "Row House"]
                    },
                    metadata={
                        "description": "Two bedrooms with hall and kitchen",
                        "typical_size": "800-1200 sq ft",
                        "suitable_for": "Small family, 2-3 people"
                    }
                ),
                "3bhk": EntityMapping(
                    primary_value="3 BHK",
                    synonyms=["3 BHK", "3 Bedroom", "3 Bedroom Hall Kitchen", "Teen BHK", "Three BHK"],
                    child_levels={
                        "size": ["Standard", "Large", "Premium", "Luxury"],
                        "type": ["Apartment", "Villa", "Row House"]
                    },
                    metadata={
                        "description": "Three bedrooms with hall and kitchen",
                        "typical_size": "1200-2000 sq ft",
                        "suitable_for": "Family, 4-5 people"
                    }
                )
            },
            
            EntityType.LOCATION.value: {
                "east_pune": EntityMapping(
                    primary_value="East Pune",
                    synonyms=["East Pune", "Purv Pune", "Eastern Pune", "East Side"],
                    child_levels={
                        "areas": ["Viman Nagar", "Kharadi", "Hadapsar", "Magarpatta", "Wagholi", "Lonikand"],
                        "features": ["IT Hub", "Airport Proximity", "Industrial Area", "Residential"]
                    },
                    metadata={
                        "description": "Eastern part of Pune city",
                        "key_features": ["IT companies", "Airport", "Industrial zones"],
                        "price_range": "₹4000-8000 per sq ft"
                    }
                ),
                "west_pune": EntityMapping(
                    primary_value="West Pune",
                    synonyms=["West Pune", "Pashchim Pune", "Western Pune", "West Side"],
                    child_levels={
                        "areas": ["Koregaon Park", "Boat Club", "Model Colony", "Aundh", "Baner", "Balewadi"],
                        "features": ["Luxury", "Educational Hub", "Residential", "Entertainment"]
                    },
                    metadata={
                        "description": "Western part of Pune city",
                        "key_features": ["Luxury properties", "Educational institutions", "Entertainment"],
                        "price_range": "₹8000-15000 per sq ft"
                    }
                ),
                "north_pune": EntityMapping(
                    primary_value="North Pune",
                    synonyms=["North Pune", "Uttar Pune", "Northern Pune", "North Side"],
                    child_levels={
                        "areas": ["Kalyani Nagar", "Yerwada", "Kharadi", "Viman Nagar", "Lohegaon", "Chandannagar"],
                        "features": ["Residential", "Airport Proximity", "Industrial", "Mixed Use"]
                    },
                    metadata={
                        "description": "Northern part of Pune city",
                        "key_features": ["Residential areas", "Airport proximity", "Industrial zones"],
                        "price_range": "₹5000-10000 per sq ft"
                    }
                ),
                "south_pune": EntityMapping(
                    primary_value="South Pune",
                    synonyms=["South Pune", "Dakshin Pune", "Southern Pune", "South Side"],
                    child_levels={
                        "areas": ["Hinjewadi", "Wakad", "Baner", "Balewadi", "Pashan", "Sus"],
                        "features": ["IT Hub", "Educational", "Residential", "Nature"]
                    },
                    metadata={
                        "description": "Southern part of Pune city",
                        "key_features": ["IT companies", "Educational institutions", "Natural surroundings"],
                        "price_range": "₹6000-12000 per sq ft"
                    }
                ),
                "central_pune": EntityMapping(
                    primary_value="Central Pune",
                    synonyms=["Central Pune", "Madhya Pune", "Center", "City Center"],
                    child_levels={
                        "areas": ["Camp", "Deccan", "FC Road", "JM Road", "Shivajinagar", "Pune Station"],
                        "features": ["Commercial", "Historical", "Transport Hub", "Mixed Use"]
                    },
                    metadata={
                        "description": "Central part of Pune city",
                        "key_features": ["Commercial areas", "Historical sites", "Transport connectivity"],
                        "price_range": "₹7000-13000 per sq ft"
                    }
                )
            },
            
            EntityType.PRICE_RANGE.value: {
                "affordable": EntityMapping(
                    primary_value="Affordable",
                    synonyms=["Budget", "Cheap", "Low Cost", "Economical", "Sasta", "Kam Daam"],
                    child_levels={
                        "range": ["Under ₹25L", "₹25L-50L", "₹50L-75L"],
                        "type": ["1 BHK", "2 BHK", "Small Villa"]
                    },
                    metadata={
                        "description": "Budget-friendly properties",
                        "price_per_sqft": "₹3000-6000",
                        "target_audience": "First-time buyers, middle class"
                    }
                ),
                "mid_range": EntityMapping(
                    primary_value="Mid Range",
                    synonyms=["Mid Range", "Moderate", "Average", "Medium", "Madhyam", "Darmiyan"],
                    child_levels={
                        "range": ["₹50L-1Cr", "₹1Cr-1.5Cr", "₹1.5Cr-2Cr"],
                        "type": ["2 BHK", "3 BHK", "Villa"]
                    },
                    metadata={
                        "description": "Moderately priced properties",
                        "price_per_sqft": "₹6000-10000",
                        "target_audience": "Established families, professionals"
                    }
                ),
                "luxury": EntityMapping(
                    primary_value="Luxury",
                    synonyms=["Premium", "High End", "Expensive", "Luxury", "Mahanga", "Premium"],
                    child_levels={
                        "range": ["₹2Cr-5Cr", "₹5Cr-10Cr", "₹10Cr+"],
                        "type": ["3 BHK+", "Villa", "Penthouse"]
                    },
                    metadata={
                        "description": "High-end luxury properties",
                        "price_per_sqft": "₹10000+",
                        "target_audience": "High net worth individuals"
                    }
                )
            },
            
            EntityType.AMENITY.value: {
                "basic": EntityMapping(
                    primary_value="Basic Amenities",
                    synonyms=["Basic", "Essential", "Standard", "Basic Facilities"],
                    child_levels={
                        "category": ["Security", "Water", "Electricity", "Parking"],
                        "type": ["24x7", "Limited Hours", "On Demand"]
                    },
                    metadata={
                        "description": "Essential amenities for daily living",
                        "included_in": "All properties",
                        "cost": "Usually included in maintenance"
                    }
                ),
                "lifestyle": EntityMapping(
                    primary_value="Lifestyle Amenities",
                    synonyms=["Lifestyle", "Recreational", "Entertainment", "Luxury Facilities"],
                    child_levels={
                        "category": ["Sports", "Entertainment", "Wellness", "Social"],
                        "type": ["Indoor", "Outdoor", "Mixed"]
                    },
                    metadata={
                        "description": "Recreational and lifestyle facilities",
                        "included_in": "Premium properties",
                        "cost": "Additional charges may apply"
                    }
                )
            },
            
            EntityType.STATUS.value: {
                "ready_to_move": EntityMapping(
                    primary_value="Ready to Move",
                    synonyms=["Ready", "Completed", "Move-in Ready", "Ready to Occupy"],
                    child_levels={
                        "type": ["Fully Furnished", "Semi-Furnished", "Unfurnished"],
                        "condition": ["New", "Resale", "Renovated"]
                    },
                    metadata={
                        "description": "Property ready for immediate occupation",
                        "advantages": ["No waiting", "Immediate possession", "No construction risk"],
                        "disadvantages": ["Higher cost", "Limited customization"]
                    }
                ),
                "under_construction": EntityMapping(
                    primary_value="Under Construction",
                    synonyms=["Under Construction", "Being Built", "In Progress", "Under Development"],
                    child_levels={
                        "stage": ["Foundation", "Structure", "Finishing", "Near Completion"],
                        "timeline": ["6 months", "1 year", "2 years", "3+ years"]
                    },
                    metadata={
                        "description": "Property under development",
                        "advantages": ["Lower cost", "Customization options", "Payment flexibility"],
                        "disadvantages": ["Waiting time", "Construction risk", "Delays possible"]
                    }
                )
            },
            
            EntityType.BUILDER.value: {
                "lodha": EntityMapping(
                    primary_value="Lodha",
                    synonyms=["Lodha Group", "Lodha", "Lodha Developers"],
                    child_levels={
                        "projects": ["Lodha Belmondo", "Lodha Park", "Lodha Splendora"],
                        "type": ["Luxury", "Premium", "Mid-Range"]
                    },
                    metadata={
                        "description": "Premium real estate developer",
                        "reputation": "High-end luxury properties",
                        "price_range": "₹1Cr+",
                        "quality": "Premium construction standards"
                    }
                ),
                "godrej": EntityMapping(
                    primary_value="Godrej",
                    synonyms=["Godrej Properties", "Godrej", "Godrej Group"],
                    child_levels={
                        "projects": ["Godrej Woods", "Godrej E-City", "Godrej Prana"],
                        "type": ["Premium", "Mid-Range", "Affordable"]
                    },
                    metadata={
                        "description": "Reputed real estate developer",
                        "reputation": "Quality construction and reliability",
                        "price_range": "₹50L-5Cr",
                        "quality": "High construction standards"
                    }
                )
            }
        }
    
    def _build_reverse_mappings(self) -> Dict[str, str]:
        """Build reverse mappings for quick lookup"""
        reverse_mappings = {}
        
        for entity_type, entities in self.entity_mappings.items():
            for entity_key, entity_mapping in entities.items():
                # Map primary value
                reverse_mappings[entity_mapping.primary_value.lower()] = f"{entity_type}:{entity_key}"
                
                # Map synonyms
                for synonym in entity_mapping.synonyms:
                    reverse_mappings[synonym.lower()] = f"{entity_type}:{entity_key}"
                
                # Map child level values
                for child_category, child_values in entity_mapping.child_levels.items():
                    for child_value in child_values:
                        reverse_mappings[child_value.lower()] = f"{entity_type}:{entity_key}:{child_category}:{child_value}"
        
        return reverse_mappings
    
    def get_entity_mapping(self, entity_type: str, entity_key: str) -> Optional[EntityMapping]:
        """Get entity mapping by type and key"""
        return self.entity_mappings.get(entity_type, {}).get(entity_key)
    
    def find_entity_by_value(self, value: str) -> Optional[Tuple[str, str, EntityMapping]]:
        """Find entity by any of its values (primary, synonym, or child)"""
        value_lower = value.lower()
        
        if value_lower in self.reverse_mappings:
            mapping_path = self.reverse_mappings[value_lower]
            parts = mapping_path.split(":")
            
            if len(parts) >= 2:
                entity_type = parts[0]
                entity_key = parts[1]
                entity_mapping = self.get_entity_mapping(entity_type, entity_key)
                
                if entity_mapping:
                    return entity_type, entity_key, entity_mapping
        
        return None
    
    def expand_entity(self, value: str) -> Dict[str, Any]:
        """Expand entity value with all its mappings and metadata"""
        result = self.find_entity_by_value(value)
        
        if result:
            entity_type, entity_key, entity_mapping = result
            
            return {
                "entity_type": entity_type,
                "entity_key": entity_key,
                "primary_value": entity_mapping.primary_value,
                "synonyms": entity_mapping.synonyms,
                "child_levels": entity_mapping.child_levels,
                "metadata": entity_mapping.metadata,
                "confidence": 1.0
            }
        
        return {"confidence": 0.0, "error": "Entity not found"}
    
    def get_suggestions(self, partial_value: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get entity suggestions based on partial input"""
        suggestions = []
        partial_lower = partial_value.lower()
        
        for entity_type, entities in self.entity_mappings.items():
            for entity_key, entity_mapping in entities.items():
                # Check primary value
                if partial_lower in entity_mapping.primary_value.lower():
                    suggestions.append({
                        "value": entity_mapping.primary_value,
                        "type": entity_type,
                        "key": entity_key,
                        "confidence": 0.9
                    })
                
                # Check synonyms
                for synonym in entity_mapping.synonyms:
                    if partial_lower in synonym.lower():
                        suggestions.append({
                            "value": synonym,
                            "type": entity_type,
                            "key": entity_key,
                            "confidence": 0.8
                        })
                
                # Check child levels
                for child_category, child_values in entity_mapping.child_levels.items():
                    for child_value in child_values:
                        if partial_lower in child_value.lower():
                            suggestions.append({
                                "value": child_value,
                                "type": entity_type,
                                "key": entity_key,
                                "category": child_category,
                                "confidence": 0.7
                            })
        
        # Sort by confidence and limit results
        suggestions.sort(key=lambda x: x["confidence"], reverse=True)
        return suggestions[:limit]
    
    def get_related_entities(self, entity_type: str, entity_key: str) -> Dict[str, List[str]]:
        """Get related entities for a given entity"""
        entity_mapping = self.get_entity_mapping(entity_type, entity_key)
        
        if not entity_mapping:
            return {}
        
        related = {}
        
        # Get entities of the same type
        same_type_entities = list(self.entity_mappings.get(entity_type, {}).keys())
        if entity_key in same_type_entities:
            same_type_entities.remove(entity_key)
        related[f"other_{entity_type}"] = same_type_entities
        
        # Get child level entities
        related["child_levels"] = entity_mapping.child_levels
        
        return related
    
    def export_mappings(self, filepath: str):
        """Export entity mappings to JSON file"""
        try:
            export_data = {}
            
            for entity_type, entities in self.entity_mappings.items():
                export_data[entity_type] = {}
                for entity_key, entity_mapping in entities.items():
                    export_data[entity_type][entity_key] = {
                        "primary_value": entity_mapping.primary_value,
                        "synonyms": entity_mapping.synonyms,
                        "child_levels": entity_mapping.child_levels,
                        "metadata": entity_mapping.metadata
                    }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Entity mappings exported to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error exporting entity mappings: {e}")
            raise

if __name__ == "__main__":
    # Test the entity mapping engine
    engine = EntityMappingEngine()
    
    # Test entity expansion
    test_values = ["carpet area", "2bhk", "east pune", "affordable", "lodha"]
    
    print("Testing Entity Mapping Engine:")
    print("=" * 50)
    
    for value in test_values:
        print(f"\nInput: {value}")
        result = engine.expand_entity(value)
        if result["confidence"] > 0:
            print(f"Found: {result['primary_value']} ({result['entity_type']})")
            print(f"Synonyms: {', '.join(result['synonyms'][:3])}")
        else:
            print("Not found")
    
    # Test suggestions
    print(f"\nSuggestions for 'pun':")
    suggestions = engine.get_suggestions("pun", limit=3)
    for suggestion in suggestions:
        print(f"- {suggestion['value']} ({suggestion['type']})")
