import json
import logging
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

@dataclass
class IntentClassification:
    """Intent classification result"""
    intent: str
    confidence: float
    matched_pattern: str
    entities: Dict[str, Any]
    suggestions: List[str]
    fallback_response: str

@dataclass
class IntentPattern:
    """Intent pattern structure"""
    pattern: str
    variations: List[str]
    confidence: float
    entity_extractors: List[str]
    fallback_response: str

class EnhancedIntentClassifier:
    """Enhanced intent classifier using comprehensive pattern matching"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.intent_patterns = self._initialize_intent_patterns()
        self.vectorizer = None
        self.pattern_vectors = None
        self._build_pattern_vectors()
    
    def _initialize_intent_patterns(self) -> Dict[str, List[IntentPattern]]:
        """Initialize comprehensive intent patterns"""
        return {
            "SEARCH_PROPERTY": [
                IntentPattern(
                    pattern="properties in [location]",
                    variations=[
                        "properties in {location}",
                        "houses in {location}",
                        "flats in {location}",
                        "{location} mein properties",
                        "{location} mein ghar",
                        "show me {location} properties",
                        "find houses in {location}",
                        "search properties in {location}",
                        "properties available in {location}",
                        "{location} properties",
                        "properties {location}",
                        "ghar {location} mein",
                        "properties {location} mein",
                        "search {location} properties",
                        "find {location} properties"
                    ],
                    confidence=0.95,
                    entity_extractors=["location"],
                    fallback_response="I can help you search for properties. Which area are you interested in?"
                ),
                IntentPattern(
                    pattern="show me [property_type]",
                    variations=[
                        "show me {property_type}",
                        "find {property_type}",
                        "search for {property_type}",
                        "{property_type} properties",
                        "{property_type} available",
                        "{property_type} properties in {location}",
                        "{property_type} {location} mein",
                        "properties {property_type}",
                        "ghar {property_type}",
                        "{property_type} ghar",
                        "search {property_type}",
                        "find {property_type} properties"
                    ],
                    confidence=0.90,
                    entity_extractors=["property_type", "location"],
                    fallback_response="I can help you find properties. What type of property are you looking for?"
                ),
                IntentPattern(
                    pattern="properties under [price]",
                    variations=[
                        "properties under {price}",
                        "houses under {price}",
                        "flats under {price}",
                        "{price} mein properties",
                        "{price} budget properties",
                        "properties {price}",
                        "ghar {price} mein",
                        "properties {price} budget",
                        "affordable properties",
                        "budget properties",
                        "cheap properties",
                        "sasta ghar",
                        "kam daam mein properties"
                    ],
                    confidence=0.88,
                    entity_extractors=["price_range"],
                    fallback_response="I can help you find properties in your budget. What's your budget range?"
                )
            ],
            
            "KNOWLEDGE_QUERY": [
                IntentPattern(
                    pattern="what is [topic]",
                    variations=[
                        "what is {topic}",
                        "what's {topic}",
                        "what is the meaning of {topic}",
                        "explain {topic}",
                        "define {topic}",
                        "tell me about {topic}",
                        "describe {topic}",
                        "what does {topic} mean",
                        "meaning of {topic}",
                        "definition of {topic}",
                        "{topic} kya hai",
                        "{topic} kya hota hai",
                        "{topic} samjhao",
                        "{topic} explain kar",
                        "{topic} batana",
                        "explain {topic} in detail",
                        "{topic} ke baare mein batao"
                    ],
                    confidence=0.95,
                    entity_extractors=["topic"],
                    fallback_response="I can help you understand real estate terms. What would you like to know about?"
                ),
                IntentPattern(
                    pattern="how to [action]",
                    variations=[
                        "how to {action}",
                        "how do i {action}",
                        "steps to {action}",
                        "process of {action}",
                        "way to {action}",
                        "{action} kaise kare",
                        "{action} kaise",
                        "{action} process kya hai",
                        "{action} steps batana",
                        "process for {action}",
                        "steps for {action}",
                        "guide for {action}"
                    ],
                    confidence=0.92,
                    entity_extractors=["action"],
                    fallback_response="I can guide you through various real estate processes. What would you like to learn about?"
                )
            ],
            
            "CALCULATOR_QUERY": [
                IntentPattern(
                    pattern="calculate [calculation_type]",
                    variations=[
                        "calculate {calculation_type}",
                        "calculate {calculation_type} for {amount}",
                        "{calculation_type} calculator",
                        "{calculation_type} calculation",
                        "compute {calculation_type}",
                        "work out {calculation_type}",
                        "{calculation_type} for {amount}",
                        "{amount} ka {calculation_type}",
                        "{calculation_type} {amount} ke liye",
                        "emi calculator",
                        "loan calculator",
                        "stamp duty calculator",
                        "registration fee calculator"
                    ],
                    confidence=0.90,
                    entity_extractors=["calculation_type", "amount"],
                    fallback_response="I can help you calculate various real estate costs. What would you like to calculate?"
                )
            ],
            
            "LOCATION_SEARCH": [
                IntentPattern(
                    pattern="properties in [direction] pune",
                    variations=[
                        "properties in {direction} pune",
                        "houses in {direction} pune",
                        "flats in {direction} pune",
                        "{direction} pune mein properties",
                        "{direction} pune mein ghar",
                        "show me {direction} pune properties",
                        "{direction} pune properties",
                        "properties {direction} pune",
                        "ghar {direction} pune mein",
                        "{direction} side properties",
                        "{direction} area properties",
                        "{direction} pune area"
                    ],
                    confidence=0.93,
                    entity_extractors=["direction"],
                    fallback_response="I can help you find properties in different areas of Pune. Which direction are you interested in?"
                )
            ],
            
            "PRICE_SEARCH": [
                IntentPattern(
                    pattern="properties [price_range]",
                    variations=[
                        "properties {price_range}",
                        "houses {price_range}",
                        "flats {price_range}",
                        "{price_range} properties",
                        "{price_range} houses",
                        "{price_range} flats",
                        "properties in {price_range}",
                        "ghar {price_range} mein",
                        "properties {price_range} budget",
                        "{price_range} budget properties",
                        "affordable properties",
                        "luxury properties",
                        "premium properties"
                    ],
                    confidence=0.89,
                    entity_extractors=["price_range"],
                    fallback_response="I can help you find properties in different price ranges. What's your budget?"
                )
            ],
            
            "AMENITY_SEARCH": [
                IntentPattern(
                    pattern="properties with [amenity]",
                    variations=[
                        "properties with {amenity}",
                        "houses with {amenity}",
                        "flats with {amenity}",
                        "{amenity} properties",
                        "properties {amenity}",
                        "ghar {amenity} ke saath",
                        "properties {amenity} facilities",
                        "{amenity} facilities properties",
                        "properties having {amenity}",
                        "{amenity} wale properties"
                    ],
                    confidence=0.87,
                    entity_extractors=["amenity"],
                    fallback_response="I can help you find properties with specific amenities. What facilities are you looking for?"
                )
            ]
        }
    
    def _build_pattern_vectors(self):
        """Build TF-IDF vectors for pattern matching"""
        all_patterns = []
        pattern_mapping = []
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                # Add main pattern
                all_patterns.append(pattern.pattern)
                pattern_mapping.append((intent, pattern))
                
                # Add variations
                for variation in pattern.variations:
                    all_patterns.append(variation)
                    pattern_mapping.append((intent, pattern))
        
        if all_patterns:
            self.vectorizer = TfidfVectorizer(
                ngram_range=(1, 3),
                stop_words='english',
                max_features=1000
            )
            self.pattern_vectors = self.vectorizer.fit_transform(all_patterns)
            self.pattern_mapping = pattern_mapping
    
    def classify_intent(self, user_input: str) -> IntentClassification:
        """Classify user intent using comprehensive pattern matching"""
        user_input_lower = user_input.lower().strip()
        
        # Try exact pattern matching first
        exact_match = self._exact_pattern_match(user_input_lower)
        if exact_match:
            return exact_match
        
        # Try semantic similarity matching
        semantic_match = self._semantic_similarity_match(user_input_lower)
        if semantic_match and semantic_match.confidence > 0.85:
            return semantic_match
        
        # Try partial pattern matching
        partial_match = self._partial_pattern_match(user_input_lower)
        if partial_match and partial_match.confidence > 0.80:
            return partial_match
        
        # No confident match found
        return self._generate_fallback_response(user_input_lower)
    
    def _exact_pattern_match(self, user_input: str) -> Optional[IntentClassification]:
        """Try exact pattern matching"""
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                # Check main pattern
                if self._matches_pattern(user_input, pattern.pattern):
                    return self._create_classification(intent, pattern, 1.0, user_input)
                
                # Check variations
                for variation in pattern.variations:
                    if self._matches_pattern(user_input, variation):
                        return self._create_classification(intent, pattern, 0.95, user_input)
        
        return None
    
    def _semantic_similarity_match(self, user_input: str) -> Optional[IntentClassification]:
        """Try semantic similarity matching using TF-IDF"""
        if not self.vectorizer or not self.pattern_vectors:
            return None
        
        try:
            # Transform user input
            user_vector = self.vectorizer.transform([user_input])
            
            # Calculate similarities
            similarities = cosine_similarity(user_vector, self.pattern_vectors).flatten()
            
            # Find best match
            best_idx = np.argmax(similarities)
            best_similarity = similarities[best_idx]
            
            if best_similarity > 0.85:
                intent, pattern = self.pattern_mapping[best_idx]
                return self._create_classification(intent, pattern, best_similarity, user_input)
        
        except Exception as e:
            self.logger.warning(f"Semantic similarity matching failed: {e}")
        
        return None
    
    def _partial_pattern_match(self, user_input: str) -> Optional[IntentClassification]:
        """Try partial pattern matching"""
        best_match = None
        best_confidence = 0.0
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                confidence = self._calculate_partial_match_confidence(user_input, pattern)
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_match = (intent, pattern, confidence)
        
        if best_match and best_match[2] > 0.80:
            intent, pattern, confidence = best_match
            return self._create_classification(intent, pattern, confidence, user_input)
        
        return None
    
    def _matches_pattern(self, user_input: str, pattern: str) -> bool:
        """Check if user input matches a pattern exactly"""
        # Replace placeholders with regex patterns
        regex_pattern = pattern.replace("[location]", r"\w+")
        regex_pattern = regex_pattern.replace("[property_type]", r"\w+")
        regex_pattern = regex_pattern.replace("[price_range]", r"\w+")
        regex_pattern = regex_pattern.replace("[direction]", r"\w+")
        regex_pattern = regex_pattern.replace("[topic]", r"\w+")
        regex_pattern = regex_pattern.replace("[action]", r"\w+")
        regex_pattern = regex_pattern.replace("[calculation_type]", r"\w+")
        regex_pattern = regex_pattern.replace("[amount]", r"\w+")
        regex_pattern = regex_pattern.replace("[amenity]", r"\w+")
        
        # Add word boundaries
        regex_pattern = r"\b" + regex_pattern + r"\b"
        
        return bool(re.search(regex_pattern, user_input, re.IGNORECASE))
    
    def _calculate_partial_match_confidence(self, user_input: str, pattern: IntentPattern) -> float:
        """Calculate confidence for partial pattern matching"""
        user_words = set(user_input.split())
        
        # Check main pattern
        pattern_words = set(pattern.pattern.split())
        main_confidence = len(user_words.intersection(pattern_words)) / len(pattern_words)
        
        # Check variations
        variation_confidences = []
        for variation in pattern.variations:
            variation_words = set(variation.split())
            confidence = len(user_words.intersection(variation_words)) / len(variation_words)
            variation_confidences.append(confidence)
        
        # Return best confidence
        return max(main_confidence, max(variation_confidences) if variation_confidences else 0)
    
    def _create_classification(self, intent: str, pattern: IntentPattern, confidence: float, user_input: str) -> IntentClassification:
        """Create intent classification result"""
        # Extract entities
        entities = self._extract_entities(user_input, pattern)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(intent, entities)
        
        return IntentClassification(
            intent=intent,
            confidence=confidence,
            matched_pattern=pattern.pattern,
            entities=entities,
            suggestions=suggestions,
            fallback_response=pattern.fallback_response
        )
    
    def _extract_entities(self, user_input: str, pattern: IntentPattern) -> Dict[str, Any]:
        """Extract entities from user input based on pattern"""
        entities = {}
        
        for extractor in pattern.entity_extractors:
            if extractor == "location":
                entities["location"] = self._extract_location(user_input)
            elif extractor == "property_type":
                entities["property_type"] = self._extract_property_type(user_input)
            elif extractor == "price_range":
                entities["price_range"] = self._extract_price_range(user_input)
            elif extractor == "direction":
                entities["direction"] = self._extract_direction(user_input)
            elif extractor == "topic":
                entities["topic"] = self._extract_topic(user_input)
            elif extractor == "action":
                entities["action"] = self._extract_action(user_input)
            elif extractor == "calculation_type":
                entities["calculation_type"] = self._extract_calculation_type(user_input)
            elif extractor == "amount":
                entities["amount"] = self._extract_amount(user_input)
            elif extractor == "amenity":
                entities["amenity"] = self._extract_amenity(user_input)
        
        return entities
    
    def _extract_location(self, user_input: str) -> Optional[str]:
        """Extract location from user input"""
        # Common Pune locations
        pune_locations = [
            "Viman Nagar", "Kharadi", "Hadapsar", "Magarpatta", "Wagholi", "Lonikand",
            "Koregaon Park", "Boat Club", "Model Colony", "Aundh", "Baner", "Balewadi",
            "Kalyani Nagar", "Yerwada", "Lohegaon", "Chandannagar", "Hinjewadi", "Wakad",
            "Pashan", "Sus", "Camp", "Deccan", "FC Road", "JM Road", "Shivajinagar"
        ]
        
        for location in pune_locations:
            if location.lower() in user_input.lower():
                return location
        
        return None
    
    def _extract_property_type(self, user_input: str) -> Optional[str]:
        """Extract property type from user input"""
        property_types = ["1bhk", "2bhk", "3bhk", "villa", "apartment", "plot", "flat", "house"]
        
        for prop_type in property_types:
            if prop_type in user_input.lower():
                return prop_type
        
        return None
    
    def _extract_price_range(self, user_input: str) -> Optional[str]:
        """Extract price range from user input"""
        price_indicators = {
            "affordable": ["affordable", "budget", "cheap", "low cost", "sasta", "kam daam"],
            "mid_range": ["mid range", "moderate", "average", "medium"],
            "luxury": ["luxury", "premium", "high end", "expensive", "mahanga"]
        }
        
        for range_type, indicators in price_indicators.items():
            for indicator in indicators:
                if indicator in user_input.lower():
                    return range_type
        
        return None
    
    def _extract_direction(self, user_input: str) -> Optional[str]:
        """Extract direction from user input"""
        directions = ["east", "west", "north", "south", "central"]
        
        for direction in directions:
            if direction in user_input.lower():
                return direction
        
        return None
    
    def _extract_topic(self, user_input: str) -> Optional[str]:
        """Extract topic from user input"""
        # Remove question words to get topic
        question_words = ["what is", "what's", "meaning of", "definition of"]
        
        for qword in question_words:
            if qword in user_input.lower():
                topic = user_input.lower().replace(qword, "").strip()
                return topic if topic else None
        
        return None
    
    def _extract_action(self, user_input: str) -> Optional[str]:
        """Extract action from user input"""
        # Remove question words to get action
        question_words = ["how to", "how do i", "steps to", "process of"]
        
        for qword in question_words:
            if qword in user_input.lower():
                action = user_input.lower().replace(qword, "").strip()
                return action if action else None
        
        return None
    
    def _extract_calculation_type(self, user_input: str) -> Optional[str]:
        """Extract calculation type from user input"""
        calc_types = ["emi", "loan", "stamp duty", "registration fee", "property tax"]
        
        for calc_type in calc_types:
            if calc_type in user_input.lower():
                return calc_type
        
        return None
    
    def _extract_amount(self, user_input: str) -> Optional[str]:
        """Extract amount from user input"""
        # Look for currency patterns
        import re
        amount_pattern = r"₹?\d+[LCR]?"
        match = re.search(amount_pattern, user_input)
        return match.group() if match else None
    
    def _extract_amenity(self, user_input: str) -> Optional[str]:
        """Extract amenity from user input"""
        amenities = ["gym", "pool", "garden", "parking", "security", "lift", "playground"]
        
        for amenity in amenities:
            if amenity in user_input.lower():
                return amenity
        
        return None
    
    def _generate_suggestions(self, intent: str, entities: Dict[str, Any]) -> List[str]:
        """Generate suggestions based on intent and entities"""
        suggestions = []
        
        if intent == "SEARCH_PROPERTY":
            if not entities.get("location"):
                suggestions.extend([
                    "Which area are you interested in?",
                    "Are you looking for properties in East, West, North, South, or Central Pune?",
                    "Popular areas: Viman Nagar, Koregaon Park, Hinjewadi, Baner"
                ])
            
            if not entities.get("property_type"):
                suggestions.extend([
                    "What type of property are you looking for?",
                    "Options: 1 BHK, 2 BHK, 3 BHK, Villa, Apartment"
                ])
        
        elif intent == "KNOWLEDGE_QUERY":
            suggestions.extend([
                "Popular topics: Carpet Area, BHK, Stamp Duty, RERA, Home Loan",
                "Property terms: Built-up Area, Super Built-up Area, ROI"
            ])
        
        elif intent == "CALCULATOR_QUERY":
            suggestions.extend([
                "I can calculate: EMI, Stamp Duty, Registration Fees, Property Tax",
                "Try: 'Calculate EMI for ₹50L loan' or 'Calculate stamp duty for ₹1Cr property'"
            ])
        
        return suggestions
    
    def _generate_fallback_response(self, user_input: str) -> IntentClassification:
        """Generate fallback response when intent is unclear"""
        return IntentClassification(
            intent="UNKNOWN",
            confidence=0.0,
            matched_pattern="",
            entities={},
            suggestions=[
                "I can help you with:",
                "• Property search in Pune",
                "• Real estate information and terms",
                "• Cost calculations (EMI, taxes, fees)",
                "• Location-specific property details"
            ],
            fallback_response="I'm not sure what you're asking. Could you please rephrase your question? I can help with property searches, real estate information, and calculations."
        )

if __name__ == "__main__":
    # Test the enhanced intent classifier
    classifier = EnhancedIntentClassifier()
    
    test_inputs = [
        "show me properties in Viman Nagar",
        "what is carpet area",
        "calculate EMI for 50L loan",
        "properties in east pune",
        "affordable 2bhk properties",
        "properties with gym",
        "hello how are you"
    ]
    
    print("Testing Enhanced Intent Classifier:")
    print("=" * 50)
    
    for user_input in test_inputs:
        print(f"\nInput: {user_input}")
        result = classifier.classify_intent(user_input)
        
        print(f"Intent: {result.intent}")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"Entities: {result.entities}")
        
        if result.suggestions:
            print("Suggestions:")
            for suggestion in result.suggestions[:2]:
                print(f"  • {suggestion}")
