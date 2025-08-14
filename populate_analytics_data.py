#!/usr/bin/env python3
"""
Populate Analytics Database with Sample Data
Creates 5 years of historical data for real estate analytics
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add backend to path
sys.path.append("backend")

from database import SessionLocal
from models import Property, Project
from sqlalchemy import text

def populate_analytics_data():
    """Populate analytics tables with sample data"""
    
    print("📊 POPULATING ANALYTICS DATABASE")
    print("=" * 50)
    
    db = SessionLocal()
    
    try:
        # Get existing properties
        properties = db.query(Property).all()
        if not properties:
            print("❌ No properties found. Please populate properties first.")
            return
        
        print(f"✅ Found {len(properties)} properties to analyze")
        
        # 1. Populate Property Price History (5 years)
        print("\n💰 Creating Property Price History...")
        create_price_history(db, properties)
        
        # 2. Populate ROI Analysis
        print("\n📊 Creating ROI Analysis...")
        create_roi_analysis(db, properties)
        
        # 3. Populate Market Reports
        print("\n📈 Creating Market Reports...")
        create_market_reports(db)
        
        print("\n✅ Analytics database populated successfully!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

def create_price_history(db, properties):
    """Create 5 years of price history for properties"""
    
    # Generate dates for last 5 years (monthly)
    start_date = datetime.now() - timedelta(days=5*365)
    dates = []
    current_date = start_date
    while current_date <= datetime.now():
        dates.append(current_date.date())
        current_date += timedelta(days=30)
    
    for property in properties:
        base_price = property.price_crores or 2.0
        base_price_sqft = property.carpet_area_sqft or 1000
        
        for date in dates:
            # Simulate price appreciation (2-15% annually)
            years_elapsed = (datetime.now().date() - date).days / 365
            appreciation_factor = 1 + (random.uniform(0.02, 0.15) * years_elapsed)
            
            current_price = base_price * appreciation_factor
            current_price_sqft = (current_price * 10000000) / base_price_sqft
            
            # Add some market volatility
            volatility = random.uniform(0.95, 1.05)
            current_price *= volatility
            
            # Determine market condition
            if appreciation_factor > 1.1:
                market_condition = "Bull"
            elif appreciation_factor < 1.02:
                market_condition = "Bear"
            else:
                market_condition = "Stable"
            
            # Insert price history
            db.execute(text("""
                INSERT INTO property_price_history 
                (property_id, record_date, price_crores, price_per_sqft, 
                 transaction_type, appreciation_rate, days_on_market, 
                 negotiation_margin, market_condition)
                VALUES (:property_id, :date, :price, :price_sqft, 
                        'Sale', :appreciation, :days, :margin, :condition)
            """), {
                'property_id': property.id,
                'date': date,
                'price': round(current_price, 2),
                'price_sqft': round(current_price_sqft, 2),
                'appreciation': round((appreciation_factor - 1) * 100, 2),
                'days': random.randint(30, 180),
                'margin': random.uniform(0, 5),
                'condition': market_condition
            })
        
        print(f"  ✅ Created price history for {property.project.project_name} {property.bhk_count}BHK")
    
    db.commit()

def create_roi_analysis(db, properties):
    """Create ROI analysis for properties"""
    
    for property in properties:
        base_price = property.price_crores or 2.0
        
        # Calculate ROI components
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
        
        # Market outlook
        if grade in ['A+', 'A']:
            outlook = 'Positive'
        elif grade in ['B+', 'B']:
            outlook = 'Neutral'
        else:
            outlook = 'Negative'
        
        # Recommendations
        if grade in ['A+', 'A']:
            recommendations = "Excellent investment opportunity with high returns and moderate risk"
        elif grade in ['B+', 'B']:
            recommendations = "Good investment with balanced risk-return profile"
        else:
            recommendations = "Consider for long-term investment with potential for improvement"
        
        # Insert ROI analysis
        db.execute(text("""
            INSERT INTO roi_analysis 
            (property_id, analysis_date, roi_percentage, rental_yield_percentage,
             appreciation_rate_percentage, total_return_percentage, investment_grade,
             risk_level, market_outlook, recommendations)
            VALUES (:property_id, :date, :roi, :rental, :appreciation, :total,
                    :grade, :risk, :outlook, :recommendations)
        """), {
            'property_id': property.id,
            'date': datetime.now().date(),
            'roi': round(total_return, 2),
            'rental': round(rental_yield, 2),
            'appreciation': round(appreciation_rate, 2),
            'total': round(total_return, 2),
            'grade': grade,
            'risk': risk,
            'outlook': outlook,
            'recommendations': recommendations
        })
    
    print(f"  ✅ Created ROI analysis for {len(properties)} properties")
    db.commit()

def create_market_reports(db):
    """Create market reports for Mumbai and Pune"""
    
    cities = ['Mumbai', 'Pune']
    localities = {
        'Mumbai': ['Bandra West', 'Andheri West', 'Worli', 'Powai', 'Thane'],
        'Pune': ['Hinjewadi', 'Koregaon Park', 'Baner', 'Kharadi', 'Viman Nagar']
    }
    
    # Generate monthly reports for last 2 years
    start_date = datetime.now() - timedelta(days=2*365)
    current_date = start_date
    
    while current_date <= datetime.now():
        for city in cities:
            for locality in localities[city]:
                # Market sentiment based on time period
                months_elapsed = (datetime.now().date() - current_date.date()).days / 30
                if months_elapsed < 6:
                    sentiment = random.choice(['Bull', 'Bull', 'Neutral'])
                elif months_elapsed < 12:
                    sentiment = random.choice(['Bull', 'Neutral', 'Neutral'])
                else:
                    sentiment = random.choice(['Bear', 'Neutral', 'Neutral'])
                
                # Supply demand ratio
                supply_demand = random.uniform(0.8, 1.5)
                
                # Price and rental trends
                price_trend = 'Rising' if sentiment == 'Bull' else 'Stable' if sentiment == 'Neutral' else 'Falling'
                rental_trend = 'Rising' if sentiment == 'Bull' else 'Stable' if sentiment == 'Neutral' else 'Falling'
                
                # Investment opportunity score
                if sentiment == 'Bull':
                    score = random.randint(7, 10)
                elif sentiment == 'Neutral':
                    score = random.randint(5, 8)
                else:
                    score = random.randint(3, 6)
                
                # Market phase
                if score >= 8:
                    phase = 'Growth'
                elif score >= 6:
                    phase = 'Recovery'
                elif score >= 4:
                    phase = 'Peak'
                else:
                    phase = 'Decline'
                
                # Insert market report
                db.execute(text("""
                    INSERT INTO market_reports 
                    (report_date, city, locality, market_sentiment, supply_demand_ratio,
                     price_trend, rental_trend, investment_opportunity_score, market_phase, key_insights)
                    VALUES (:date, :city, :locality, :sentiment, :ratio, :price, :rental, :score, :phase, :insights)
                """), {
                    'date': current_date.date(),
                    'city': city,
                    'locality': locality,
                    'sentiment': sentiment,
                    'ratio': round(supply_demand, 2),
                    'price': price_trend,
                    'rental': rental_trend,
                    'score': score,
                    'phase': phase,
                    'insights': f"{locality} showing {sentiment.lower()} market with {price_trend.lower()} prices"
                })
        
        current_date += timedelta(days=30)
    
    print(f"  ✅ Created market reports for {len(cities)} cities")
    db.commit()

if __name__ == "__main__":
    populate_analytics_data()
