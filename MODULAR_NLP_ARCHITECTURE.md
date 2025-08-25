# 🏗️ Modular NLP Architecture

## 📖 Overview

This project implements a **modular NLP architecture** that completely separates **Search Properties** and **Knowledge Base** functionality into independent engines. This prevents interference between models and allows for independent training, updates, and operation.

## 🎯 Key Benefits

### ✅ **No Interference**
- Search Properties Engine operates independently
- Knowledge Base Engine operates independently
- Changes to one engine don't affect the other
- Independent training and model updates

### ✅ **Scalability**
- Each engine can be scaled independently
- Different teams can work on different engines
- Independent deployment and updates
- Separate performance monitoring

### ✅ **Maintainability**
- Clear separation of concerns
- Independent bug fixes and improvements
- Easier testing and debugging
- Modular code organization

## 🏛️ Architecture Components

### 1. **Search Properties Engine** (`search_properties_engine.py`)
- **Purpose**: Handles property search queries
- **Capabilities**: Intent classification, entity extraction, search criteria building
- **Training Data**: `training_data/search_properties_training_data.json`
- **Model**: TF-IDF + Cosine Similarity
- **Intents**: Location, BHK, Price, Amenities, Property Type, Status

### 2. **Knowledge Base Engine** (`knowledge_base_engine.py`)
- **Purpose**: Handles knowledge and educational queries
- **Capabilities**: Question matching, answer retrieval, suggestions
- **Training Data**: `training_data/knowledge_base_training_data.json`
- **Model**: TF-IDF + Cosine Similarity
- **Categories**: Terminology, Legal, Processes, Investment

### 3. **NLP Orchestrator** (`nlp_orchestrator.py`)
- **Purpose**: Routes queries to appropriate engines
- **Capabilities**: Query classification, intelligent routing, fallback handling
- **Routing Logic**: Pattern matching + confidence scoring
- **Fallback**: Automatic engine switching for ambiguous queries

## 🔄 How It Works

### **Query Routing Process**

1. **Input Query** → NLP Orchestrator
2. **Pattern Analysis** → Check for knowledge vs search patterns
3. **Engine Selection** → Route to appropriate engine
4. **Response Generation** → Get response from selected engine
5. **Fallback Handling** → Switch engines if needed

### **Routing Logic**

```python
def route_query(self, query: str) -> OrchestratedResponse:
    # Step 1: Check if it's a knowledge query
    if self._is_knowledge_query(query):
        return self._handle_knowledge_query(query)
    
    # Step 2: Check if it's a search query
    elif self._is_search_query(query):
        return self._handle_search_query(query)
    
    # Step 3: Fallback - let both engines try
    else:
        return self._handle_ambiguous_query(query)
```

### **No Interference Guarantee**

- **Separate Training Data**: Each engine has its own JSON file
- **Independent Models**: TF-IDF vectorizers are separate
- **Isolated Updates**: Training one engine doesn't affect the other
- **Separate Statistics**: Performance metrics are tracked independently

## 📁 File Structure

```
backend/services/
├── search_properties_engine.py      # Search properties engine
├── knowledge_base_engine.py         # Knowledge base engine
├── nlp_orchestrator.py             # Query routing orchestrator
└── __pycache__/                    # Python cache files

training_data/
├── search_properties_training_data.json    # Search training data
├── knowledge_base_training_data.json       # Knowledge training data
└── ... (other training files)

test_modular_nlp.py                 # Test script
MODULAR_NLP_ARCHITECTURE.md         # This documentation
```

## 🧪 Testing the Architecture

### **Run the Test Suite**

```bash
python test_modular_nlp.py
```

### **Test Individual Engines**

```python
# Test Search Properties Engine
from backend.services.search_properties_engine import SearchPropertiesEngine
search_engine = SearchPropertiesEngine()
result = search_engine.classify_intent("Show me 2 BHK apartments in Pune")

# Test Knowledge Base Engine
from backend.services.knowledge_base_engine import KnowledgeBaseEngine
knowledge_engine = KnowledgeBaseEngine()
result = knowledge_engine.search_knowledge("What is carpet area?")
```

### **Test the Orchestrator**

```python
from backend.services.nlp_orchestrator import NLPOrchestrator
orchestrator = NLPOrchestrator()

# Test routing
result = orchestrator.route_query("What is carpet area?")
print(f"Routed to: {result.engine_used}")
print(f"Confidence: {result.confidence}")
```

## 📊 Training Data Structure

### **Search Properties Training Data**

```json
{
  "search_properties": {
    "intents": {
      "SEARCH_BY_LOCATION": {
        "examples": ["I want a house in Mumbai", "Show me properties in Pune"],
        "entities": ["LOCATION", "CITY", "LOCALITY"]
      },
      "SEARCH_BY_BHK": {
        "examples": ["2 BHK apartments", "3 BHK houses"],
        "entities": ["BHK", "PROPERTY_TYPE"]
      }
    },
    "entities": {
      "LOCATION": {
        "cities": ["Mumbai", "Delhi", "Bangalore"],
        "localities": ["Bandra", "Andheri", "Powai"]
      }
    }
  }
}
```

### **Knowledge Base Training Data**

```json
{
  "knowledge_base": {
    "terminology": [
      {
        "question": "what is carpet area",
        "keywords": ["carpet area", "carpet", "area"],
        "answer": "Carpet area is the actual usable area...",
        "category": "terminology",
        "difficulty": "beginner"
      }
    ]
  },
  "intent_patterns": {
    "knowledge_query": ["what is", "how to", "tell me about"]
  }
}
```

## 🔧 Configuration

### **Routing Thresholds**

```python
class NLPOrchestrator:
    def __init__(self):
        # Routing thresholds
        self.knowledge_threshold = 0.7    # Knowledge query confidence
        self.search_threshold = 0.6       # Search query confidence
```

### **Model Parameters**

```python
# TF-IDF Vectorizer Configuration
self.vectorizer = TfidfVectorizer(
    max_features=1000,           # Maximum features
    stop_words='english',        # Remove stop words
    ngram_range=(1, 2)          # Unigrams and bigrams
)
```

## 📈 Performance Monitoring

### **Engine Statistics**

```python
stats = orchestrator.get_engine_statistics()
print(stats)

# Output:
{
    "search_properties_engine": {
        "status": "initialized",
        "training_examples": 90,
        "intents_supported": ["SEARCH_BY_LOCATION", "SEARCH_BY_BHK", ...]
    },
    "knowledge_base_engine": {
        "status": "initialized",
        "total_qa_pairs": 15,
        "categories": {"terminology": 5, "legal_regulatory": 4, ...}
    },
    "orchestrator": {
        "routing_thresholds": {"knowledge": 0.7, "search": 0.6},
        "status": "active"
    }
}
```

## 🚀 Adding New Features

### **Adding New Search Intent**

1. **Update Training Data**:
```json
"NEW_INTENT": {
    "examples": ["New example queries"],
    "entities": ["NEW_ENTITY"],
    "description": "Description of the intent"
}
```

2. **Retrain Engine**:
```python
search_engine.train_model(new_data)
search_engine.save_model()
```

### **Adding New Knowledge Category**

1. **Update Training Data**:
```json
"new_category": [
    {
        "question": "new question",
        "keywords": ["keyword1", "keyword2"],
        "answer": "New answer content"
    }
]
```

2. **Retrain Engine**:
```python
knowledge_engine.train_model(new_data)
knowledge_engine.save_model()
```

## 🛠️ Troubleshooting

### **Common Issues**

1. **Import Errors**: Ensure backend directory is in Python path
2. **Training Data Issues**: Check JSON file format and structure
3. **Model Initialization**: Verify TF-IDF vectorizer setup
4. **Routing Problems**: Check confidence thresholds

### **Debug Mode**

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable detailed logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
```

## 🔮 Future Enhancements

### **Planned Features**

- **Machine Learning Models**: Replace TF-IDF with BERT/transformers
- **Real-time Training**: Online learning capabilities
- **Performance Analytics**: Detailed metrics and insights
- **API Endpoints**: RESTful API for each engine
- **Model Versioning**: Track model versions and performance

### **Integration Possibilities**

- **External APIs**: Connect to real estate databases
- **Chatbot Integration**: WhatsApp, Telegram bots
- **Mobile Apps**: Native mobile applications
- **Web Dashboard**: Admin interface for training

## 📝 Best Practices

### **Development Guidelines**

1. **Keep Engines Independent**: Never share data between engines
2. **Consistent Interfaces**: Use similar method names across engines
3. **Error Handling**: Implement proper exception handling
4. **Logging**: Use structured logging for debugging
5. **Testing**: Write comprehensive tests for each engine

### **Training Guidelines**

1. **Quality Data**: Ensure training examples are accurate
2. **Balanced Categories**: Maintain equal representation
3. **Regular Updates**: Retrain models with new data
4. **Validation**: Test models before deployment
5. **Documentation**: Document all training data changes

## 📄 License

This modular NLP architecture is part of the Real Estate AI Assistant project. All code is open source and available for modification and improvement.

---

**🎯 Ready to use!** The modular architecture is fully implemented and tested. Each engine operates independently, ensuring no interference between search properties and knowledge base functionality.
