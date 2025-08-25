import json
import random
from typing import List, Dict, Any
from dataclasses import dataclass
import logging

@dataclass
class AugmentationConfig:
    """Configuration for data augmentation"""
    variations_per_qa: int = 25
    include_hinglish: bool = True
    include_typos: bool = True
    include_regional: bool = True
    pune_locations: bool = True

class DataAugmentationEngine:
    """Engine for generating training data variations"""
    
    def __init__(self, config: AugmentationConfig = None):
        self.config = config or AugmentationConfig()
        self.logger = logging.getLogger(__name__)
        
        # Pune locations and directions
        self.pune_locations = {
            "east": ["Viman Nagar", "Kharadi", "Hadapsar", "Magarpatta", "Wagholi", "Lonikand"],
            "west": ["Koregaon Park", "Boat Club", "Model Colony", "Aundh", "Baner", "Balewadi"],
            "south": ["Hinjewadi", "Wakad", "Baner", "Balewadi", "Pashan", "Sus"],
            "north": ["Kalyani Nagar", "Yerwada", "Kharadi", "Viman Nagar", "Lohegaon", "Chandannagar"],
            "central": ["Camp", "Deccan", "FC Road", "JM Road", "Shivajinagar", "Pune Station"]
        }
        
        # Common variations for questions
        self.question_patterns = {
            "what_is": [
                "what is", "what's", "what is the meaning of", "explain", "define",
                "tell me about", "describe", "what does", "meaning of", "definition of",
                "samjhao", "kya hai", "kya hota hai", "explain kar", "batana"
            ],
            "how_to": [
                "how to", "how do i", "steps to", "process of", "way to",
                "kaise", "kaise kare", "process kya hai", "steps batana"
            ],
            "where": [
                "where", "which area", "which location", "kahan", "kis area mein",
                "kis jagah", "location", "area"
            ],
            "when": [
                "when", "kab", "kis time", "timing", "date", "samay"
            ]
        }
        
        # Entity mappings for auto-expansion
        self.entity_mappings = {
            "property_type": {
                "1bhk": ["1 BHK", "1 Bedroom", "1 Bedroom Hall Kitchen", "Ek BHK"],
                "2bhk": ["2 BHK", "2 Bedroom", "2 Bedroom Hall Kitchen", "Do BHK"],
                "3bhk": ["3 BHK", "3 Bedroom", "3 Bedroom Hall Kitchen", "Teen BHK"],
                "villa": ["Villa", "Independent House", "Bungalow", "Ghar"],
                "apartment": ["Apartment", "Flat", "Unit", "Ghar"]
            },
            "price_range": {
                "affordable": ["Budget", "Cheap", "Low Cost", "Economical", "Sasta", "Kam Daam"],
                "luxury": ["Premium", "High End", "Expensive", "Luxury", "Mahanga", "Premium"],
                "mid_range": ["Mid Range", "Moderate", "Average", "Medium", "Madhyam", "Darmiyan"]
            },
            "location_direction": {
                "east": ["East", "Purv", "Purva", "East Side", "East Area"],
                "west": ["West", "Pashchim", "West Side", "West Area"],
                "north": ["North", "Uttar", "North Side", "North Area"],
                "south": ["South", "Dakshin", "South Side", "South Area"],
                "central": ["Central", "Madhya", "Center", "City Center"]
            }
        }
        
        # Common typos and variations
        self.typo_patterns = {
            "carpet": ["carpt", "carpet", "karpet", "carpet"],
            "area": ["aria", "area", "area", "area"],
            "property": ["proprty", "property", "property", "property"],
            "bhk": ["bhk", "bhk", "bhk", "bhk"],
            "pune": ["pune", "pune", "pune", "pune"]
        }
    
    def generate_question_variations(self, original_question: str, category: str) -> List[str]:
        """Generate 20-30 variations of a question"""
        variations = [original_question]
        
        # Extract key entities from the question
        entities = self._extract_entities(original_question)
        
        # Generate variations based on question type
        if "what is" in original_question.lower():
            variations.extend(self._generate_what_is_variations(original_question, entities))
        elif "how to" in original_question.lower():
            variations.extend(self._generate_how_to_variations(original_question, entities))
        elif "where" in original_question.lower():
            variations.extend(self._generate_where_variations(original_question, entities))
        
        # Add Hinglish variations
        if self.config.include_hinglish:
            variations.extend(self._generate_hinglish_variations(original_question, entities))
        
        # Add Pune-specific variations
        if self.config.include_regional and self.config.pune_locations:
            variations.extend(self._generate_pune_variations(original_question, entities))
        
        # Add typo variations
        if self.config.include_typos:
            variations.extend(self._generate_typo_variations(original_question))
        
        # Ensure we have enough variations
        while len(variations) < self.config.variations_per_qa:
            variations.extend(self._generate_semantic_variations(original_question, entities))
        
        # Remove duplicates and limit to target count
        unique_variations = list(dict.fromkeys(variations))
        return unique_variations[:self.config.variations_per_qa]
    
    def _extract_entities(self, question: str) -> Dict[str, str]:
        """Extract key entities from question for targeted variation generation"""
        entities = {}
        question_lower = question.lower()
        
        # Extract property types
        for prop_type, variations in self.entity_mappings["property_type"].items():
            if prop_type in question_lower:
                entities["property_type"] = prop_type
                break
        
        # Extract price ranges
        for price_range, variations in self.entity_mappings["price_range"].items():
            if price_range in question_lower:
                entities["price_range"] = price_range
                break
        
        # Extract locations
        for direction, locations in self.pune_locations.items():
            for location in locations:
                if location.lower() in question_lower:
                    entities["location"] = location
                    entities["direction"] = direction
                    break
        
        return entities
    
    def _generate_what_is_variations(self, question: str, entities: Dict[str, str]) -> List[str]:
        """Generate variations for 'what is' questions"""
        variations = []
        base_entity = self._get_base_entity(question)
        
        if base_entity:
            variations.extend([
                f"what is {base_entity}",
                f"what's {base_entity}",
                f"what is the meaning of {base_entity}",
                f"explain {base_entity}",
                f"define {base_entity}",
                f"tell me about {base_entity}",
                f"describe {base_entity}",
                f"what does {base_entity} mean",
                f"meaning of {base_entity}",
                f"definition of {base_entity}",
                f"{base_entity} kya hai",
                f"{base_entity} kya hota hai",
                f"{base_entity} samjhao",
                f"{base_entity} explain kar",
                f"{base_entity} batana"
            ])
        
        return variations
    
    def _generate_how_to_variations(self, question: str, entities: Dict[str, str]) -> List[str]:
        """Generate variations for 'how to' questions"""
        variations = []
        base_entity = self._get_base_entity(question)
        
        if base_entity:
            variations.extend([
                f"how to {base_entity}",
                f"how do i {base_entity}",
                f"steps to {base_entity}",
                f"process of {base_entity}",
                f"way to {base_entity}",
                f"{base_entity} kaise kare",
                f"{base_entity} kaise",
                f"{base_entity} process kya hai",
                f"{base_entity} steps batana"
            ])
        
        return variations
    
    def _generate_where_variations(self, question: str, entities: Dict[str, str]) -> List[str]:
        """Generate variations for location-based questions"""
        variations = []
        
        if "location" in entities:
            location = entities["location"]
            direction = entities.get("direction", "")
            
            variations.extend([
                f"where is {location}",
                f"which area is {location}",
                f"location of {location}",
                f"{location} kahan hai",
                f"{location} kis area mein hai",
                f"{location} kis jagah hai",
                f"{location} location",
                f"{location} area"
            ])
            
            if direction:
                variations.extend([
                    f"properties in {direction} Pune",
                    f"houses in {direction} Pune",
                    f"flats in {direction} Pune",
                    f"{direction} Pune mein properties",
                    f"{direction} Pune mein ghar",
                    f"show me {direction} Pune properties"
                ])
        
        return variations
    
    def _generate_hinglish_variations(self, question: str, entities: Dict[str, str]) -> List[str]:
        """Generate Hinglish variations"""
        variations = []
        base_entity = self._get_base_entity(question)
        
        if base_entity:
            variations.extend([
                f"{base_entity} kya hai",
                f"{base_entity} kya hota hai",
                f"{base_entity} samjhao",
                f"{base_entity} explain kar",
                f"{base_entity} batana",
                f"Tell me {base_entity} ke bare mein",
                f"Explain {base_entity} in detail",
                f"{base_entity} ke baare mein batao"
            ])
        
        return variations
    
    def _generate_pune_variations(self, question: str, entities: Dict[str, str]) -> List[str]:
        """Generate Pune-specific variations"""
        variations = []
        
        # Add Pune location variations
        for direction, locations in self.pune_locations.items():
            for location in locations:
                if location.lower() in question.lower():
                    variations.extend([
                        f"properties in {location}, Pune",
                        f"houses in {location}, Pune",
                        f"flats in {location}, Pune",
                        f"{location} mein properties",
                        f"{location} mein ghar",
                        f"show me {location} properties",
                        f"find houses in {location}",
                        f"search properties in {location}"
                    ])
                    break
        
        # Add direction-based variations
        for direction in self.pune_locations.keys():
            if direction in question.lower():
                variations.extend([
                    f"properties in {direction} Pune",
                    f"houses in {direction} Pune",
                    f"flats in {direction} Pune",
                    f"{direction} Pune mein properties",
                    f"{direction} Pune mein ghar",
                    f"show me {direction} Pune properties"
                ])
        
        return variations
    
    def _generate_typo_variations(self, question: str) -> List[str]:
        """Generate typo variations"""
        variations = []
        
        for correct, typos in self.typo_patterns.items():
            if correct in question.lower():
                for typo in typos:
                    if typo != correct:
                        typo_question = question.lower().replace(correct, typo)
                        variations.append(typo_question)
        
        return variations
    
    def _generate_semantic_variations(self, question: str, entities: Dict[str, str]) -> List[str]:
        """Generate semantic variations based on entities"""
        variations = []
        
        if "property_type" in entities:
            prop_type = entities["property_type"]
            for variation in self.entity_mappings["property_type"].get(prop_type, []):
                if variation != prop_type:
                    new_question = question.lower().replace(prop_type, variation)
                    variations.append(new_question)
        
        if "price_range" in entities:
            price_range = entities["price_range"]
            for variation in self.entity_mappings["price_range"].get(price_range, []):
                if variation != price_range:
                    new_question = question.lower().replace(price_range, variation)
                    variations.append(new_question)
        
        return variations
    
    def _get_base_entity(self, question: str) -> str:
        """Extract the main entity being asked about"""
        # Remove question words to get the base entity
        question_lower = question.lower()
        
        # Remove common question starters
        for starter in ["what is", "what's", "how to", "where", "when", "why"]:
            if question_lower.startswith(starter):
                return question_lower[len(starter):].strip()
        
        return question_lower.strip()
    
    def augment_training_data(self, training_data: Dict[str, Any]) -> Dict[str, Any]:
        """Augment the entire training dataset"""
        augmented_data = training_data.copy()
        
        for category, qa_list in training_data.get("knowledge_base", {}).items():
            if isinstance(qa_list, list):
                augmented_qa_list = []
                
                for qa in qa_list:
                    if isinstance(qa, dict) and "question" in qa:
                        # Generate variations for the question
                        variations = self.generate_question_variations(qa["question"], category)
                        
                        # Create augmented Q&A pairs
                        for variation in variations:
                            augmented_qa = qa.copy()
                            augmented_qa["question"] = variation
                            augmented_qa["original_question"] = qa["question"]  # Keep reference
                            augmented_qa["variation_type"] = "augmented"
                            augmented_qa_list.append(augmented_qa)
                
                augmented_data["knowledge_base"][category] = augmented_qa_list
        
        return augmented_data
    
    def save_augmented_data(self, augmented_data: Dict[str, Any], filepath: str):
        """Save augmented data to file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(augmented_data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Augmented data saved to {filepath}")
        except Exception as e:
            self.logger.error(f"Error saving augmented data: {e}")
            raise

if __name__ == "__main__":
    # Test the augmentation engine
    config = AugmentationConfig(
        variations_per_qa=25,
        include_hinglish=True,
        include_typos=True,
        include_regional=True,
        pune_locations=True
    )
    
    engine = DataAugmentationEngine(config)
    
    # Test question variation generation
    test_question = "what is carpet area"
    variations = engine.generate_question_variations(test_question, "terminology")
    
    print(f"Original: {test_question}")
    print(f"Generated {len(variations)} variations:")
    for i, variation in enumerate(variations, 1):
        print(f"{i:2d}. {variation}")
