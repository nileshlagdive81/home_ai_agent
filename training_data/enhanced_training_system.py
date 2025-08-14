#!/usr/bin/env python3
"""
Enhanced Training System for Real Estate NLP
Combines field-specific training with advanced NLP capabilities
"""

import json
import spacy
import re
from typing import Dict, List, Tuple, Any
from pathlib import Path
import random

class EnhancedRealEstateTrainer:
    """Enhanced trainer for real estate NLP with field-specific training"""
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        """Initialize the enhanced trainer"""
        try:
            self.nlp = spacy.load(model_name)
            print(f"✅ Loaded spaCy model: {model_name}")
        except OSError:
            print(f"❌ Model {model_name} not found. Please install it with: python -m spacy download {model_name}")
            raise
        
        # Load training data
        self.training_data = self.load_training_data()
        self.field_queries = self.load_field_queries()
        
        # Initialize custom entities
        self.custom_entities = [
            "PROJECT_NAME", "DEVELOPER", "LOCATION", "PROPERTY_TYPE", "QUANTITY",
            "STATUS", "DATE", "RERA_NUMBER", "DESCRIPTION", "FEATURES",
            "BHK", "AREA", "PRICE", "AMENITY", "DISTANCE", "PROJECT_ID"
        ]
        
        # Add custom entity labels
        self.setup_custom_entities()
    
    def load_training_data(self) -> Dict:
        """Load the main training data"""
        try:
            with open("intent_training_data.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️ intent_training_data.json not found, using default data")
            return self.get_default_training_data()
    
    def load_field_queries(self) -> Dict:
        """Load field-specific training data"""
        try:
            with open("field_training_data.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️ field_training_data.json not found, using default data")
            return self.get_default_field_data()
    
    def get_default_training_data(self) -> Dict:
        """Default training data if files are not found"""
        return {
            "intents": {
                "SEARCH_PROPERTY": {
                    "examples": ["Show me properties", "Find apartments", "Search for houses"],
                    "responses": ["I'll help you find properties matching your criteria."]
                },
                "GET_DETAILS": {
                    "examples": ["What is the project name?", "Tell me about this project"],
                    "responses": ["Here are the details about the property."]
                }
            }
        }
    
    def get_default_field_data(self) -> Dict:
        """Default field data if files are not found"""
        return {
            "project_fields": {
                "project_name": {
                    "intent": "GET_DETAILS",
                    "examples": ["What is the project name?", "Project name please"],
                    "entities": ["PROJECT_NAME"]
                }
            }
        }
    
    def setup_custom_entities(self):
        """Setup custom entity types in the NLP model"""
        ner = self.nlp.get_pipe("ner")
        
        for entity in self.custom_entities:
            if entity not in ner.labels:
                ner.add_label(entity)
                print(f"✅ Added entity label: {entity}")
    
    def create_field_training_examples(self) -> List[Dict]:
        """Create comprehensive training examples from field data"""
        examples = []
        
        # Process project fields
        for field_name, field_data in self.field_queries.get("project_fields", {}).items():
            intent = field_data["intent"]
            entities = field_data["entities"]
            
            for query in field_data["examples"]:
                example = self.create_example_from_query(query, intent, entities)
                examples.append(example)
        
        # Process property unit fields
        for field_name, field_data in self.field_queries.get("property_unit_fields", {}).items():
            intent = field_data["intent"]
            entities = field_data["entities"]
            
            for query in field_data["examples"]:
                example = self.create_example_from_query(query, intent, entities)
                examples.append(example)
        
        # Process amenity fields
        for field_name, field_data in self.field_queries.get("amenity_fields", {}).items():
            intent = field_data["intent"]
            entities = field_data["entities"]
            
            for query in field_data["examples"]:
                example = self.create_example_from_query(query, intent, entities)
                examples.append(example)
        
        # Process nearby places
        for place_name, place_data in self.field_queries.get("nearby_places", {}).items():
            intent = place_data["intent"]
            entities = place_data["entities"]
            
            for query in place_data["examples"]:
                example = self.create_example_from_query(query, intent, entities)
                examples.append(example)
        
        # Process simple search queries
        for search_type, search_data in self.field_queries.get("simple_search_queries", {}).items():
            intent = search_data["intent"]
            entities = search_data["entities"]
            
            for query in search_data["examples"]:
                example = self.create_example_from_query(query, intent, entities)
                examples.append(example)
        
        return examples
    
    def create_example_from_query(self, query: str, intent: str, entities: List[str]) -> Dict:
        """Create a training example from a query"""
        # Extract entities based on query content
        extracted_entities = []
        
        # Extract PROJECT_NAME
        if "PROJECT_NAME" in entities and "project" in query.lower():
            start = query.lower().find("project")
            end = start + len("project")
            extracted_entities.append((start, end, "PROJECT_NAME"))
        
        # Extract DEVELOPER
        if "DEVELOPER" in entities and ("developer" in query.lower() or "builder" in query.lower()):
            if "developer" in query.lower():
                start = query.lower().find("developer")
                end = start + len("developer")
            else:
                start = query.lower().find("builder")
                end = start + len("builder")
            extracted_entities.append((start, end, "DEVELOPER"))
        
        # Extract LOCATION
        if "LOCATION" in entities:
            location_keywords = ["locality", "area", "city", "mumbai", "delhi", "bangalore"]
            for keyword in location_keywords:
                if keyword in query.lower():
                    start = query.lower().find(keyword)
                    end = start + len(keyword)
                    extracted_entities.append((start, end, "LOCATION"))
                    break
        
        # Extract BHK
        if "BHK" in entities:
            bhk_match = re.search(r'(\d+)BHK', query, re.IGNORECASE)
            if bhk_match:
                start = bhk_match.start()
                end = bhk_match.end()
                extracted_entities.append((start, end, "BHK"))
            elif "bhk" in query.lower() or "bedroom" in query.lower():
                start = query.lower().find("bhk") if "bhk" in query.lower() else query.lower().find("bedroom")
                end = start + len("bhk") if "bhk" in query.lower() else start + len("bedroom")
                extracted_entities.append((start, end, "BHK"))
        
        # Extract PRICE
        if "PRICE" in entities:
            price_keywords = ["price", "cost", "amount", "lakh", "crore"]
            for keyword in price_keywords:
                if keyword in query.lower():
                    start = query.lower().find(keyword)
                    end = start + len(keyword)
                    extracted_entities.append((start, end, "PRICE"))
                    break
        
        # Extract AMENITY
        if "AMENITY" in entities:
            amenity_keywords = ["amenity", "facility", "feature"]
            for keyword in amenity_keywords:
                if keyword in query.lower():
                    start = query.lower().find(keyword)
                    end = start + len(keyword)
                    extracted_entities.append((start, end, "AMENITY"))
                    break
        
        return {
            "text": query,
            "intent": intent,
            "entities": extracted_entities
        }
    
    def train_model(self, training_examples: List[Dict], iterations: int = 30) -> bool:
        """Train the NLP model with the provided examples"""
        try:
            print(f"🚀 Starting training with {len(training_examples)} examples...")
            
            # Prepare training data for spaCy
            train_data = []
            for example in training_examples:
                # Create entity spans
                ents = []
                for start, end, label in example["entities"]:
                    span = self.nlp.make_doc(example["text"])[start:end]
                    ents.append(span)
                
                # Create training example
                doc = self.nlp.make_doc(example["text"])
                ents = filter_spans(ents)
                doc.ents = ents
                
                from spacy.training import Example
                train_data.append(Example.from_dict(doc, {"entities": [(e.start, e.end, e.label_) for e in ents]}))
            
            print(f"✅ Prepared {len(train_data)} training examples")
            
            # Training configuration
            dropout = 0.5
            losses = {}
            
            # Train the model
            for i in range(iterations):
                random.shuffle(train_data)
                self.nlp.update(train_data, drop=dropout, losses=losses)
                
                if i % 5 == 0:
                    print(f"  Iteration {i+1}/{iterations}, Losses: {losses}")
            
            print("✅ Training completed!")
            return True
            
        except Exception as e:
            print(f"❌ Training failed: {e}")
            return False
    
    def save_model(self, output_dir: str = "./trained_model") -> bool:
        """Save the trained model"""
        try:
            output_path = Path(output_dir)
            if not output_path.exists():
                output_path.mkdir()
            
            self.nlp.to_disk(output_path)
            print(f"✅ Model saved to {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save model: {e}")
            return False
    
    def test_model(self, test_queries: List[str]) -> None:
        """Test the trained model with sample queries"""
        print("\n🧪 Testing trained model...")
        print("=" * 50)
        
        for query in test_queries:
            doc = self.nlp(query)
            print(f"\nQuery: {query}")
            print(f"Entities: {[(e.text, e.label_) for e in doc.ents]}")
            
            # Intent classification based on entities
            intent = self.classify_intent_from_entities(doc.ents)
            print(f"Detected Intent: {intent}")
    
    def classify_intent_from_entities(self, entities) -> str:
        """Classify intent based on extracted entities"""
        entity_labels = [e.label_ for e in entities]
        
        if "LOCATION" in entity_labels and "BHK" in entity_labels:
            return "SEARCH_PROPERTY"
        elif "LOCATION" in entity_labels:
            return "FILTER_BY_LOCATION"
        elif "BHK" in entity_labels:
            return "FILTER_BY_BHK"
        elif "PRICE" in entity_labels:
            return "PRICE_QUERY"
        elif "AMENITY" in entity_labels:
            return "FILTER_BY_AMENITY"
        else:
            return "GET_DETAILS"
    
    def run_comprehensive_training(self) -> bool:
        """Run the complete training pipeline"""
        print("🚀 Starting Comprehensive NLP Training for Real Estate...")
        
        # Create training examples
        training_examples = self.create_field_training_examples()
        print(f"✅ Created {len(training_examples)} training examples")
        
        # Train the model
        success = self.train_model(training_examples)
        
        if success:
            # Save the model
            self.save_model()
            
            # Test the model
            test_queries = [
                "Show me 2BHK properties in Mumbai",
                "What is the project name?",
                "How much does it cost?",
                "Is there metro nearby?",
                "What are the amenities?",
                "When can I move in?",
                "Properties under 50 lakhs"
            ]
            
            self.test_model(test_queries)
            
            print("\n🎉 Comprehensive training completed successfully!")
            return True
        else:
            print("❌ Training failed!")
            return False

def filter_spans(spans):
    """Filter overlapping spans"""
    sorted_spans = sorted(spans, key=lambda x: x.start)
    filtered = []
    for span in sorted_spans:
        if not any(span.start < f.end and span.end > f.start for f in filtered):
            filtered.append(span)
    return filtered

def main():
    """Main function to run the enhanced training system"""
    try:
        # Initialize the enhanced trainer
        trainer = EnhancedRealEstateTrainer()
        
        # Run comprehensive training
        success = trainer.run_comprehensive_training()
        
        if success:
            print("\n🎉 Enhanced NLP Training System completed successfully!")
            print("You can now use the trained model for advanced real estate queries.")
        else:
            print("\n💥 Enhanced NLP Training System failed!")
            
    except Exception as e:
        print(f"❌ Error in enhanced training system: {e}")

if __name__ == "__main__":
    main()
