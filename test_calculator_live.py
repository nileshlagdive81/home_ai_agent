#!/usr/bin/env python3
"""
Live Calculator Test with Dummy Data
Simulates both Budget-First and Property-First scenarios
"""

import math
import json

class LiveCalculatorTest:
    def __init__(self):
        self.test_results = {}
        
    def calculate_emi(self, principal, rate, tenure):
        """Calculate EMI using the same formula as the calculator"""
        monthly_rate = rate / (12 * 100)
        number_of_payments = tenure * 12
        
        if monthly_rate == 0:
            return principal / number_of_payments
        
        emi = principal * monthly_rate * math.pow(1 + monthly_rate, number_of_payments) / \
              (math.pow(1 + monthly_rate, number_of_payments) - 1)
        
        return round(emi)
    
    def calculate_foir(self, monthly_income, monthly_obligations):
        """Calculate FOIR (Fixed Obligations to Income Ratio)"""
        if monthly_income == 0:
            return 0
        return (monthly_obligations / monthly_income) * 100
    
    def get_foir_status(self, foir):
        """Get FOIR status and color"""
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
    
    def calculate_max_loan_amount(self, monthly_income, monthly_obligations, interest_rate, tenure):
        """Calculate maximum loan amount using the same logic as calculator"""
        max_foir = 45  # Banks typically allow 40-50% FOIR for home loans
        max_emi = (monthly_income * max_foir / 100) - monthly_obligations
        
        if max_emi <= 0:
            return 0
        
        # Reverse EMI calculation to find principal
        monthly_rate = interest_rate / (12 * 100)
        number_of_payments = tenure * 12
        
        if monthly_rate == 0:
            return max_emi * number_of_payments
        
        principal = max_emi * (math.pow(1 + monthly_rate, number_of_payments) - 1) / \
                   (monthly_rate * math.pow(1 + monthly_rate, number_of_payments))
        
        return round(principal)
    
    def calculate_stamp_duty(self, property_price, location):
        """Calculate stamp duty for different states"""
        stamp_duty_rates = {
            'maharashtra': 0.05,  # 5%
            'karnataka': 0.05,    # 5%
            'tamil-nadu': 0.07,   # 7%
            'delhi': 0.06,        # 6%
            'telangana': 0.05,    # 5%
            'gujarat': 0.045,     # 4.5%
            'other': 0.05         # Default 5%
        }
        
        rate = stamp_duty_rates.get(location, 0.05)
        return round(property_price * rate)
    
    def calculate_registration_charges(self, property_price):
        """Calculate registration charges (typically 1%)"""
        return round(property_price * 0.01)
    
    def test_budget_first_scenario(self):
        """Test Scenario 1: User wants to see their affordability"""
        print("=" * 80)
        print("🏠 SCENARIO 1: BUDGET-FIRST - User Wants to See Their Affordability")
        print("=" * 80)
        
        # Dummy Data
        user_data = {
            "grossIncome": 75000,        # ₹75,000 monthly
            "age": 30,
            "workExperience": 5,
            "cibilScore": "650-749",     # Good score
            "savings": 500000,           # ₹5 Lakhs
            "existingEMIs": 15000,       # ₹15,000
            "rent": 12000,               # ₹12,000
            "utilities": 3000,           # ₹3,000
            "groceries": 8000,           # ₹8,000
            "subscriptions": 2000,       # ₹2,000
            "insurance": 24000,          # ₹24,000 yearly
            "schoolFees": 0,             # No school fees
            "propertyTax": 0,            # No property tax
            "otherYearly": 12000,        # ₹12,000 yearly
            "coApplicant": "no",         # No co-applicant
            "coApplicantIncome": 0,
            "coApplicantEMIs": 0
        }
        
        print("📊 USER INPUT DATA:")
        print(f"   Monthly Income: ₹{user_data['grossIncome']:,}")
        print(f"   Age: {user_data['age']} years")
        print(f"   Work Experience: {user_data['workExperience']} years")
        print(f"   CIBIL Score: {user_data['cibilScore']}")
        print(f"   Savings: ₹{user_data['savings']:,}")
        print(f"   Existing EMIs: ₹{user_data['existingEMIs']:,}")
        print(f"   Monthly Rent: ₹{user_data['rent']:,}")
        print(f"   Monthly Utilities: ₹{user_data['utilities']:,}")
        print(f"   Monthly Groceries: ₹{user_data['groceries']:,}")
        print(f"   Monthly Subscriptions: ₹{user_data['subscriptions']:,}")
        print(f"   Yearly Insurance: ₹{user_data['insurance']:,}")
        print(f"   Other Yearly Expenses: ₹{user_data['otherYearly']:,}")
        print()
        
        # Step 1: Calculate Monthly Obligations
        print("🔢 STEP 1: CALCULATE MONTHLY OBLIGATIONS")
        monthly_expenses = user_data['rent'] + user_data['utilities'] + user_data['groceries'] + user_data['subscriptions']
        yearly_expenses = user_data['insurance'] + user_data['schoolFees'] + user_data['propertyTax'] + user_data['otherYearly']
        monthly_yearly_expenses = yearly_expenses / 12
        total_monthly_obligations = monthly_expenses + monthly_yearly_expenses + user_data['existingEMIs']
        
        print(f"   Monthly Expenses: ₹{monthly_expenses:,}")
        print(f"   Yearly Expenses: ₹{yearly_expenses:,}")
        print(f"   Monthly Yearly Expenses: ₹{monthly_yearly_expenses:,.0f}")
        print(f"   Existing EMIs: ₹{user_data['existingEMIs']:,}")
        print(f"   Total Monthly Obligations: ₹{total_monthly_obligations:,.0f}")
        print()
        
        # Step 2: Calculate Total Monthly Income
        print("💰 STEP 2: CALCULATE TOTAL MONTHLY INCOME")
        total_monthly_income = user_data['grossIncome']
        if user_data['coApplicant'] == 'yes' and user_data['coApplicantIncome']:
            total_monthly_income += user_data['coApplicantIncome']
            total_monthly_obligations += user_data['coApplicantEMIs']
        
        print(f"   Gross Monthly Income: ₹{user_data['grossIncome']:,}")
        print(f"   Co-Applicant Income: ₹{user_data['coApplicantIncome']:,}")
        print(f"   Total Monthly Income: ₹{total_monthly_income:,}")
        print()
        
        # Step 3: Calculate FOIR
        print("📊 STEP 3: CALCULATE FOIR (Fixed Obligations to Income Ratio)")
        foir = self.calculate_foir(total_monthly_income, total_monthly_obligations)
        foir_status = self.get_foir_status(foir)
        
        print(f"   FOIR Formula: (₹{total_monthly_obligations:,.0f} / ₹{total_monthly_income:,}) × 100")
        print(f"   FOIR: {foir:.1f}%")
        print(f"   Status: {foir_status['status']} (Risk: {foir_status['risk']})")
        print(f"   Color: {foir_status['color']}")
        print()
        
        # Step 4: Calculate Maximum Loan Amount
        print("🏦 STEP 4: CALCULATE MAXIMUM LOAN AMOUNT")
        interest_rate = 8.5  # 8.5% per annum
        tenure = 20          # 20 years
        
        print(f"   Interest Rate: {interest_rate}%")
        print(f"   Loan Tenure: {tenure} years")
        print(f"   Bank Max FOIR: 45%")
        
        max_loan_amount = self.calculate_max_loan_amount(total_monthly_income, total_monthly_obligations, interest_rate, tenure)
        
        if max_loan_amount > 0:
            print(f"   Maximum EMI Available: ₹{(total_monthly_income * 0.45 - total_monthly_obligations):,.0f}")
            print(f"   Maximum Loan Amount: ₹{max_loan_amount:,}")
        else:
            print(f"   ❌ User cannot afford any loan with current obligations!")
            print(f"   Maximum EMI Available: ₹{(total_monthly_income * 0.45 - total_monthly_obligations):,.0f}")
            print(f"   Recommendation: Reduce monthly obligations first")
        
        print()
        
        # Step 5: Calculate Maximum Property Price
        print("🏠 STEP 5: CALCULATE MAXIMUM PROPERTY PRICE")
        max_property_price = max_loan_amount + user_data['savings']
        
        print(f"   Maximum Loan Amount: ₹{max_loan_amount:,}")
        print(f"   User Savings: ₹{user_data['savings']:,}")
        print(f"   Maximum Property Price: ₹{max_property_price:,}")
        print()
        
        # Step 6: Calculate Maximum EMI
        print("💳 STEP 6: CALCULATE MAXIMUM EMI")
        max_emi = self.calculate_emi(max_loan_amount, interest_rate, tenure)
        print(f"   Maximum EMI: ₹{max_emi:,}")
        print()
        
        # Store results
        self.test_results['budget_first'] = {
            "user_data": user_data,
            "monthly_obligations": total_monthly_obligations,
            "monthly_income": total_monthly_income,
            "foir": foir,
            "foir_status": foir_status,
            "max_loan_amount": max_loan_amount,
            "max_property_price": max_property_price,
            "max_emi": max_emi,
            "affordable": max_loan_amount > 0
        }
        
        return self.test_results['budget_first']
    
    def test_property_first_scenario(self):
        """Test Scenario 2: User has property in mind - check affordability"""
        print("=" * 80)
        print("🏗️ SCENARIO 2: PROPERTY-FIRST - Check if User Can Afford Specific Property")
        print("=" * 80)
        
        # Dummy Data
        property_data = {
            "propertyPrice": 5000000,    # ₹50 Lakhs property
            "propertyLocation": "maharashtra",
            "pfGrossIncome": 80000,      # ₹80,000 monthly
            "pfAge": 32,
            "pfWorkExperience": 6,
            "pfCibilScore": "750-900",   # Excellent score
            "pfSavings": 1000000,        # ₹10 Lakhs
            "pfExistingEMIs": 10000,     # ₹10,000
            "pfRent": 15000,             # ₹15,000
            "pfUtilities": 4000,         # ₹4,000
            "pfGroceries": 10000,        # ₹10,000
            "pfSubscriptions": 3000,     # ₹3,000
            "interestRate": 8.5,         # 8.5% interest
            "loanTenure": 20             # 20 years
        }
        
        print("📊 PROPERTY & USER DATA:")
        print(f"   Property Price: ₹{property_data['propertyPrice']:,}")
        print(f"   Property Location: {property_data['propertyLocation'].title()}")
        print(f"   Monthly Income: ₹{property_data['pfGrossIncome']:,}")
        print(f"   Age: {property_data['pfAge']} years")
        print(f"   Work Experience: {property_data['pfWorkExperience']} years")
        print(f"   CIBIL Score: {property_data['pfCibilScore']}")
        print(f"   Savings: ₹{property_data['pfSavings']:,}")
        print(f"   Existing EMIs: ₹{property_data['pfExistingEMIs']:,}")
        print(f"   Monthly Rent: ₹{property_data['pfRent']:,}")
        print(f"   Monthly Utilities: ₹{property_data['pfUtilities']:,}")
        print(f"   Monthly Groceries: ₹{property_data['pfGroceries']:,}")
        print(f"   Monthly Subscriptions: ₹{property_data['pfSubscriptions']:,}")
        print(f"   Interest Rate: {property_data['interestRate']}%")
        print(f"   Loan Tenure: {property_data['loanTenure']} years")
        print()
        
        # Step 1: Calculate Monthly Obligations
        print("🔢 STEP 1: CALCULATE MONTHLY OBLIGATIONS")
        monthly_expenses = property_data['pfRent'] + property_data['pfUtilities'] + property_data['pfGroceries'] + property_data['pfSubscriptions']
        total_monthly_obligations = monthly_expenses + property_data['pfExistingEMIs']
        
        print(f"   Monthly Expenses: ₹{monthly_expenses:,}")
        print(f"   Existing EMIs: ₹{property_data['pfExistingEMIs']:,}")
        print(f"   Total Monthly Obligations: ₹{total_monthly_obligations:,}")
        print()
        
        # Step 2: Calculate Total Monthly Income
        print("💰 STEP 2: CALCULATE TOTAL MONTHLY INCOME")
        total_monthly_income = property_data['pfGrossIncome']
        print(f"   Total Monthly Income: ₹{total_monthly_income:,}")
        print()
        
        # Step 3: Calculate FOIR
        print("📊 STEP 3: CALCULATE FOIR")
        foir = self.calculate_foir(total_monthly_income, total_monthly_obligations)
        foir_status = self.get_foir_status(foir)
        
        print(f"   FOIR: {foir:.1f}%")
        print(f"   Status: {foir_status['status']} (Risk: {foir_status['risk']})")
        print()
        
        # Step 4: Calculate Property Costs
        print("🏛️ STEP 4: CALCULATE PROPERTY COSTS")
        stamp_duty = self.calculate_stamp_duty(property_data['propertyPrice'], property_data['propertyLocation'])
        registration = self.calculate_registration_charges(property_data['propertyPrice'])
        total_cost = property_data['propertyPrice'] + stamp_duty + registration
        
        print(f"   Property Price: ₹{property_data['propertyPrice']:,}")
        print(f"   Stamp Duty (5%): ₹{stamp_duty:,}")
        print(f"   Registration (1%): ₹{registration:,}")
        print(f"   Total Cost: ₹{total_cost:,}")
        print()
        
        # Step 5: Calculate Required Loan Amount
        print("🏦 STEP 5: CALCULATE REQUIRED LOAN AMOUNT")
        required_loan_amount = total_cost - property_data['pfSavings']
        print(f"   Total Cost: ₹{total_cost:,}")
        print(f"   User Savings: ₹{property_data['pfSavings']:,}")
        print(f"   Required Loan Amount: ₹{required_loan_amount:,}")
        print()
        
        # Step 6: Calculate Required EMI
        print("💳 STEP 6: CALCULATE REQUIRED EMI")
        required_emi = self.calculate_emi(required_loan_amount, property_data['interestRate'], property_data['loanTenure'])
        print(f"   Required EMI: ₹{required_emi:,}")
        print()
        
        # Step 7: Calculate Maximum EMI User Can Afford
        print("💳 STEP 7: CALCULATE MAXIMUM EMI USER CAN AFFORD")
        max_loan_amount = self.calculate_max_loan_amount(total_monthly_income, total_monthly_obligations, property_data['interestRate'], property_data['loanTenure'])
        max_emi = self.calculate_emi(max_loan_amount, property_data['interestRate'], property_data['loanTenure'])
        
        print(f"   Maximum Loan Amount: ₹{max_loan_amount:,}")
        print(f"   Maximum EMI: ₹{max_emi:,}")
        print()
        
        # Step 8: Check Affordability
        print("✅ STEP 8: CHECK AFFORDABILITY")
        affordable = required_emi <= max_emi
        
        print(f"   Required EMI: ₹{required_emi:,}")
        print(f"   Maximum EMI: ₹{max_emi:,}")
        print(f"   Affordability Check: ₹{required_emi:,} <= ₹{max_emi:,}")
        print(f"   Result: {'✅ AFFORDABLE' if affordable else '❌ NOT AFFORDABLE'}")
        print()
        
        # Step 9: Calculate Down Payment
        print("💰 STEP 9: CALCULATE DOWN PAYMENT")
        min_down_payment = property_data['propertyPrice'] * 0.20  # Minimum 20%
        required_down_payment = property_data['propertyPrice'] - required_loan_amount
        down_payment = max(min_down_payment, required_down_payment)
        
        print(f"   Minimum Down Payment (20%): ₹{min_down_payment:,}")
        print(f"   Required Down Payment: ₹{required_down_payment:,}")
        print(f"   Final Down Payment: ₹{down_payment:,}")
        print()
        
        # Store results
        self.test_results['property_first'] = {
            "property_data": property_data,
            "monthly_obligations": total_monthly_obligations,
            "monthly_income": total_monthly_income,
            "foir": foir,
            "foir_status": foir_status,
            "stamp_duty": stamp_duty,
            "registration": registration,
            "total_cost": total_cost,
            "required_loan_amount": required_loan_amount,
            "required_emi": required_emi,
            "max_loan_amount": max_loan_amount,
            "max_emi": max_emi,
            "affordable": affordable,
            "down_payment": down_payment
        }
        
        return self.test_results['property_first']
    
    def run_complete_test(self):
        """Run both scenarios and show comprehensive results"""
        print("🚀 STARTING COMPLETE CALCULATOR TEST WITH DUMMY DATA")
        print("=" * 80)
        
        # Test both scenarios
        budget_results = self.test_budget_first_scenario()
        property_results = self.test_property_first_scenario()
        
        # Generate summary
        print("=" * 80)
        print("📊 COMPLETE TEST RESULTS SUMMARY")
        print("=" * 80)
        
        print("🏠 SCENARIO 1 - BUDGET-FIRST RESULTS:")
        print(f"   ✅ User can afford property up to: ₹{budget_results['max_property_price']:,}")
        print(f"   🏦 Maximum loan amount: ₹{budget_results['max_loan_amount']:,}")
        print(f"   💳 Maximum EMI: ₹{budget_results['max_emi']:,}")
        print(f"   📊 FOIR: {budget_results['foir']:.1f}% ({budget_results['foir_status']['status']})")
        print(f"   🎯 Affordability: {'✅ YES' if budget_results['affordable'] else '❌ NO'}")
        print()
        
        print("🏗️ SCENARIO 2 - PROPERTY-FIRST RESULTS:")
        print(f"   🏠 Property Price: ₹{property_results['property_data']['propertyPrice']:,}")
        print(f"   💰 Total Cost: ₹{property_results['total_cost']:,}")
        print(f"   🏦 Required Loan: ₹{property_results['required_loan_amount']:,}")
        print(f"   💳 Required EMI: ₹{property_results['required_emi']:,}")
        print(f"   💳 Maximum EMI: ₹{property_results['max_emi']:,}")
        print(f"   💰 Down Payment: ₹{property_results['down_payment']:,}")
        print(f"   📊 FOIR: {property_results['foir']:.1f}% ({property_results['foir_status']['status']})")
        print(f"   🎯 Affordability: {'✅ YES' if property_results['affordable'] else '❌ NO'}")
        print()
        
        # Save detailed results
        with open("calculator_live_test_results.json", "w") as f:
            json.dump(self.test_results, f, indent=2)
        
        print("📄 Detailed results saved to: calculator_live_test_results.json")
        print("🎉 Calculator test completed successfully!")
        
        return self.test_results

if __name__ == "__main__":
    tester = LiveCalculatorTest()
    results = tester.run_complete_test()
