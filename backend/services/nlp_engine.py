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

@dataclass
class QueryIntent:
    """Represents the detected intent and confidence"""
    intent: str
    confidence: float
    entities: List[ExtractedEntity]

class RealEstateNLPEngine:
    """NLP Engine for Real Estate queries using spaCy"""
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        """Initialize the NLP engine with spaCy model"""
        try:
            self.nlp = spacy.load(model_name)
            print(f"✅ Loaded spaCy model: {model_name}")
        except OSError:
            print(f"❌ Model {model_name} not found. Please install it with: python -m spacy download {model_name}")
            raise
        
        # Define real estate specific intents
        self.intents = {
            "SEARCH_PROPERTY": [
                "find", "search", "looking for", "want", "need", "show me", "get me",
                "available", "properties", "flats", "houses", "apartments"
            ],
            "FILTER_BY_AMENITY": [
                "near", "close to", "nearby", "within", "distance", "metro", "hospital",
                "school", "office", "station", "mall", "park", "garden"
            ],
            "COMPARE_PROPERTIES": [
                "compare", "difference", "vs", "versus", "better", "best", "which one"
            ],
            "BOOK_VIEWING": [
                "book", "schedule", "appointment", "visit", "viewing", "tour", "see",
                "tomorrow", "next week", "this weekend"
            ],
            "GET_DETAILS": [
                "what", "details", "information", "tell me", "how much", "price",
                "area", "bhk", "floor", "status", "completion"
            ],
            "PRICE_QUERY": [
                "price", "cost", "budget", "affordable", "expensive", "cheap",
                "per sq ft", "total cost", "booking amount"
            ]
        }
        
        # Define entity patterns for real estate domain
        self.entity_patterns = {
            "LOCATION": {
                "cities": ["mumbai", "delhi", "bangalore", "pune", "hyderabad", "chennai", "kolkata", "ahmedabad"],
                "localities": ["bandra", "andheri", "powai", "thane", "navi mumbai", "gurgaon", "noida"],
                "landmarks": ["airport", "metro", "railway", "bus stand", "mall", "hospital", "school"]
            },
            "PROPERTY_TYPE": {
                "bhk": ["1bhk", "2bhk", "3bhk", "4bhk", "5bhk", "1 bhk", "2 bhk", "3 bhk"],
                "property_types": ["flat", "apartment", "house", "villa", "penthouse", "studio"]
            },
            "AMENITY": {
                "basic": ["parking", "lift", "security", "water", "power"],
                "luxury": ["swimming pool", "gym", "clubhouse", "garden", "playground"],
                "security": ["cctv", "guard", "gated", "24x7 security"],
                "recreation": ["park", "playground", "clubhouse", "community hall"]
            },
            "PRICE": {
                "ranges": ["under 50 lakhs", "50-100 lakhs", "1-2 crores", "above 2 crores"],
                "units": ["lakhs", "crores", "per sq ft", "sq ft"]
            },
            "TEMPORAL": {
                "dates": ["today", "tomorrow", "next week", "this month", "next month"],
                "time": ["morning", "afternoon", "evening", "9am", "2pm"]
            }
        }
    
    def extract_entities(self, text: str) -> List[ExtractedEntity]:
        """Extract entities from the query text"""
        entities = []
        text_lower = text.lower()
        
        # Process with spaCy
        doc = self.nlp(text_lower)
        
        # Extract named entities
        for ent in doc.ents:
            if ent.label_ in ["GPE", "LOC", "FAC"]:  # Location entities
                entities.append(ExtractedEntity(
                    text=ent.text,
                    label="LOCATION",
                    start=ent.start_char,
                    end=ent.end_char,
                    confidence=0.9
                ))
        
        # Extract custom entities using patterns
        for entity_type, patterns in self.entity_patterns.items():
            for category, values in patterns.items():
                for value in values:
                    if value in text_lower:
                        start = text_lower.find(value)
                        if start != -1:
                            entities.append(ExtractedEntity(
                                text=value,
                                label=entity_type,
                                start=start,
                                end=start + len(value),
                                confidence=0.8
                            ))
        
        # Extract numbers (BHK, price, area) with improved context
        numbers = re.findall(r'\d+(?:\.\d+)?', text)
        for num in numbers:
            # Check if it's BHK - look for context around the number
            num_start = text.find(num)
            num_end = num_start + len(num)
            
            # Look for BHK context in a window around the number
            context_start = max(0, num_start - 10)
            context_end = min(len(text), num_end + 10)
            context = text[context_start:context_end].lower()
            
            if any(bhk in context for bhk in ["bhk", "bedroom", "bed room"]):
                entities.append(ExtractedEntity(
                    text=num,
                    label="BHK",
                    start=num_start,
                    end=num_end,
                    confidence=0.9
                ))
        
        # Extract price ranges with comprehensive patterns
        price_patterns = [
            # Under/Below/Less than patterns
            r'under\s+(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)',
            r'below\s+(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)',
            r'less\s+than\s+(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)',
            r'<=\s*(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)',
            r'<=\s*(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)',
            
            # Above/Over/More than patterns
            r'above\s+(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)',
            r'more\s+than\s+(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)',
            r'over\s+(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)',
            r'>=\s*(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)',
            r'>=\s*(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)',
            
            # Range patterns
            r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)',
            r'(\d+(?:\.\d+)?)\s*to\s*(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)',
            r'between\s+(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|crore|crores)\s*to\s*(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|crore|crores)',
            
            # Exact patterns
            r'equal\s+to\s+(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)',
            r'=\s*(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)',
            
            # Greater/Less than with symbols
            r'>\s*(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)',
            r'<\s*(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)'
        ]
        
        for pattern in price_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                entities.append(ExtractedEntity(
                    text=match.group(0),
                    label="PRICE",
                    start=match.start(),
                    end=match.end(),
                    confidence=0.95
                ))
        
        # Extract BHK with comparison operators
        bhk_patterns = [
            r'bhk\s*>=?\s*(\d+(?:\.\d+)?)',      # BHK >= X
            r'bhk\s*<=?\s*(\d+(?:\.\d+)?)',      # BHK <= X
            r'bhk\s*>\s*(\d+(?:\.\d+)?)',        # BHK > X
            r'bhk\s*<\s*(\d+(?:\.\d+)?)',        # BHK < X
            r'(\d+(?:\.\d+)?)\s*bhk',            # X BHK
            r'(\d+(?:\.\d+)?)\s*bedroom',        # X bedroom
            r'(\d+(?:\.\d+)?)\s*bed\s*room',     # X bed room
        ]
        
        for pattern in bhk_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                entities.append(ExtractedEntity(
                    text=match.group(0),
                    label="BHK",
                    start=match.start(),
                    end=match.end(),
                    confidence=0.9
                ))
        
        # Extract carpet area with comparison operators
        carpet_area_patterns = [
            r'carpet\s+area\s+(?:under|below|less\s+than)\s+(\d+)\s*sqft',
            r'carpet\s+area\s+(?:above|over|more\s+than)\s+(\d+)\s*sqft',
            r'carpet\s+area\s+between\s+(\d+)\s*(?:to|-)\s*(\d+)\s*sqft',
            r'carpet\s+area\s*>=?\s*(\d+)\s*sqft',
            r'carpet\s+area\s*<=?\s*(\d+)\s*sqft',
            r'carpet\s+area\s*>\s*(\d+)\s*sqft',
            r'carpet\s+area\s*<\s*(\d+)\s*sqft',
            r'area\s+(?:under|below|less\s+than)\s+(\d+)\s*sqft',
            r'area\s+(?:above|over|more\s+than)\s+(\d+)\s*sqft',
            r'area\s+between\s+(\d+)\s*(?:to|-)\s*(\d+)\s*sqft',
            r'area\s*>=?\s*(\d+)\s*sqft',
            r'area\s*<=?\s*(\d+)\s*sqft',
            r'area\s*>\s*(\d+)\s*sqft',
            r'area\s*<\s*(\d+)\s*sqft',
            r'(\d+)\s*sqft\s+(?:and\s+)?(?:above|below|under|over)',
            r'(\d+)\s*sqft\s+to\s+(\d+)\s*sqft'
        ]
        
        for pattern in carpet_area_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                entities.append(ExtractedEntity(
                    text=match.group(0),
                    label="CARPET_AREA",
                    start=match.start(),
                    end=match.end(),
                    confidence=0.9
                ))
        
        return entities
    
    def classify_intent(self, text: str) -> Tuple[str, float]:
        """Classify the intent of the query"""
        text_lower = text.lower()
        
        # Calculate confidence scores for each intent
        intent_scores = {}
        
        for intent, keywords in self.intents.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            
            if score > 0:
                intent_scores[intent] = score / len(keywords)
        
        if not intent_scores:
            return "UNKNOWN", 0.0
        
        # Return the intent with highest confidence
        best_intent = max(intent_scores.items(), key=lambda x: x[1])
        return best_intent[0], best_intent[1]
    
    def process_query(self, query: str) -> QueryIntent:
        """Process a natural language query and return intent and entities"""
        # Extract entities
        entities = self.extract_entities(query)
        
        # Classify intent
        intent, confidence = self.classify_intent(query)
        
        return QueryIntent(
            intent=intent,
            confidence=confidence,
            entities=entities
        )
    
    def get_search_criteria(self, query: str) -> Dict:
        """Convert NLP query to search criteria with improved operator handling"""
        intent_result = self.process_query(query)
        
        criteria = {
            "intent": intent_result.intent,
            "confidence": intent_result.confidence,
            "filters": {}
        }
        
        # Extract filters from entities
        for entity in intent_result.entities:
            if entity.label == "LOCATION":
                criteria["filters"]["location"] = entity.text
            elif entity.label == "BHK":
                # Extract BHK value and operator
                bhk_info = self.extract_bhk_with_operator(entity.text)
                if bhk_info:
                    criteria["filters"]["bhk"] = bhk_info["value"]
                    criteria["filters"]["bhk_operator"] = bhk_info["operator"]
            elif entity.label == "PROPERTY_TYPE":
                criteria["filters"]["property_type"] = entity.text
            elif entity.label == "PRICE":
                # Extract price with operator
                price_info = self.extract_price_with_operator(entity.text)
                if price_info:
                    criteria["filters"]["price_range"] = price_info["text"]
                    criteria["filters"]["price_operator"] = price_info["operator"]
                    criteria["filters"]["price_value"] = price_info["value"]
            elif entity.label == "CARPET_AREA":
                # Extract carpet area with operator
                area_info = self.extract_area_with_operator(entity.text)
                if area_info:
                    criteria["filters"]["carpet_area"] = area_info["text"]
                    criteria["filters"]["area_operator"] = area_info["operator"]
                    criteria["filters"]["area_value"] = area_info["value"]
            elif entity.label == "AMENITY":
                if "amenities" not in criteria["filters"]:
                    criteria["filters"]["amenities"] = []
                criteria["filters"]["amenities"].append(entity.text)
        
        return criteria
    
    def extract_bhk_with_operator(self, text: str) -> Optional[Dict]:
        """Extract BHK value and comparison operator"""
        text_lower = text.lower()
        
        # Patterns for BHK with operators
        patterns = [
            (r'bhk\s*>=?\s*(\d+(?:\.\d+)?)', '>='),
            (r'bhk\s*<=?\s*(\d+(?:\.\d+)?)', '<='),
            (r'bhk\s*>\s*(\d+(?:\.\d+)?)', '>'),
            (r'bhk\s*<\s*(\d+(?:\.\d+)?)', '<'),
            (r'(\d+(?:\.\d+)?)\s*bhk', '='),
            (r'(\d+(?:\.\d+)?)\s*bedroom', '='),
            (r'(\d+(?:\.\d+)?)\s*bed\s*room', '='),
        ]
        
        for pattern, operator in patterns:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    value = float(match.group(1))
                    return {
                        "value": value,
                        "operator": operator,
                        "text": text
                    }
                except ValueError:
                    continue
        
        return None
    
    def extract_price_with_operator(self, text: str) -> Optional[Dict]:
        """Extract price value and comparison operator"""
        text_lower = text.lower()
        
        # Patterns for price with operators
        patterns = [
            (r'under\s+(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)', '<'),
            (r'below\s+(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)', '<'),
            (r'less\s+than\s+(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)', '<'),
            (r'<=\s*(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)', '<='),
            (r'above\s+(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)', '>'),
            (r'more\s+than\s+(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)', '>'),
            (r'over\s+(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)', '>'),
            (r'>=\s*(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)', '>='),
            (r'>\s*(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)', '>'),
            (r'<\s*(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)', '<'),
            (r'equal\s+to\s+(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)', '='),
            (r'=\s*(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)', '='),
        ]
        
        for pattern, operator in patterns:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    value = float(match.group(1))
                    # Convert to rupees
                    if 'lakh' in text_lower:
                        value = value * 100000
                    elif 'crore' in text_lower or 'cr' in text_lower:
                        value = value * 10000000
                    
                    return {
                        "value": value,
                        "operator": operator,
                        "text": text
                    }
                except ValueError:
                    continue
        
        return None
    
    def extract_area_with_operator(self, text: str) -> Optional[Dict]:
        """Extract carpet area value and comparison operator"""
        text_lower = text.lower()
        
        # Patterns for carpet area with operators
        patterns = [
            (r'carpet\s+area\s+(?:under|below|less\s+than)\s+(\d+)\s*sqft', '<'),
            (r'carpet\s+area\s+(?:above|over|more\s+than)\s+(\d+)\s*sqft', '>'),
            (r'carpet\s+area\s*>=?\s*(\d+)\s*sqft', '>='),
            (r'carpet\s+area\s*<=?\s*(\d+)\s*sqft', '<='),
            (r'carpet\s+area\s*>\s*(\d+)\s*sqft', '>'),
            (r'carpet\s+area\s*<\s*(\d+)\s*sqft', '<'),
            (r'area\s+(?:under|below|less\s+than)\s+(\d+)\s*sqft', '<'),
            (r'area\s+(?:above|over|more\s+than)\s+(\d+)\s*sqft', '>'),
            (r'area\s*>=?\s*(\d+)\s*sqft', '>='),
            (r'area\s*<=?\s*(\d+)\s*sqft', '<='),
            (r'area\s*>\s*(\d+)\s*sqft', '>'),
            (r'area\s*<\s*(\d+)\s*sqft', '<'),
        ]
        
        for pattern, operator in patterns:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    value = int(match.group(1))
                    return {
                        "value": value,
                        "operator": operator,
                        "text": text
                    }
                except ValueError:
                    continue
        
        return None
    
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
    
    print("Testing NLP Engine:")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = nlp_engine.process_query(query)
        print(f"Intent: {result.intent} (confidence: {result.confidence:.2f})")
        print(f"Entities: {[f'{e.text}({e.label})' for e in result.entities]}")
        
        criteria = nlp_engine.get_search_criteria(query)
        print(f"Search Criteria: {criteria['filters']}")
