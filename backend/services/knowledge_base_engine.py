"""
Knowledge Base NLP Engine - Modular Architecture
Handles knowledge queries independently from search properties
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
class KnowledgeResponse:
    """Knowledge base query response"""
    query: str
    category: str
    question: str
    answer: str
    confidence: float
    suggestions: List[str]

class KnowledgeBaseEngine:
    """Independent engine for knowledge base queries"""
    
    def __init__(self, model_path: str = None):
        """Initialize the knowledge base engine"""
        self.model_path = model_path or "training_data/knowledge_base_model.pkl"
        self.vectorizer = None
        self.knowledge_base = {}
        self.training_data = self._load_training_data()
        self._initialize_models()
    
    def _load_training_data(self) -> Dict:
        """Load knowledge base specific training data"""
        training_file = "training_data/knowledge_base_training_data.json"
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
        """Create default training data structure for knowledge base"""
        return {
            "knowledge_base": {
                "terminology": [
                    {
                        "question": "what is carpet area",
                        "keywords": ["carpet area", "carpet", "area", "what is carpet", "carpet area meaning"],
                        "answer": """<strong>🏠 Carpet Area:</strong><br><br>
                        <strong>Definition:</strong> Carpet area is the actual usable area within the walls of your apartment/house where you can lay a carpet.<br><br>
                        <strong>What's Included:</strong>
                        • Living room, bedrooms, kitchen, bathrooms<br>
                        • Internal walls and columns<br>
                        • Balcony area (50% of balcony)<br><br>
                        <strong>What's NOT Included:</strong>
                        • External walls thickness<br>
                        • Common areas (lobby, stairs, lift)<br>
                        • Terrace, garden, parking<br><br>
                        <strong>Formula:</strong> Carpet Area = Built-up Area - (Wall thickness + Common areas)<br><br>
                        <strong>Example:</strong> If built-up area is 1000 sq ft, carpet area might be 800-850 sq ft."""
                    },
                    {
                        "question": "what is bhk",
                        "keywords": ["bhk", "bedroom", "bed room", "what is bhk", "bhk meaning", "bedroom hall kitchen"],
                        "answer": """<strong>🛏️ BHK (Bedroom, Hall, Kitchen):</strong><br><br>
                        <strong>Definition:</strong> BHK is a standard way to describe the layout of residential properties in India.<br><br>
                        <strong>Components:</strong>
                        • <strong>B</strong> = Bedroom(s)<br>
                        • <strong>H</strong> = Hall (Living room)<br>
                        • <strong>K</strong> = Kitchen<br><br>
                        <strong>Common BHK Types:</strong>
                        • <strong>1 BHK:</strong> 1 Bedroom + 1 Hall + 1 Kitchen<br>
                        • <strong>2 BHK:</strong> 2 Bedrooms + 1 Hall + 1 Kitchen<br>
                        • <strong>3 BHK:</strong> 3 Bedrooms + 1 Hall + 1 Kitchen<br><br>
                        <strong>Example:</strong> 2 BHK means you get 2 bedrooms, 1 living room, and 1 kitchen."""
                    }
                ],
                "legal_regulatory": [
                    {
                        "question": "what is rera",
                        "keywords": ["rera", "real estate regulation act", "what is rera", "rera act", "real estate regulation"],
                        "answer": """<strong>⚖️ RERA (Real Estate Regulation and Development Act):</strong><br><br>
                        <strong>Definition:</strong> RERA is a law enacted by the Indian government to protect homebuyers and bring transparency to the real estate sector.<br><br>
                        <strong>Key Features:</strong>
                        • <strong>Project Registration:</strong> All projects must be registered with RERA<br>
                        • <strong>Transparency:</strong> Developers must disclose project details, approvals, and timelines<br>
                        • <strong>Escrow Account:</strong> 70% of project funds must be in separate bank accounts<br>
                        • <strong>Timeline Compliance:</strong> Developers must complete projects on time<br><br>
                        <strong>Benefits for Buyers:</strong>
                        • Protection against project delays<br>
                        • Transparent project information<br>
                        • Legal recourse for grievances<br>
                        • Standardized sale agreements"""
                    }
                ],
                "processes": [
                    {
                        "question": "how to buy property in india",
                        "keywords": ["how to buy", "buying process", "property buying", "steps to buy", "buying home"],
                        "answer": """<strong>🏠 Complete Property Buying Process in India:</strong><br><br>
                        <strong>Step 1: Planning & Research</strong>
                        • Determine budget and requirements<br>
                        • Research locations and property types<br>
                        • Check property prices and trends<br><br>
                        <strong>Step 2: Property Search</strong>
                        • Visit properties and projects<br>
                        • Compare different options<br>
                        • Check developer reputation<br><br>
                        <strong>Step 3: Legal Verification</strong>
                        • Verify property documents<br>
                        • Check title and ownership<br>
                        • Verify approvals and NOCs<br><br>
                        <strong>Step 4: Financial Planning</strong>
                        • Arrange down payment<br>
                        • Apply for home loan<br>
                        • Calculate total costs (including taxes)<br><br>
                        <strong>Timeline:</strong> 3-6 months for complete process"""
                    }
                ],
                "investment": [
                    {
                        "question": "is real estate good investment",
                        "keywords": ["investment", "good investment", "real estate investment", "worth investing", "investment advice"],
                        "answer": """<strong>💰 Real Estate as an Investment:</strong><br><br>
                        <strong>Pros:</strong>
                        • <strong>Tangible Asset:</strong> Physical property you can see and touch<br>
                        • <strong>Appreciation:</strong> Property values generally increase over time<br>
                        • <strong>Rental Income:</strong> Regular monthly income from tenants<br>
                        • <strong>Tax Benefits:</strong> Deductions on home loan interest and property tax<br>
                        • <strong>Hedge Against Inflation:</strong> Property values rise with inflation<br><br>
                        <strong>Cons:</strong>
                        • <strong>Illiquid:</strong> Takes time to sell<br>
                        • <strong>High Transaction Costs:</strong> Stamp duty, registration, brokerage<br>
                        • <strong>Maintenance:</strong> Regular repairs and upkeep required<br>
                        • <strong>Market Risk:</strong> Property values can decrease<br><br>
                        <strong>Best Investment Scenarios:</strong>
                        • Long-term investment (5+ years)<br>
                        • High-growth locations<br>
                        • Good rental demand<br>
                        • Stable income source"""
                    }
                ]
            },
            "intent_patterns": {
                "knowledge_query": [
                    "what is", "how to", "tell me about", "explain", "define", "meaning of",
                    "what are", "how do", "can you explain", "i want to know about"
                ]
            }
        }
    
    def _initialize_models(self):
        """Initialize NLP models for knowledge base"""
        try:
            # Load knowledge base data
            self.knowledge_base = self.training_data["knowledge_base"]
            
            # Initialize TF-IDF vectorizer for question matching
            self.vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 3)
            )
            
            # Prepare training data for vectorizer
            training_texts = []
            training_labels = []
            
            for category, qa_pairs in self.knowledge_base.items():
                for qa in qa_pairs:
                    training_texts.append(qa["question"])
                    training_labels.append(f"{category}:{qa['question']}")
            
            # Fit vectorizer
            if training_texts:
                self.vectorizer.fit(training_texts)
                print(f"✅ Knowledge Base Engine initialized with {len(training_texts)} training examples")
            else:
                print("⚠️ No training data available for knowledge base")
                
        except Exception as e:
            print(f"❌ Error initializing knowledge base models: {e}")
    
    def is_knowledge_query(self, query: str) -> bool:
        """Check if a query is a knowledge query"""
        query_lower = query.lower()
        patterns = self.training_data["intent_patterns"]["knowledge_query"]
        
        return any(pattern in query_lower for pattern in patterns)
    
    def search_knowledge(self, query: str) -> Optional[KnowledgeResponse]:
        """Search the knowledge base for relevant answers"""
        try:
            if not self.is_knowledge_query(query):
                return None
            
            query_lower = query.lower()
            
            # Use TF-IDF for similarity matching
            if self.vectorizer:
                query_vector = self.vectorizer.transform([query_lower])
                
                best_match = None
                best_score = 0.0
                best_category = ""
                best_question = ""
                
                # Search through all categories
                for category, qa_pairs in self.knowledge_base.items():
                    for qa in qa_pairs:
                        # Check exact keyword matches first
                        if any(keyword in query_lower for keyword in qa["keywords"]):
                            score = 0.9  # High confidence for exact matches
                        else:
                            # Use TF-IDF similarity
                            question_vector = self.vectorizer.transform([qa["question"]])
                            score = cosine_similarity(query_vector, question_vector)[0][0]
                        
                        if score > best_score and score > 0.3:  # Minimum threshold
                            best_score = score
                            best_match = qa
                            best_category = category
                            best_question = qa["question"]
                
                if best_match:
                    # Get suggestions for related questions
                    suggestions = self._get_suggestions(best_category, best_question)
                    
                    return KnowledgeResponse(
                        query=query,
                        category=best_category,
                        question=best_question,
                        answer=best_match["answer"],
                        confidence=best_score,
                        suggestions=suggestions
                    )
            
            return None
            
        except Exception as e:
            print(f"❌ Error searching knowledge base: {e}")
            return None
    
    def _get_suggestions(self, category: str, current_question: str) -> List[str]:
        """Get suggestions for related questions"""
        suggestions = []
        try:
            qa_pairs = self.knowledge_base.get(category, [])
            
            # Get up to 3 suggestions, excluding current question
            for qa in qa_pairs:
                if qa["question"] != current_question and len(suggestions) < 3:
                    suggestions.append(qa["question"].title())
            
            # If not enough suggestions in current category, add from others
            if len(suggestions) < 3:
                for cat, cat_qa_pairs in self.knowledge_base.items():
                    if cat != category:
                        for qa in cat_qa_pairs:
                            if len(suggestions) < 3:
                                suggestions.append(qa["question"].title())
                            else:
                                break
                        if len(suggestions) >= 3:
                            break
                            
        except Exception as e:
            print(f"❌ Error getting suggestions: {e}")
        
        return suggestions
    
    def get_categories(self) -> List[str]:
        """Get list of available knowledge categories"""
        return list(self.knowledge_base.keys())
    
    def get_category_qa_pairs(self, category: str) -> List[Dict]:
        """Get all Q&A pairs for a specific category"""
        return self.knowledge_base.get(category, [])
    
    def add_qa_pair(self, category: str, question: str, keywords: List[str], answer: str):
        """Add a new Q&A pair to the knowledge base"""
        try:
            if category not in self.knowledge_base:
                self.knowledge_base[category] = []
            
            new_qa = {
                "question": question.lower(),
                "keywords": [kw.lower() for kw in keywords],
                "answer": answer
            }
            
            self.knowledge_base[category].append(new_qa)
            
            # Retrain the model with new data
            self._initialize_models()
            
            print(f"✅ Added new Q&A pair to category '{category}'")
            
        except Exception as e:
            print(f"❌ Error adding Q&A pair: {e}")
    
    def train_model(self, new_training_data: Dict):
        """Train the model with new data"""
        try:
            # Update knowledge base
            if "knowledge_base" in new_training_data:
                for category, qa_pairs in new_training_data["knowledge_base"].items():
                    if category not in self.knowledge_base:
                        self.knowledge_base[category] = []
                    
                    for qa in qa_pairs:
                        self.knowledge_base[category].append(qa)
            
            # Update intent patterns
            if "intent_patterns" in new_training_data:
                self.training_data["intent_patterns"].update(new_training_data["intent_patterns"])
            
            # Reinitialize models with new data
            self._initialize_models()
            
            print("✅ Knowledge base model retrained successfully")
            
        except Exception as e:
            print(f"❌ Error training knowledge base model: {e}")
    
    def save_model(self, path: str = None):
        """Save the trained model"""
        try:
            save_path = path or self.model_path
            
            # Update training data with current knowledge base
            self.training_data["knowledge_base"] = self.knowledge_base
            
            # Save training data
            training_file = "training_data/knowledge_base_training_data.json"
            with open(training_file, 'w', encoding='utf-8') as f:
                json.dump(self.training_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Knowledge base model saved to {training_file}")
            
        except Exception as e:
            print(f"❌ Error saving knowledge base model: {e}")
    
    def evaluate_model(self, test_queries: List[Tuple[str, str, str]]) -> Dict[str, float]:
        """Evaluate model performance on test queries"""
        try:
            correct = 0
            total = len(test_queries)
            
            for query, expected_category, expected_question in test_queries:
                result = self.search_knowledge(query)
                if result and result.category == expected_category and result.question == expected_question:
                    correct += 1
            
            accuracy = correct / total if total > 0 else 0.0
            
            return {
                "accuracy": accuracy,
                "correct_predictions": correct,
                "total_queries": total
            }
            
        except Exception as e:
            print(f"❌ Error evaluating knowledge base model: {e}")
            return {"accuracy": 0.0, "correct_predictions": 0, "total_queries": 0}
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        try:
            total_qa_pairs = sum(len(qa_pairs) for qa_pairs in self.knowledge_base.values())
            total_categories = len(self.knowledge_base)
            
            category_stats = {}
            for category, qa_pairs in self.knowledge_base.items():
                category_stats[category] = len(qa_pairs)
            
            return {
                "total_qa_pairs": total_qa_pairs,
                "total_categories": total_categories,
                "category_distribution": category_stats,
                "model_initialized": self.vectorizer is not None
            }
            
        except Exception as e:
            print(f"❌ Error getting statistics: {e}")
            return {}
