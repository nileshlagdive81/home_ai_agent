#!/usr/bin/env python3
"""
Analytics NLP Demo
Demonstrates the analytics NLP engine with various real estate queries
"""

import sys
import json
from datetime import datetime

# Add backend to path
sys.path.append("backend")

from services.analytics_nlp_engine import AnalyticsNLPEngine

def demo_analytics_nlp():
    """Demo the analytics NLP engine"""
    
    print("🚀 REAL ESTATE ANALYTICS NLP DEMO")
    print("=" * 60)
    print(f"📅 Demo Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Initialize the engine
    engine = AnalyticsNLPEngine()
    
    # Test queries for different analytics scenarios
    test_queries = [
        # ROI Analysis Queries
        "What are the best ROI properties in Pune?",
        "Show me properties with ROI above 15%",
        "Which 2BHK properties give the highest returns?",
        "Find A+ grade investment properties in Mumbai",
        
        # Price Trends Queries
        "Show me price trends for 3BHK in Mumbai",
        "How have property prices changed over the last 2 years?",
        "Price analysis for properties under 2 crores",
        
        # Market Intelligence Queries
        "Market report for Pune real estate",
        "What is the market sentiment in Mumbai?",
        "Real estate market analysis and insights",
        
        # Investment Ranking Queries
        "Rank properties by ROI in descending order",
        "Top 10 investment properties in Pune",
        "Best vs worst performing properties",
        
        # Location Analysis Queries
        "Which areas have the highest investment potential?",
        "Compare different localities by ROI",
        "Best neighborhoods for real estate investment",
        
        # Complex Multi-Criteria Queries
        "Show me 2BHK properties in Mumbai with ROI above 12% and A grade",
        "Find low risk, high return properties under 3 crores",
        "Which city has better investment opportunities: Mumbai or Pune?"
    ]
    
    print("🔍 TESTING ANALYTICS NLP ENGINE")
    print("-" * 40)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i:2d}. 🔍 Query: {query}")
        print("   " + "=" * (len(query) + 8))
        
        try:
            # Analyze the query
            intent = engine.analyze_query(query)
            print(f"   🎯 Intent: {intent.intent_type}")
            print(f"   🏙️  City: {intent.city or 'Any'}")
            print(f"   🏠 BHK: {intent.bhk_count or 'Any'}")
            print(f"   💰 ROI Threshold: {intent.roi_threshold or 'Any'}")
            print(f"   📊 Investment Grade: {intent.investment_grade or 'Any'}")
            print(f"   ⚠️  Risk Level: {intent.risk_level or 'Any'}")
            
            # Execute the query
            print(f"   ⚡ Executing query...")
            result = engine.execute_analytics_query(intent)
            
            # Display results
            print(f"   ✅ Query Type: {result['query_type']}")
            print(f"   📊 Total Results: {result.get('total_results', result.get('total_ranked', result.get('total_data_points', result.get('total_reports', result.get('total_locations', result.get('summary', {}).get('total_properties', 0)))))}")
            
            # Show sample results
            if 'results' in result and result['results']:
                print(f"   🏆 Top Results:")
                for j, prop in enumerate(result['results'][:3], 1):
                    print(f"      {j}. {prop['project_name']} - {prop['city']} ({prop['bhk_count']}BHK)")
                    print(f"         ROI: {prop['roi_percentage']:.2f}% | Grade: {prop['investment_grade']} | Risk: {prop['risk_level']}")
            
            elif 'ranking' in result and result['ranking']:
                print(f"   🏆 Top Rankings:")
                for j, prop in enumerate(result['ranking'][:3], 1):
                    print(f"      {j}. {prop['project_name']} - {prop['city']} ({prop['bhk_count']}BHK)")
                    print(f"         ROI: {prop['roi_percentage']:.2f}% | Grade: {prop['investment_grade']}")
            
            elif 'trends' in result and result['trends']:
                print(f"   📈 Price Trends:")
                print(f"      Time Period: {result['time_period']}")
                print(f"      Data Points: {len(result['trends'])}")
            
            elif 'reports' in result and result['reports']:
                print(f"   📊 Market Reports:")
                for j, report in enumerate(result['reports'][:2], 1):
                    print(f"      {j}. {report['city']} - {report['market_sentiment']} | Score: {report['investment_opportunity_score']}")
            
            elif 'locations' in result and result['locations']:
                print(f"   🗺️  Location Analysis:")
                for j, loc in enumerate(result['locations'][:3], 1):
                    print(f"      {j}. {loc['city']} - {loc['locality']} | Avg ROI: {loc['avg_roi_percentage']:.2f}%")
            
            elif 'top_performers' in result and result['top_performers']:
                print(f"   🏆 Top Performers:")
                for j, prop in enumerate(result['top_performers'][:3], 1):
                    print(f"      {j}. {prop['project_name']} - {prop['city']} | ROI: {prop['roi_percentage']:.2f}%")
            
            # Show filters applied
            if result.get('filters_applied'):
                print(f"   🔧 Filters Applied: {json.dumps(result['filters_applied'], indent=6)}")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print("   " + "-" * 50)
    
    print(f"\n🎉 ANALYTICS NLP DEMO COMPLETED!")
    print(f"📊 Tested {len(test_queries)} different query types")
    print(f"🔍 Intent Classification: ROI Analysis, Price Trends, Market Intelligence, Investment Ranking, Location Analysis")
    print(f"🏗️  Entity Extraction: City, BHK, Price Range, ROI Threshold, Investment Grade, Risk Level")
    
    # Close the engine
    engine.close()

if __name__ == "__main__":
    demo_analytics_nlp()

