"""
NLP Orchestrator - Routes queries to appropriate engines
Prevents interference between search properties and knowledge base models
"""

from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass
import logging

# Import the modular engines
from .search_properties_engine import SearchPropertiesEngine, SearchIntent
from .knowledge_base_engine import KnowledgeBaseEngine, KnowledgeResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class OrchestratedResponse:
    """Unified response from the orchestrator"""
    query: str
    engine_used: str
    confidence: float
    response_data: Union[SearchIntent, KnowledgeResponse]
    routing_reason: str

class NLPOrchestrator:
    """Routes queries to appropriate engines without interference"""
    
    def __init__(self):
        """Initialize the orchestrator with both engines"""
        logger.info("🚀 Initializing NLP Orchestrator...")
        
        # Initialize both engines independently
        self.search_engine = SearchPropertiesEngine()
        self.knowledge_engine = KnowledgeBaseEngine()
        
        # Routing thresholds
        self.knowledge_threshold = 0.7
        self.search_threshold = 0.6
        
        logger.info("✅ NLP Orchestrator initialized successfully")
        logger.info(f"📊 Search Properties Engine: {self.search_engine.__class__.__name__}")
        logger.info(f"📚 Knowledge Base Engine: {self.knowledge_engine.__class__.__name__}")
    
    def route_query(self, query: str) -> OrchestratedResponse:
        """Route a query to the appropriate engine"""
        try:
            logger.info(f"🔍 Routing query: '{query}'")
            
            # Step 1: Check if it's a knowledge query
            if self._is_knowledge_query(query):
                logger.info("📚 Query classified as knowledge query")
                return self._handle_knowledge_query(query)
            
            # Step 2: Check if it's a search query
            elif self._is_search_query(query):
                logger.info("🏠 Query classified as search query")
                return self._handle_search_query(query)
            
            # Step 3: Fallback - let both engines try
            else:
                logger.info("🤔 Query type unclear, trying both engines")
                return self._handle_ambiguous_query(query)
                
        except Exception as e:
            logger.error(f"❌ Error routing query: {e}")
            return OrchestratedResponse(
                query=query,
                engine_used="error",
                confidence=0.0,
                response_data=None,
                routing_reason=f"Error: {str(e)}"
            )
    
    def _is_knowledge_query(self, query: str) -> bool:
        """Check if query is clearly a knowledge query"""
        query_lower = query.lower()
        
        # Strong knowledge indicators
        knowledge_patterns = [
            "what is", "how to", "tell me about", "explain", "define", 
            "meaning of", "what are", "how do", "can you explain",
            "i want to know about", "what does", "how does",
            "tell me more about", "describe", "elaborate on"
        ]
        
        # Check for knowledge patterns
        has_knowledge_pattern = any(pattern in query_lower for pattern in knowledge_patterns)
        
        # Check if knowledge engine can handle it
        knowledge_response = self.knowledge_engine.search_knowledge(query)
        knowledge_confidence = knowledge_response.confidence if knowledge_response else 0.0
        
        # Strong knowledge query if pattern matches and confidence is high
        return has_knowledge_pattern and knowledge_confidence > self.knowledge_threshold
    
    def _is_search_query(self, query: str) -> bool:
        """Check if query is clearly a search query"""
        query_lower = query.lower()
        
        # Strong search indicators
        search_patterns = [
            "show me", "find", "looking for", "need", "want",
            "properties", "houses", "apartments", "flats", "villas",
            "in", "near", "with", "under", "above", "between"
        ]
        
        # Check for search patterns
        has_search_pattern = any(pattern in query_lower for pattern in search_patterns)
        
        # Check if search engine can handle it
        search_response = self.search_engine.classify_intent(query)
        search_confidence = search_response.confidence if search_response else 0.0
        
        # Strong search query if pattern matches and confidence is high
        return has_search_pattern and search_confidence > self.search_threshold
    
    def _handle_knowledge_query(self, query: str) -> OrchestratedResponse:
        """Handle knowledge queries"""
        try:
            knowledge_response = self.knowledge_engine.search_knowledge(query)
            
            if knowledge_response:
                return OrchestratedResponse(
                    query=query,
                    engine_used="knowledge_base",
                    confidence=knowledge_response.confidence,
                    response_data=knowledge_response,
                    routing_reason="Clear knowledge query pattern with high confidence"
                )
            else:
                # Fallback to search engine
                return self._handle_search_query(query)
                
        except Exception as e:
            logger.error(f"❌ Error handling knowledge query: {e}")
            return self._handle_search_query(query)
    
    def _handle_search_query(self, query: str) -> OrchestratedResponse:
        """Handle search queries"""
        try:
            search_response = self.search_engine.classify_intent(query)
            
            if search_response:
                return OrchestratedResponse(
                    query=query,
                    engine_used="search_properties",
                    confidence=search_response.confidence,
                    response_data=search_response,
                    routing_reason="Clear search query pattern with high confidence"
                )
            else:
                # Fallback to knowledge engine
                return self._handle_knowledge_query(query)
                
        except Exception as e:
            logger.error(f"❌ Error handling search query: {e}")
            return self._handle_knowledge_query(query)
    
    def _handle_ambiguous_query(self, query: str) -> OrchestratedResponse:
        """Handle queries that could be either type"""
        try:
            # Try both engines
            knowledge_response = self.knowledge_engine.search_knowledge(query)
            search_response = self.search_engine.classify_intent(query)
            
            knowledge_confidence = knowledge_response.confidence if knowledge_response else 0.0
            search_confidence = search_response.confidence if search_response else 0.0
            
            # Route to the engine with higher confidence
            if knowledge_confidence > search_confidence and knowledge_confidence > 0.3:
                return OrchestratedResponse(
                    query=query,
                    engine_used="knowledge_base",
                    confidence=knowledge_confidence,
                    response_data=knowledge_response,
                    routing_reason=f"Ambiguous query - knowledge engine had higher confidence ({knowledge_confidence:.2f} vs {search_confidence:.2f})"
                )
            elif search_confidence > 0.3:
                return OrchestratedResponse(
                    query=query,
                    engine_used="search_properties",
                    confidence=search_confidence,
                    response_data=search_response,
                    routing_reason=f"Ambiguous query - search engine had higher confidence ({search_confidence:.2f} vs {knowledge_confidence:.2f})"
                )
            else:
                # Neither engine confident enough
                return OrchestratedResponse(
                    query=query,
                    engine_used="fallback",
                    confidence=0.0,
                    response_data=None,
                    routing_reason="Neither engine confident enough - query may need clarification"
                )
                
        except Exception as e:
            logger.error(f"❌ Error handling ambiguous query: {e}")
            return OrchestratedResponse(
                query=query,
                engine_used="error",
                confidence=0.0,
                response_data=None,
                routing_reason=f"Error handling ambiguous query: {str(e)}"
            )
    
    def get_engine_statistics(self) -> Dict[str, Any]:
        """Get statistics from both engines"""
        try:
            search_stats = self.search_engine.evaluate_model([])  # Empty test for stats
            knowledge_stats = self.knowledge_engine.get_statistics()
            
            return {
                "search_properties_engine": {
                    "status": "initialized",
                    "training_examples": len(self.search_engine.training_data.get("search_properties", {}).get("intents", {})),
                    "intents_supported": list(self.search_engine.training_data.get("search_properties", {}).get("intents", {}).keys())
                },
                "knowledge_base_engine": {
                    "status": "initialized",
                    "total_qa_pairs": knowledge_stats.get("total_qa_pairs", 0),
                    "categories": knowledge_stats.get("category_distribution", {}),
                    "model_initialized": knowledge_stats.get("model_initialized", False)
                },
                "orchestrator": {
                    "routing_thresholds": {
                        "knowledge": self.knowledge_threshold,
                        "search": self.search_threshold
                    },
                    "status": "active"
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting engine statistics: {e}")
            return {"error": str(e)}
    
    def retrain_engines(self, search_data: Dict = None, knowledge_data: Dict = None):
        """Retrain both engines independently"""
        try:
            logger.info("🔄 Starting engine retraining...")
            
            # Retrain search engine
            if search_data:
                logger.info("🏠 Retraining search properties engine...")
                self.search_engine.train_model(search_data)
                self.search_engine.save_model()
            
            # Retrain knowledge engine
            if knowledge_data:
                logger.info("📚 Retraining knowledge base engine...")
                self.knowledge_engine.train_model(knowledge_data)
                self.knowledge_engine.save_model()
            
            logger.info("✅ Engine retraining completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Error retraining engines: {e}")
    
    def test_routing(self, test_queries: List[str]) -> List[OrchestratedResponse]:
        """Test routing with multiple queries"""
        results = []
        
        for query in test_queries:
            try:
                result = self.route_query(query)
                results.append(result)
                logger.info(f"✅ Routed '{query}' to {result.engine_used} (confidence: {result.confidence:.2f})")
            except Exception as e:
                logger.error(f"❌ Error routing query '{query}': {e}")
                results.append(OrchestratedResponse(
                    query=query,
                    engine_used="error",
                    confidence=0.0,
                    response_data=None,
                    routing_reason=f"Error: {str(e)}"
                ))
        
        return results
