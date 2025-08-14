-- Real Estate Analytics Database Schema
-- Comprehensive system for ROI analysis, price trends, and market intelligence

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Historical Property Price Table
CREATE TABLE IF NOT EXISTS property_price_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    property_id UUID REFERENCES properties(id),
    record_date DATE NOT NULL,
    price_lakhs NUMERIC(10,2),
    price_crores NUMERIC(10,2),
    price_per_sqft NUMERIC(10,2),
    transaction_type VARCHAR(50), -- Sale, Rent, Lease
    appreciation_rate NUMERIC(5,2), -- Annual appreciation percentage
    days_on_market INTEGER,
    negotiation_margin NUMERIC(5,2), -- Price reduction percentage
    market_condition VARCHAR(50), -- Bull, Bear, Stable
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Rental History Table
CREATE TABLE IF NOT EXISTS rental_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    property_id UUID REFERENCES properties(id),
    record_date DATE NOT NULL,
    rental_amount_monthly NUMERIC(10,2),
    rental_amount_yearly NUMERIC(10,2),
    rental_yield_percentage NUMERIC(5,2),
    vacancy_rate NUMERIC(5,2),
    tenant_type VARCHAR(50), -- Family, Bachelors, Corporate
    lease_terms_months INTEGER,
    maintenance_cost_monthly NUMERIC(8,2),
    rental_trend VARCHAR(50), -- Increasing, Decreasing, Stable
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Market Reports Table
CREATE TABLE IF NOT EXISTS market_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    report_date DATE NOT NULL,
    city VARCHAR(100) NOT NULL,
    locality VARCHAR(100),
    market_sentiment VARCHAR(50), -- Bull, Bear, Neutral
    supply_demand_ratio NUMERIC(5,2),
    price_trend VARCHAR(50), -- Rising, Falling, Stable
    rental_trend VARCHAR(50), -- Rising, Falling, Stable
    investment_opportunity_score INTEGER CHECK (investment_opportunity_score >= 1 AND investment_opportunity_score <= 10),
    market_phase VARCHAR(50), -- Recovery, Growth, Peak, Decline
    key_insights TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Economic Indicators Table
CREATE TABLE IF NOT EXISTS economic_indicators (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    indicator_date DATE NOT NULL,
    indicator_name VARCHAR(100) NOT NULL,
    indicator_value NUMERIC(10,4),
    change_percentage NUMERIC(5,2),
    source VARCHAR(100),
    impact_on_real_estate VARCHAR(50), -- Positive, Negative, Neutral
    trend_direction VARCHAR(50), -- Up, Down, Stable
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Infrastructure Projects Table
CREATE TABLE IF NOT EXISTS infrastructure_projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_name VARCHAR(200) NOT NULL,
    project_type VARCHAR(100), -- Metro, Highway, Airport, Smart City
    city VARCHAR(100) NOT NULL,
    locality VARCHAR(100),
    start_date DATE,
    completion_date DATE,
    impact_radius_km NUMERIC(5,2),
    property_price_impact_percentage NUMERIC(5,2),
    rental_impact_percentage NUMERIC(5,2),
    project_status VARCHAR(50), -- Planned, Under Construction, Completed
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. User Watchlists Table
CREATE TABLE IF NOT EXISTS user_watchlists (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_email VARCHAR(200) NOT NULL,
    user_phone VARCHAR(20),
    property_id UUID REFERENCES properties(id),
    watchlist_type VARCHAR(50), -- Investment, Purchase, Rental
    alert_preferences JSONB, -- Email, SMS, WhatsApp preferences
    investment_criteria JSONB, -- ROI, price range, location preferences
    notification_settings JSONB, -- Frequency, threshold settings
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Investment Portfolio Table
CREATE TABLE IF NOT EXISTS investment_portfolio (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_email VARCHAR(200) NOT NULL,
    property_id UUID REFERENCES properties(id),
    investment_amount NUMERIC(12,2),
    purchase_date DATE,
    current_value NUMERIC(12,2),
    roi_percentage NUMERIC(5,2),
    appreciation_rate_percentage NUMERIC(5,2),
    holding_period_months INTEGER,
    investment_status VARCHAR(50), -- Active, Sold, Under Review
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. ROI Analysis Table
CREATE TABLE IF NOT EXISTS roi_analysis (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    property_id UUID REFERENCES properties(id),
    analysis_date DATE NOT NULL,
    roi_percentage NUMERIC(5,2),
    rental_yield_percentage NUMERIC(5,2),
    appreciation_rate_percentage NUMERIC(5,2),
    total_return_percentage NUMERIC(5,2),
    investment_grade VARCHAR(10), -- A+, A, B+, B, C
    risk_level VARCHAR(20), -- Low, Medium, High
    market_outlook VARCHAR(50), -- Positive, Neutral, Negative
    recommendations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_property_price_history_property_id ON property_price_history(property_id);
CREATE INDEX idx_property_price_history_date ON property_price_history(record_date);
CREATE INDEX idx_rental_history_property_id ON rental_history(property_id);
CREATE INDEX idx_rental_history_date ON rental_history(record_date);
CREATE INDEX idx_market_reports_city_date ON market_reports(city, report_date);
CREATE INDEX idx_economic_indicators_date ON economic_indicators(indicator_date);
CREATE INDEX idx_infrastructure_projects_city ON infrastructure_projects(city);
CREATE INDEX idx_user_watchlists_email ON user_watchlists(user_email);
CREATE INDEX idx_investment_portfolio_email ON investment_portfolio(user_email);
CREATE INDEX idx_roi_analysis_property_id ON roi_analysis(property_id);

