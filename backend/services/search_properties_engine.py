"""
Search Properties NLP Engine - Modular Architecture
Handles property search queries independently from knowledge base
"""

from typing import Dict, List, Optional, Tuple, Any
import re
import json
import os
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

@dataclass
class SearchIntent:
    """Search intent classification result"""
    intent: str
    confidence: float
    entities: Dict[str, Any]
    search_criteria: Dict[str, Any]

class SearchPropertiesEngine:
    """Independent engine for property search queries"""
    
    def __init__(self, model_path: str = None):
        """Initialize the search properties engine"""
        self.model_path = model_path or "training_data/search_properties_model.pkl"
        self.vectorizer = None
        self.intent_classifier = None
        self.entity_extractor = None
        self.training_data = self._load_training_data()
        self._initialize_models()
    
    def _load_training_data(self) -> Dict:
        """Load search properties specific training data"""
        training_file = "training_data/search_properties_training_data.json"
        try:
            if os.path.exists(training_file):
                with open(training_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Create default training data structure
                return self._create_default_training_data()
        except Exception as e:
            print(f"Error loading training data: {e}")
            return self._create_default_training_data()
    
    def _create_default_training_data(self) -> Dict:
        """Create default training data structure for search properties"""
        return {
            "search_properties": {
                "intents": {
                    "SEARCH_BY_LOCATION": {
                        "examples": [
                            "I want a house in Mumbai",
                            "Show me properties in Pune",
                            "Find apartments in Bangalore",
                            "Properties in Delhi NCR"
                        ],
                        "entities": ["LOCATION", "CITY", "LOCALITY"]
                    },
                    "SEARCH_BY_BHK": {
                        "examples": [
                            "2 BHK apartments",
                            "3 BHK houses",
                            "1 BHK flats",
                            "4 BHK villas"
                        ],
                        "entities": ["BHK", "PROPERTY_TYPE"]
                    },
                    "SEARCH_BY_PRICE": {
                        "examples": [
                            "Properties under 50 lakhs",
                            "Houses above 1 crore",
                            "Flats between 30-60 lakhs"
                        ],
                        "entities": ["PRICE_RANGE", "BUDGET"]
                    },
                    "SEARCH_BY_AMENITIES": {
                        "examples": [
                            "Properties near metro station",
                            "Houses with swimming pool",
                            "Flats near good schools"
                        ],
                        "entities": ["AMENITY", "NEARBY_PLACE"]
                    }
                },
                "entities": {
                    "LOCATION": {
                        "cities": ["Mumbai", "Delhi", "Bangalore", "Pune", "Hyderabad", "Chennai", "Kolkata"],
                        "localities": ["Bandra", "Andheri", "Powai", "Whitefield", "Hinjewadi", "Baner"]
                    },
                    "BHK": ["1 BHK", "2 BHK", "3 BHK", "4 BHK", "1BHK", "2BHK", "3BHK", "4BHK"],
                    "PROPERTY_TYPE": ["Apartment", "House", "Villa", "Flat", "Penthouse", "Studio"],
                    "PRICE_RANGE": ["Under 50 Lakhs", "50-100 Lakhs", "1-2 Crores", "Above 2 Crores"],
                    "AMENITY": ["Metro Station", "Railway Station", "Airport", "Hospital", "School", "Mall"]
                }
            }
        }
    
    def _initialize_models(self):
        """Initialize NLP models for search properties"""
        try:
            # Initialize TF-IDF vectorizer for intent classification
            self.vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            
            # Prepare training data for vectorizer
            training_texts = []
            training_labels = []
            
            for intent, data in self.training_data["search_properties"]["intents"].items():
                for example in data["examples"]:
                    training_texts.append(example.lower())
                    training_labels.append(intent)
            
            # Fit vectorizer
            if training_texts:
                self.vectorizer.fit(training_texts)
                print(f"✅ Search Properties Engine initialized with {len(training_texts)} training examples")
            else:
                print("⚠️ No training data available for search properties")
                
        except Exception as e:
            print(f"❌ Error initializing search properties models: {e}")
    
    def classify_intent(self, query: str) -> SearchIntent:
        """Classify the search intent from a query"""
        try:
            query_lower = query.lower()
            
            # Use TF-IDF for intent classification
            if self.vectorizer:
                query_vector = self.vectorizer.transform([query_lower])
                
                # Find best matching intent
                best_intent = None
                best_confidence = 0.0
                
                for intent, data in self.training_data["search_properties"]["intents"].items():
                    for example in data["examples"]:
                        example_vector = self.vectorizer.transform([example.lower()])
                        similarity = cosine_similarity(query_vector, example_vector)[0][0]
                        
                        if similarity > best_confidence:
                            best_confidence = similarity
                            best_intent = intent
                
                # Extract entities
                entities = self._extract_entities(query_lower)
                
                # Build search criteria
                search_criteria = self._build_search_criteria(intent, entities)
                
                return SearchIntent(
                    intent=best_intent or "UNKNOWN",
                    confidence=best_confidence,
                    entities=entities,
                    search_criteria=search_criteria
                )
            
        except Exception as e:
            print(f"❌ Error classifying search intent: {e}")
            return SearchIntent(
                intent="ERROR",
                confidence=0.0,
                entities={},
                search_criteria={}
            )
    
    def _extract_entities(self, query: str) -> Dict[str, Any]:
        """Extract entities from the search query"""
        entities = {}
        
        try:
            # Extract locations
            for city in self.training_data["search_properties"]["entities"]["LOCATION"]["cities"]:
                if city.lower() in query:
                    entities["city"] = city
                    break
            
            for locality in self.training_data["search_properties"]["entities"]["LOCATION"]["localities"]:
                if locality.lower() in query:
                    entities["locality"] = locality
                    break
            
            # Extract BHK
            for bhk in self.training_data["search_properties"]["entities"]["BHK"]:
                if bhk.lower().replace(" ", "") in query.replace(" ", ""):
                    entities["bhk"] = bhk
                    break
            
            # Extract property type
            for prop_type in self.training_data["search_properties"]["entities"]["PROPERTY_TYPE"]:
                if prop_type.lower() in query:
                    entities["property_type"] = prop_type
                    break
            
            # Extract price range
            for price_range in self.training_data["search_properties"]["entities"]["PRICE_RANGE"]:
                if any(word in query for word in price_range.lower().split()):
                    entities["price_range"] = price_range
                    break
            
            # Extract amenities
            for amenity in self.training_data["search_properties"]["entities"]["AMENITY"]:
                if amenity.lower() in query:
                    entities["amenity"] = amenity
                    break
            
        except Exception as e:
            print(f"❌ Error extracting entities: {e}")
        
        return entities
    
    def _build_search_criteria(self, intent: str, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Build search criteria from intent and entities"""
        criteria = {
            "filters": {},
            "sort_by": "relevance",
            "limit": 20
        }
        
        try:
            # Add entity-based filters
            if "city" in entities:
                criteria["filters"]["city"] = entities["city"]
            
            if "locality" in entities:
                criteria["filters"]["locality"] = entities["locality"]
            
            if "bhk" in entities:
                criteria["filters"]["bhk"] = entities["bhk"]
            
            if "property_type" in entities:
                criteria["filters"]["property_type"] = entities["property_type"]
            
            if "price_range" in entities:
                criteria["filters"]["price_range"] = entities["price_range"]
            
            if "amenity" in entities:
                criteria["filters"]["amenity"] = entities["amenity"]
            
            # Intent-specific criteria
            if intent == "SEARCH_BY_PRICE":
                criteria["sort_by"] = "price"
            elif intent == "SEARCH_BY_LOCATION":
                criteria["sort_by"] = "location_relevance"
            
        except Exception as e:
            print(f"❌ Error building search criteria: {e}")
        
        return criteria
    
    def process_query(self, query: str) -> SearchIntent:
        """Main method to process a search properties query"""
        return self.classify_intent(query)
    
    def get_search_criteria(self, query: str) -> Dict[str, Any]:
        """Get search criteria for a query"""
        intent_result = self.classify_intent(query)
        return intent_result.search_criteria
    
    def train_model(self, new_training_data: Dict):
        """Train the model with new data"""
        try:
            # Update training data
            self.training_data["search_properties"]["intents"].update(
                new_training_data.get("intents", {})
            )
            
            # Reinitialize models with new data
            self._initialize_models()
            
            print("✅ Search properties model retrained successfully")
            
        except Exception as e:
            print(f"❌ Error training search properties model: {e}")
    
    def save_model(self, path: str = None):
        """Save the trained model"""
        try:
            save_path = path or self.model_path
            # Save training data
            training_file = "training_data/search_properties_training_data.json"
            with open(training_file, 'w', encoding='utf-8') as f:
                json.dump(self.training_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Search properties model saved to {training_file}")
            
        except Exception as e:
            print(f"❌ Error saving search properties model: {e}")
    
    def evaluate_model(self, test_queries: List[Tuple[str, str]]) -> Dict[str, float]:
        """Evaluate model performance on test queries"""
        try:
            correct = 0
            total = len(test_queries)
            
            for query, expected_intent in test_queries:
                result = self.classify_intent(query)
                if result.intent == expected_intent:
                    correct += 1
            
            accuracy = correct / total if total > 0 else 0.0
            
            return {
                "accuracy": accuracy,
                "correct_predictions": correct,
                "total_queries": total
            }
            
        except Exception as e:
            print(f"❌ Error evaluating search properties model: {e}")
            return {"accuracy": 0.0, "correct_predictions": 0, "total_queries": 0}
