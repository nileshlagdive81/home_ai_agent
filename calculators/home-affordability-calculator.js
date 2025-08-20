// Home Affordability Calculator - Integrated with Real Estate App
// Single calculator page with smart guidance built into results

class HomeAffordabilityCalculator {
    constructor() {
        this.init();
    }

    init() {
        this.setupFormHandlers();
        this.setupCoApplicantToggle();
        this.setupFlexibleLoanToggle();
        console.log('Home Affordability Calculator initialized');
    }

    // Form Handlers Setup
    setupFormHandlers() {
        const calculatorForm = document.getElementById('affordabilityCalculator');
        if (calculatorForm) {
            calculatorForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleCalculation();
            });
        }

        // Add real-time EMI variation updates for flexible loans
        const downPaymentInput = document.getElementById('downPayment');
        const interestRateInput = document.getElementById('interestRate');
        const loanTenureInput = document.getElementById('loanTenure');

        if (downPaymentInput) {
            downPaymentInput.addEventListener('input', () => {
                if (document.getElementById('loanType').value === 'flexible') {
                    this.updateEMIVariations();
                }
            });
        }

        if (interestRateInput) {
            interestRateInput.addEventListener('input', () => {
                if (document.getElementById('loanType').value === 'flexible') {
                    this.updateEMIVariations();
                }
            });
        }

        if (loanTenureInput) {
            loanTenureInput.addEventListener('input', () => {
                if (document.getElementById('loanType').value === 'flexible') {
                    this.updateEMIVariations();
                }
            });
        }
    }

    // Co-Applicant Toggle
    setupCoApplicantToggle() {
        const coApplicantSelect = document.getElementById('coApplicant');
        if (coApplicantSelect) {
            coApplicantSelect.addEventListener('change', this.toggleCoApplicantFields);
        }
    }

    toggleCoApplicantFields() {
        const coApplicantFields = document.getElementById('coApplicantIncomeGroup');
        const coApplicant = document.getElementById('coApplicant').value;
        
        if (coApplicant === 'yes') {
            coApplicantFields.style.display = 'block';
        } else {
            coApplicantFields.style.display = 'none';
            // Clear co-applicant fields
            document.getElementById('coApplicantIncome').value = '';
        }
    }

    // Flexible Loan Options Toggle
    setupFlexibleLoanToggle() {
        const loanTypeSelect = document.getElementById('loanType');
        if (loanTypeSelect) {
            loanTypeSelect.addEventListener('change', this.toggleFlexibleOptions);
        }
    }

    toggleFlexibleOptions() {
        const flexibleOptions = document.getElementById('flexibleOptions');
        const loanType = document.getElementById('loanType').value;
        
        if (loanType === 'flexible') {
            flexibleOptions.style.display = 'block';
            this.updateEMIVariations();
        } else {
            flexibleOptions.style.display = 'none';
        }
    }

    // Update EMI Variations for Flexible Loans
    updateEMIVariations() {
        const downPayment = parseFloat(document.getElementById('downPayment').value) || 0;
        const interestRate = parseFloat(document.getElementById('interestRate').value) || 8.5;
        const loanTenure = parseInt(document.getElementById('loanTenure').value) || 20;
        
        if (downPayment > 0 && interestRate > 0 && loanTenure > 0) {
            const loanAmount = this.calculateMaxLoanAmount(
                parseFloat(document.getElementById('grossIncome').value) || 0,
                this.calculateTotalMonthlyObligations(),
                interestRate,
                loanTenure
            );
            
            // Calculate EMIs for different rates
            const emiLower = this.calculateEMI(loanAmount, Math.max(interestRate - 2, 7.5), loanTenure);
            const emiSelected = this.calculateEMI(loanAmount, interestRate, loanTenure);
            const emiHigher = this.calculateEMI(loanAmount, Math.min(interestRate + 3, 12), loanTenure);
            
            // Update display
            document.getElementById('emiLower').textContent = `₹${this.formatNumber(emiLower)}`;
            document.getElementById('emiSelected').textContent = `₹${this.formatNumber(emiSelected)}`;
            document.getElementById('emiHigher').textContent = `₹${this.formatNumber(emiHigher)}`;
        }
    }

    // Calculate Total Monthly Obligations
    calculateTotalMonthlyObligations() {
        const formData = this.collectFormData();
        // Remove rent from expenses as it doesn't apply when purchasing
        const monthlyExpenses = formData.utilities + formData.groceries + formData.subscriptions + formData.otherMonthly;
        const yearlyExpenses = formData.insurance + formData.schoolFees + formData.propertyTax + formData.otherYearly;
        const monthlyYearlyExpenses = yearlyExpenses / 12;
        // Include monthly savings as it's money set aside, not available for EMI
        return Math.round(monthlyExpenses + monthlyYearlyExpenses + formData.existingEMIs + formData.monthlySavings);
    }

    // Form Data Collection
    collectFormData() {
        const form = document.getElementById('affordabilityCalculator');
        const formData = new FormData(form);
        const data = {};

        for (let [key, value] of formData.entries()) {
            if (value === '') {
                data[key] = key === 'cibilScore' || key === 'propertyOwnership' || key === 'loanType' ? '' : 0;
            } else if (key === 'cibilScore' || key === 'propertyOwnership' || key === 'loanType') {
                data[key] = value; // Keep as string for select options
            } else if (key.includes('Age') || key.includes('Experience') || key.includes('Tenure')) {
                data[key] = parseInt(value) || 0;
            } else {
                data[key] = parseFloat(value) || 0;
            }
        }

        return data;
    }

    // Main Calculation Handler
    handleCalculation() {
        console.log('Processing affordability calculation...');
        
        try {
            const formData = this.collectFormData();
            console.log('Form data collected:', formData);

            // Validate required fields
            if (!this.validateFormData(formData)) {
                return;
            }

            // Process calculation
            const results = this.calculateAffordability(formData);
            
            // Display results with smart guidance
            this.displayResults(results);
            
        } catch (error) {
            console.error('Error in calculation:', error);
            this.showError('An error occurred during calculation. Please try again.');
        }
    }

    // Data Validation
    validateFormData(data) {
        const required = ['grossIncome', 'age', 'workExperience', 'cibilScore', 'downPayment'];
        
        for (let field of required) {
            if (!data[field] || data[field] === 0) {
                this.showError(`Please fill in ${field.replace(/([A-Z])/g, ' $1').toLowerCase()}`);
                return false;
            }
        }

        if (data.age < 18 || data.age > 70) {
            this.showError('Age must be between 18 and 70 years');
            return false;
        }

        if (data.workExperience < 0 || data.workExperience > 50) {
            this.showError('Work experience must be between 0 and 50 years');
            return false;
        }

        if (data.interestRate < 7.5 || data.interestRate > 12) {
            this.showError('Interest rate must be between 7.5% and 12%');
            return false;
        }

        return true;
    }

    // ===== CORE CALCULATION METHODS =====

    // EMI Calculation Formula
    calculateEMI(principal, rate, tenure) {
        const monthlyRate = rate / (12 * 100);
        const numberOfPayments = tenure * 12;
        
        if (monthlyRate === 0) return principal / numberOfPayments;
        
        const emi = principal * monthlyRate * Math.pow(1 + monthlyRate, numberOfPayments) / 
                   (Math.pow(1 + monthlyRate, numberOfPayments) - 1);
        
        return Math.round(emi);
    }

    // FOIR (Fixed Obligations to Income Ratio) Calculation
    calculateFOIR(monthlyIncome, monthlyObligations) {
        if (monthlyIncome === 0) return 0;
        return (monthlyObligations / monthlyIncome) * 100;
    }

    // Get FOIR Status and Color
    getFOIRStatus(foir) {
        if (foir <= 30) return { status: 'Excellent', color: '#10b981', risk: 'Very Low' };
        if (foir <= 40) return { status: 'Good', color: '#3b82f6', risk: 'Low' };
        if (foir <= 50) return { status: 'Fair', color: '#f59e0b', risk: 'Moderate' };
        if (foir <= 60) return { status: 'Poor', color: '#ef4444', risk: 'High' };
        return { status: 'Critical', color: '#dc2626', risk: 'Very High' };
    }

    // Home Buying Readiness Score
    calculateReadinessScore(data, foir) {
        let score = 100;
        
        // FOIR impact (40% weight)
        if (foir <= 30) score -= 0;
        else if (foir <= 40) score -= 10;
        else if (foir <= 50) score -= 25;
        else if (foir <= 60) score -= 45;
        else score -= 70;
        
        // Age impact (20% weight)
        if (data.age >= 25 && data.age <= 45) score -= 0;
        else if (data.age >= 18 && data.age <= 24) score -= 15;
        else if (data.age >= 46 && data.age <= 60) score -= 10;
        else score -= 25;
        
        // Work experience impact (20% weight)
        if (data.workExperience >= 3) score -= 0;
        else if (data.workExperience >= 1) score -= 10;
        else score -= 20;
        
        // CIBIL score impact (20% weight)
        const cibilScore = this.parseCibilScore(data.cibilScore);
        if (cibilScore >= 750) score -= 0;
        else if (cibilScore >= 650) score -= 15;
        else if (cibilScore >= 550) score -= 30;
        else score -= 50;
        
        return Math.max(0, Math.round(score));
    }

    // Parse CIBIL Score from range
    parseCibilScore(cibilRange) {
        if (!cibilRange || typeof cibilRange !== 'string') return 0;
        
        // Handle "Don't know" option - use medium risk (650)
        if (cibilRange.toLowerCase().includes('don\'t know') || cibilRange.toLowerCase().includes('dont know')) {
            return 650; // Medium risk score
        }
        
        const match = cibilRange.match(/(\d+)-(\d+)/);
        if (match) {
            return parseInt(match[1]);
        }
        return 0;
    }

    // Get Readiness Status
    getReadinessStatus(score) {
        if (score >= 80) return { status: 'Excellent', color: '#10b981', description: 'Ready to buy' };
        if (score >= 60) return { status: 'Good', color: '#3b82f6', description: 'Nearly ready' };
        if (score >= 40) return { status: 'Fair', color: '#f59e0b', description: 'Needs improvement' };
        if (score >= 20) return { status: 'Poor', color: '#ef4444', description: 'Significant work needed' };
        return { status: 'Critical', color: '#dc2626', description: 'Not ready' };
    }

    // Calculate Savings Profile Rating
    calculateSavingsProfile(monthlyIncome, monthlySavings, totalSavings) {
        // Calculate savings rate (monthly savings as % of income)
        const savingsRate = monthlyIncome > 0 ? (monthlySavings / monthlyIncome) * 100 : 0;
        
        // Calculate emergency fund months (total savings / monthly expenses)
        const monthlyExpenses = monthlyIncome * 0.6; // Assume 60% of income goes to expenses
        const emergencyFundMonths = monthlyExpenses > 0 ? totalSavings / monthlyExpenses : 0;
        
        let score = 0;
        let status, color, description, recommendations;
        
        // Score based on savings rate (50% weight)
        if (savingsRate >= 30) score += 50;
        else if (savingsRate >= 20) score += 40;
        else if (savingsRate >= 15) score += 30;
        else if (savingsRate >= 10) score += 20;
        else if (savingsRate >= 5) score += 10;
        
        // Score based on emergency fund (30% weight)
        if (emergencyFundMonths >= 12) score += 30;
        else if (emergencyFundMonths >= 8) score += 25;
        else if (emergencyFundMonths >= 6) score += 20;
        else if (emergencyFundMonths >= 4) score += 15;
        else if (emergencyFundMonths >= 2) score += 10;
        
        // Score based on total savings amount (20% weight)
        if (totalSavings >= monthlyIncome * 12) score += 20;
        else if (totalSavings >= monthlyIncome * 8) score += 15;
        else if (totalSavings >= monthlyIncome * 6) score += 10;
        else if (totalSavings >= monthlyIncome * 3) score += 5;
        
        // Determine status and recommendations
        if (score >= 80) {
            status = 'Excellent';
            color = '#10b981';
            description = 'Strong savings discipline with excellent emergency fund';
            recommendations = [
                'Maintain your current savings rate',
                'Consider investing in higher-yield instruments',
                'You have excellent financial security'
            ];
        } else if (score >= 60) {
            status = 'Good';
            color = '#3b82f6';
            description = 'Good savings habits with adequate emergency fund';
            recommendations = [
                'Try to increase savings rate to 20-30%',
                'Build emergency fund to 8-12 months',
                'Consider systematic investment plans'
            ];
        } else if (score >= 40) {
            status = 'Fair';
            color = '#f59e0b';
            description = 'Moderate savings with room for improvement';
            recommendations = [
                'Aim for 15-20% monthly savings rate',
                'Build emergency fund to 6-8 months',
                'Start with small, consistent savings'
            ];
        } else if (score >= 20) {
            status = 'Poor';
            color = '#ef4444';
            description = 'Low savings rate, needs immediate attention';
            recommendations = [
                'Start with 10% monthly savings',
                'Build emergency fund to 3-6 months',
                'Reduce non-essential expenses',
                'Consider additional income sources'
            ];
        } else {
            status = 'Critical';
            color = '#dc2626';
            description = 'Very low savings, high financial risk';
            recommendations = [
                'Immediate focus on building emergency fund',
                'Aim for minimum 10% monthly savings',
                'Review and reduce all expenses',
                'Seek financial counseling if needed'
            ];
        }
        
        return {
            score: Math.round(score),
            status,
            color,
            description,
            savingsRate: Math.round(savingsRate * 10) / 10,
            emergencyFundMonths: Math.round(emergencyFundMonths * 10) / 10,
            recommendations
        };
    }

    // Maximum Loan Amount Calculation
    calculateMaxLoanAmount(monthlyIncome, monthlyObligations, interestRate, tenure) {
        // Calculate available amount for EMI (this is what user can actually afford)
        const availableForEMI = monthlyIncome - monthlyObligations;
        
        if (availableForEMI <= 0) return 0;
        
        // Reverse EMI calculation to find principal
        const monthlyRate = interestRate / (12 * 100);
        const numberOfPayments = tenure * 12;
        
        if (monthlyRate === 0) return availableForEMI * numberOfPayments;
        
        const principal = availableForEMI * (Math.pow(1 + monthlyRate, numberOfPayments) - 1) / 
                         (monthlyRate * Math.pow(1 + monthlyRate, numberOfPayments));
        
        return Math.round(principal);
    }

    // Main Affordability Calculation
    calculateAffordability(data) {
        console.log('Processing affordability calculation with real formulas...');
        
        // Calculate monthly obligations (excluding rent as it doesn't apply when purchasing)
        const monthlyExpenses = data.utilities + data.groceries + data.subscriptions + data.otherMonthly;
        const yearlyExpenses = data.insurance + data.schoolFees + data.propertyTax + data.otherYearly;
        const monthlyYearlyExpenses = yearlyExpenses / 12;
        // Include monthly savings as it's money set aside, not available for EMI
        const totalMonthlyObligations = Math.round(monthlyExpenses + monthlyYearlyExpenses + data.existingEMIs + data.monthlySavings);
        
        // Calculate total monthly income (including co-applicant if applicable)
        let totalMonthlyIncome = data.grossIncome;
        if (data.coApplicant === 'yes' && data.coApplicantIncome) {
            totalMonthlyIncome += data.coApplicantIncome;
        }
        
        // Calculate FOIR
        const foir = this.calculateFOIR(totalMonthlyIncome, totalMonthlyObligations);
        const foirStatus = this.getFOIRStatus(foir);
        
        // Calculate readiness score
        const readinessScore = this.calculateReadinessScore(data, foir);
        const readinessStatus = this.getReadinessStatus(readinessScore);
        
        // Calculate savings profile
        const savingsProfile = this.calculateSavingsProfile(totalMonthlyIncome, data.monthlySavings, data.savings);
        
        // Calculate maximum loan amount
        const maxLoanAmount = this.calculateMaxLoanAmount(totalMonthlyIncome, totalMonthlyObligations, data.interestRate, data.loanTenure);
        
        // Calculate maximum property price (loan + savings)
        const maxPropertyPrice = maxLoanAmount + data.downPayment;
        
        // Calculate maximum EMI
        const maxEMI = this.calculateEMI(maxLoanAmount, data.interestRate, data.loanTenure);
        
        // Generate smart guidance and recommendations
        const guidance = this.generateSmartGuidance(data, foir, readinessScore, maxPropertyPrice, totalMonthlyIncome, totalMonthlyObligations);
        
        return {
            status: 'success',
            message: 'Your affordability calculation is complete!',
            data: data,
            results: {
                totalMonthlyIncome: totalMonthlyIncome,
                totalMonthlyObligations: totalMonthlyObligations,
                foir: foir,
                foirStatus: foirStatus,
                readinessScore: readinessScore,
                readinessStatus: readinessStatus,
                savingsProfile: savingsProfile,
                maxEMI: maxEMI,
                maxLoanAmount: maxLoanAmount,
                maxPropertyPrice: maxPropertyPrice,
                guidance: guidance,
                breakdown: {
                    monthlyExpenses: monthlyExpenses,
                    yearlyExpenses: yearlyExpenses,
                    monthlyYearlyExpenses: monthlyYearlyExpenses,
                    existingEMIs: data.existingEMIs,
                    coApplicantIncome: data.coApplicant === 'yes' ? data.coApplicantIncome : 0
                }
            }
        };
    }

    // ===== SMART GUIDANCE GENERATION =====

    generateSmartGuidance(data, foir, readinessScore, maxPropertyPrice, monthlyIncome, monthlyObligations) {
        const guidance = {
            summary: this.generateGuidanceSummary(foir, readinessScore, maxPropertyPrice),
            recommendations: this.generateRecommendations(data, foir, readinessScore, maxPropertyPrice),
            improvementStrategies: this.generateImprovementStrategies(data, foir, monthlyIncome, monthlyObligations),
            whatIfScenarios: this.generateWhatIfScenarios(data, foir, maxPropertyPrice),
            riskAssessment: this.assessRiskLevel(foir, readinessScore, data)
        };
        
        return guidance;
    }

    generateGuidanceSummary(foir, readinessScore, maxPropertyPrice) {
        let summary = '';
        
        if (foir <= 30 && readinessScore >= 80) {
            summary = `Excellent! Your financial profile is ideal for home buying. You can afford properties up to ₹${this.formatNumber(maxPropertyPrice)} with strong loan eligibility.`;
        } else if (foir <= 45 && readinessScore >= 60) {
            summary = `Good! Your financial profile is suitable for home buying. You can afford properties up to ₹${this.formatNumber(maxPropertyPrice)} with standard loan terms.`;
        } else if (foir <= 60 && readinessScore >= 40) {
            summary = `Fair. Your financial profile needs some improvement for optimal home buying. Currently you can afford properties up to ₹${this.formatNumber(maxPropertyPrice)}.`;
        } else {
            summary = `Your financial profile needs significant improvement before home buying. Focus on reducing expenses and improving credit score.`;
        }
        
        return summary;
    }

    generateRecommendations(data, foir, readinessScore, maxPropertyPrice) {
        const recommendations = [];
        
        if (foir > 50) {
            recommendations.push('Reduce existing EMIs and monthly expenses to improve FOIR');
        }
        
        if (readinessScore < 60) {
            recommendations.push('Improve your CIBIL score for better loan terms');
            recommendations.push('Consider increasing your work experience');
        }
        
        if (data.downPayment < maxPropertyPrice * 0.20) {
            recommendations.push('Increase your down payment to cover a significant portion of the property price');
        }
        
        if (data.coApplicant === 'no' && foir > 40) {
            recommendations.push('Consider adding a co-applicant for better loan eligibility');
        }
        
        if (recommendations.length === 0) {
            recommendations.push('Your financial profile is excellent for home buying');
            recommendations.push(`Consider properties in the ₹${this.formatNumber(maxPropertyPrice)} range`);
        }
        
        return recommendations;
    }

    generateImprovementStrategies(data, foir, monthlyIncome, monthlyObligations) {
        const strategies = [];
        
        // FOIR Improvement Strategies
        if (foir > 45) {
            strategies.push({
                category: 'FOIR Reduction',
                priority: 'high',
                strategies: [
                    {
                        action: 'Reduce existing EMIs',
                        impact: `Could reduce FOIR by ${Math.min(5, foir - 45).toFixed(1)}%`,
                        timeline: '1-3 months',
                        effort: 'medium'
                    },
                    {
                        action: 'Increase down payment',
                        impact: 'Reduces loan amount and EMI',
                        timeline: '3-6 months',
                        effort: 'high'
                    },
                    {
                        action: 'Extend loan tenure',
                        impact: 'Reduces monthly EMI',
                        timeline: 'immediate',
                        effort: 'low'
                    }
                ]
            });
        }
        
        // CIBIL Score Improvement
        const cibilScore = this.parseCibilScore(data.cibilScore);
        if (cibilScore < 750) {
            strategies.push({
                category: 'CIBIL Score Improvement',
                priority: 'high',
                strategies: [
                    {
                        action: 'Pay bills on time',
                        impact: 'Improve credit history',
                        timeline: '6-12 months',
                        effort: 'low'
                    },
                    {
                        action: 'Reduce credit utilization',
                        impact: 'Lower credit risk',
                        timeline: '3-6 months',
                        effort: 'medium'
                    }
                ]
            });
        }
        
        return strategies;
    }

    generateWhatIfScenarios(data, foir, maxPropertyPrice) {
        const scenarios = [];
        
        // Scenario 1: Reduce EMIs
        if (data.existingEMIs > 0) {
            const reducedEMIs = data.existingEMIs * 0.5;
            const newFOIR = this.calculateFOIRWithChanges({ existingEMIs: reducedEMIs }, data);
            const newMaxLoan = this.calculateMaxLoanAmountWithChanges({ existingEMIs: reducedEMIs }, data);
            const currentLoanAmount = maxPropertyPrice - data.downPayment;
            
            // Only add scenario if we have valid calculations
            if (currentLoanAmount > 0 && newMaxLoan > 0) {
                const loanIncreasePercent = ((newMaxLoan - currentLoanAmount) / currentLoanAmount * 100);
                
                scenarios.push({
                    title: 'Reduce Existing EMIs by 50%',
                    description: 'What if you reduce your current EMIs?',
                    changes: {
                        current: { foir: foir, maxLoan: currentLoanAmount },
                        projected: { foir: newFOIR, maxLoan: newMaxLoan }
                    },
                    improvement: {
                        foirReduction: (foir - newFOIR).toFixed(1),
                        loanIncrease: loanIncreasePercent.toFixed(1)
                    },
                    effort: 'medium',
                    timeline: '3-6 months'
                });
            }
        }
        
        // Scenario 2: Increase Savings
        if (data.downPayment > 0 && data.downPayment < 1000000) {
            const increasedDownPayment = Math.min(data.downPayment * 2, 1000000);
            const newMaxPropertyPrice = (maxPropertyPrice - data.downPayment) + increasedDownPayment;
            
            // Only add scenario if we have valid calculations
            if (data.downPayment > 0 && maxPropertyPrice > 0) {
                const downPaymentIncreasePercent = ((increasedDownPayment - data.downPayment) / data.downPayment * 100);
                const propertyIncreasePercent = ((newMaxPropertyPrice - maxPropertyPrice) / maxPropertyPrice * 100);
                
                scenarios.push({
                    title: 'Double Your Down Payment',
                    description: 'What if you increase your down payment?',
                    changes: {
                        current: { downPayment: data.downPayment, maxPropertyPrice: maxPropertyPrice },
                        projected: { downPayment: increasedDownPayment, maxPropertyPrice: newMaxPropertyPrice }
                    },
                    improvement: {
                        downPaymentIncrease: downPaymentIncreasePercent.toFixed(1),
                        propertyIncrease: propertyIncreasePercent.toFixed(1)
                    },
                    effort: 'high',
                    timeline: '6-12 months'
                });
            }
        }
        
        return scenarios;
    }

    assessRiskLevel(foir, readinessScore, data) {
        let riskScore = 0;
        let riskFactors = [];
        
        // FOIR Risk
        if (foir > 60) {
            riskScore += 40;
            riskFactors.push('Very high FOIR (>60%)');
        } else if (foir > 45) {
            riskScore += 25;
            riskFactors.push('High FOIR (>45%)');
        }
        
        // CIBIL Risk
        const cibilScore = this.parseCibilScore(data.cibilScore);
        if (cibilScore < 550) {
            riskScore += 30;
            riskFactors.push('Poor CIBIL score');
        } else if (cibilScore < 650) {
            riskScore += 15;
            riskFactors.push('Fair CIBIL score');
        }
        
        // Income Risk
        if (data.grossIncome < 50000) {
            riskScore += 20;
            riskFactors.push('Low monthly income');
        }
        
        // Risk Level Classification
        let riskLevel, color, message;
        if (riskScore >= 70) {
            riskLevel = 'High Risk';
            color = '#ef4444';
            message = 'Significant improvements needed before loan approval';
        } else if (riskScore >= 40) {
            riskLevel = 'Medium Risk';
            color = '#f59e0b';
            message = 'Moderate improvements recommended for better terms';
        } else if (riskScore >= 20) {
            riskLevel = 'Low Risk';
            color = '#3b82f6';
            message = 'Minor improvements can enhance loan terms';
        } else {
            riskLevel = 'Very Low Risk';
            color = '#10b981';
            message = 'Excellent financial profile for loan approval';
        }
        
        return {
            riskScore,
            riskLevel,
            color,
            message,
            riskFactors
        };
    }

    // Helper methods for what-if calculations
    calculateFOIRWithChanges(changes, originalData) {
        const tempData = { ...originalData, ...changes };
        const monthlyIncome = tempData.grossIncome + (tempData.coApplicant === 'yes' ? tempData.coApplicantIncome : 0);
        // Remove rent from expenses calculation
        const monthlyExpenses = tempData.utilities + tempData.groceries + tempData.subscriptions + tempData.otherMonthly;
        const yearlyExpenses = tempData.insurance + tempData.schoolFees + tempData.propertyTax + tempData.otherYearly;
        // Include monthly savings in obligations
        const totalMonthlyObligations = Math.round(monthlyExpenses + (yearlyExpenses / 12) + tempData.existingEMIs + tempData.monthlySavings);
        
        return (totalMonthlyObligations / monthlyIncome) * 100;
    }

    calculateMaxLoanAmountWithChanges(changes, originalData) {
        const tempData = { ...originalData, ...changes };
        const monthlyIncome = tempData.grossIncome + (tempData.coApplicant === 'yes' ? tempData.coApplicantIncome : 0);
        // Remove rent from expenses calculation
        const monthlyExpenses = tempData.utilities + tempData.groceries + tempData.subscriptions + tempData.otherMonthly;
        const yearlyExpenses = tempData.insurance + tempData.schoolFees + tempData.propertyTax + tempData.otherYearly;
        // Include monthly savings in obligations
        const totalMonthlyObligations = Math.round(monthlyExpenses + (yearlyExpenses / 12) + tempData.existingEMIs + tempData.monthlySavings);
        
        const availableForEMI = monthlyIncome - totalMonthlyObligations;
        
        if (availableForEMI <= 0) return 0;
        
        const interestRate = tempData.interestRate / 100 / 12;
        const tenure = tempData.loanTenure * 12;
        
        return availableForEMI * ((Math.pow(1 + interestRate, tenure) - 1) / (interestRate * Math.pow(1 + interestRate, tenure)));
    }

    // ===== RESULTS DISPLAY =====

    displayResults(results) {
        console.log('Displaying results with smart guidance:', results);
        
        // Hide form and show results section
        document.getElementById('affordabilityCalculator').style.display = 'none';
        document.getElementById('resultsSection').style.display = 'block';
        
        // Generate and display results HTML
        const resultsHTML = this.generateResultsHTML(results);
        document.getElementById('resultsSection').innerHTML = resultsHTML;
        
        // Draw expenses pie chart
        this.drawExpensesPieChart(results);
        
        // Draw income vs EMI projection chart
        this.drawIncomeEMIChart(results);
        
        // Setup EMI adjustment controls
        this.setupEMIAdjustment(results);
        
        // Scroll to results
        document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
    }

    generateResultsHTML(results) {
        const foirStatus = results.results.foirStatus;
        const readinessStatus = results.results.readinessStatus;
        const guidance = results.results.guidance;
        
        // Generate clear affordability statement
        const affordabilityStatement = `🎯 <strong>As per your financials, you can afford properties up to ₹${this.formatNumber(results.results.maxPropertyPrice)}</strong>`;
        
        let html = `
            <div class="results-header">
                <h3><i class="fas fa-chart-line"></i> Your Affordability Report</h3>
                <p>${results.message}</p>
            </div>
            
            <!-- AFFORDABILITY SUMMARY - PROMINENT DISPLAY -->
            <div class="affordability-summary">
                <div class="affordability-message">
                    ${affordabilityStatement}
                </div>
            </div>
            
            <div class="results-content">
                <!-- Key Metrics Row -->
                <div class="key-metrics-row">
                    <div class="metric-card foir-card">
                        <div class="metric-header">
                            <h4><i class="fas fa-percentage"></i> FOIR</h4>
                            <span class="metric-status" style="color: ${foirStatus.color}">${foirStatus.status}</span>
                        </div>
                        <div class="metric-value">${results.results.foir.toFixed(1)}%</div>
                        <div class="metric-risk">Risk: ${foirStatus.risk}</div>
                    </div>
                    
                    <div class="metric-card readiness-card">
                        <div class="metric-header">
                            <h4><i class="fas fa-star"></i> Home Buying Readiness</h4>
                            <span class="metric-status" style="color: ${readinessStatus.color}">${readinessStatus.status}</span>
                        </div>
                        <div class="metric-value">${results.results.readinessScore}/100</div>
                        <div class="metric-description">${readinessStatus.description}</div>
                    </div>
                </div>
                
                <!-- Income vs Expenses Summary -->
                <div class="income-expenses-summary">
                    <h4><i class="fas fa-balance-scale"></i> Income vs Expenses Summary</h4>
                    <div class="income-expenses-grid">
                        <div class="income-section">
                            <h5><i class="fas fa-arrow-up" style="color: #10b981;"></i> Monthly Income</h5>
                            <div class="income-breakdown">
                                <div class="income-item">
                                    <span class="label">Your Income:</span>
                                    <span class="value">₹${this.formatNumber(results.data.grossIncome)}</span>
                                </div>
                                ${results.data.coApplicant === 'yes' && results.data.coApplicantIncome ? `
                                <div class="income-item">
                                    <span class="label">Co-Applicant Income:</span>
                                    <span class="value">₹${this.formatNumber(results.data.coApplicantIncome)}</span>
                                </div>
                                ` : ''}
                                <div class="income-total">
                                    <span class="label">Total Monthly Income:</span>
                                    <span class="value">₹${this.formatNumber(results.results.totalMonthlyIncome)}</span>
                                </div>
                            </div>
                        </div>
                        
                        <div class="expenses-section">
                            <h5><i class="fas fa-arrow-down" style="color: #ef4444;"></i> Monthly Expenses</h5>
                            <div class="expenses-breakdown">
                                                                 <div class="expenses-group">
                                     <h6>Monthly Obligations:</h6>
                                     <div class="expense-item">
                                         <span class="label">Utilities:</span>
                                         <span class="value">₹${this.formatNumber(results.data.utilities)}</span>
                                     </div>
                                     <div class="expense-item">
                                         <span class="label">Groceries:</span>
                                         <span class="value">₹${this.formatNumber(results.data.groceries)}</span>
                                     </div>
                                     <div class="expense-item">
                                         <span class="label">Subscriptions:</span>
                                         <span class="value">₹${this.formatNumber(results.data.subscriptions)}</span>
                                     </div>
                                     <div class="expense-item">
                                         <span class="label">Other Monthly:</span>
                                         <span class="value">₹${this.formatNumber(results.data.otherMonthly)}</span>
                                     </div>
                                     <div class="expense-item">
                                         <span class="label">Existing EMIs:</span>
                                         <span class="value">₹${this.formatNumber(results.data.existingEMIs)}</span>
                                     </div>
                                     <div class="expense-item">
                                         <span class="label">Monthly Savings:</span>
                                         <span class="value">₹${this.formatNumber(results.data.monthlySavings)}</span>
                                     </div>
                                 </div>
                                
                                <div class="expenses-group">
                                    <h6>Yearly Expenses (Monthly):</h6>
                                    <div class="expense-item">
                                        <span class="label">Insurance:</span>
                                        <span class="value">₹${this.formatNumber(results.data.insurance / 12)}</span>
                                    </div>
                                    <div class="expense-item">
                                        <span class="label">School Fees:</span>
                                        <span class="value">₹${this.formatNumber(results.data.schoolFees / 12)}</span>
                                    </div>
                                    <div class="expense-item">
                                        <span class="label">Property Tax:</span>
                                        <span class="value">₹${this.formatNumber(results.data.propertyTax / 12)}</span>
                                    </div>
                                    <div class="expense-item">
                                        <span class="label">Other Yearly:</span>
                                        <span class="value">₹${this.formatNumber(results.data.otherYearly / 12)}</span>
                                    </div>
                                </div>
                                
                                <div class="expenses-total">
                                    <span class="label">Total Monthly Expenses:</span>
                                    <span class="value">₹${this.formatNumber(results.results.totalMonthlyObligations)}</span>
                                </div>
                            </div>
                        </div>
                                         </div>
                     
                     <!-- Expenses Pie Chart -->
                     <div class="expenses-pie-chart">
                         <h6><i class="fas fa-chart-pie"></i> Expenses Breakdown</h6>
                         <div class="pie-chart-container">
                             <canvas id="expensesPieChart" width="200" height="200"></canvas>
                             <div class="pie-chart-legend">
                                 <div class="legend-item">
                                     <span class="legend-color" style="background: #3b82f6;"></span>
                                     <span class="legend-label">Utilities</span>
                                     <span class="legend-value">₹${this.formatNumber(results.data.utilities)}</span>
                                 </div>
                                 <div class="legend-item">
                                     <span class="legend-color" style="background: #10b981;"></span>
                                     <span class="legend-label">Groceries</span>
                                     <span class="legend-value">₹${this.formatNumber(results.data.groceries)}</span>
                                 </div>
                                 <div class="legend-item">
                                     <span class="legend-color" style="background: #f59e0b;"></span>
                                     <span class="legend-label">Subscriptions</span>
                                     <span class="legend-value">₹${this.formatNumber(results.data.subscriptions)}</span>
                                 </div>
                                 <div class="legend-item">
                                     <span class="legend-color" style="background: #ef4444;"></span>
                                     <span class="legend-label">Other Monthly</span>
                                     <span class="legend-value">₹${this.formatNumber(results.data.otherMonthly)}</span>
                                 </div>
                                 <div class="legend-item">
                                     <span class="legend-color" style="background: #8b5cf6;"></span>
                                     <span class="legend-label">Existing EMIs</span>
                                     <span class="legend-value">₹${this.formatNumber(results.data.existingEMIs)}</span>
                                 </div>
                                 <div class="legend-item">
                                     <span class="legend-color" style="background: #06b6d4;"></span>
                                     <span class="legend-label">Yearly (Monthly)</span>
                                     <span class="legend-value">₹${this.formatNumber(results.results.breakdown.monthlyYearlyExpenses)}</span>
                                 </div>
                             </div>
                         </div>
                     </div>
                     
                     <div class="cash-flow-summary">
                         <div class="cash-flow-item">
                             <span class="label">Available for EMI:</span>
                             <span class="value">₹${this.formatNumber(results.results.totalMonthlyIncome - results.results.totalMonthlyObligations)}</span>
                         </div>
                         <div class="cash-flow-item">
                             <span class="label">FOIR Ratio:</span>
                             <span class="value">${results.results.foir.toFixed(1)}%</span>
                         </div>
                     </div>
                 </div>
                
                                 <!-- Savings Profile Section -->
                 <div class="savings-profile-section">
                     <h4><i class="fas fa-piggy-bank"></i> Your Savings Profile</h4>
                     <div class="savings-profile-content">
                         <div class="savings-metrics">
                             <div class="savings-metric">
                                 <h5>Savings Rate</h5>
                                 <div class="metric-value">${results.results.savingsProfile.savingsRate}%</div>
                                 <div class="metric-description">of monthly income</div>
                             </div>
                             <div class="savings-metric">
                                 <h5>Emergency Fund</h5>
                                 <div class="metric-value">${results.results.savingsProfile.emergencyFundMonths} months</div>
                                 <div class="metric-description">of expenses covered</div>
                             </div>
                             <div class="savings-metric">
                                 <h5>Total Savings</h5>
                                 <div class="metric-value">₹${this.formatNumber(results.data.savings)}</div>
                                 <div class="metric-description">available liquid wealth</div>
                             </div>
                         </div>
                         <div class="savings-rating">
                             <div class="rating-header">
                                 <h5>Savings Rating</h5>
                                 <span class="rating-status" style="color: ${results.results.savingsProfile.color}">${results.results.savingsProfile.status}</span>
                             </div>
                             <div class="rating-score">${results.results.savingsProfile.score}/100</div>
                             <p class="rating-description">${results.results.savingsProfile.description}</p>
                         </div>
                         <div class="savings-recommendations">
                             <h6>Recommendations:</h6>
                             <ul>
                                 ${results.results.savingsProfile.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                             </ul>
                         </div>
                     </div>
                 </div>
                 
                 <!-- Smart Guidance Summary -->
                 <div class="guidance-summary">
                     <h4><i class="fas fa-lightbulb"></i> Smart Guidance Summary</h4>
                     <p>${guidance.summary}</p>
                 </div>
                
                <!-- Detailed Results -->
                <div class="detailed-results">
                    <h4><i class="fas fa-calculator"></i> Calculation Results</h4>
                    <div class="results-grid">
                        <div class="result-item">
                            <h5>Maximum Property Price</h5>
                            <div class="result-value">₹${this.formatNumber(results.results.maxPropertyPrice)}</div>
                        </div>
                        <div class="result-item">
                            <h5>Maximum Loan Amount</h5>
                            <div class="result-value">₹${this.formatNumber(results.results.maxLoanAmount)}</div>
                        </div>
                        <div class="result-item">
                            <h5>Down Payment</h5>
                            <div class="result-value">₹${this.formatNumber(results.data.downPayment)}</div>
                        </div>
                        <div class="result-item">
                            <h5>Maximum Monthly EMI</h5>
                            <div class="result-value">₹${this.formatNumber(results.results.maxEMI)}</div>
                        </div>
                        <div class="result-item">
                            <h5>Loan Type</h5>
                            <div class="result-value">${results.data.loanType === 'flexible' ? 'Flexible Rate' : 'Fixed Rate'}</div>
                        </div>
                        <div class="result-item">
                            <h5>Interest Rate</h5>
                            <div class="result-value">${results.data.interestRate}%</div>
                        </div>
                        <div class="result-item">
                            <h5>Monthly Income</h5>
                            <div class="result-value">₹${this.formatNumber(results.results.totalMonthlyIncome)}</div>
                        </div>
                        <div class="result-item">
                            <h5>Monthly Obligations</h5>
                            <div class="result-value">₹${this.formatNumber(results.results.totalMonthlyObligations)}</div>
                        </div>
                    </div>
                    
                                         ${results.data.loanType === 'flexible' ? this.generateEMIVariationsHTML(results) : ''}
                 </div>
                 
                 <!-- Income vs EMI Projection Graph -->
                 <div class="income-emi-projection">
                     <h4><i class="fas fa-chart-line"></i> Income vs EMI Projection (5 Years)</h4>
                     <p>See how your income growth affects your savings potential over time</p>
                     
                     <div class="emi-adjustment-controls">
                         <label for="emiAdjustment">Adjust EMI (₹):</label>
                         <input type="range" id="emiAdjustment" min="0" max="100" value="100" step="5">
                         <span id="emiAdjustmentValue">₹0</span>
                         <small>Drag to reduce EMI and see increased savings</small>
                     </div>
                     
                     <div class="projection-chart-container">
                         <canvas id="incomeEMIChart" width="600" height="300"></canvas>
                     </div>
                     
                     <div class="projection-summary">
                         <div class="projection-metrics">
                             <div class="projection-metric">
                                 <h6>Total Savings (5 Years)</h6>
                                 <div class="metric-value" id="totalSavings5Years">₹0</div>
                             </div>
                             <div class="projection-metric">
                                 <h6>Monthly Savings (Year 5)</h6>
                                 <div class="metric-value" id="monthlySavingsYear5">₹0</div>
                             </div>
                             <div class="projection-metric">
                                 <h6>Income Growth Rate</h6>
                                 <div class="metric-value">8% per year</div>
                             </div>
                         </div>
                     </div>
                 </div>
                 
                 <!-- Smart Recommendations -->
                <div class="recommendations-section">
                    <h4><i class="fas fa-lightbulb"></i> Smart Recommendations</h4>
                    <div class="recommendations-list">
                        ${guidance.recommendations.map(rec => `<div class="recommendation-item"><i class="fas fa-check"></i> ${rec}</div>`).join('')}
                    </div>
                </div>
                
                <!-- Improvement Strategies -->
                ${this.generateImprovementStrategiesHTML(guidance.improvementStrategies)}
                
                <!-- What-If Scenarios -->
                ${this.generateWhatIfScenariosHTML(guidance.whatIfScenarios)}
                
                <!-- Risk Assessment -->
                ${this.generateRiskAssessmentHTML(guidance.riskAssessment)}
                
                <!-- Action Buttons -->
                <div class="results-actions">
                    <button class="btn btn-secondary" onclick="this.goBackToCalculator()">
                        <i class="fas fa-arrow-left"></i> Calculate Again
                    </button>
                    <button class="btn btn-primary" onclick="window.print()">
                        <i class="fas fa-print"></i> Print Report
                    </button>
                </div>
            </div>
        `;
        
        return html;
    }

    generateImprovementStrategiesHTML(strategies) {
        if (strategies.length === 0) return '';
        
        return `
            <div class="improvement-strategies">
                <h4><i class="fas fa-lightbulb"></i> Improvement Strategies</h4>
                <div class="strategies-list">
                    ${strategies.map(strategy => `
                        <div class="strategy-group">
                            <h5>${strategy.category}</h5>
                            <div class="strategy-items">
                                ${strategy.strategies.map(item => `
                                    <div class="strategy-item">
                                        <div class="strategy-action">
                                            <i class="fas fa-arrow-right"></i>
                                            <span>${item.action}</span>
                                        </div>
                                        <div class="strategy-details">
                                            <span class="impact">${item.impact}</span>
                                            <span class="timeline">${item.timeline}</span>
                                            <span class="effort effort-${item.effort}">${item.effort}</span>
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    generateWhatIfScenariosHTML(scenarios) {
        if (scenarios.length === 0) return '';
        
        return `
            <div class="what-if-scenarios">
                <h4><i class="fas fa-magic"></i> What-If Scenarios</h4>
                <p>Explore how different financial decisions could impact your home buying potential</p>
                <div class="scenarios-grid">
                    ${scenarios.map(scenario => `
                        <div class="scenario-card">
                            <h5>${scenario.title}</h5>
                            <p>${scenario.description}</p>
                            <div class="scenario-impact">
                                ${scenario.improvement.foirReduction ? `
                                    <div class="impact-item">
                                        <span class="impact-label">FOIR Reduction:</span>
                                        <span class="impact-value positive">-${scenario.improvement.foirReduction}%</span>
                                    </div>
                                ` : ''}
                                ${scenario.improvement.loanIncrease ? `
                                    <div class="impact-item">
                                        <span class="impact-label">Loan Increase:</span>
                                        <span class="impact-value positive">+${scenario.improvement.loanIncrease}%</span>
                                    </div>
                                ` : ''}
                                ${scenario.improvement.downPaymentIncrease ? `
                                    <div class="impact-item">
                                        <span class="impact-label">Down Payment Increase:</span>
                                        <span class="impact-value positive">+${scenario.improvement.downPaymentIncrease}%</span>
                                    </div>
                                ` : ''}
                                ${scenario.improvement.propertyIncrease ? `
                                    <div class="impact-item">
                                        <span class="impact-label">Property Price Increase:</span>
                                        <span class="impact-value positive">+${scenario.improvement.propertyIncrease}%</span>
                                    </div>
                                ` : ''}
                            </div>
                            <div class="scenario-meta">
                                <span class="effort effort-${scenario.effort}">${scenario.effort}</span>
                                <span class="timeline">${scenario.timeline}</span>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    generateRiskAssessmentHTML(riskAssessment) {
        return `
            <div class="risk-assessment">
                <h4><i class="fas fa-shield-alt"></i> Risk Assessment</h4>
                <div class="risk-summary">
                    <div class="risk-level" style="color: ${riskAssessment.color}">
                        <h5>Risk Level: ${riskAssessment.riskLevel}</h5>
                        <p>${riskAssessment.message}</p>
                    </div>
                    <div class="risk-factors">
                        <h6>Risk Factors:</h6>
                        <ul>
                            ${riskAssessment.riskFactors.map(factor => `<li>${factor}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            </div>
        `;
    }

        // Generate EMI Variations HTML for Flexible Loans
    generateEMIVariationsHTML(results) {
        const interestRate = results.data.interestRate;
        const loanAmount = results.results.maxLoanAmount;
        const tenure = results.data.loanTenure;
        
        // Calculate EMIs for different rates
        const emiLower = this.calculateEMI(loanAmount, Math.max(interestRate - 2, 7.5), tenure);
        const emiSelected = this.calculateEMI(loanAmount, interestRate, tenure);
        const emiHigher = this.calculateEMI(loanAmount, Math.min(interestRate + 3, 12), tenure);
        
        return `
            <div class="emi-variations-results">
                <h4><i class="fas fa-chart-line"></i> EMI Variations (Flexible Loan)</h4>
                <div class="emi-variations-grid">
                    <div class="emi-variation-result">
                        <h5>Rate - 2%:</h5>
                        <div class="emi-value">₹${this.formatNumber(emiLower)}</div>
                    </div>
                    <div class="emi-variation-result selected">
                        <h5>Selected Rate:</h5>
                        <div class="emi-value">₹${this.formatNumber(emiSelected)}</div>
                    </div>
                    <div class="emi-variation-result">
                        <h5>Rate + 3%:</h5>
                        <div class="emi-value">₹${this.formatNumber(emiHigher)}</div>
                    </div>
                </div>
                <div class="emi-note">
                    <p><strong>EMI variations based on interest rate changes</strong></p>
                </div>
            </div>
        `;
    }

    // Draw Income vs EMI Projection Chart
    drawIncomeEMIChart(results) {
        const canvas = document.getElementById('incomeEMIChart');
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;
        
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        // Chart configuration
        const padding = 40;
        const chartWidth = width - 2 * padding;
        const chartHeight = height - 2 * padding;
        
        // Data for 5 years
        const years = [1, 2, 3, 4, 5];
        const baseIncome = results.results.totalMonthlyIncome;
        const baseEMI = results.results.maxEMI;
        
        // Get income growth rate from slider (default 8%)
        const incomeGrowthSlider = document.getElementById('incomeGrowthRate');
        const incomeGrowthRate = incomeGrowthSlider ? parseFloat(incomeGrowthSlider.value) / 100 : 0.08;
        
        // Calculate income growth based on slider value
        const incomes = years.map(year => baseIncome * Math.pow(1 + incomeGrowthRate, year - 1));
        const emis = years.map(() => baseEMI); // EMI remains constant
        
        // Find min and max values for scaling
        const minValue = 0;
        const maxValue = Math.max(...incomes) * 1.1;
        
        // Scale function
        const scaleX = (value) => padding + (value / (years.length - 1)) * chartWidth;
        const scaleY = (value) => height - padding - (value / maxValue) * chartHeight;
        
        // Draw grid lines
        ctx.strokeStyle = '#374151';
        ctx.lineWidth = 1;
        ctx.setLineDash([2, 2]);
        
        // Horizontal grid lines
        for (let i = 0; i <= 5; i++) {
            const y = padding + (i / 5) * chartHeight;
            ctx.beginPath();
            ctx.moveTo(padding, y);
            ctx.lineTo(width - padding, y);
            ctx.stroke();
            
            // Y-axis labels
            const value = (maxValue * (1 - i / 5)).toFixed(0);
            ctx.fillStyle = '#9ca3af';
            ctx.font = '12px Arial';
            ctx.textAlign = 'right';
            ctx.fillText(`₹${this.formatNumber(value)}`, padding - 10, y + 4);
        }
        
        // Vertical grid lines
        for (let i = 0; i < years.length; i++) {
            const x = scaleX(i);
            ctx.beginPath();
            ctx.moveTo(x, padding);
            ctx.lineTo(x, height - padding);
            ctx.stroke();
            
            // X-axis labels
            ctx.fillStyle = '#9ca3af';
            ctx.font = '12px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(`Year ${years[i]}`, x, height - padding + 20);
        }
        
        // Reset line style
        ctx.setLineDash([]);
        
        // Draw income line
        ctx.strokeStyle = '#10b981';
        ctx.lineWidth = 3;
        ctx.beginPath();
        years.forEach((year, index) => {
            const x = scaleX(index);
            const y = scaleY(incomes[index]);
            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });
        ctx.stroke();
        
        // Draw EMI line
        ctx.strokeStyle = '#ef4444';
        ctx.lineWidth = 3;
        ctx.beginPath();
        years.forEach((year, index) => {
            const x = scaleX(index);
            const y = scaleY(emis[index]);
            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });
        ctx.stroke();
        
        // Draw data points
        years.forEach((year, index) => {
            // Income points
            ctx.fillStyle = '#10b981';
            ctx.beginPath();
            ctx.arc(scaleX(index), scaleY(incomes[index]), 4, 0, 2 * Math.PI);
            ctx.fill();
            
            // EMI points
            ctx.fillStyle = '#ef4444';
            ctx.beginPath();
            ctx.arc(scaleX(index), scaleY(emis[index]), 4, 0, 2 * Math.PI);
            ctx.fill();
        });
        
        // Add legend
        ctx.fillStyle = '#e5e7eb';
        ctx.font = '14px Arial';
        ctx.textAlign = 'left';
        
        // Income legend
        ctx.fillStyle = '#10b981';
        ctx.fillRect(width - 120, padding, 15, 3);
        ctx.fillStyle = '#e5e7eb';
        ctx.fillText('Income (8% growth)', width - 100, padding + 8);
        
        // EMI legend
        ctx.fillStyle = '#ef4444';
        ctx.fillRect(width - 120, padding + 20, 15, 3);
        ctx.fillStyle = '#e5e7eb';
        ctx.fillText('EMI (constant)', width - 100, padding + 28);
    }
    
    // Setup EMI adjustment controls
    setupEMIAdjustment(results) {
        const emiSlider = document.getElementById('emiAdjustment');
        const emiValueDisplay = document.getElementById('emiAdjustmentValue');
        const incomeSlider = document.getElementById('incomeGrowthRate');
        const incomeValueDisplay = document.getElementById('incomeGrowthRateValue');
        const totalSavingsDisplay = document.getElementById('totalSavings5Years');
        const monthlySavingsTodayDisplay = document.getElementById('monthlySavingsToday');
        const monthlySavingsYear5Display = document.getElementById('monthlySavingsYear5');
        
        if (!emiSlider || !emiValueDisplay || !incomeSlider || !incomeValueDisplay) return;
        
        const baseEMI = results.results.maxEMI;
        const baseIncome = results.results.totalMonthlyIncome;
        
        // Set EMI slider range (0% to 100% of calculated EMI)
        emiSlider.max = 100;
        emiSlider.value = 100;
        
        // Set income growth slider range (0% to 20% per year)
        incomeSlider.min = 0;
        incomeSlider.max = 20;
        incomeSlider.value = 8;
        
        const updateProjection = () => {
            const emiPercentage = parseInt(emiSlider.value);
            const adjustedEMI = (baseEMI * emiPercentage) / 100;
            const incomeGrowthRate = parseFloat(incomeSlider.value) / 100;
            
            // Update displays
            emiValueDisplay.textContent = `₹${this.formatNumber(adjustedEMI)}`;
            incomeValueDisplay.textContent = `${incomeSlider.value}% per year`;
            
            // Calculate 5-year projection
            const years = [1, 2, 3, 4, 5];
            let totalSavings = 0;
            
            years.forEach(year => {
                const yearIncome = baseIncome * Math.pow(1 + incomeGrowthRate, year - 1);
                const yearSavings = yearIncome - adjustedEMI;
                totalSavings += yearSavings;
            });
            
            // Calculate monthly savings today and in year 5
            const monthlySavingsToday = baseIncome - adjustedEMI;
            const year5Income = baseIncome * Math.pow(1 + incomeGrowthRate, 4);
            const year5Savings = year5Income - adjustedEMI;
            
            // Update displays
            totalSavingsDisplay.textContent = `₹${this.formatNumber(totalSavings)}`;
            monthlySavingsTodayDisplay.textContent = `₹${this.formatNumber(monthlySavingsToday)}`;
            monthlySavingsYear5Display.textContent = `₹${this.formatNumber(year5Savings)}`;
            
            // Redraw chart with new EMI and income growth rate
            this.drawIncomeEMIChartWithAdjustedEMI(results, adjustedEMI, incomeGrowthRate);
        };
        
        // Add event listeners
        emiSlider.addEventListener('input', updateProjection);
        incomeSlider.addEventListener('input', updateProjection);
        
        // Initial update
        updateProjection();
        
        // Also draw initial chart
        this.drawIncomeEMIChart(results);
    }
    
    // Draw chart with adjusted EMI
    drawIncomeEMIChartWithAdjustedEMI(results, adjustedEMI, incomeGrowthRate = 0.08) {
        const canvas = document.getElementById('incomeEMIChart');
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;
        
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        // Chart configuration
        const padding = 40;
        const chartWidth = width - 2 * padding;
        const chartHeight = height - 2 * padding;
        
        // Data for 5 years
        const years = [1, 2, 3, 4, 5];
        const baseIncome = results.results.totalMonthlyIncome;
        
        // Calculate income growth based on incomeGrowthRate parameter
        const incomes = years.map(year => baseIncome * Math.pow(1 + incomeGrowthRate, year - 1));
        const emis = years.map(() => adjustedEMI); // Adjusted EMI
        
        // Find min and max values for scaling
        const minValue = 0;
        const maxValue = Math.max(...incomes) * 1.1;
        
        // Scale function
        const scaleX = (value) => padding + (value / (years.length - 1)) * chartWidth;
        const scaleY = (value) => height - padding - (value / maxValue) * chartHeight;
        
        // Draw grid lines
        ctx.strokeStyle = '#374151';
        ctx.lineWidth = 1;
        ctx.setLineDash([2, 2]);
        
        // Horizontal grid lines
        for (let i = 0; i <= 5; i++) {
            const y = padding + (i / 5) * chartHeight;
            ctx.beginPath();
            ctx.moveTo(padding, y);
            ctx.lineTo(width - padding, y);
            ctx.stroke();
            
            // Y-axis labels
            const value = (maxValue * (1 - i / 5)).toFixed(0);
            ctx.fillStyle = '#9ca3af';
            ctx.font = '12px Arial';
            ctx.textAlign = 'right';
            ctx.fillText(`₹${this.formatNumber(value)}`, padding - 10, y + 4);
        }
        
        // Vertical grid lines
        for (let i = 0; i < years.length; i++) {
            const x = scaleX(i);
            ctx.beginPath();
            ctx.moveTo(x, padding);
            ctx.lineTo(x, height - padding);
            ctx.stroke();
            
            // X-axis labels
            ctx.fillStyle = '#9ca3af';
            ctx.font = '12px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(`Year ${years[i]}`, x, height - padding + 20);
        }
        
        // Reset line style
        ctx.setLineDash([]);
        
        // Draw income line
        ctx.strokeStyle = '#10b981';
        ctx.lineWidth = 3;
        ctx.beginPath();
        years.forEach((year, index) => {
            const x = scaleX(index);
            const y = scaleY(incomes[index]);
            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });
        ctx.stroke();
        
        // Draw EMI line
        ctx.strokeStyle = '#ef4444';
        ctx.lineWidth = 3;
        ctx.beginPath();
        years.forEach((year, index) => {
            const x = scaleX(index);
            const y = scaleY(emis[index]);
            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });
        ctx.stroke();
        
        // Draw data points
        years.forEach((year, index) => {
            // Income points
            ctx.fillStyle = '#10b981';
            ctx.beginPath();
            ctx.arc(scaleX(index), scaleY(incomes[index]), 4, 0, 2 * Math.PI);
            ctx.fill();
            
            // EMI points
            ctx.fillStyle = '#ef4444';
            ctx.beginPath();
            ctx.arc(scaleX(index), scaleY(emis[index]), 4, 0, 2 * Math.PI);
            ctx.fill();
        });
        
        // Add legend
        ctx.fillStyle = '#e5e7eb';
        ctx.font = '14px Arial';
        ctx.textAlign = 'left';
        
        // Income legend
        ctx.fillStyle = '#10b981';
        ctx.fillRect(width - 120, padding, 15, 3);
        ctx.fillStyle = '#e5e7eb';
        ctx.fillText('Income (8% growth)', width - 120, padding + 8);
        
        // EMI legend
        ctx.fillStyle = '#ef4444';
        ctx.fillRect(width - 120, padding + 20, 15, 3);
        ctx.fillStyle = '#e5e7eb';
        ctx.fillText(`EMI (₹${this.formatNumber(adjustedEMI)})`, width - 120, padding + 28);
    }
    
    // Draw Expenses Pie Chart
    drawExpensesPieChart(results) {
        const canvas = document.getElementById('expensesPieChart');
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;
        const centerX = width / 2;
        const centerY = height / 2;
        const radius = Math.min(centerX, centerY) - 10;
        
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        // Expense data
        const expenses = [
            { label: 'Utilities', value: results.data.utilities, color: '#3b82f6' },
            { label: 'Groceries', value: results.data.groceries, color: '#10b981' },
            { label: 'Subscriptions', value: results.data.subscriptions, color: '#f59e0b' },
            { label: 'Other Monthly', value: results.data.otherMonthly, color: '#ef4444' },
            { label: 'Existing EMIs', value: results.data.existingEMIs, color: '#8b5cf6' },
            { label: 'Yearly (Monthly)', value: results.results.breakdown.monthlyYearlyExpenses, color: '#06b6d4' },
            { label: 'Monthly Savings', value: results.data.monthlySavings, color: '#059669' }
        ];
        
        // Calculate total
        const total = expenses.reduce((sum, expense) => sum + expense.value, 0);
        if (total === 0) return;
        
        // Draw pie chart
        let currentAngle = -Math.PI / 2; // Start from top
        
        expenses.forEach(expense => {
            if (expense.value > 0) {
                const sliceAngle = (expense.value / total) * 2 * Math.PI;
                
                ctx.beginPath();
                ctx.moveTo(centerX, centerY);
                ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
                ctx.closePath();
                ctx.fillStyle = expense.color;
                ctx.fill();
                
                currentAngle += sliceAngle;
            }
        });
        
        // Add center text
        ctx.fillStyle = '#fff';
        ctx.font = '14px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('Total', centerX, centerY - 5);
        ctx.fillText(`₹${this.formatNumber(total)}`, centerX, centerY + 10);
    }

    // Utility Methods
    formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    goBackToCalculator() {
        document.getElementById('resultsSection').style.display = 'none';
        document.getElementById('affordabilityCalculator').style.display = 'block';
        document.getElementById('affordabilityCalculator').scrollIntoView({ behavior: 'smooth' });
    }

    // Error Handling
    showError(message) {
        console.error('Error:', message);
        
        // Create error notification
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-notification';
        errorDiv.innerHTML = `
            <div class="error-content">
                <i class="fas fa-exclamation-triangle"></i>
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        // Add error notification to page
        document.body.appendChild(errorDiv);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentElement) {
                errorDiv.remove();
            }
        }, 5000);
    }
}

// Initialize calculator when page loads
document.addEventListener('DOMContentLoaded', function() {
    window.calculator = new HomeAffordabilityCalculator();
});

// Global function for co-applicant toggle
function toggleCoApplicantFields() {
    if (window.calculator) {
        window.calculator.toggleCoApplicantFields();
    }
}

// Global function for flexible loan options toggle
function toggleFlexibleOptions() {
    if (window.calculator) {
        window.calculator.toggleFlexibleOptions();
    }
}
