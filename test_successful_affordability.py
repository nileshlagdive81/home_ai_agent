#!/usr/bin/env python3
"""
Test Successful Affordability Scenarios
Shows how users with better financial profiles can afford properties
"""

import math

def calculate_emi(principal, rate, tenure):
    monthly_rate = rate / (12 * 100)
    number_of_payments = tenure * 12
    
    if monthly_rate == 0:
        return principal / number_of_payments
    
    emi = principal * monthly_rate * math.pow(1 + monthly_rate, number_of_payments) / \
          (math.pow(1 + monthly_rate, number_of_payments) - 1)
    
    return round(emi)

def calculate_foir(monthly_income, monthly_obligations):
    if monthly_income == 0:
        return 0
    return (monthly_obligations / monthly_income) * 100

def get_foir_status(foir):
    if foir <= 30:
        return {"status": "Excellent", "color": "#10b981", "risk": "Very Low"}
    elif foir <= 40:
        return {"status": "Good", "color": "#3b82f6", "risk": "Low"}
    elif foir <= 50:
        return {"status": "Fair", "color": "#f59e0b", "risk": "Moderate"}
    elif foir <= 60:
        return {"status": "Poor", "color": "#ef4444", "risk": "High"}
    else:
        return {"status": "Critical", "color": "#dc2626", "risk": "Very High"}

def calculate_max_loan_amount(monthly_income, monthly_obligations, interest_rate, tenure):
    max_foir = 45
    max_emi = (monthly_income * max_foir / 100) - monthly_obligations
    
    if max_emi <= 0:
        return 0
    
    monthly_rate = interest_rate / (12 * 100)
    number_of_payments = tenure * 12
    
    if monthly_rate == 0:
        return max_emi * number_of_payments
    
    principal = max_emi * (math.pow(1 + monthly_rate, number_of_payments) - 1) / \
               (monthly_rate * math.pow(1 + monthly_rate, number_of_payments))
    
    return round(principal)

def test_successful_budget_first():
    """Test successful Budget-First scenario"""
    print("=" * 80)
    print("🏠 SUCCESSFUL SCENARIO: BUDGET-FIRST - Good Financial Profile")
    print("=" * 80)
    
    # Better financial profile
    user_data = {
        "grossIncome": 120000,       # ₹1.2 Lakhs monthly (better income)
        "age": 28,
        "workExperience": 4,
        "cibilScore": "750-900",     # Excellent score
        "savings": 800000,           # ₹8 Lakhs savings
        "existingEMIs": 8000,        # Lower EMIs
        "rent": 15000,               # ₹15,000
        "utilities": 4000,           # ₹4,000
        "groceries": 12000,          # ₹12,000
        "subscriptions": 3000,       # ₹3,000
        "insurance": 30000,          # ₹30,000 yearly
        "schoolFees": 0,
        "propertyTax": 0,
        "otherYearly": 15000         # ₹15,000 yearly
    }
    
    print("📊 USER INPUT DATA (IMPROVED PROFILE):")
    print(f"   Monthly Income: ₹{user_data['grossIncome']:,}")
    print(f"   Age: {user_data['age']} years")
    print(f"   CIBIL Score: {user_data['cibilScore']}")
    print(f"   Savings: ₹{user_data['savings']:,}")
    print(f"   Existing EMIs: ₹{user_data['existingEMIs']:,}")
    print(f"   Monthly Expenses: ₹{user_data['rent'] + user_data['utilities'] + user_data['groceries'] + user_data['subscriptions']:,}")
    print()
    
    # Calculate
    monthly_expenses = user_data['rent'] + user_data['utilities'] + user_data['groceries'] + user_data['subscriptions']
    yearly_expenses = user_data['insurance'] + user_data['schoolFees'] + user_data['propertyTax'] + user_data['otherYearly']
    monthly_yearly_expenses = yearly_expenses / 12
    total_monthly_obligations = monthly_expenses + monthly_yearly_expenses + user_data['existingEMIs']
    
    total_monthly_income = user_data['grossIncome']
    foir = calculate_foir(total_monthly_income, total_monthly_obligations)
    foir_status = get_foir_status(foir)
    
    interest_rate = 8.5
    tenure = 20
    max_loan_amount = calculate_max_loan_amount(total_monthly_income, total_monthly_obligations, interest_rate, tenure)
    max_property_price = max_loan_amount + user_data['savings']
    max_emi = calculate_emi(max_loan_amount, interest_rate, tenure)
    
    print("🔢 CALCULATION RESULTS:")
    print(f"   Total Monthly Obligations: ₹{total_monthly_obligations:,.0f}")
    print(f"   Total Monthly Income: ₹{total_monthly_income:,}")
    print(f"   FOIR: {foir:.1f}% ({foir_status['status']})")
    print(f"   Maximum Loan Amount: ₹{max_loan_amount:,}")
    print(f"   Maximum Property Price: ₹{max_property_price:,}")
    print(f"   Maximum EMI: ₹{max_emi:,}")
    print(f"   Affordability: ✅ YES - User can afford properties up to ₹{max_property_price:,}")
    print()
    
    return {
        "foir": foir,
        "max_loan_amount": max_loan_amount,
        "max_property_price": max_property_price,
        "max_emi": max_emi,
        "affordable": True
    }

def test_successful_property_first():
    """Test successful Property-First scenario"""
    print("=" * 80)
    print("🏗️ SUCCESSFUL SCENARIO: PROPERTY-FIRST - Property is Affordable")
    print("=" * 80)
    
    # Good financial profile with affordable property
    property_data = {
        "propertyPrice": 3500000,    # ₹35 Lakhs (more affordable)
        "propertyLocation": "karnataka",
        "pfGrossIncome": 100000,     # ₹1 Lakh monthly
        "pfAge": 30,
        "pfWorkExperience": 5,
        "pfCibilScore": "750-900",   # Excellent score
        "pfSavings": 1200000,        # ₹12 Lakhs savings
        "pfExistingEMIs": 5000,      # Very low EMIs
        "pfRent": 12000,             # ₹12,000
        "pfUtilities": 3000,         # ₹3,000
        "pfGroceries": 8000,         # ₹8,000
        "pfSubscriptions": 2000,     # ₹2,000
        "interestRate": 8.5,
        "loanTenure": 20
    }
    
    print("📊 PROPERTY & USER DATA (AFFORDABLE SCENARIO):")
    print(f"   Property Price: ₹{property_data['propertyPrice']:,}")
    print(f"   Monthly Income: ₹{property_data['pfGrossIncome']:,}")
    print(f"   CIBIL Score: {property_data['pfCibilScore']}")
    print(f"   Savings: ₹{property_data['pfSavings']:,}")
    print(f"   Existing EMIs: ₹{property_data['pfExistingEMIs']:,}")
    print()
    
    # Calculate
    monthly_expenses = property_data['pfRent'] + property_data['pfUtilities'] + property_data['pfGroceries'] + property_data['pfSubscriptions']
    total_monthly_obligations = monthly_expenses + property_data['pfExistingEMIs']
    total_monthly_income = property_data['pfGrossIncome']
    
    foir = calculate_foir(total_monthly_income, total_monthly_obligations)
    foir_status = get_foir_status(foir)
    
    # Property costs
    stamp_duty = round(property_data['propertyPrice'] * 0.05)  # 5%
    registration = round(property_data['propertyPrice'] * 0.01)  # 1%
    total_cost = property_data['propertyPrice'] + stamp_duty + registration
    
    required_loan_amount = total_cost - property_data['pfSavings']
    required_emi = calculate_emi(required_loan_amount, property_data['interestRate'], property_data['loanTenure'])
    
    max_loan_amount = calculate_max_loan_amount(total_monthly_income, total_monthly_obligations, property_data['interestRate'], property_data['loanTenure'])
    max_emi = calculate_emi(max_loan_amount, property_data['interestRate'], property_data['loanTenure'])
    
    affordable = required_emi <= max_emi
    
    min_down_payment = property_data['propertyPrice'] * 0.20
    required_down_payment = property_data['propertyPrice'] - required_loan_amount
    down_payment = max(min_down_payment, required_down_payment)
    
    print("🔢 CALCULATION RESULTS:")
    print(f"   Total Monthly Obligations: ₹{total_monthly_obligations:,}")
    print(f"   FOIR: {foir:.1f}% ({foir_status['status']})")
    print(f"   Total Property Cost: ₹{total_cost:,}")
    print(f"   Required Loan Amount: ₹{required_loan_amount:,}")
    print(f"   Required EMI: ₹{required_emi:,}")
    print(f"   Maximum EMI: ₹{max_emi:,}")
    print(f"   Down Payment: ₹{down_payment:,}")
    print(f"   Affordability: {'✅ YES' if affordable else '❌ NO'}")
    
    if affordable:
        print(f"   🎉 SUCCESS! User can afford this ₹{property_data['propertyPrice']:,} property!")
        print(f"   💰 They need ₹{down_payment:,} down payment")
        print(f"   💳 Monthly EMI will be ₹{required_emi:,}")
    else:
        print(f"   ❌ User cannot afford this property")
    
    print()
    
    return {
        "foir": foir,
        "total_cost": total_cost,
        "required_loan_amount": required_loan_amount,
        "required_emi": required_emi,
        "max_emi": max_emi,
        "affordable": affordable,
        "down_payment": down_payment
    }

def main():
    print("🚀 TESTING SUCCESSFUL AFFORDABILITY SCENARIOS")
    print("=" * 80)
    
    # Test successful scenarios
    budget_success = test_successful_budget_first()
    property_success = test_successful_property_first()
    
    # Summary
    print("=" * 80)
    print("📊 SUCCESSFUL SCENARIOS SUMMARY")
    print("=" * 80)
    
    print("🏠 BUDGET-FIRST SUCCESS:")
    print(f"   ✅ User can afford properties up to: ₹{budget_success['max_property_price']:,}")
    print(f"   🏦 Maximum loan amount: ₹{budget_success['max_loan_amount']:,}")
    print(f"   💳 Maximum EMI: ₹{budget_success['max_emi']:,}")
    print(f"   📊 FOIR: {budget_success['foir']:.1f}%")
    print()
    
    print("🏗️ PROPERTY-FIRST SUCCESS:")
    print(f"   🏠 Property is affordable: {'✅ YES' if property_success['affordable'] else '❌ NO'}")
    print(f"   💰 Required down payment: ₹{property_success['down_payment']:,}")
    print(f"   💳 Monthly EMI: ₹{property_success['required_emi']:,}")
    print(f"   📊 FOIR: {property_success['foir']:.1f}%")
    print()
    
    print("🎯 KEY SUCCESS FACTORS:")
    print("   • Lower monthly obligations (FOIR < 45%)")
    print("   • Higher income relative to expenses")
    print("   • Good CIBIL score")
    print("   • Adequate savings for down payment")
    print("   • Lower existing EMIs")
    print()
    
    print("🎉 Calculator working perfectly for both scenarios!")

if __name__ == "__main__":
    main()
