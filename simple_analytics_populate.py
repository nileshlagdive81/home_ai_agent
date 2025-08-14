#!/usr/bin/env python3
"""
Simple Analytics Populate Script
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add backend to path
sys.path.append("backend")

from database import SessionLocal
from models import Property
from sqlalchemy import text

def main():
    print("🚀 STARTING ANALYTICS POPULATION")
    print("=" * 50)
    
    db = SessionLocal()
    
    try:
        # Get properties
        print("1. Getting properties...")
        properties = db.query(Property).limit(10).all()  # Limit to 10 for testing
        print(f"   ✅ Found {len(properties)} properties")
        
        # Create ROI analysis
        print("\n2. Creating ROI analysis...")
        for i, prop in enumerate(properties):
            rental_yield = random.uniform(2.5, 4.5)
            appreciation_rate = random.uniform(8.0, 18.0)
            total_return = rental_yield + appreciation_rate
            
            # Investment grade
            if total_return >= 20:
                grade = 'A+'
            elif total_return >= 15:
                grade = 'A'
            elif total_return >= 12:
                grade = 'B+'
            elif total_return >= 8:
                grade = 'B'
            else:
                grade = 'C'
            
            # Risk level
            if appreciation_rate > 15:
                risk = 'High'
            elif appreciation_rate > 10:
                risk = 'Medium'
            else:
                risk = 'Low'
            
            # Insert ROI analysis
            db.execute(text("""
                INSERT INTO roi_analysis 
                (property_id, analysis_date, roi_percentage, rental_yield_percentage,
                 appreciation_rate_percentage, total_return_percentage, investment_grade,
                 risk_level, market_outlook, recommendations)
                VALUES (:property_id, :date, :roi, :rental, :appreciation, :total,
                        :grade, :risk, :outlook, :recommendations)
            """), {
                'property_id': prop.id,
                'date': datetime.now().date(),
                'roi': round(total_return, 2),
                'rental': round(rental_yield, 2),
                'appreciation': round(appreciation_rate, 2),
                'total': round(total_return, 2),
                'grade': grade,
                'risk': risk,
                'outlook': 'Positive' if grade in ['A+', 'A'] else 'Neutral',
                'recommendations': f"Investment grade {grade} with {risk} risk"
            })
            
            print(f"   ✅ Created ROI for property {i+1}: {grade} grade, {risk} risk")
        
        db.commit()
        print(f"   ✅ ROI analysis completed for {len(properties)} properties")
        
        # Create market reports
        print("\n3. Creating market reports...")
        cities = ['Mumbai', 'Pune']
        for city in cities:
            db.execute(text("""
                INSERT INTO market_reports 
                (report_date, city, locality, market_sentiment, supply_demand_ratio,
                 price_trend, rental_trend, investment_opportunity_score, market_phase, key_insights)
                VALUES (:date, :city, :locality, :sentiment, :ratio, :price, :rental, :score, :phase, :insights)
            """), {
                'date': datetime.now().date(),
                'city': city,
                'locality': 'Central',
                'sentiment': 'Bull',
                'ratio': 1.2,
                'price': 'Rising',
                'rental': 'Rising',
                'score': 8,
                'phase': 'Growth',
                'insights': f"{city} showing strong growth with rising prices"
            })
            print(f"   ✅ Created market report for {city}")
        
        db.commit()
        print("   ✅ Market reports completed")
        
        print("\n🎉 ANALYTICS POPULATION COMPLETED!")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()

