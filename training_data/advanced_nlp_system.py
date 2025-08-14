#!/usr/bin/env python3
"""
Advanced NLP System for Real Estate
Next phase development with enhanced capabilities
"""

import json
import spacy
import re
from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path
import random
from datetime import datetime, timedelta
import math

class AdvancedRealEstateNLP:
    """Advanced NLP system for real estate with enhanced capabilities"""
    
    def __init__(self, model_path: Optional[str] = None):
        """Initialize the advanced NLP system"""
        if model_path and Path(model_path).exists():
            try:
                self.nlp = spacy.load(model_path)
                print(f"✅ Loaded trained model from: {model_path}")
            except Exception as e:
                print(f"⚠️ Failed to load trained model: {e}")
                self.load_base_model()
        else:
            self.load_base_model()
        
        # Initialize advanced features
        self.setup_advanced_features()
        
        # Load advanced training data
        self.advanced_data = self.load_advanced_data()
        
    def load_base_model(self):
        """Load the base spaCy model"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
            print("✅ Loaded base spaCy model: en_core_web_sm")
        except OSError:
            print("❌ Base model not found. Please install: python -m spacy download en_core_web_sm")
            raise
    
    def setup_advanced_features(self):
        """Setup advanced NLP features"""
        # Add custom entity labels
        custom_entities = [
            "PROJECT_NAME", "DEVELOPER", "LOCATION", "PROPERTY_TYPE", "QUANTITY",
            "STATUS", "DATE", "RERA_NUMBER", "DESCRIPTION", "FEATURES",
            "BHK", "AREA", "PRICE", "AMENITY", "DISTANCE", "PROJECT_ID",
            "EMI_AMOUNT", "DOWN_PAYMENT", "INTEREST_RATE", "LOAN_TERM",
            "RENTAL_YIELD", "APPRECIATION_RATE", "MAINTENANCE_COST"
        ]
        
        ner = self.nlp.get_pipe("ner")
        for entity in custom_entities:
            if entity not in ner.labels:
                ner.add_label(entity)
        
        # Add custom pipeline components
        if "textcat" not in self.nlp.pipe_names:
            textcat = self.nlp.add_pipe("textcat")
            textcat.add_label("SEARCH_PROPERTY")
            textcat.add_label("GET_DETAILS")
            textcat.add_label("COMPARE_PROPERTIES")
            textcat.add_label("PRICE_QUERY")
            textcat.add_label("FILTER_BY_LOCATION")
            textcat.add_label("FILTER_BY_BHK")
            textcat.add_label("FILTER_BY_AMENITY")
            textcat.add_label("BOOK_PROPERTY")
            textcat.add_label("GET_FINANCIAL_DETAILS")
        
        print("✅ Advanced NLP features configured")
    
    def load_advanced_data(self) -> Dict:
        """Load advanced training and configuration data"""
        return {
            "financial_patterns": {
                "emi_calculation": {
                    "patterns": [
                        r"EMI for (\d+)BHK.*?(\d+)\s*(lakh|crore)",
                        r"monthly payment.*?(\d+)\s*(lakh|crore).*?(\d+)% down",
                        r"installment.*?(\d+)\s*(lakh|crore).*?(\d+) years"
                    ],
                    "entities": ["BHK", "PRICE", "QUANTITY", "LOAN_TERM"]
                },
                "investment_analysis": {
                    "patterns": [
                        r"rental yield.*?(\d+)%",
                        r"appreciation.*?(\d+)%",
                        r"ROI.*?(\d+)%",
                        r"maintenance cost.*?(\d+)\s*(lakh|crore)"
                    ],
                    "entities": ["QUANTITY", "PRICE"]
                }
            },
            "temporal_patterns": {
                "festival_dates": {
                    "diwali": "October-November",
                    "holi": "March",
                    "eid": "Variable",
                    "christmas": "December 25"
                },
                "relative_dates": {
                    "next month": 1,
                    "next quarter": 3,
                    "next year": 12,
                    "next 6 months": 6
                }
            },
            "spatial_patterns": {
                "proximity_keywords": {
                    "very close": 0.5,
                    "close": 1.0,
                    "nearby": 2.0,
                    "within reach": 3.0,
                    "accessible": 5.0
                },
                "landmark_types": {
                    "metro": "transport",
                    "airport": "transport",
                    "hospital": "healthcare",
                    "school": "education",
                    "mall": "shopping",
                    "park": "recreation"
                }
            }
        }
    
    def process_advanced_query(self, query: str) -> Dict[str, Any]:
        """Process advanced real estate queries with enhanced capabilities"""
        doc = self.nlp(query)
        
        # Extract basic entities
        entities = self.extract_entities(doc)
        
        # Advanced entity extraction
        financial_info = self.extract_financial_info(query)
        temporal_info = self.extract_temporal_info(query)
        spatial_info = self.extract_spatial_info(query)
        
        # Intent classification
        intent = self.classify_advanced_intent(doc, entities, financial_info, temporal_info, spatial_info)
        
        # Generate search criteria
        search_criteria = self.generate_advanced_search_criteria(
            entities, financial_info, temporal_info, spatial_info
        )
        
        # Confidence scoring
        confidence = self.calculate_confidence(doc, entities, intent)
        
        return {
            "query": query,
            "intent": intent,
            "entities": entities,
            "financial_info": financial_info,
            "temporal_info": temporal_info,
            "spatial_info": spatial_info,
            "search_criteria": search_criteria,
            "confidence": confidence,
            "suggestions": self.generate_suggestions(intent, entities)
        }
    
    def extract_entities(self, doc) -> List[Dict]:
        """Extract entities from the document"""
        entities = []
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            })
        return entities
    
    def extract_financial_info(self, query: str) -> Dict[str, Any]:
        """Extract financial information from query"""
        financial_info = {}
        
        # EMI calculation patterns
        emi_patterns = self.advanced_data["financial_patterns"]["emi_calculation"]["patterns"]
        for pattern in emi_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                financial_info["emi_calculation"] = {
                    "bhk": match.group(1) if len(match.groups()) > 0 else None,
                    "price": match.group(2) if len(match.groups()) > 1 else None,
                    "unit": match.group(3) if len(match.groups()) > 2 else None,
                    "down_payment": match.group(4) if len(match.groups()) > 3 else None,
                    "loan_term": match.group(5) if len(match.groups()) > 4 else None
                }
                break
        
        # Investment analysis patterns
        investment_patterns = self.advanced_data["financial_patterns"]["investment_analysis"]["patterns"]
        for pattern in investment_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                if "rental yield" in query.lower():
                    financial_info["rental_yield"] = match.group(1)
                elif "appreciation" in query.lower():
                    financial_info["appreciation_rate"] = match.group(1)
                elif "ROI" in query.lower():
                    financial_info["roi"] = match.group(1)
                elif "maintenance" in query.lower():
                    financial_info["maintenance_cost"] = match.group(1)
        
        return financial_info
    
    def extract_temporal_info(self, query: str) -> Dict[str, Any]:
        """Extract temporal information from query"""
        temporal_info = {}
        
        # Festival references
        festival_dates = self.advanced_data["temporal_patterns"]["festival_dates"]
        for festival, date_info in festival_dates.items():
            if festival in query.lower():
                temporal_info["festival"] = festival
                temporal_info["festival_date"] = date_info
        
        # Relative dates
        relative_dates = self.advanced_data["temporal_patterns"]["relative_dates"]
        for relative_term, months in relative_dates.items():
            if relative_term in query.lower():
                temporal_info["relative_date"] = relative_term
                temporal_info["months_ahead"] = months
                # Calculate actual date
                target_date = datetime.now() + timedelta(days=months*30)
                temporal_info["target_date"] = target_date.strftime("%Y-%m-%d")
        
        # Specific dates
        date_patterns = [
            r"(\d{1,2})/(\d{1,2})/(\d{4})",
            r"(\d{1,2})-(\d{1,2})-(\d{4})",
            r"(\d{1,2})\s+(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})"
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                temporal_info["specific_date"] = match.group(0)
                break
        
        return temporal_info
    
    def extract_spatial_info(self, query: str) -> Dict[str, Any]:
        """Extract spatial information from query"""
        spatial_info = {}
        
        # Proximity analysis
        proximity_keywords = self.advanced_data["spatial_patterns"]["proximity_keywords"]
        for keyword, distance in proximity_keywords.items():
            if keyword in query.lower():
                spatial_info["proximity"] = keyword
                spatial_info["max_distance_km"] = distance
        
        # Landmark analysis
        landmark_types = self.advanced_data["spatial_patterns"]["landmark_types"]
        landmarks = []
        for landmark, category in landmark_types.items():
            if landmark in query.lower():
                landmarks.append({
                    "name": landmark,
                    "category": category
                })
        
        if landmarks:
            spatial_info["landmarks"] = landmarks
        
        # Distance ranges
        distance_patterns = [
            r"within\s+(\d+)\s*km",
            r"(\d+)\s*km\s+away",
            r"less\s+than\s+(\d+)\s*km"
        ]
        
        for pattern in distance_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                spatial_info["distance_range"] = match.group(1)
                break
        
        return spatial_info
    
    def classify_advanced_intent(self, doc, entities: List[Dict], financial_info: Dict, 
                                temporal_info: Dict, spatial_info: Dict) -> str:
        """Classify intent using advanced analysis"""
        # Use text classification if available
        if "textcat" in self.nlp.pipe_names:
            textcat = self.nlp.get_pipe("textcat")
            scores = textcat.predict([doc])
            predicted_cat = max(scores[0], key=lambda x: x[1])
            if predicted_cat[1] > 0.5:
                return predicted_cat[0]
        
        # Fallback to rule-based classification
        entity_labels = [e["label"] for e in entities]
        
        # Financial queries
        if financial_info:
            if "emi_calculation" in financial_info:
                return "GET_FINANCIAL_DETAILS"
            elif any(key in financial_info for key in ["rental_yield", "appreciation_rate", "roi"]):
                return "INVESTMENT_ANALYSIS"
        
        # Temporal queries
        if temporal_info:
            if "festival" in temporal_info or "relative_date" in temporal_info:
                return "TEMPORAL_SEARCH"
        
        # Spatial queries
        if spatial_info:
            if "landmarks" in spatial_info and len(spatial_info["landmarks"]) > 1:
                return "MULTI_LANDMARK_SEARCH"
            elif "proximity" in spatial_info:
                return "PROXIMITY_SEARCH"
        
        # Multi-field queries
        if len(entity_labels) >= 3:
            return "COMPLEX_SEARCH"
        elif len(entity_labels) == 2:
            return "MULTI_CRITERIA_SEARCH"
        elif len(entity_labels) == 1:
            return "SINGLE_CRITERIA_SEARCH"
        else:
            return "GENERAL_QUERY"
    
    def generate_advanced_search_criteria(self, entities: List[Dict], financial_info: Dict,
                                        temporal_info: Dict, spatial_info: Dict) -> Dict[str, Any]:
        """Generate advanced search criteria for database queries"""
        criteria = {}
        
        # Basic entity criteria
        for entity in entities:
            if entity["label"] == "BHK":
                criteria["bhk"] = entity["text"]
            elif entity["label"] == "LOCATION":
                criteria["location"] = entity["text"]
            elif entity["label"] == "PRICE":
                criteria["price_range"] = entity["text"]
            elif entity["label"] == "AMENITY":
                if "amenities" not in criteria:
                    criteria["amenities"] = []
                criteria["amenities"].append(entity["text"])
        
        # Financial criteria
        if financial_info:
            criteria["financial"] = financial_info
        
        # Temporal criteria
        if temporal_info:
            criteria["temporal"] = temporal_info
        
        # Spatial criteria
        if spatial_info:
            criteria["spatial"] = spatial_info
        
        return criteria
    
    def calculate_confidence(self, doc, entities: List[Dict], intent: str) -> float:
        """Calculate confidence score for the analysis"""
        base_confidence = 0.5
        
        # Entity confidence
        if entities:
            entity_confidence = min(len(entities) * 0.2, 0.4)
            base_confidence += entity_confidence
        
        # Intent confidence based on complexity
        intent_confidence_map = {
            "SINGLE_CRITERIA_SEARCH": 0.1,
            "MULTI_CRITERIA_SEARCH": 0.2,
            "COMPLEX_SEARCH": 0.3,
            "MULTI_LANDMARK_SEARCH": 0.25,
            "PROXIMITY_SEARCH": 0.2,
            "TEMPORAL_SEARCH": 0.15,
            "INVESTMENT_ANALYSIS": 0.3,
            "GET_FINANCIAL_DETAILS": 0.25
        }
        
        base_confidence += intent_confidence_map.get(intent, 0.1)
        
        # Document length confidence
        doc_confidence = min(len(doc) * 0.01, 0.2)
        base_confidence += doc_confidence
        
        return min(base_confidence, 1.0)
    
    def generate_suggestions(self, intent: str, entities: List[Dict]) -> List[str]:
        """Generate helpful suggestions based on intent and entities"""
        suggestions = []
        
        if intent == "SINGLE_CRITERIA_SEARCH":
            suggestions.append("Consider adding more criteria for better results")
            suggestions.append("Try specifying location or price range")
        
        elif intent == "MULTI_CRITERIA_SEARCH":
            suggestions.append("Great! You've provided multiple criteria")
            suggestions.append("Consider adding amenities or nearby places")
        
        elif intent == "COMPLEX_SEARCH":
            suggestions.append("Excellent! Complex search detected")
            suggestions.append("Results will be highly specific to your needs")
        
        elif intent == "PROXIMITY_SEARCH":
            suggestions.append("Proximity search detected")
            suggestions.append("Results will be sorted by distance")
        
        elif intent == "TEMPORAL_SEARCH":
            suggestions.append("Time-based search detected")
            suggestions.append("Results will include project timelines")
        
        elif intent == "INVESTMENT_ANALYSIS":
            suggestions.append("Investment analysis mode")
            suggestions.append("Results will include ROI and yield data")
        
        return suggestions
    
    def train_advanced_model(self, training_data: List[Dict], iterations: int = 50) -> bool:
        """Train the advanced NLP model"""
        try:
            print(f"🚀 Starting advanced training with {len(training_data)} examples...")
            
            # Prepare training data
            train_data = []
            for example in training_data:
                # Create spaCy training example
                doc = self.nlp.make_doc(example["text"])
                
                # Add entities
                ents = []
                for start, end, label in example["entities"]:
                    span = doc.char_span(start, end, label=label)
                    if span:
                        ents.append(span)
                
                doc.ents = ents
                
                # Add text classification
                cats = {cat: 0.0 for cat in ["SEARCH_PROPERTY", "GET_DETAILS", "COMPARE_PROPERTIES", 
                                            "PRICE_QUERY", "FILTER_BY_LOCATION", "FILTER_BY_BHK", 
                                            "FILTER_BY_AMENITY", "BOOK_PROPERTY", "GET_FINANCIAL_DETAILS"]}
                cats[example["intent"]] = 1.0
                doc.cats = cats
                
                from spacy.training import Example
                train_data.append(Example.from_dict(doc, {"entities": [(e.start, e.end, e.label_) for e in ents], "cats": cats}))
            
            # Training
            losses = {}
            for i in range(iterations):
                random.shuffle(train_data)
                self.nlp.update(train_data, drop=0.5, losses=losses)
                
                if i % 10 == 0:
                    print(f"  Iteration {i+1}/{iterations}, Losses: {losses}")
            
            print("✅ Advanced training completed!")
            return True
            
        except Exception as e:
            print(f"❌ Advanced training failed: {e}")
            return False
    
    def save_advanced_model(self, output_dir: str = "./advanced_trained_model") -> bool:
        """Save the advanced trained model"""
        try:
            output_path = Path(output_dir)
            if not output_path.exists():
                output_path.mkdir()
            
            self.nlp.to_disk(output_path)
            print(f"✅ Advanced model saved to {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save advanced model: {e}")
            return False

def main():
    """Main function to demonstrate advanced NLP capabilities"""
    print("🚀 Advanced Real Estate NLP System")
    print("=" * 50)
    
    try:
        # Initialize advanced NLP system
        nlp_system = AdvancedRealEstateNLP()
        
        # Test queries
        test_queries = [
            "Show me 2BHK apartments in Mumbai under 1 crore with swimming pool",
            "What's the EMI for a 3BHK flat costing 80 lakhs with 20% down payment?",
            "Properties near metro if within 1km, or near hospital if more than 1km away",
            "Which project will be ready by next Diwali?",
            "Compare Tech Park Residences and Heritage Gardens based on price and amenities",
            "Properties between Bandra and Andheri, closer to the sea",
            "Projects with gym, swimming pool, and security, but no clubhouse"
        ]
        
        print("\n🧪 Testing Advanced NLP Capabilities...")
        for i, query in enumerate(test_queries, 1):
            print(f"\n{i}. Query: {query}")
            result = nlp_system.process_advanced_query(query)
            
            print(f"   Intent: {result['intent']}")
            print(f"   Confidence: {result['confidence']:.2f}")
            print(f"   Entities: {[f'{e['text']}({e['label']})' for e in result['entities']]}")
            
            if result['financial_info']:
                print(f"   Financial: {result['financial_info']}")
            if result['temporal_info']:
                print(f"   Temporal: {result['temporal_info']}")
            if result['spatial_info']:
                print(f"   Spatial: {result['spatial_info']}")
            
            print(f"   Suggestions: {', '.join(result['suggestions'])}")
        
        print("\n🎉 Advanced NLP System demonstration completed!")
        
    except Exception as e:
        print(f"❌ Error in advanced NLP system: {e}")

if __name__ == "__main__":
    main()
