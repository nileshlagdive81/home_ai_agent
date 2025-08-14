#!/usr/bin/env python3
"""
Comprehensive Testing Script for Indian Real Estate NLP System
Tests all capabilities with Indian context queries
"""
import json
import sys
import os
from typing import List, Dict, Any
from pathlib import Path

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

class IndianRealEstateNLPTester:
    def __init__(self):
        self.test_results = {}
        self.training_data = {}
        self.load_test_data()
        
    def load_test_data(self):
        """Load Indian real estate training data for testing"""
        try:
            with open("indian_real_estate_training_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.training_data = data.get("indian_real_estate_queries", {})
                print(f"✅ Loaded test data with {len(self.training_data)} categories")
        except FileNotFoundError:
            print("❌ Test data file not found")
            
    def setup_test_scenarios(self) -> Dict[str, List[Dict]]:
        """Setup comprehensive test scenarios"""
        scenarios = {
            "basic_search_tests": [
                {
                    "query": "Mujhe Mumbai mein ghar chahiye",
                    "expected_intent": "SEARCH_PROPERTY",
                    "expected_entities": ["LOCATION", "PROPERTY_TYPE"],
                    "description": "Basic Hindi search query"
                },
                {
                    "query": "I need a 2 BHK apartment in Bangalore",
                    "expected_intent": "FILTER_BY_BHK",
                    "expected_entities": ["BHK", "PROPERTY_TYPE", "LOCATION"],
                    "description": "Basic English search with BHK"
                },
                {
                    "query": "Delhi NCR mein flat kya rate hai",
                    "expected_intent": "PRICE_QUERY",
                    "expected_entities": ["LOCATION", "PROPERTY_TYPE"],
                    "description": "Price inquiry in Hindi"
                }
            ],
            "complex_multi_criteria_tests": [
                {
                    "query": "Mumbai mein 2 BHK under 1 crore mein swimming pool aur gym ke saath, metro station 1km door, international school 2km door, ready to move property chahiye",
                    "expected_intent": "COMPLEX_SEARCH",
                    "expected_entities": ["LOCATION", "BHK", "PRICE", "AMENITY", "AMENITY", "NEARBY_PLACE", "MEASUREMENT", "NEARBY_PLACE", "MEASUREMENT", "STATUS"],
                    "description": "Complex Hindi query with multiple criteria"
                },
                {
                    "query": "Need 3 BHK villa in Bangalore under 2 crores with garden, security, CCTV, power backup, club house facilities, 5km from IT park, 15km from airport, in good locality",
                    "expected_intent": "COMPLEX_SEARCH",
                    "expected_entities": ["BHK", "PROPERTY_TYPE", "LOCATION", "PRICE", "AMENITY", "AMENITY", "AMENITY", "AMENITY", "AMENITY", "MEASUREMENT", "NEARBY_PLACE", "MEASUREMENT", "NEARBY_PLACE"],
                    "description": "Complex English query with multiple criteria"
                }
            ],
            "cultural_context_tests": [
                {
                    "query": "Joint family ke liye kaunsa layout better hai",
                    "expected_intent": "GET_DETAILS",
                    "expected_entities": [],
                    "description": "Cultural context - joint family"
                },
                {
                    "query": "Puja room kaise arrange kar sakte hain",
                    "expected_intent": "GET_DETAILS",
                    "expected_entities": [],
                    "description": "Cultural context - puja room"
                },
                {
                    "query": "Kitchen mein gas connection kaise milega",
                    "expected_intent": "GET_DETAILS",
                    "expected_entities": ["AMENITY"],
                    "description": "Cultural context - gas connection"
                }
            ],
            "financial_planning_tests": [
                {
                    "query": "50 lakhs mein kya milega Mumbai mein",
                    "expected_intent": "PRICE_QUERY",
                    "expected_entities": ["PRICE", "LOCATION"],
                    "description": "Budget-based search in Hindi"
                },
                {
                    "query": "EMI kitni padegi 80 lakhs ke liye",
                    "expected_intent": "FINANCIAL_ANALYSIS",
                    "expected_entities": ["FINANCIAL_TERM", "PRICE"],
                    "description": "EMI calculation query"
                },
                {
                    "query": "Down payment kitna dena padega",
                    "expected_intent": "FINANCIAL_ANALYSIS",
                    "expected_entities": ["FINANCIAL_TERM"],
                    "description": "Down payment inquiry"
                }
            ],
            "location_and_amenity_tests": [
                {
                    "query": "Bandra West mein locality kaise hai",
                    "expected_intent": "FILTER_BY_LOCATION",
                    "expected_entities": ["LOCATION"],
                    "description": "Locality inquiry"
                },
                {
                    "query": "Swimming pool available hai project mein",
                    "expected_intent": "FILTER_BY_AMENITY",
                    "expected_entities": ["AMENITY"],
                    "description": "Amenity availability check"
                },
                {
                    "query": "Metro station kitne door hai",
                    "expected_intent": "GET_DETAILS",
                    "expected_entities": ["NEARBY_PLACE"],
                    "description": "Distance to metro station"
                }
            ],
            "project_status_tests": [
                {
                    "query": "Project kab complete hoga",
                    "expected_intent": "GET_DETAILS",
                    "expected_entities": ["TIMELINE"],
                    "description": "Project completion timeline"
                },
                {
                    "query": "Ready to move property chahiye",
                    "expected_intent": "FILTER_BY_STATUS",
                    "expected_entities": ["STATUS"],
                    "description": "Ready to move property search"
                },
                {
                    "query": "RERA number available hai",
                    "expected_intent": "GET_DETAILS",
                    "expected_entities": ["DOCUMENT"],
                    "description": "RERA number inquiry"
                }
            ],
            "comparison_tests": [
                {
                    "query": "ABC Residency aur XYZ Heights mein kaunsa better hai",
                    "expected_intent": "COMPARE_PROPERTIES",
                    "expected_entities": ["PROJECT_NAME", "PROJECT_NAME"],
                    "description": "Property comparison query"
                },
                {
                    "query": "Donon projects mein price difference kya hai",
                    "expected_intent": "COMPARE_PROPERTIES",
                    "expected_entities": ["PRICE"],
                    "description": "Price comparison query"
                }
            ],
            "investment_analysis_tests": [
                {
                    "query": "Investment ke liye kaunsa area better hai",
                    "expected_intent": "INVESTMENT_ANALYSIS",
                    "expected_entities": [],
                    "description": "Investment area recommendation"
                },
                {
                    "query": "Rental yield kitna expect kar sakte hain",
                    "expected_intent": "INVESTMENT_ANALYSIS",
                    "expected_entities": ["FINANCIAL_TERM"],
                    "description": "Rental yield expectation"
                },
                {
                    "query": "Property value kitna increase hoga 5 saal mein",
                    "expected_intent": "INVESTMENT_ANALYSIS",
                    "expected_entities": ["MEASUREMENT"],
                    "description": "Future value appreciation"
                }
            ]
        }
        return scenarios
        
    def test_query_processing(self, query: str, expected_intent: str, expected_entities: List[str], description: str) -> Dict[str, Any]:
        """Test individual query processing"""
        print(f"\n🔍 Testing: {description}")
        print(f"Query: {query}")
        
        # Simulate NLP processing (since we don't have the actual trained model yet)
        # In real scenario, this would use the trained spaCy model
        
        # Extract basic entities using regex patterns
        extracted_entities = self.extract_basic_entities(query)
        
        # Determine intent based on content
        detected_intent = self.determine_intent_from_content(query, extracted_entities)
        
        # Calculate accuracy
        entity_accuracy = self.calculate_entity_accuracy(extracted_entities, expected_entities)
        intent_accuracy = 1.0 if detected_intent == expected_intent else 0.0
        
        result = {
            "query": query,
            "expected_intent": expected_intent,
            "detected_intent": detected_intent,
            "expected_entities": expected_entities,
            "extracted_entities": extracted_entities,
            "entity_accuracy": entity_accuracy,
            "intent_accuracy": intent_accuracy,
            "overall_accuracy": (entity_accuracy + intent_accuracy) / 2,
            "description": description
        }
        
        print(f"Expected Intent: {expected_intent}")
        print(f"Detected Intent: {detected_intent}")
        print(f"Expected Entities: {expected_entities}")
        print(f"Extracted Entities: {extracted_entities}")
        print(f"Entity Accuracy: {entity_accuracy:.2f}")
        print(f"Intent Accuracy: {intent_accuracy:.2f}")
        print(f"Overall Accuracy: {result['overall_accuracy']:.2f}")
        
        return result
        
    def extract_basic_entities(self, query: str) -> List[str]:
        """Extract basic entities using regex patterns"""
        entities = []
        
        # BHK detection
        if re.search(r'\d+(?:\.\d+)?\s*BHK', query, re.IGNORECASE):
            entities.append("BHK")
            
        # Price detection
        if re.search(r'\d+(?:\.\d+)?\s*(?:lakh|lakhs|crore|crores)', query, re.IGNORECASE):
            entities.append("PRICE")
            
        # Location detection
        if re.search(r'(?:in|mein|se|nearby)\s+([A-Za-z\s]+(?:NCR|West|East|North|South)?)', query, re.IGNORECASE):
            entities.append("LOCATION")
            
        # Amenity detection
        amenities = ['swimming pool', 'gym', 'parking', 'security', 'garden', 'club house', 'power backup', 'lift', 'CCTV']
        for amenity in amenities:
            if amenity.lower() in query.lower():
                entities.append("AMENITY")
                break
                
        # Property type detection
        property_types = ['apartment', 'flat', 'villa', 'penthouse', 'duplex', 'studio', 'plot', 'house', 'ghar', 'makaan']
        for prop_type in property_types:
            if prop_type.lower() in query.lower():
                entities.append("PROPERTY_TYPE")
                break
                
        # Financial term detection
        financial_terms = ['EMI', 'down payment', 'interest rate', 'processing fee', 'stamp duty', 'registration', 'GST', 'maintenance charges', 'ROI', 'rental yield']
        for term in financial_terms:
            if term.lower() in query.lower():
                entities.append("FINANCIAL_TERM")
                break
                
        # Status detection
        status_terms = ['ready to move', 'under construction', 'new launch', 'pre-launch', 'possession', 'completion', 'construction']
        for term in status_terms:
            if term.lower() in query.lower():
                entities.append("STATUS")
                break
                
        return entities
        
    def determine_intent_from_content(self, query: str, entities: List[str]) -> str:
        """Determine intent based on query content and entities"""
        query_lower = query.lower()
        
        # Complex search detection
        if len(entities) >= 4:
            return "COMPLEX_SEARCH"
            
        # Specific intent detection
        if "BHK" in entities and "PRICE" in entities:
            return "FILTER_BY_BHK_AND_PRICE"
            
        if "LOCATION" in entities and "AMENITY" in entities:
            return "FILTER_BY_LOCATION_AND_AMENITY"
            
        if "PRICE" in entities:
            return "PRICE_QUERY"
            
        if "BHK" in entities:
            return "FILTER_BY_BHK"
            
        if "LOCATION" in entities:
            return "FILTER_BY_LOCATION"
            
        if "AMENITY" in entities:
            return "FILTER_BY_AMENITY"
            
        if "FINANCIAL_TERM" in entities:
            return "FINANCIAL_ANALYSIS"
            
        if "STATUS" in entities:
            return "FILTER_BY_STATUS"
            
        # Cultural context detection
        cultural_keywords = ['joint family', 'puja room', 'gas connection', 'kitchen', 'balcony', 'dining area']
        if any(keyword in query_lower for keyword in cultural_keywords):
            return "GET_DETAILS"
            
        # Investment analysis detection
        investment_keywords = ['investment', 'ROI', 'rental yield', 'appreciation', 'capital gain']
        if any(keyword in query_lower for keyword in investment_keywords):
            return "INVESTMENT_ANALYSIS"
            
        # Comparison detection
        comparison_keywords = ['better', 'compare', 'difference', 'versus', 'aur', 'donon']
        if any(keyword in query_lower for keyword in comparison_keywords):
            return "COMPARE_PROPERTIES"
            
        return "SEARCH_PROPERTY"
        
    def calculate_entity_accuracy(self, extracted: List[str], expected: List[str]) -> float:
        """Calculate entity extraction accuracy"""
        if not expected:
            return 1.0 if not extracted else 0.0
            
        if not extracted:
            return 0.0
            
        # Calculate precision and recall
        correct = len(set(extracted) & set(expected))
        precision = correct / len(extracted) if extracted else 0.0
        recall = correct / len(expected) if expected else 0.0
        
        # F1 score
        if precision + recall == 0:
            return 0.0
        return 2 * (precision * recall) / (precision + recall)
        
    def run_comprehensive_testing(self):
        """Run comprehensive testing of all scenarios"""
        print("🚀 Starting Comprehensive Indian Real Estate NLP Testing")
        print("=" * 80)
        
        scenarios = self.setup_test_scenarios()
        all_results = []
        
        for scenario_name, test_cases in scenarios.items():
            print(f"\n📋 Testing Scenario: {scenario_name}")
            print("-" * 60)
            
            scenario_results = []
            for test_case in test_cases:
                result = self.test_query_processing(
                    test_case["query"],
                    test_case["expected_intent"],
                    test_case["expected_entities"],
                    test_case["description"]
                )
                scenario_results.append(result)
                all_results.append(result)
                
            # Calculate scenario statistics
            avg_accuracy = sum(r["overall_accuracy"] for r in scenario_results) / len(scenario_results)
            print(f"\n📊 Scenario {scenario_name} - Average Accuracy: {avg_accuracy:.2f}")
            
        # Calculate overall statistics
        self.calculate_overall_statistics(all_results)
        
        # Generate test report
        self.generate_test_report(all_results)
        
        print("\n🎉 Comprehensive Testing Completed!")
        
    def calculate_overall_statistics(self, results: List[Dict]):
        """Calculate overall testing statistics"""
        print("\n📊 OVERALL TESTING STATISTICS")
        print("=" * 50)
        
        total_queries = len(results)
        avg_entity_accuracy = sum(r["entity_accuracy"] for r in results) / total_queries
        avg_intent_accuracy = sum(r["intent_accuracy"] for r in results) / total_queries
        avg_overall_accuracy = sum(r["overall_accuracy"] for r in results) / total_queries
        
        print(f"Total Queries Tested: {total_queries}")
        print(f"Average Entity Accuracy: {avg_entity_accuracy:.2f}")
        print(f"Average Intent Accuracy: {avg_intent_accuracy:.2f}")
        print(f"Average Overall Accuracy: {avg_overall_accuracy:.2f}")
        
        # Accuracy distribution
        high_accuracy = len([r for r in results if r["overall_accuracy"] >= 0.8])
        medium_accuracy = len([r for r in results if 0.5 <= r["overall_accuracy"] < 0.8])
        low_accuracy = len([r for r in results if r["overall_accuracy"] < 0.5])
        
        print(f"\nAccuracy Distribution:")
        print(f"High Accuracy (≥80%): {high_accuracy} queries")
        print(f"Medium Accuracy (50-79%): {medium_accuracy} queries")
        print(f"Low Accuracy (<50%): {low_accuracy} queries")
        
    def generate_test_report(self, results: List[Dict]):
        """Generate detailed test report"""
        report_file = "indian_real_estate_nlp_test_report.json"
        
        report = {
            "test_summary": {
                "total_queries": len(results),
                "test_date": str(Path().cwd()),
                "test_type": "Comprehensive Indian Real Estate NLP Testing"
            },
            "detailed_results": results,
            "recommendations": self.generate_recommendations(results)
        }
        
        try:
            with open(report_file, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\n📄 Detailed test report saved to: {report_file}")
        except Exception as e:
            print(f"❌ Failed to save test report: {str(e)}")
            
    def generate_recommendations(self, results: List[Dict]) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        # Analyze entity extraction performance
        entity_accuracies = [r["entity_accuracy"] for r in results]
        avg_entity_accuracy = sum(entity_accuracies) / len(entity_accuracies)
        
        if avg_entity_accuracy < 0.7:
            recommendations.append("Entity extraction accuracy is below 70%. Consider improving regex patterns and adding more training examples.")
            
        # Analyze intent classification performance
        intent_accuracies = [r["intent_accuracy"] for r in results]
        avg_intent_accuracy = sum(intent_accuracies) / len(intent_accuracies)
        
        if avg_intent_accuracy < 0.8:
            recommendations.append("Intent classification accuracy is below 80%. Consider refining intent detection logic and adding more context-aware rules.")
            
        # Analyze query complexity handling
        complex_queries = [r for r in results if len(r["expected_entities"]) >= 4]
        if complex_queries:
            complex_accuracy = sum(r["overall_accuracy"] for r in complex_queries) / len(complex_queries)
            if complex_accuracy < 0.6:
                recommendations.append("Complex query handling needs improvement. Consider enhancing multi-entity extraction and relationship mapping.")
                
        # General recommendations
        recommendations.extend([
            "Consider adding more Hindi-English mixed language training examples",
            "Implement fuzzy matching for entity extraction to handle spelling variations",
            "Add context-aware entity disambiguation for ambiguous terms",
            "Consider implementing confidence scoring for entity extraction and intent classification"
        ])
        
        return recommendations

def main():
    """Main function to run testing"""
    import re  # Import regex module
    
    tester = IndianRealEstateNLPTester()
    tester.run_comprehensive_testing()

if __name__ == "__main__":
    main()
