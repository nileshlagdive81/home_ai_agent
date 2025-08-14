import spacy
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import re

@dataclass
class ExtractedEntity:
    """Represents an extracted entity from the query"""
    text: str
    label: str
    start: int
    end: int
    confidence: float
    context: Dict  # Additional context like operator, value, unit

@dataclass
class QueryIntent:
    """Represents the detected intent and confidence"""
    intent: str
    confidence: float
    entities: List[ExtractedEntity]

class RealEstateNLPEngine:
    """INTENT-DRIVEN NLP Engine for Real Estate queries using spaCy"""
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        """Initialize the NLP engine with spaCy model"""
        try:
            self.nlp = spacy.load(model_name)
            print(f"✅ Loaded spaCy model: {model_name}")
        except OSError:
            print(f"❌ Model {model_name} not found. Please install it with: python -m spacy download {model_name}")
            raise
        
        # INTENT-DRIVEN: Define intents based on semantic meaning, not keywords
        self.intents = {
            "SEARCH_PROPERTY": {
                "description": "User wants to find properties based on criteria",
                "semantic_indicators": ["find", "search", "looking for", "want", "need", "show me", "get me", "available"],
                "context_indicators": ["properties", "flats", "houses", "apartments", "real estate"]
            },
            "FILTER_BY_AMENITY": {
                "description": "User wants properties with specific amenities or near landmarks",
                "semantic_indicators": ["near", "close to", "nearby", "within", "distance"],
                "context_indicators": ["metro", "hospital", "school", "office", "station", "mall", "park", "garden"]
            },
            "COMPARE_PROPERTIES": {
                "description": "User wants to compare different properties",
                "semantic_indicators": ["compare", "difference", "vs", "versus", "better", "best", "which one"],
                "context_indicators": ["properties", "projects", "buildings"]
            },
            "BOOK_VIEWING": {
                "description": "User wants to schedule a property viewing",
                "semantic_indicators": ["book", "schedule", "appointment", "visit", "viewing", "tour", "see"],
                "context_indicators": ["tomorrow", "next week", "this weekend", "today"]
            },
            "GET_DETAILS": {
                "description": "User wants specific information about properties",
                "semantic_indicators": ["what", "details", "information", "tell me", "how much"],
                "context_indicators": ["price", "area", "bhk", "floor", "status", "completion"]
            },
            "PRICE_QUERY": {
                "description": "User is asking about pricing information",
                "semantic_indicators": ["price", "cost", "budget", "affordable", "expensive", "cheap"],
                "context_indicators": ["per sq ft", "total cost", "booking amount", "lakhs", "crores"]
            }
        }
    
    def extract_entities_with_context(self, text: str) -> List[ExtractedEntity]:
        """INTENT-DRIVEN: Extract entities with full semantic context"""
        entities = []
        text_lower = text.lower()
        
        print(f"🔍 INTENT-DRIVEN: Analyzing semantic meaning of: '{text}'")
        
        # Process with spaCy for linguistic understanding
        doc = self.nlp(text)
        
        # INTENT-DRIVEN: Extract entities based on semantic understanding, not just patterns
        
        # 1. LOCATION entities (cities, localities, landmarks)
        self._extract_location_entities(doc, entities, text_lower)
        
        # 2. BHK entities with semantic context
        self._extract_bhk_entities(doc, entities, text_lower)
        
        # 3. PRICE entities with semantic context (MOST IMPORTANT)
        self._extract_price_entities_with_context(doc, entities, text_lower)
        
        # 4. CARPET AREA entities with semantic context
        self._extract_area_entities_with_context(doc, entities, text_lower)
        
        # 5. AMENITY entities with semantic context
        self._extract_amenity_entities(doc, entities, text_lower)
        
        print(f"🔍 INTENT-DRIVEN: Total entities with context: {len(entities)}")
        for entity in entities:
            print(f"🔍 INTENT-DRIVEN: Entity: {entity.label} = '{entity.text}' with context: {entity.context}")
        
        return entities
    
    def _extract_location_entities(self, doc, entities, text_lower):
        """Extract location entities using spaCy's NER and common Indian cities"""
        # First, check for common Indian cities in the text
        indian_cities = [
            "mumbai", "delhi", "bangalore", "hyderabad", "chennai", "kolkata", "pune", 
            "ahmedabad", "jaipur", "lucknow", "kanpur", "nagpur", "indore", "thane",
            "bhopal", "visakhapatnam", "patna", "vadodara", "ghaziabad", "ludhiana",
            "agra", "nashik", "faridabad", "meerut", "rajkot", "kalyan", "vasai",
            "vashi", "navi mumbai", "gurgaon", "noida", "greater noida", "faridabad"
        ]
        
        # Check for city mentions in the text
        for city in indian_cities:
            if city in text_lower:
                # Check if it's actually being requested as a location
                context_words = self._get_context_words(text_lower, text_lower.find(city), text_lower.find(city) + len(city), 10)
                if any(word in context_words for word in ["in", "at", "near", "from", "of", "within", "around"]):
                    entities.append(ExtractedEntity(
                        text=city,
                        label="LOCATION",
                        start=text_lower.find(city),
                        end=text_lower.find(city) + len(city),
                        confidence=0.9,
                        context={"type": "city", "full_text": city, "semantic_meaning": "required_location"}
                    ))
                    print(f"🔍 INTENT-DRIVEN: Found LOCATION entity: '{city}' (Indian city)")
                    return  # Exit after finding first city
        
        # Fallback to spaCy's NER for other location entities
        for ent in doc.ents:
            if ent.label_ in ["GPE", "LOC", "FAC"]:  # Location entities
                entities.append(ExtractedEntity(
                    text=ent.text,
                    label="LOCATION",
                    start=ent.start_char,
                    end=ent.end_char,
                    confidence=0.8,
                    context={"type": ent.label_, "full_text": ent.text}
                ))
                print(f"🔍 INTENT-DRIVEN: Found LOCATION entity: '{ent.text}' ({ent.label_})")
    
    def _extract_bhk_entities(self, doc, entities, text_lower):
        """Extract BHK entities with semantic understanding"""
        # Look for BHK patterns in the context of property specifications
        bhk_patterns = [
            r'(\d+(?:\.\d+)?)\s*bhk',
            r'(\d+(?:\.\d+)?)\s*bedroom',
            r'(\d+(?:\.\d+)?)\s*bed\s*room'
        ]
        
        for pattern in bhk_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                # INTENT-DRIVEN: Check if this is actually about property BHK, not just a number
                context_words = self._get_context_words(text_lower, match.start(), match.end(), 10)
                if any(word in context_words for word in ["property", "flat", "apartment", "house", "real estate", "bhk"]):
                    entities.append(ExtractedEntity(
                        text=match.group(0),
                        label="BHK",
                        start=match.start(),
                        end=match.end(),
                        confidence=0.9,
                        context={"value": float(match.group(1)), "operator": "=", "unit": "bhk"}
                    ))
                    print(f"🔍 INTENT-DRIVEN: Found BHK entity: '{match.group(0)}' in property context")
    
    def _extract_price_entities_with_context(self, doc, entities, text_lower):
        """INTENT-DRIVEN: Extract price entities with full semantic context"""
        print(f"🔍 INTENT-DRIVEN: Analyzing price context in: '{text_lower}'")
        
        # INTENT-DRIVEN: First, understand the semantic structure of the query
        # Look for price-related semantic patterns
        
        # Pattern 1: "under X crore/lakh" - semantic understanding
        under_patterns = [
            r'(under|below|less\s+than)\s+(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)',
            r'(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)\s+(?:or\s+)?(?:less|below|under)',
            r'price\s+(?:under|below|less\s+than)\s+(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)',
            r'budget\s+(?:under|below|less\s+than)\s+(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)',
            r'cost\s+(?:under|below|less\s+than)\s+(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)',
            # Additional patterns for common variations
            r'properties?\s+(?:under|below|less\s+than)\s+(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)',
            r'flats?\s+(?:under|below|less\s+than)\s+(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)',
            r'houses?\s+(?:under|below|less\s+than)\s+(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)',
            r'apartments?\s+(?:under|below|less\s+than)\s+(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)',
            # More comprehensive patterns
            r'(?:properties?|flats?|houses?|apartments?)\s+(?:under|below|less\s+than)\s+(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)',
            r'(?:under|below|less\s+than)\s+(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)',
            r'(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)\s+(?:under|below|less\s+than)'
        ]
        
        # Pattern 2: "above X crore/lakh" - semantic understanding
        above_patterns = [
            r'(above|over|more\s+than)\s+(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)',
            r'(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)\s+(?:or\s+)?(?:more|above|over)',
            r'price\s+(?:above|over|more\s+than)\s+(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)',
            r'budget\s+(?:above|over|more\s+than)\s+(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)',
            r'cost\s+(?:above|over|more\s+than)\s+(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)',
            # Additional patterns for common variations
            r'properties?\s+(?:above|over|more\s+than)\s+(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)',
            r'flats?\s+(?:above|over|more\s+than)\s+(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)',
            r'houses?\s+(?:above|over|more\s+than)\s+(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)',
            r'apartments?\s+(?:above|over|more\s+than)\s+(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)'
        ]
        
        # Pattern 3: Exact price - semantic understanding
        exact_patterns = [
            r'(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)\s+(?:exactly|precisely|exact)',
            r'price\s+(?:is|of)\s+(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)',
            r'(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)\s+(?:flat|apartment|property)',
            # Additional patterns for exact matches
            r'(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)\s*[=]\s*(\d+(?:\.\d+)?)',
            r'(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)\s+(?:flat|apartment|property|bhk)'
        ]
        
        # INTENT-DRIVEN: Check each pattern with semantic validation
        found_price = False
        
        # Check "under" patterns first (most common in real estate)
        for pattern in under_patterns:
            if not found_price:
                matches = re.finditer(pattern, text_lower)
                for match in matches:
                    # INTENT-DRIVEN: Validate this is actually about price, not area or other attributes
                    if self._is_price_context(text_lower, match.start(), match.end()):
                        value = float(match.group(2))
                        unit = match.group(3)
                        price_in_rupees = self._convert_to_rupees(value, unit)
                        
                        entities.append(ExtractedEntity(
                            text=match.group(0),
                            label="PRICE",
                            start=match.start(),
                            end=match.end(),
                            confidence=0.95,
                            context={
                                "value": price_in_rupees,
                                "operator": "<",
                                "unit": unit,
                                "original_value": value,
                                "semantic_meaning": "less_than"
                            }
                        ))
                        print(f"🔍 INTENT-DRIVEN: Found PRICE entity (under): '{match.group(0)}' = < {price_in_rupees} rupees")
                        found_price = True
                        break
        
        # Check "above" patterns
        for pattern in above_patterns:
            if not found_price:
                matches = re.finditer(pattern, text_lower)
                for match in matches:
                    if self._is_price_context(text_lower, match.start(), match.end()):
                        value = float(match.group(2))
                        unit = match.group(3)
                        price_in_rupees = self._convert_to_rupees(value, unit)
                        
                        entities.append(ExtractedEntity(
                            text=match.group(0),
                            label="PRICE",
                            start=match.start(),
                            end=match.end(),
                            confidence=0.95,
                            context={
                                "value": price_in_rupees,
                                "operator": ">",
                                "unit": unit,
                                "original_value": value,
                                "semantic_meaning": "more_than"
                            }
                        ))
                        print(f"🔍 INTENT-DRIVEN: Found PRICE entity (above): '{match.group(0)}' = > {price_in_rupees} rupees")
                        found_price = True
                        break
        
        # Check exact price patterns
        for pattern in exact_patterns:
            if not found_price:
                matches = re.finditer(pattern, text_lower)
                for match in matches:
                    if self._is_price_context(text_lower, match.start(), match.end()):
                        value = float(match.group(1))
                        unit = match.group(2)
                        price_in_rupees = self._convert_to_rupees(value, unit)
                        
                        entities.append(ExtractedEntity(
                            text=match.group(0),
                            label="PRICE",
                            start=match.start(),
                            end=match.end(),
                            confidence=0.95,
                            context={
                                "value": price_in_rupees,
                                "operator": "=",
                                "unit": unit,
                                "original_value": value,
                                "semantic_meaning": "exact"
                            }
                        ))
                        print(f"🔍 INTENT-DRIVEN: Found PRICE entity (exact): '{match.group(0)}' = = {price_in_rupees} rupees")
                        found_price = True
                        break
        
        # FALLBACK: If no price entity found, try to extract any price-related information
        if not found_price:
            self._extract_price_fallback(text_lower, entities)
    
    def _extract_area_entities_with_context(self, doc, entities, text_lower):
        """INTENT-DRIVEN: Extract carpet area entities with semantic context"""
        # INTENT-DRIVEN: Look for area-related semantic patterns
        area_patterns = [
            # Patterns with sqft
            r'carpet\s+area\s+(?:under|below|less\s+than)\s+(\d{3,5})\s*sqft',
            r'carpet\s+area\s+(?:above|over|more\s+than)\s+(\d{3,5})\s*sqft',
            r'carpet\s+area\s+(\d{3,5})\s*sqft',
            r'(\d{3,5})\s*sqft\s+(?:carpet\s+)?area',
            r'area\s+(?:under|below|less\s+than)\s+(\d{3,5})\s*sqft',
            r'area\s+(?:above|over|more\s+than)\s+(\d{3,5})\s*sqft',
            # Patterns without sqft (common in natural language)
            r'carpet\s+area\s+(?:under|below|less\s+than)\s+(\d{3,5})',
            r'carpet\s+area\s+(?:above|over|more\s+than)\s+(\d{3,5})',
            r'carpet\s+area\s+(\d{3,5})',
            r'area\s+(?:under|below|less\s+than)\s+(\d{3,5})',
            r'area\s+(?:above|over|more\s+than)\s+(\d{3,5})',
            # Direct number patterns for area
            r'(\d{3,5})\s+(?:sqft|square\s+feet)\s+(?:carpet\s+)?area'
        ]
        
        for pattern in area_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                # INTENT-DRIVEN: Validate this is about area, not price
                if self._is_area_context(text_lower, match.start(), match.end()):
                    value = int(match.group(1))
                    operator = self._extract_area_operator(match.group(0))
                    
                    entities.append(ExtractedEntity(
                        text=match.group(0),
                        label="CARPET_AREA",
                        start=match.start(),
                        end=match.end(),
                        confidence=0.9,
                        context={
                            "value": value,
                            "operator": operator,
                            "unit": "sqft",
                            "semantic_meaning": "carpet_area"
                        }
                    ))
                    print(f"🔍 INTENT-DRIVEN: Found CARPET_AREA entity: '{match.group(0)}' = {operator} {value} sqft")
    
    def _extract_amenity_entities(self, doc, entities, text_lower):
        """INTENT-DRIVEN: Extract amenity entities with semantic context"""
        amenity_keywords = [
            "gym", "swimming pool", "parking", "lift", "security", "garden", 
            "playground", "clubhouse", "hospital", "school", "metro", "railway", "airport", "mall", "park"
        ]
        
        for amenity in amenity_keywords:
            if amenity in text_lower:
                # INTENT-DRIVEN: Check if this amenity is actually being requested
                context_words = self._get_context_words(text_lower, text_lower.find(amenity), text_lower.find(amenity) + len(amenity), 15)
                if any(word in context_words for word in ["with", "having", "including", "near", "close", "nearby"]):
                    entities.append(ExtractedEntity(
                        text=amenity,
                        label="AMENITY",
                        start=text_lower.find(amenity),
                        end=text_lower.find(amenity) + len(amenity),
                        confidence=0.85,
                        context={"type": "amenity", "semantic_meaning": "required_feature"}
                    ))
                    print(f"🔍 INTENT-DRIVEN: Found AMENITY entity: '{amenity}'")
    
    def _is_price_context(self, text_lower, start, end):
        """INTENT-DRIVEN: Determine if the matched text is actually about price"""
        # Get surrounding context
        context_start = max(0, start - 20)
        context_end = min(len(text_lower), end + 20)
        context = text_lower[context_start:context_end]
        
        # Price indicators
        price_indicators = ["price", "cost", "budget", "lakh", "crore", "rupee", "rs", "₹"]
        
        # Area indicators (to avoid confusion)
        area_indicators = ["sqft", "square feet", "area", "carpet", "built-up"]
        
        # Check if context contains price indicators
        has_price_context = any(indicator in context for indicator in price_indicators)
        
        # Check if context contains area indicators (conflicting)
        has_area_context = any(indicator in context for indicator in area_indicators)
        
        # INTENT-DRIVEN: If it has price context and NO area context, it's about price
        return has_price_context and not has_area_context
    
    def _is_area_context(self, text_lower, start, end):
        """INTENT-DRIVEN: Determine if the matched text is actually about area"""
        context_start = max(0, start - 20)
        context_end = min(len(text_lower), end + 20)
        context = text_lower[context_start:context_end]
        
        area_indicators = ["sqft", "square feet", "area", "carpet", "built-up", "size"]
        price_indicators = ["price", "cost", "budget", "lakh", "crore", "rupee"]
        
        has_area_context = any(indicator in context for indicator in area_indicators)
        has_price_context = any(indicator in context for indicator in price_indicators)
        
        return has_area_context and not has_price_context
    
    def _extract_area_operator(self, text):
        """INTENT-DRIVEN: Extract operator from area text"""
        if any(word in text for word in ["under", "below", "less than"]):
            return "<"
        elif any(word in text for word in ["above", "over", "more than"]):
            return ">"
        else:
            return "="
    
    def _get_context_words(self, text_lower, start, end, window_size):
        """Get words around a match for context analysis"""
        context_start = max(0, start - window_size)
        context_end = min(len(text_lower), end + window_size)
        return text_lower[context_start:context_end]
    
    def _convert_to_rupees(self, value, unit):
        """Convert price to rupees based on unit"""
        if 'lakh' in unit:
            return value * 100000
        elif 'crore' in unit or 'cr' in unit:
            return value * 10000000
        elif 'thousand' in unit:
            return value * 1000
        else:
            return value
    
    def _extract_price_fallback(self, text_lower: str, entities: List[ExtractedEntity]):
        """FALLBACK: Extract price information using simpler pattern matching"""
        print(f"🔍 FALLBACK: Attempting to extract price from: '{text_lower}'")
        
        # Simple fallback patterns for common price expressions
        fallback_patterns = [
            # "under X crore/lakh" variations
            r'(?:under|below|less\s+than)\s+(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)',
            # "above X crore/lakh" variations  
            r'(?:above|over|more\s+than)\s+(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)',
            # "X crore/lakh" (exact)
            r'(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)'
        ]
        
        for i, pattern in enumerate(fallback_patterns):
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                try:
                    value = float(match.group(1))
                    unit = match.group(0).split()[-1]  # Get the unit from the matched text
                    
                    # Determine operator based on pattern index
                    if i == 0:  # under/below/less than
                        operator = "<"
                        semantic_meaning = "less_than"
                    elif i == 1:  # above/over/more than
                        operator = ">"
                        semantic_meaning = "more_than"
                    else:  # exact
                        operator = "="
                        semantic_meaning = "exact"
                    
                    price_in_rupees = self._convert_to_rupees(value, unit)
                    
                    entities.append(ExtractedEntity(
                        text=match.group(0),
                        label="PRICE",
                        start=text_lower.find(match.group(0)),
                        end=text_lower.find(match.group(0)) + len(match.group(0)),
                        confidence=0.8,  # Lower confidence for fallback
                        context={
                            "value": price_in_rupees,
                            "operator": operator,
                            "unit": unit,
                            "original_value": value,
                            "semantic_meaning": semantic_meaning
                        }
                    ))
                    print(f"🔍 FALLBACK: Found PRICE entity: '{match.group(0)}' = {operator} {price_in_rupees} rupees")
                    return  # Exit after first successful match
                    
                except (ValueError, IndexError) as e:
                    print(f"🔍 FALLBACK: Error parsing fallback pattern: {e}")
                    continue
    
    def classify_intent(self, text: str) -> Tuple[str, float]:
        """INTENT-DRIVEN: Classify intent based on semantic understanding"""
        text_lower = text.lower()
        
        # INTENT-DRIVEN: Calculate confidence based on semantic indicators, not just keyword counting
        intent_scores = {}
        
        for intent_name, intent_info in self.intents.items():
            score = 0
            
            # Check semantic indicators (primary)
            for indicator in intent_info["semantic_indicators"]:
                if indicator in text_lower:
                    score += 2  # Higher weight for semantic indicators
            
            # Check context indicators (secondary)
            for indicator in intent_info["context_indicators"]:
                if indicator in text_lower:
                    score += 1  # Lower weight for context indicators
            
            if score > 0:
                # Normalize score
                intent_scores[intent_name] = min(score / (len(intent_info["semantic_indicators"]) + len(intent_info["context_indicators"])), 1.0)
        
        if not intent_scores:
            return "UNKNOWN", 0.0
        
        # Return the intent with highest confidence
        best_intent = max(intent_scores.items(), key=lambda x: x[1])
        return best_intent[0], best_intent[1]
    
    def process_query(self, query: str) -> QueryIntent:
        """INTENT-DRIVEN: Process query with semantic understanding"""
        # Extract entities with full context
        entities = self.extract_entities_with_context(query)
        
        # Classify intent semantically
        intent, confidence = self.classify_intent(query)
        
        return QueryIntent(
            intent=intent,
            confidence=confidence,
            entities=entities
        )
    
    def get_search_criteria(self, query: str) -> Dict:
        """INTENT-DRIVEN: Convert semantically understood query to search criteria"""
        intent_result = self.process_query(query)
        
        criteria = {
            "intent": intent_result.intent,
            "confidence": intent_result.confidence,
            "filters": {}
        }
        
        # INTENT-DRIVEN: Extract filters from entities with their semantic context
        for entity in intent_result.entities:
            if entity.label == "LOCATION":
                criteria["filters"]["location"] = entity.text
            elif entity.label == "BHK":
                criteria["filters"]["bhk"] = entity.context["value"]
                criteria["filters"]["bhk_operator"] = entity.context["operator"]
            elif entity.label == "PRICE":
                # Use the semantic context directly - no need for separate extraction
                criteria["filters"]["price_range"] = entity.text
                criteria["filters"]["price_operator"] = entity.context["operator"]
                criteria["filters"]["price_value"] = entity.context["value"]
            elif entity.label == "CARPET_AREA":
                criteria["filters"]["carpet_area"] = entity.text
                criteria["filters"]["area_operator"] = entity.context["operator"]
                criteria["filters"]["area_value"] = entity.context["value"]
            elif entity.label == "AMENITY":
                if "amenities" not in criteria["filters"]:
                    criteria["filters"]["amenities"] = []
                criteria["filters"]["amenities"].append(entity.text)
        
        return criteria
    
    def get_suggestions(self, partial_query: str) -> List[str]:
        """Get search suggestions based on partial query"""
        suggestions = []
        
        if "bhk" in partial_query.lower():
            suggestions.extend(["1 BHK", "2 BHK", "3 BHK", "4 BHK", "5+ BHK"])
        
        if any(word in partial_query.lower() for word in ["mumbai", "delhi", "bangalore"]):
            suggestions.extend(["Mumbai", "Delhi", "Bangalore", "Pune", "Hyderabad"])
        
        if any(word in partial_query.lower() for word in ["near", "close", "metro"]):
            suggestions.extend(["Near Metro", "Near Hospital", "Near School", "Near Mall"])
        
        return suggestions[:5]  # Return top 5 suggestions

# Example usage and testing
if __name__ == "__main__":
    # Initialize NLP engine
    nlp_engine = RealEstateNLPEngine()
    
    # Test queries
    test_queries = [
        "I want a 2BHK flat in Mumbai",
        "Show me properties near metro station",
        "What's the price of 3BHK in Bandra?",
        "Book a site visit for tomorrow",
        "Compare these two projects"
    ]
    
    print("Testing INTENT-DRIVEN NLP Engine:")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = nlp_engine.process_query(query)
        print(f"Intent: {result.intent} (confidence: {result.confidence:.2f})")
        print(f"Entities: {[f'{e.text}({e.label})' for e in result.entities]}")
        
        criteria = nlp_engine.get_search_criteria(query)
        print(f"Search Criteria: {criteria['filters']}")
