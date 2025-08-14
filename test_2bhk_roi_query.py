#!/usr/bin/env python3
import sys
sys.path.append('backend')

from services.analytics_nlp_engine import AnalyticsNLPEngine

def test_2bhk_roi_query():
    print("🔍 TESTING: Show me 2BHK properties with ROI above 15%")
    print("=" * 60)
    
    engine = AnalyticsNLPEngine()
    
    try:
        # Analyze the query
        query = "Show me 2BHK properties with ROI above 15%"
        intent = engine.analyze_query(query)
        
        print(f"🎯 Intent: {intent.intent_type}")
        print(f"🏠 BHK: {intent.bhk_count}")
        print(f"💰 ROI Threshold: {intent.roi_threshold}%")
        print(f"🏙️  City: {intent.city or 'Any'}")
        
        # Execute the query
        print("\n⚡ Executing query...")
        result = engine.execute_analytics_query(intent)
        
        print(f"✅ Query Type: {result['query_type']}")
        print(f"📊 Total Results: {result['total_results']}")
        
        if result['results']:
            print("\n🏆 Top Results:")
            for i, prop in enumerate(result['results'][:10], 1):
                print(f"   {i:2d}. {prop['project_name']} - {prop['city']} ({prop['bhk_count']}BHK)")
                print(f"       💰 Price: {prop['price_crores']:.2f} cr | 📏 Area: {prop['carpet_area_sqft']} sqft")
                print(f"       📈 ROI: {prop['roi_percentage']:.2f}% | 🏅 Grade: {prop['investment_grade']} | ⚠️  Risk: {prop['risk_level']}")
                print(f"       💡 {prop['recommendations']}")
                print()
        else:
            print("❌ No results found")
        
        # Show filters applied
        print(f"🔧 Filters Applied: {result['filters_applied']}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        engine.close()

if __name__ == "__main__":
    test_2bhk_roi_query()

