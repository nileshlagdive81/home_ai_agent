#!/usr/bin/env python3
"""
Analytics NLP Engine
Handles real estate analytics queries like ROI, price trends, market intelligence
"""

import re
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from sqlalchemy import text, func, and_, or_, desc, asc
from database import SessionLocal
from models import Property, Project, PropertyPriceHistory, ROIAnalysis, MarketReports

@dataclass
class AnalyticsIntent:
    """Analytics query intent classification"""
    intent_type: str
    city: Optional[str] = None
    bhk_count: Optional[int] = None
    price_range: Optional[Dict[str, float]] = None
    roi_threshold: Optional[float] = None
    investment_grade: Optional[str] = None
    risk_level: Optional[str] = None
    time_period: Optional[str] = None
    market_sentiment: Optional[str] = None
    comparison_type: Optional[str] = None

class AnalyticsNLPEngine:
    """NLP engine for real estate analytics queries"""
    
    def __init__(self):
        self.db = SessionLocal()
        
        # Analytics intent patterns
        self.intent_patterns = {
            'roi_analysis': [
                r'(?:what are|show me|find|get).*(?:best|top|highest|good).*(?:roi|return|investment).*(?:properties|homes|flats)',
                r'(?:roi|return|investment).*(?:analysis|report|data)',
                r'(?:which|what).*(?:properties|homes).*(?:give|have|offer).*(?:best|highest).*(?:roi|return)'
            ],
            'price_trends': [
                r'(?:price|cost).*(?:trend|movement|change|growth|appreciation)',
                r'(?:how).*(?:prices|costs).*(?:changed|moved|grown).*(?:over|in|during)',
                r'(?:price|cost).*(?:history|analysis|forecast|prediction)'
            ],
            'market_intelligence': [
                r'(?:market|real estate).*(?:report|analysis|intelligence|insights)',
                r'(?:what).*(?:market|real estate).*(?:doing|performing|trending)',
                r'(?:market|real estate).*(?:sentiment|outlook|forecast)'
            ],
            'investment_ranking': [
                r'(?:rank|order|sort).*(?:properties|homes).*(?:by|according to).*(?:roi|return|investment)',
                r'(?:top|best|worst).*(?:investments|properties).*(?:in|for|at)',
                r'(?:compare|vs|versus).*(?:properties|homes).*(?:investment|roi)'
            ],
            'location_analysis': [
                r'(?:which|what).*(?:area|locality|neighborhood).*(?:best|good|profitable)',
                r'(?:area|locality|neighborhood).*(?:analysis|comparison|ranking)',
                r'(?:best|top).*(?:areas|localities).*(?:for|to).*(?:invest|buy)'
            ]
        }
        
        # Entity extraction patterns
        self.entity_patterns = {
            'city': r'\b(Mumbai|Pune|Delhi|Bangalore|Chennai|Hyderabad|Kolkata)\b',
            'bhk': r'\b(\d+)\s*(?:BHK|bhk|bedroom)\b',
            'price_range': r'\b(?:under|below|less than|above|more than|over)\s*(\d+(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs)\b',
            'roi_threshold': r'\b(?:above|over|more than|below|under|less than)\s*(\d+(?:\.\d+)?)\s*%\b',
            'investment_grade': r'\b(A\+|A|B\+|B|C)\b',
            'risk_level': r'\b(high|medium|low)\s*risk\b',
            'time_period': r'\b(last|past|previous)\s*(\d+)\s*(?:year|month|week)s?\b'
        }
    
    def analyze_query(self, user_query: str) -> AnalyticsIntent:
        """Analyze user query and extract intent and entities"""
        
        query_lower = user_query.lower()
        
        # Determine intent type
        intent_type = self._classify_intent(query_lower)
        
        # Extract entities
        city = self._extract_city(user_query)
        bhk_count = self._extract_bhk(user_query)
        price_range = self._extract_price_range(user_query)
        roi_threshold = self._extract_roi_threshold(user_query)
        investment_grade = self._extract_investment_grade(user_query)
        risk_level = self._extract_risk_level(user_query)
        time_period = self._extract_time_period(user_query)
        
        return AnalyticsIntent(
            intent_type=intent_type,
            city=city,
            bhk_count=bhk_count,
            price_range=price_range,
            roi_threshold=roi_threshold,
            investment_grade=investment_grade,
            risk_level=risk_level,
            time_period=time_period
        )
    
    def _classify_intent(self, query: str) -> str:
        """Classify the intent of the query"""
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query):
                    return intent
        return 'general_analytics'
    
    def _extract_city(self, query: str) -> Optional[str]:
        """Extract city from query"""
        match = re.search(self.entity_patterns['city'], query, re.IGNORECASE)
        return match.group(1) if match else None
    
    def _extract_bhk(self, query: str) -> Optional[int]:
        """Extract BHK count from query"""
        match = re.search(self.entity_patterns['bhk'], query, re.IGNORECASE)
        return int(match.group(1)) if match else None
    
    def _extract_price_range(self, query: str) -> Optional[Dict[str, float]]:
        """Extract price range from query"""
        match = re.search(self.entity_patterns['price_range'], query, re.IGNORECASE)
        if match:
            operator = match.group(0).split()[0].lower()
            value = float(match.group(1))
            unit = 'crore' if 'cr' in match.group(0) else 'lakh'
            return {'operator': operator, 'value': value, 'unit': unit}
        return None
    
    def _extract_roi_threshold(self, query: str) -> Optional[float]:
        """Extract ROI threshold from query"""
        match = re.search(self.entity_patterns['roi_threshold'], query, re.IGNORECASE)
        return float(match.group(1)) if match else None
    
    def _extract_investment_grade(self, query: str) -> Optional[str]:
        """Extract investment grade from query"""
        match = re.search(self.entity_patterns['investment_grade'], query, re.IGNORECASE)
        return match.group(1) if match else None
    
    def _extract_risk_level(self, query: str) -> Optional[str]:
        """Extract risk level from query"""
        match = re.search(self.entity_patterns['risk_level'], query, re.IGNORECASE)
        return match.group(1).lower() if match else None
    
    def _extract_time_period(self, query: str) -> Optional[str]:
        """Extract time period from query"""
        match = re.search(self.entity_patterns['time_period'], query, re.IGNORECASE)
        if match:
            number = int(match.group(2))
            unit = match.group(3)
            return f"{number}_{unit}"
        return None
    
    def execute_analytics_query(self, intent: AnalyticsIntent) -> Dict[str, Any]:
        """Execute analytics query based on intent"""
        
        if intent.intent_type == 'roi_analysis':
            return self._get_roi_analysis(intent)
        elif intent.intent_type == 'price_trends':
            return self._get_price_trends(intent)
        elif intent.intent_type == 'market_intelligence':
            return self._get_market_intelligence(intent)
        elif intent.intent_type == 'investment_ranking':
            return self._get_investment_ranking(intent)
        elif intent.intent_type == 'location_analysis':
            return self._get_location_analysis(intent)
        else:
            return self._get_general_analytics(intent)
    
    def _get_roi_analysis(self, intent: AnalyticsIntent) -> Dict[str, Any]:
        """Get ROI analysis for properties"""
        
        query = self.db.query(
            Property.id,
            Property.bhk_count,
            Property.price_crores,
            Property.carpet_area_sqft,
            Project.name.label('project_name'),
            Project.city,
            ROIAnalysis.roi_percentage,
            ROIAnalysis.investment_grade,
            ROIAnalysis.risk_level,
            ROIAnalysis.recommendations
        ).join(
            Project, Property.project_id == Project.id
        ).join(
            ROIAnalysis, Property.id == ROIAnalysis.property_id
        )
        
        # Apply filters
        if intent.city:
            query = query.filter(Project.city.ilike(f"%{intent.city}%"))
        
        if intent.bhk_count:
            query = query.filter(Property.bhk_count == intent.bhk_count)
        
        if intent.roi_threshold:
            query = query.filter(ROIAnalysis.roi_percentage >= intent.roi_threshold)
        
        if intent.investment_grade:
            query = query.filter(ROIAnalysis.investment_grade == intent.investment_grade)
        
        if intent.risk_level:
            query = query.filter(ROIAnalysis.risk_level.ilike(f"%{intent.risk_level}%"))
        
        # Order by ROI
        query = query.order_by(desc(ROIAnalysis.roi_percentage))
        
        results = query.limit(20).all()
        
        return {
            'query_type': 'ROI Analysis',
            'filters_applied': self._get_applied_filters(intent),
            'total_results': len(results),
            'results': [
                {
                    'property_id': str(r.id),
                    'project_name': r.project_name,
                    'city': r.city,
                    'bhk_count': r.bhk_count,
                    'price_crores': float(r.price_crores) if r.price_crores else None,
                    'carpet_area_sqft': r.carpet_area_sqft,
                    'roi_percentage': float(r.roi_percentage),
                    'investment_grade': r.investment_grade,
                    'risk_level': r.risk_level,
                    'recommendations': r.recommendations
                }
                for r in results
            ]
        }
    
    def _get_price_trends(self, intent: AnalyticsIntent) -> Dict[str, Any]:
        """Get price trends analysis"""
        
        # Get price history for the last 2 years
        end_date = datetime.now()
        start_date = end_date - timedelta(days=2*365)
        
        query = self.db.query(
            PropertyPriceHistory.record_date,
            func.avg(PropertyPriceHistory.price_crores).label('avg_price'),
            func.avg(PropertyPriceHistory.appreciation_rate).label('avg_appreciation'),
            PropertyPriceHistory.market_condition,
            Project.city
        ).join(
            Property, PropertyPriceHistory.property_id == Property.id
        ).join(
            Project, Property.project_id == Project.id
        ).filter(
            PropertyPriceHistory.record_date >= start_date.date()
        )
        
        if intent.city:
            query = query.filter(Project.city.ilike(f"%{intent.city}%"))
        
        if intent.bhk_count:
            query = query.filter(Property.bhk_count == intent.bhk_count)
        
        results = query.group_by(
            PropertyPriceHistory.record_date,
            PropertyPriceHistory.market_condition,
            Project.city
        ).order_by(
            PropertyPriceHistory.record_date
        ).all()
        
        return {
            'query_type': 'Price Trends Analysis',
            'filters_applied': self._get_applied_filters(intent),
            'time_period': f"{start_date.date()} to {end_date.date()}",
            'total_data_points': len(results),
            'trends': [
                {
                    'date': str(r.record_date),
                    'avg_price_crores': float(r.avg_price) if r.avg_price else None,
                    'avg_appreciation_rate': float(r.avg_appreciation) if r.avg_appreciation else None,
                    'market_condition': r.market_condition,
                    'city': r.city
                }
                for r in results
            ]
        }
    
    def _get_market_intelligence(self, intent: AnalyticsIntent) -> Dict[str, Any]:
        """Get market intelligence and reports"""
        
        query = self.db.query(MarketReports).order_by(desc(MarketReports.report_date))
        
        if intent.city:
            query = query.filter(MarketReports.city.ilike(f"%{intent.city}%"))
        
        if intent.market_sentiment:
            query = query.filter(MarketReports.market_sentiment.ilike(f"%{intent.market_sentiment}%"))
        
        results = query.limit(10).all()
        
        return {
            'query_type': 'Market Intelligence',
            'filters_applied': self._get_applied_filters(intent),
            'total_reports': len(results),
            'reports': [
                {
                    'report_date': str(r.report_date),
                    'city': r.city,
                    'locality': r.locality,
                    'market_sentiment': r.market_sentiment,
                    'investment_opportunity_score': r.investment_opportunity_score,
                    'market_phase': r.market_phase,
                    'key_insights': r.key_insights
                }
                for r in results
            ]
        }
    
    def _get_investment_ranking(self, intent: AnalyticsIntent) -> Dict[str, Any]:
        """Get investment ranking of properties"""
        
        query = self.db.query(
            Property.id,
            Property.bhk_count,
            Property.price_crores,
            Project.name.label('project_name'),
            Project.city,
            ROIAnalysis.roi_percentage,
            ROIAnalysis.investment_grade,
            ROIAnalysis.risk_level
        ).join(
            Project, Property.project_id == Project.id
        ).join(
            ROIAnalysis, Property.id == ROIAnalysis.property_id
        )
        
        # Apply filters
        if intent.city:
            query = query.filter(Project.city.ilike(f"%{intent.city}%"))
        
        if intent.bhk_count:
            query = query.filter(Property.bhk_count == intent.bhk_count)
        
        if intent.investment_grade:
            query = query.filter(ROIAnalysis.investment_grade == intent.investment_grade)
        
        # Order by ROI for ranking
        query = query.order_by(desc(ROIAnalysis.roi_percentage))
        
        results = query.limit(50).all()
        
        return {
            'query_type': 'Investment Ranking',
            'filters_applied': self._get_applied_filters(intent),
            'total_ranked': len(results),
            'ranking': [
                {
                    'rank': i + 1,
                    'property_id': str(r.id),
                    'project_name': r.project_name,
                    'city': r.city,
                    'bhk_count': r.bhk_count,
                    'price_crores': float(r.price_crores) if r.price_crores else None,
                    'roi_percentage': float(r.roi_percentage),
                    'investment_grade': r.investment_grade,
                    'risk_level': r.risk_level
                }
                for i, r in enumerate(results)
            ]
        }
    
    def _get_location_analysis(self, intent: AnalyticsIntent) -> Dict[str, Any]:
        """Get location-based analysis"""
        
        query = self.db.query(
            Project.city,
            Project.locality,
            func.avg(ROIAnalysis.roi_percentage).label('avg_roi'),
            func.avg(ROIAnalysis.risk_level).label('avg_risk'),
            func.count(Property.id).label('property_count')
        ).join(
            Property, Project.id == Property.project_id
        ).join(
            ROIAnalysis, Property.id == ROIAnalysis.property_id
        ).group_by(
            Project.city, Project.locality
        )
        
        if intent.city:
            query = query.filter(Project.city.ilike(f"%{intent.city}%"))
        
        results = query.order_by(desc(func.avg(ROIAnalysis.roi_percentage))).all()
        
        return {
            'query_type': 'Location Analysis',
            'filters_applied': self._get_applied_filters(intent),
            'total_locations': len(results),
            'locations': [
                {
                    'city': r.city,
                    'locality': r.locality,
                    'avg_roi_percentage': float(r.avg_roi) if r.avg_roi else None,
                    'avg_risk_level': r.avg_risk,
                    'property_count': r.property_count
                }
                for r in results
            ]
        }
    
    def _get_general_analytics(self, intent: AnalyticsIntent) -> Dict[str, Any]:
        """Get general analytics overview"""
        
        # Get summary statistics
        total_properties = self.db.query(Property).count()
        total_roi_analysis = self.db.query(ROIAnalysis).count()
        total_market_reports = self.db.query(MarketReports).count()
        
        # Get top performing properties
        top_properties = self.db.query(
            Property.id,
            Property.bhk_count,
            Property.price_crores,
            Project.name.label('project_name'),
            Project.city,
            ROIAnalysis.roi_percentage,
            ROIAnalysis.investment_grade
        ).join(
            Project, Property.project_id == Project.id
        ).join(
            ROIAnalysis, Property.id == ROIAnalysis.property_id
        ).order_by(
            desc(ROIAnalysis.roi_percentage)
        ).limit(5).all()
        
        return {
            'query_type': 'General Analytics Overview',
            'summary': {
                'total_properties': total_properties,
                'total_roi_analysis': total_roi_analysis,
                'total_market_reports': total_market_reports
            },
            'top_performers': [
                {
                    'property_id': str(r.id),
                    'project_name': r.project_name,
                    'city': r.city,
                    'bhk_count': r.bhk_count,
                    'price_crores': float(r.price_crores) if r.price_crores else None,
                    'roi_percentage': float(r.roi_percentage),
                    'investment_grade': r.investment_grade
                }
                for r in top_properties
            ]
        }
    
    def _get_applied_filters(self, intent: AnalyticsIntent) -> Dict[str, Any]:
        """Get list of applied filters"""
        filters = {}
        
        if intent.city:
            filters['city'] = intent.city
        if intent.bhk_count:
            filters['bhk_count'] = intent.bhk_count
        if intent.price_range:
            filters['price_range'] = intent.price_range
        if intent.roi_threshold:
            filters['roi_threshold'] = f"{intent.roi_threshold}%"
        if intent.investment_grade:
            filters['investment_grade'] = intent.investment_grade
        if intent.risk_level:
            filters['risk_level'] = intent.risk_level
        if intent.time_period:
            filters['time_period'] = intent.time_period
        
        return filters
    
    def close(self):
        """Close database connection"""
        self.db.close()

# Example usage and testing
if __name__ == "__main__":
    engine = AnalyticsNLPEngine()
    
    # Test queries
    test_queries = [
        "What are the best ROI properties in Pune?",
        "Show me price trends for 2BHK in Mumbai",
        "Which areas have the highest investment potential?",
        "Rank properties by ROI above 15%",
        "Market report for Mumbai real estate"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        intent = engine.analyze_query(query)
        print(f"Intent: {intent.intent_type}")
        print(f"Entities: {intent}")
        
        try:
            result = engine.execute_analytics_query(intent)
            print(f"Results: {len(result.get('results', result.get('ranking', result.get('trends', result.get('reports', result.get('locations', result.get('top_performers', []))))))} items")
        except Exception as e:
            print(f"Error: {str(e)}")
    
    engine.close()

