from backend.services.nlp_engine import RealEstateNLPEngine

# Test the NLP engine directly
nlp_engine = RealEstateNLPEngine()

# Test a simple query
query = "carpet area less than 1400"
print(f"Testing query: '{query}'")

# Process the query
result = nlp_engine.process_query(query)
print(f"Intent: {result.intent}")
print(f"Confidence: {result.confidence}")
print(f"Entities: {len(result.entities)}")

for entity in result.entities:
    print(f"  - {entity.label}: '{entity.text}'")

# Get search criteria
criteria = nlp_engine.get_search_criteria(query)
print(f"\nSearch criteria: {criteria['filters']}")
