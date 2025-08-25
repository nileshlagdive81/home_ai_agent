import json
import logging
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from uuid import uuid4

from .data_augmentation_engine import DataAugmentationEngine, AugmentationConfig
from .entity_mapping_engine import EntityMappingEngine
from .enhanced_intent_classifier import EnhancedIntentClassifier, IntentClassification
from .auto_learning_system import AutoLearningSystem, UserInteraction

@dataclass
class EnhancedQueryResult:
    """Enhanced query processing result"""
    intent: str
    confidence: float
    entities: Dict[str, Any]
    response: str
    suggestions: List[str]
    user_display: Dict[str, Any]
    learning_data: Dict[str, Any]

class EnhancedNLPOrchestrator:
    """Enhanced NLP orchestrator integrating all components"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.logger = logging.getLogger(__name__)
        self.config = config or {}
        
        # Initialize components
        self.data_augmentation_engine = DataAugmentationEngine(
            AugmentationConfig(
                variations_per_qa=25,
                include_hinglish=True,
                include_typos=True,
                include_regional=True,
                pune_locations=True
            )
        )
        
        self.entity_mapping_engine = EntityMappingEngine()
        self.intent_classifier = EnhancedIntentClassifier()
        self.auto_learning_system = AutoLearningSystem()
        
        # Performance tracking
        self.query_count = 0
        self.start_time = time.time()
        
        self.logger.info("Enhanced NLP Orchestrator initialized successfully")
    
    def process_query(self, user_input: str, session_id: Optional[str] = None) -> EnhancedQueryResult:
        """Process user query through the enhanced NLP pipeline"""
        start_time = time.time()
        self.query_count += 1
        
        try:
            # Step 1: Intent Classification
            intent_result = self.intent_classifier.classify_intent(user_input)
            
            # Step 2: Entity Expansion and Mapping
            expanded_entities = self._expand_entities(intent_result.entities)
            
            # Step 3: Generate Response
            response, user_display = self._generate_response(intent_result, expanded_entities)
            
            # Step 4: Record for Learning
            self._record_interaction(user_input, intent_result, response, session_id)
            
            # Step 5: Generate Suggestions
            suggestions = self._generate_suggestions(intent_result, expanded_entities)
            
            # Step 6: Prepare Learning Data
            learning_data = self._prepare_learning_data(intent_result, expanded_entities)
            
            processing_time = time.time() - start_time
            
            self.logger.info(f"Query processed in {processing_time:.3f}s - Intent: {intent_result.intent}, Confidence: {intent_result.confidence:.2f}")
            
            return EnhancedQueryResult(
                intent=intent_result.intent,
                confidence=intent_result.confidence,
                entities=expanded_entities,
                response=response,
                suggestions=suggestions,
                user_display=user_display,
                learning_data=learning_data
            )
            
        except Exception as e:
            self.logger.error(f"Error processing query: {e}")
            return self._generate_error_response(user_input, str(e))
    
    def _expand_entities(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Expand entities using the entity mapping engine"""
        expanded = {}
        
        for entity_type, entity_value in entities.items():
            if entity_value:
                # Get entity mapping
                mapping = self.entity_mapping_engine.expand_entity(entity_value)
                
                if mapping["confidence"] > 0:
                    expanded[entity_type] = {
                        "original_value": entity_value,
                        "mapped_value": mapping["primary_value"],
                        "synonyms": mapping["synonyms"],
                        "child_levels": mapping["child_levels"],
                        "metadata": mapping["metadata"],
                        "confidence": mapping["confidence"]
                    }
                else:
                    # Keep original if no mapping found
                    expanded[entity_type] = {
                        "original_value": entity_value,
                        "mapped_value": entity_value,
                        "synonyms": [],
                        "child_levels": {},
                        "metadata": {},
                        "confidence": 0.0
                    }
        
        return expanded
    
    def _generate_response(self, intent_result: IntentClassification, expanded_entities: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """Generate response and user display information"""
        response = ""
        user_display = {
            "intent": intent_result.intent,
            "confidence": intent_result.confidence,
            "entities": {},
            "suggestions": intent_result.suggestions
        }
        
        if intent_result.intent == "SEARCH_PROPERTY":
            response, user_display = self._generate_property_search_response(intent_result, expanded_entities)
        elif intent_result.intent == "KNOWLEDGE_QUERY":
            response, user_display = self._generate_knowledge_response(intent_result, expanded_entities)
        elif intent_result.intent == "CALCULATOR_QUERY":
            response, user_display = self._generate_calculator_response(intent_result, expanded_entities)
        elif intent_result.intent == "LOCATION_SEARCH":
            response, user_display = self._generate_location_response(intent_result, expanded_entities)
        elif intent_result.intent == "PRICE_SEARCH":
            response, user_display = self._generate_price_response(intent_result, expanded_entities)
        elif intent_result.intent == "AMENITY_SEARCH":
            response, user_display = self._generate_amenity_response(intent_result, expanded_entities)
        else:
            response = intent_result.fallback_response
            user_display["message"] = "Intent not recognized"
        
        return response, user_display
    
    def _generate_property_search_response(self, intent_result: IntentClassification, expanded_entities: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """Generate property search response"""
        response_parts = []
        user_display = {
            "intent": "SEARCH_PROPERTY",
            "confidence": intent_result.confidence,
            "entities": {},
            "search_criteria": {}
        }
        
        # Build response based on extracted entities
        if "location" in expanded_entities:
            location_info = expanded_entities["location"]
            response_parts.append(f"Searching for properties in {location_info['mapped_value']}")
            user_display["entities"]["location"] = location_info
            user_display["search_criteria"]["location"] = location_info["mapped_value"]
        
        if "property_type" in expanded_entities:
            prop_info = expanded_entities["property_type"]
            response_parts.append(f"Type: {prop_info['mapped_value']}")
            user_display["entities"]["property_type"] = prop_info
            user_display["search_criteria"]["property_type"] = prop_info["mapped_value"]
        
        if "price_range" in expanded_entities:
            price_info = expanded_entities["price_range"]
            response_parts.append(f"Price Range: {price_info['mapped_value']}")
            user_display["entities"]["price_range"] = price_info
            user_display["search_criteria"]["price_range"] = price_info["mapped_value"]
        
        if response_parts:
            response = "🔍 " + " | ".join(response_parts)
            response += "\n\nI'll search our database for properties matching your criteria."
        else:
            response = "🔍 I can help you search for properties. Please specify your preferences for location, property type, or price range."
        
        return response, user_display
    
    def _generate_knowledge_response(self, intent_result: IntentClassification, expanded_entities: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """Generate knowledge query response"""
        user_display = {
            "intent": "KNOWLEDGE_QUERY",
            "confidence": intent_result.confidence,
            "entities": {},
            "topic": None
        }
        
        if "topic" in expanded_entities:
            topic_info = expanded_entities["topic"]
            user_display["entities"]["topic"] = topic_info
            user_display["topic"] = topic_info["mapped_value"]
            
            response = f"📚 I can help you understand {topic_info['mapped_value']} in real estate.\n\n"
            response += "Let me search our knowledge base for detailed information about this topic."
        else:
            response = "📚 I can help you understand various real estate terms and concepts.\n\n"
            response += "What specific topic would you like to learn about?"
        
        return response, user_display
    
    def _generate_calculator_response(self, intent_result: IntentClassification, expanded_entities: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """Generate calculator query response"""
        user_display = {
            "intent": "CALCULATOR_QUERY",
            "confidence": intent_result.confidence,
            "entities": {},
            "calculation_type": None
        }
        
        if "calculation_type" in expanded_entities:
            calc_info = expanded_entities["calculation_type"]
            user_display["entities"]["calculation_type"] = calc_info
            user_display["calculation_type"] = calc_info["mapped_value"]
            
            response = f"🧮 I can help you calculate {calc_info['mapped_value']}.\n\n"
            
            if "amount" in expanded_entities:
                amount_info = expanded_entities["amount"]
                response += f"Amount: {amount_info['mapped_value']}\n"
                user_display["entities"]["amount"] = amount_info
            
            response += "\nLet me calculate this for you."
        else:
            response = "🧮 I can help you calculate various real estate costs including EMI, stamp duty, registration fees, and more.\n\n"
            response += "What would you like to calculate?"
        
        return response, user_display
    
    def _generate_location_response(self, intent_result: IntentClassification, expanded_entities: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """Generate location search response"""
        user_display = {
            "intent": "LOCATION_SEARCH",
            "confidence": intent_result.confidence,
            "entities": {},
            "direction": None
        }
        
        if "direction" in expanded_entities:
            direction_info = expanded_entities["direction"]
            user_display["entities"]["direction"] = direction_info
            user_display["direction"] = direction_info["mapped_value"]
            
            response = f"📍 Searching for properties in {direction_info['mapped_value']} Pune.\n\n"
            response += f"This area includes popular localities like: {', '.join(direction_info['child_levels'].get('areas', [])[:3])}"
        else:
            response = "📍 I can help you find properties in different areas of Pune.\n\n"
            response += "Which direction are you interested in? (East, West, North, South, or Central)"
        
        return response, user_display
    
    def _generate_price_response(self, intent_result: IntentClassification, expanded_entities: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """Generate price search response"""
        user_display = {
            "intent": "PRICE_SEARCH",
            "confidence": intent_result.confidence,
            "entities": {},
            "price_range": None
        }
        
        if "price_range" in expanded_entities:
            price_info = expanded_entities["price_range"]
            user_display["entities"]["price_range"] = price_info
            user_display["price_range"] = price_info["mapped_value"]
            
            response = f"💰 Searching for {price_info['mapped_value']} properties.\n\n"
            response += f"Price Range: {price_info['metadata'].get('price_per_sqft', 'Varies')}\n"
            response += f"Target Audience: {price_info['metadata'].get('target_audience', 'General')}"
        else:
            response = "💰 I can help you find properties in different price ranges.\n\n"
            response += "What's your budget? (Affordable, Mid-range, or Luxury)"
        
        return response, user_display
    
    def _generate_amenity_response(self, intent_result: IntentClassification, expanded_entities: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """Generate amenity search response"""
        user_display = {
            "intent": "AMENITY_SEARCH",
            "confidence": intent_result.confidence,
            "entities": {},
            "amenity": None
        }
        
        if "amenity" in expanded_entities:
            amenity_info = expanded_entities["amenity"]
            user_display["entities"]["amenity"] = amenity_info
            user_display["amenity"] = amenity_info["mapped_value"]
            
            response = f"🏊 Searching for properties with {amenity_info['mapped_value']}.\n\n"
            response += f"Category: {amenity_info['child_levels'].get('category', ['Various'])[0]}\n"
            response += f"Type: {amenity_info['child_levels'].get('type', ['Mixed'])[0]}"
        else:
            response = "🏊 I can help you find properties with specific amenities.\n\n"
            response += "What facilities are you looking for? (Gym, Pool, Garden, Security, etc.)"
        
        return response, user_display
    
    def _generate_suggestions(self, intent_result: IntentClassification, expanded_entities: Dict[str, Any]) -> List[str]:
        """Generate contextual suggestions"""
        suggestions = []
        
        # Add intent-specific suggestions
        if intent_result.intent == "SEARCH_PROPERTY":
            if not expanded_entities.get("location"):
                suggestions.append("📍 Specify a location: 'properties in Viman Nagar'")
            if not expanded_entities.get("property_type"):
                suggestions.append("🏠 Specify property type: '2 BHK properties'")
            if not expanded_entities.get("price_range"):
                suggestions.append("💰 Specify budget: 'affordable properties'")
        
        elif intent_result.intent == "KNOWLEDGE_QUERY":
            suggestions.extend([
                "📚 Popular topics: Carpet Area, BHK, Stamp Duty, RERA",
                "💡 Try: 'What is carpet area?' or 'Explain BHK'"
            ])
        
        elif intent_result.intent == "CALCULATOR_QUERY":
            suggestions.extend([
                "🧮 Calculate: EMI, Stamp Duty, Registration Fees",
                "💡 Try: 'Calculate EMI for ₹50L loan'"
            ])
        
        # Add general suggestions
        suggestions.extend([
            "🔍 Search properties by location, type, or price",
            "📚 Learn about real estate terms and processes",
            "🧮 Calculate costs and EMI"
        ])
        
        return suggestions[:5]  # Limit to 5 suggestions
    
    def _record_interaction(self, user_input: str, intent_result: IntentClassification, response: str, session_id: Optional[str] = None):
        """Record user interaction for learning"""
        try:
            if not session_id:
                session_id = str(uuid4())
            
            interaction = UserInteraction(
                timestamp=time.time(),
                user_input=user_input,
                intent_classified=intent_result.intent,
                confidence=intent_result.confidence,
                entities_extracted=intent_result.entities,
                response_given=response,
                session_id=session_id
            )
            
            self.auto_learning_system.record_interaction(interaction)
            
        except Exception as e:
            self.logger.warning(f"Could not record interaction: {e}")
    
    def _prepare_learning_data(self, intent_result: IntentClassification, expanded_entities: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare learning data for analysis"""
        return {
            "intent": intent_result.intent,
            "confidence": intent_result.confidence,
            "entities_count": len(expanded_entities),
            "entity_types": list(expanded_entities.keys()),
            "pattern_matched": intent_result.matched_pattern,
            "timestamp": time.time()
        }
    
    def _generate_error_response(self, user_input: str, error_message: str) -> EnhancedQueryResult:
        """Generate error response when processing fails"""
        return EnhancedQueryResult(
            intent="ERROR",
            confidence=0.0,
            entities={},
            response=f"I encountered an error while processing your request: {error_message}. Please try rephrasing your question.",
            suggestions=[
                "Try using simpler language",
                "Check your spelling",
                "Ask about specific topics like properties, costs, or terms"
            ],
            user_display={
                "intent": "ERROR",
                "confidence": 0.0,
                "error": error_message,
                "message": "Processing failed"
            },
            learning_data={
                "error": error_message,
                "timestamp": time.time()
            }
        )
    
    def augment_training_data(self, training_data: Dict[str, Any]) -> Dict[str, Any]:
        """Augment training data using the data augmentation engine"""
        try:
            self.logger.info("Starting training data augmentation")
            augmented_data = self.data_augmentation_engine.augment_training_data(training_data)
            self.logger.info("Training data augmentation completed")
            return augmented_data
        except Exception as e:
            self.logger.error(f"Error augmenting training data: {e}")
            raise
    
    def get_entity_suggestions(self, partial_input: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get entity suggestions based on partial input"""
        try:
            return self.entity_mapping_engine.get_suggestions(partial_input, limit)
        except Exception as e:
            self.logger.error(f"Error getting entity suggestions: {e}")
            return []
    
    def get_learning_statistics(self) -> Dict[str, Any]:
        """Get learning system statistics"""
        try:
            stats = self.auto_learning_system.get_learning_statistics()
            stats.update({
                "orchestrator_queries_processed": self.query_count,
                "orchestrator_uptime": time.time() - self.start_time,
                "component_status": {
                    "data_augmentation": "active",
                    "entity_mapping": "active",
                    "intent_classifier": "active",
                    "auto_learning": "active"
                }
            })
            return stats
        except Exception as e:
            self.logger.error(f"Error getting learning statistics: {e}")
            return {}
    
    def export_learning_data(self, filepath: str):
        """Export learning data"""
        try:
            self.auto_learning_system.export_learning_data(filepath)
        except Exception as e:
            self.logger.error(f"Error exporting learning data: {e}")
            raise
    
    def get_popular_patterns(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most popular learned patterns"""
        try:
            patterns = self.auto_learning_system.get_popular_patterns(limit)
            return [pattern.__dict__ for pattern in patterns]
        except Exception as e:
            self.logger.error(f"Error getting popular patterns: {e}")
            return []
    
    def get_user_preferences(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user preferences"""
        try:
            prefs = self.auto_learning_system.get_user_preferences(user_id)
            return prefs.__dict__ if prefs else None
        except Exception as e:
            self.logger.error(f"Error getting user preferences: {e}")
            return None

if __name__ == "__main__":
    # Test the enhanced NLP orchestrator
    orchestrator = EnhancedNLPOrchestrator()
    
    test_queries = [
        "show me properties in Viman Nagar",
        "what is carpet area",
        "calculate EMI for 50L loan",
        "properties in east pune",
        "affordable 2bhk properties",
        "properties with gym"
    ]
    
    print("Testing Enhanced NLP Orchestrator:")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = orchestrator.process_query(query, "test_session_123")
        
        print(f"Intent: {result.intent}")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"Response: {result.response[:100]}...")
        print(f"Entities: {list(result.entities.keys())}")
        
        if result.suggestions:
            print("Suggestions:")
            for suggestion in result.suggestions[:2]:
                print(f"  • {suggestion}")
    
    # Get statistics
    stats = orchestrator.get_learning_statistics()
    print(f"\nLearning Statistics:")
    print(f"Queries Processed: {stats.get('orchestrator_queries_processed', 0)}")
    print(f"Uptime: {stats.get('orchestrator_uptime', 0):.1f} seconds")
    
    # Get popular patterns
    patterns = orchestrator.get_popular_patterns(5)
    print(f"\nPopular Patterns: {len(patterns)}")
