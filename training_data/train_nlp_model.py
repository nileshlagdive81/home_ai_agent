#!/usr/bin/env python3
"""
Training script for the NLP model using field-specific training data
"""

import json
import spacy
from spacy.tokens import DocBin
from spacy.util import filter_spans
from spacy.training import Example
import random
from pathlib import Path

def load_training_data(file_path: str):
    """Load training data from JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_training_examples(training_data):
    """Create spaCy training examples from the training data"""
    examples = []
    
    # Process project fields
    for field_name, field_data in training_data["project_fields"].items():
        intent = field_data["intent"]
        entities = field_data["entities"]
        
        for query in field_data["examples"]:
            # Create entity annotations
            ents = []
            
            # Simple entity extraction based on field type
            if "PROJECT_NAME" in entities:
                # Find project name patterns
                if "project" in query.lower():
                    start = query.lower().find("project")
                    end = start + len("project")
                    ents.append((start, end, "PROJECT_NAME"))
            
            elif "DEVELOPER" in entities:
                # Find developer patterns
                if "developer" in query.lower() or "builder" in query.lower():
                    start = query.lower().find("developer") if "developer" in query.lower() else query.lower().find("builder")
                    end = start + len("developer") if "developer" in query.lower() else start + len("builder")
                    ents.append((start, end, "DEVELOPER"))
            
            elif "LOCATION" in entities:
                # Find location patterns
                if "locality" in query.lower() or "area" in query.lower() or "city" in query.lower():
                    start = query.lower().find("locality") if "locality" in query.lower() else query.lower().find("area") if "area" in query.lower() else query.lower().find("city")
                    end = start + len("locality") if "locality" in query.lower() else start + len("area") if "area" in query.lower() else start + len("city")
                    ents.append((start, end, "LOCATION"))
            
            elif "PROPERTY_TYPE" in entities:
                # Find property type patterns
                if "property" in query.lower() or "apartment" in query.lower() or "villa" in query.lower():
                    start = query.lower().find("property") if "property" in query.lower() else query.lower().find("apartment") if "apartment" in query.lower() else query.lower().find("villa")
                    end = start + len("property") if "property" in query.lower() else start + len("apartment") if "apartment" in query.lower() else start + len("villa")
                    ents.append((start, end, "PROPERTY_TYPE"))
            
            elif "QUANTITY" in entities:
                # Find quantity patterns
                if "how many" in query.lower() or "count" in query.lower() or "number" in query.lower():
                    start = query.lower().find("how many") if "how many" in query.lower() else query.lower().find("count") if "count" in query.lower() else query.lower().find("number")
                    end = start + len("how many") if "how many" in query.lower() else start + len("count") if "count" in query.lower() else start + len("number")
                    ents.append((start, end, "QUANTITY"))
            
            elif "STATUS" in entities:
                # Find status patterns
                if "status" in query.lower() or "ready" in query.lower() or "completed" in query.lower():
                    start = query.lower().find("status") if "status" in query.lower() else query.lower().find("ready") if "ready" in query.lower() else query.lower().find("completed")
                    end = start + len("status") if "status" in query.lower() else start + len("ready") if "ready" in query.lower() else start + len("completed")
                    ents.append((start, end, "STATUS"))
            
            elif "DATE" in entities:
                # Find date patterns
                if "when" in query.lower() or "date" in query.lower():
                    start = query.lower().find("when") if "when" in query.lower() else query.lower().find("date")
                    end = start + len("when") if "when" in query.lower() else start + len("date")
                    ents.append((start, end, "DATE"))
            
            elif "RERA_NUMBER" in entities:
                # Find RERA patterns
                if "rera" in query.lower():
                    start = query.lower().find("rera")
                    end = start + len("rera")
                    ents.append((start, end, "RERA_NUMBER"))
            
            elif "DESCRIPTION" in entities:
                # Find description patterns
                if "about" in query.lower() or "description" in query.lower() or "details" in query.lower():
                    start = query.lower().find("about") if "about" in query.lower() else query.lower().find("description") if "description" in query.lower() else query.lower().find("details")
                    end = start + len("about") if "about" in query.lower() else start + len("description") if "description" in query.lower() else start + len("details")
                    ents.append((start, end, "DESCRIPTION"))
            
            elif "FEATURES" in entities:
                # Find features patterns
                if "highlights" in query.lower() or "features" in query.lower() or "special" in query.lower():
                    start = query.lower().find("highlights") if "highlights" in query.lower() else query.lower().find("features") if "features" in query.lower() else query.lower().find("special")
                    end = start + len("highlights") if "highlights" in query.lower() else start + len("features") if "features" in query.lower() else start + len("special")
                    ents.append((start, end, "FEATURES"))
            
            # Create training example
            example = {
                "text": query,
                "intent": intent,
                "entities": ents
            }
            examples.append(example)
    
    # Process property unit fields
    for field_name, field_data in training_data["property_unit_fields"].items():
        intent = field_data["intent"]
        entities = field_data["entities"]
        
        for query in field_data["examples"]:
            ents = []
            
            if "BHK" in entities:
                if "bhk" in query.lower() or "bedroom" in query.lower():
                    start = query.lower().find("bhk") if "bhk" in query.lower() else query.lower().find("bedroom")
                    end = start + len("bhk") if "bhk" in query.lower() else start + len("bedroom")
                    ents.append((start, end, "BHK"))
            
            elif "AREA" in entities:
                if "area" in query.lower() or "size" in query.lower() or "square" in query.lower():
                    start = query.lower().find("area") if "area" in query.lower() else query.lower().find("size") if "size" in query.lower() else query.lower().find("square")
                    end = start + len("area") if "area" in query.lower() else start + len("size") if "size" in query.lower() else start + len("square")
                    ents.append((start, end, "AREA"))
            
            elif "PRICE" in entities:
                if "price" in query.lower() or "cost" in query.lower() or "amount" in query.lower():
                    start = query.lower().find("price") if "price" in query.lower() else query.lower().find("cost") if "cost" in query.lower() else query.lower().find("amount")
                    end = start + len("price") if "price" in query.lower() else start + len("cost") if "cost" in query.lower() else start + len("amount")
                    ents.append((start, end, "PRICE"))
            
            example = {
                "text": query,
                "intent": intent,
                "entities": ents
            }
            examples.append(example)
    
    # Process amenity fields
    for field_name, field_data in training_data["amenity_fields"].items():
        intent = field_data["intent"]
        entities = field_data["entities"]
        
        for query in field_data["examples"]:
            ents = []
            
            if "AMENITY" in entities:
                if "amenity" in query.lower() or "facility" in query.lower() or "feature" in query.lower():
                    start = query.lower().find("amenity") if "amenity" in query.lower() else query.lower().find("facility") if "facility" in query.lower() else query.lower().find("feature")
                    end = start + len("amenity") if "amenity" in query.lower() else start + len("facility") if "facility" in query.lower() else start + len("feature")
                    ents.append((start, end, "AMENITY"))
            
            example = {
                "text": query,
                "intent": intent,
                "entities": ents
            }
            examples.append(example)
    
    # Process nearby places
    for place_name, place_data in training_data["nearby_places"].items():
        intent = place_data["intent"]
        entities = place_data["entities"]
        
        for query in place_data["examples"]:
            ents = []
            
            if "LOCATION" in entities:
                if place_name.replace("_", " ") in query.lower():
                    start = query.lower().find(place_name.replace("_", " "))
                    end = start + len(place_name.replace("_", " "))
                    ents.append((start, end, "LOCATION"))
            
            if "DISTANCE" in entities:
                if "distance" in query.lower() or "far" in query.lower() or "nearby" in query.lower():
                    start = query.lower().find("distance") if "distance" in query.lower() else query.lower().find("far") if "far" in query.lower() else query.lower().find("nearby")
                    end = start + len("distance") if "distance" in query.lower() else start + len("far") if "far" in query.lower() else start + len("nearby")
                    ents.append((start, end, "DISTANCE"))
            
            example = {
                "text": query,
                "intent": intent,
                "entities": ents
            }
            examples.append(example)
    
    # Process simple search queries
    for search_type, search_data in training_data["simple_search_queries"].items():
        intent = search_data["intent"]
        entities = search_data["entities"]
        
        for query in search_data["examples"]:
            ents = []
            
            if "LOCATION" in entities:
                # Find city names in the query
                cities = ["mumbai", "delhi", "bangalore", "pune", "hyderabad", "chennai", "kolkata", "ahmedabad"]
                for city in cities:
                    if city in query.lower():
                        start = query.lower().find(city)
                        end = start + len(city)
                        ents.append((start, end, "LOCATION"))
                        break
            
            elif "BHK" in entities:
                # Find BHK numbers in the query
                import re
                bhk_match = re.search(r'(\d+)BHK', query, re.IGNORECASE)
                if bhk_match:
                    start = bhk_match.start()
                    end = bhk_match.end()
                    ents.append((start, end, "BHK"))
            
            elif "PRICE" in entities:
                # Find price patterns in the query
                if "lakh" in query.lower() or "crore" in query.lower() or "under" in query.lower():
                    start = query.lower().find("lakh") if "lakh" in query.lower() else query.lower().find("crore") if "crore" in query.lower() else query.lower().find("under")
                    end = start + len("lakh") if "lakh" in query.lower() else start + len("crore") if "crore" in query.lower() else start + len("under")
                    ents.append((start, end, "PRICE"))
            
            elif "STATUS" in entities:
                # Find status patterns in the query
                if "ready" in query.lower() or "construction" in query.lower() or "completed" in query.lower() or "new" in query.lower():
                    start = query.lower().find("ready") if "ready" in query.lower() else query.lower().find("construction") if "construction" in query.lower() else query.lower().find("completed") if "completed" in query.lower() else query.lower().find("new")
                    end = start + len("ready") if "ready" in query.lower() else start + len("construction") if "construction" in query.lower() else start + len("completed") if "completed" in query.lower() else start + len("new")
                    ents.append((start, end, "STATUS"))
            
            example = {
                "text": query,
                "intent": intent,
                "entities": ents
            }
            examples.append(example)
    
    return examples

def train_nlp_model(training_examples, model_name="en_core_web_sm", output_dir="./trained_model"):
    """Train the NLP model with the provided examples"""
    
    # Load the base model
    try:
        nlp = spacy.load(model_name)
        print(f"✅ Loaded base model: {model_name}")
    except OSError:
        print(f"❌ Model {model_name} not found. Please install it with: python -m spacy download {model_name}")
        return None
    
    # Add custom entity types if they don't exist
    ner = nlp.get_pipe("ner")
    custom_entities = [
        "PROJECT_NAME", "DEVELOPER", "LOCATION", "PROPERTY_TYPE", "QUANTITY",
        "STATUS", "DATE", "RERA_NUMBER", "DESCRIPTION", "FEATURES",
        "BHK", "AREA", "PRICE", "AMENITY", "DISTANCE"
    ]
    
    for entity in custom_entities:
        if entity not in ner.labels:
            ner.add_label(entity)
            print(f"✅ Added entity label: {entity}")
    
    # Prepare training data
    train_data = []
    for example in training_examples:
        # Create entity spans
        ents = []
        for start, end, label in example["entities"]:
            span = nlp.make_doc(example["text"])[start:end]
            ents.append(span)
        
        # Create training example
        doc = nlp.make_doc(example["text"])
        ents = filter_spans(ents)
        doc.ents = ents
        
        train_data.append(Example.from_dict(doc, {"entities": [(e.start, e.end, e.label_) for e in ents]}))
    
    print(f"✅ Prepared {len(train_data)} training examples")
    
    # Training configuration
    n_iter = 30
    dropout = 0.5
    
    # Train the model
    print("🚀 Starting training...")
    losses = {}
    
    for i in range(n_iter):
        random.shuffle(train_data)
        nlp.update(train_data, drop=dropout, losses=losses)
        
        if i % 5 == 0:
            print(f"  Iteration {i+1}/{n_iter}, Losses: {losses}")
    
    print("✅ Training completed!")
    
    # Save the trained model
    output_path = Path(output_dir)
    if not output_path.exists():
        output_path.mkdir()
    
    nlp.to_disk(output_path)
    print(f"✅ Model saved to {output_path}")
    
    return nlp

def test_trained_model(nlp, test_queries):
    """Test the trained model with sample queries"""
    print("\n🧪 Testing trained model...")
    print("=" * 50)
    
    for query in test_queries:
        doc = nlp(query)
        print(f"\nQuery: {query}")
        print(f"Entities: {[(e.text, e.label_) for e in doc.ents]}")
        
        # Simple intent classification based on entities
        if any(e.label_ == "LOCATION" for e in doc.ents):
            if any(e.label_ == "BHK" for e in doc.ents):
                intent = "SEARCH_PROPERTY"
            else:
                intent = "FILTER_BY_LOCATION"
        elif any(e.label_ == "BHK" for e in doc.ents):
            intent = "FILTER_BY_BHK"
        elif any(e.label_ == "PRICE" for e in doc.ents):
            intent = "PRICE_QUERY"
        elif any(e.label_ == "AMENITY" for e in doc.ents):
            intent = "FILTER_BY_AMENITY"
        else:
            intent = "GET_DETAILS"
        
        print(f"Detected Intent: {intent}")

def main():
    """Main training function"""
    print("🚀 Starting NLP Model Training for Real Estate...")
    
    # Load training data
    training_data = load_training_data("field_training_data.json")
    print(f"✅ Loaded training data with {len(training_data)} categories")
    
    # Create training examples
    training_examples = create_training_examples(training_data)
    print(f"✅ Created {len(training_examples)} training examples")
    
    # Train the model
    trained_model = train_nlp_model(training_examples)
    
    if trained_model:
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
        
        test_trained_model(trained_model, test_queries)
        
        print("\n🎉 Training completed successfully!")
        print("You can now use the trained model for better entity recognition and intent classification.")
    else:
        print("❌ Training failed!")

if __name__ == "__main__":
    main()
