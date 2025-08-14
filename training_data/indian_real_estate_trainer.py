#!/usr/bin/env python3
"""
Indian Real Estate NLP Trainer
Specialized training system for Indian real estate queries with Hindi-English mixed language support
"""
import json
import spacy
import re
from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path
import random
from spacy.training import Example
from spacy.util import filter_spans

class IndianRealEstateTrainer:
    def __init__(self, model_name: str = "en_core_web_sm"):
        self.model_name = model_name
        self.nlp = None
        self.training_data = {}
        self.indian_context = {}
        self.setup_model()
        
    def setup_model(self):
        """Load spaCy model and setup custom entities"""
        try:
            self.nlp = spacy.load(self.model_name)
            print(f"✅ Loaded base model: {self.model_name}")
        except OSError:
            print(f"⚠️ Model {self.model_name} not found. Downloading...")
            spacy.cli.download(self.model_name)
            self.nlp = spacy.load(self.model_name)
        
        self.setup_custom_entities()
        
    def setup_custom_entities(self):
        """Setup custom entity labels for Indian real estate"""
        # Remove existing NER pipe if it exists
        if "ner" in self.nlp.pipe_names:
            ner = self.nlp.get_pipe("ner")
        else:
            ner = self.nlp.add_pipe("ner")
            
        # Add custom entity labels
        custom_entities = [
            "PROJECT_NAME", "DEVELOPER", "LOCATION", "CITY", "LOCALITY",
            "PROPERTY_TYPE", "BHK", "AREA", "PRICE", "AMENITY", "FACILITY",
            "NEARBY_PLACE", "DISTANCE", "TIMELINE", "STATUS", "DOCUMENT",
            "FINANCIAL_TERM", "MEASUREMENT", "CURRENCY", "INTENT"
        ]
        
        for entity in custom_entities:
            ner.add_label(entity)
            
        print(f"✅ Added {len(custom_entities)} custom entity labels")
        
    def load_training_data(self):
        """Load Indian real estate training data"""
        try:
            with open("indian_real_estate_training_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.training_data = data.get("indian_real_estate_queries", {})
                self.indian_context = data.get("indian_cultural_context", {})
                print(f"✅ Loaded training data with {len(self.training_data)} categories")
                return True
        except FileNotFoundError:
            print("❌ Training data file not found")
            return False
            
    def create_training_examples(self) -> List[Dict]:
        """Create comprehensive training examples from Indian real estate data"""
        examples = []
        
        # Process each category of queries
        for category, queries in self.training_data.items():
            print(f"Processing category: {category}")
            
            for query in queries:
                # Determine intent based on category
                intent = self.classify_intent_from_category(category)
                
                # Extract entities based on query content
                entities = self.extract_entities_from_query(query)
                
                # Create training example
                example = {
                    "text": query,
                    "intent": intent,
                    "entities": entities,
                    "category": category
                }
                examples.append(example)
                
        print(f"✅ Created {len(examples)} training examples")
        return examples
        
    def classify_intent_from_category(self, category: str) -> str:
        """Classify intent based on query category"""
        intent_mapping = {
            "basic_search_queries": "SEARCH_PROPERTY",
            "bhk_and_size_queries": "FILTER_BY_BHK",
            "price_and_payment_queries": "PRICE_QUERY",
            "location_and_locality_queries": "FILTER_BY_LOCATION",
            "amenity_and_facility_queries": "FILTER_BY_AMENITY",
            "project_status_and_timeline_queries": "GET_DETAILS",
            "developer_and_builder_queries": "GET_DETAILS",
            "investment_and_roi_queries": "INVESTMENT_ANALYSIS",
            "complex_multi_criteria_queries": "COMPLEX_SEARCH",
            "cultural_and_lifestyle_queries": "GET_DETAILS",
            "legal_and_documentation_queries": "GET_DETAILS",
            "comparison_and_analysis_queries": "COMPARE_PROPERTIES",
            "temporal_and_seasonal_queries": "TEMPORAL_SEARCH",
            "financial_planning_queries": "FINANCIAL_ANALYSIS",
            "neighborhood_and_community_queries": "GET_DETAILS",
            "future_development_queries": "FUTURE_ANALYSIS"
        }
        return intent_mapping.get(category, "GENERAL_QUERY")
        
    def extract_entities_from_query(self, query: str) -> List[Dict]:
        """Extract entities from Indian real estate query"""
        entities = []
        
        # Extract BHK information
        bhk_patterns = [
            r'(\d+(?:\.\d+)?)\s*BHK',
            r'(\d+(?:\.\d+)?)\s*bedroom',
            r'(\d+(?:\.\d+)?)\s*RK'
        ]
        
        for pattern in bhk_patterns:
            matches = re.finditer(pattern, query, re.IGNORECASE)
            for match in matches:
                entities.append({
                    "start": match.start(),
                    "end": match.end(),
                    "label": "BHK",
                    "text": match.group(0)
                })
                
        # Extract price information
        price_patterns = [
            r'(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|crore|crores)',
            r'under\s+(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|crore|crores)',
            r'(\d+(?:\.\d+)?)\s*crore\s+budget',
            r'(\d+(?:\.\d+)?)\s*lakh\s+ke\s+liye'
        ]
        
        for pattern in price_patterns:
            matches = re.finditer(pattern, query, re.IGNORECASE)
            for match in matches:
                entities.append({
                    "start": match.start(),
                    "end": match.end(),
                    "label": "PRICE",
                    "text": match.group(0)
                })
                
        # Extract location information
        location_patterns = [
            r'in\s+([A-Za-z\s]+(?:NCR|West|East|North|South)?)',
            r'([A-Za-z\s]+(?:NCR|West|East|North|South)?)\s+mein',
            r'([A-Za-z\s]+(?:NCR|West|East|North|South)?)\s+se\s+kitne\s+door',
            r'([A-Za-z\s]+(?:NCR|West|East|North|South)?)\s+nearby'
        ]
        
        for pattern in location_patterns:
            matches = re.finditer(pattern, query, re.IGNORECASE)
            for match in matches:
                entities.append({
                    "start": match.start(),
                    "end": match.end(),
                    "label": "LOCATION",
                    "text": match.group(1).strip()
                })
                
        # Extract amenities
        amenity_patterns = [
            r'swimming\s+pool',
            r'gym',
            r'parking',
            r'security',
            r'garden',
            r'club\s+house',
            r'power\s+backup',
            r'lift',
            r'CCTV',
            r'play\s+area'
        ]
        
        for pattern in amenity_patterns:
            matches = re.finditer(pattern, query, re.IGNORECASE)
            for match in matches:
                entities.append({
                    "start": match.start(),
                    "end": match.end(),
                    "label": "AMENITY",
                    "text": match.group(0)
                })
                
        # Extract property types
        property_patterns = [
            r'apartment',
            r'flat',
            r'villa',
            r'penthouse',
            r'duplex',
            r'studio',
            r'plot',
            r'house',
            r'ghar',
            r'makaan'
        ]
        
        for pattern in property_patterns:
            matches = re.finditer(pattern, query, re.IGNORECASE)
            for match in matches:
                entities.append({
                    "start": match.start(),
                    "end": match.end(),
                    "label": "PROPERTY_TYPE",
                    "text": match.group(0)
                })
                
        # Extract measurements
        measurement_patterns = [
            r'(\d+(?:\.\d+)?)\s*square\s+feet',
            r'(\d+(?:\.\d+)?)\s*sq\s*ft',
            r'(\d+(?:\.\d+)?)\s*km',
            r'(\d+(?:\.\d+)?)\s*meter',
            r'(\d+(?:\.\d+)?)\s*acre'
        ]
        
        for pattern in measurement_patterns:
            matches = re.finditer(pattern, query, re.IGNORECASE)
            for match in matches:
                entities.append({
                    "start": match.start(),
                    "end": match.end(),
                    "label": "MEASUREMENT",
                    "text": match.group(0)
                })
                
        # Extract financial terms
        financial_patterns = [
            r'EMI',
            r'down\s+payment',
            r'interest\s+rate',
            r'processing\s+fee',
            r'stamp\s+duty',
            r'registration',
            r'GST',
            r'maintenance\s+charges',
            r'ROI',
            r'rental\s+yield'
        ]
        
        for pattern in financial_patterns:
            matches = re.finditer(pattern, query, re.IGNORECASE)
            for match in matches:
                entities.append({
                    "start": match.start(),
                    "end": match.end(),
                    "label": "FINANCIAL_TERM",
                    "text": match.group(0)
                })
                
        # Extract temporal information
        temporal_patterns = [
            r'ready\s+to\s+move',
            r'under\s+construction',
            r'new\s+launch',
            r'pre-launch',
            r'possession',
            r'completion',
            r'construction'
        ]
        
        for pattern in temporal_patterns:
            matches = re.finditer(pattern, query, re.IGNORECASE)
            for match in matches:
                entities.append({
                    "start": match.start(),
                    "end": match.end(),
                    "label": "STATUS",
                    "text": match.group(0)
                })
                
        return entities
        
    def create_spacy_examples(self, training_examples: List[Dict]) -> List[Example]:
        """Convert training examples to spaCy Example objects"""
        spacy_examples = []
        
        for example in training_examples:
            text = example["text"]
            entities = example["entities"]
            
            # Create doc
            doc = self.nlp.make_doc(text)
            
            # Create entity spans
            spans = []
            for entity in entities:
                span = doc.char_span(
                    entity["start"], 
                    entity["end"], 
                    label=entity["label"]
                )
                if span:
                    spans.append(span)
                    
            # Filter overlapping spans
            filtered_spans = filter_spans(spans)
            
            # Create example
            example_doc = doc.copy()
            example_doc.ents = filtered_spans
            
            spacy_example = Example.from_dict(example_doc, {"entities": [(span.start_char, span.end_char, span.label_) for span in filtered_spans]})
            spacy_examples.append(spacy_example)
            
        return spacy_examples
        
    def train_model(self, training_examples: List[Dict], iterations: int = 50) -> bool:
        """Train the NLP model with Indian real estate data"""
        try:
            # Convert to spaCy examples
            spacy_examples = self.create_spacy_examples(training_examples)
            
            if not spacy_examples:
                print("❌ No valid training examples created")
                return False
                
            print(f"✅ Created {len(spacy_examples)} spaCy training examples")
            
            # Get NER pipe
            ner = self.nlp.get_pipe("ner")
            
            # Training loop
            print(f"🚀 Starting training with {iterations} iterations...")
            
            for iteration in range(iterations):
                losses = {}
                
                # Shuffle examples
                random.shuffle(spacy_examples)
                
                # Update model
                self.nlp.update(spacy_examples, drop=0.5, losses=losses)
                
                if (iteration + 1) % 10 == 0:
                    print(f"Iteration {iteration + 1}/{iterations}, Losses: {losses}")
                    
            print("✅ Training completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Training failed: {str(e)}")
            return False
            
    def save_model(self, output_dir: str = "./indian_real_estate_model") -> bool:
        """Save the trained model"""
        try:
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)
            
            self.nlp.to_disk(output_path)
            print(f"✅ Model saved to {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save model: {str(e)}")
            return False
            
    def test_model(self, test_queries: List[str]) -> None:
        """Test the trained model with sample queries"""
        print("\n🧪 Testing trained model...")
        
        for query in test_queries:
            print(f"\nQuery: {query}")
            
            doc = self.nlp(query)
            
            # Extract entities
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            print(f"Entities: {entities}")
            
            # Determine intent (based on entities and content)
            intent = self.determine_intent_from_entities(entities, query)
            print(f"Intent: {intent}")
            
    def determine_intent_from_entities(self, entities: List[Tuple[str, str]], query: str) -> str:
        """Determine intent based on extracted entities and query content"""
        entity_labels = [label for _, label in entities]
        
        # Complex search detection
        if len(entities) >= 4:
            return "COMPLEX_SEARCH"
            
        # Specific intent detection
        if "BHK" in entity_labels and "PRICE" in entity_labels:
            return "FILTER_BY_BHK_AND_PRICE"
            
        if "LOCATION" in entity_labels and "AMENITY" in entity_labels:
            return "FILTER_BY_LOCATION_AND_AMENITY"
            
        if "PRICE" in entity_labels:
            return "PRICE_QUERY"
            
        if "BHK" in entity_labels:
            return "FILTER_BY_BHK"
            
        if "LOCATION" in entity_labels:
            return "FILTER_BY_LOCATION"
            
        if "AMENITY" in entity_labels:
            return "FILTER_BY_AMENITY"
            
        return "SEARCH_PROPERTY"
        
    def run_comprehensive_training(self) -> bool:
        """Run complete training pipeline"""
        print("🚀 Starting Indian Real Estate NLP Training Pipeline")
        
        # Load training data
        if not self.load_training_data():
            return False
            
        # Create training examples
        training_examples = self.create_training_examples()
        
        if not training_examples:
            print("❌ No training examples created")
            return False
            
        # Train model
        if not self.train_model(training_examples):
            return False
            
        # Save model
        if not self.save_model():
            return False
            
        # Test model
        test_queries = [
            "Mumbai mein 2 BHK under 1 crore chahiye",
            "Bangalore mein swimming pool ke saath villa chahiye",
            "Delhi mein metro station ke paas property dekh raha hun"
        ]
        
        self.test_model(test_queries)
        
        print("🎉 Indian Real Estate NLP Training Pipeline Completed!")
        return True

def main():
    """Main function to run training"""
    trainer = IndianRealEstateTrainer()
    trainer.run_comprehensive_training()

if __name__ == "__main__":
    main()
