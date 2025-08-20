// Full Pay or Home Loan Calculator JavaScript

class FullPayOrLoanCalculator {
    constructor() {
        this.initializeEventListeners();
        this.setupFormValidation();
    }

    initializeEventListeners() {
        const form = document.getElementById('fullPayOrLoanCalculator');
        if (form) {
            form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }

        // Real-time updates for loan amount
        const loanAmountInput = document.getElementById('loanAmount');
        if (loanAmountInput) {
            loanAmountInput.addEventListener('input', () => this.updateLoanAmountValidation());
        }

        // Real-time updates for property price
        const propertyPriceInput = document.getElementById('propertyPrice');
        if (propertyPriceInput) {
            propertyPriceInput.addEventListener('input', () => this.updateLoanAmountValidation());
        }
    }

    setupFormValidation() {
        const form = document.getElementById('fullPayOrLoanCalculator');
        if (form) {
            form.addEventListener('input', (e) => this.validateInput(e.target));
        }
    }

    validateInput(input) {
        const value = parseFloat(input.value);
        const min = parseFloat(input.min);
        const max = parseFloat(input.max);

        if (value < min) {
            input.setCustomValidity(`Value must be at least ${this.formatNumber(min)}`);
        } else if (value > max) {
            input.setCustomValidity(`Value must be at most ${this.formatNumber(max)}`);
        } else {
            input.setCustomValidity('');
        }
    }

    updateLoanAmountValidation() {
        const propertyPrice = parseFloat(document.getElementById('propertyPrice').value) || 0;
        const loanAmountInput = document.getElementById('loanAmount');
        const moneyAtHand = parseFloat(document.getElementById('moneyAtHand').value) || 0;

        if (propertyPrice > 0) {
            loanAmountInput.max = propertyPrice;
            loanAmountInput.setCustomValidity('');
        }

        if (loanAmountInput.value > propertyPrice) {
            loanAmountInput.setCustomValidity('Loan amount cannot exceed property price');
        } else {
            loanAmountInput.setCustomValidity('');
        }
    }

    handleFormSubmit(e) {
        e.preventDefault();
        
        if (this.validateForm()) {
            const formData = this.collectFormData();
            const results = this.calculateResults(formData);
            this.displayResults(results);
            this.showResultsSection();
        }
    }

    validateForm() {
        const form = document.getElementById('fullPayOrLoanCalculator');
        return form.checkValidity();
    }

    collectFormData() {
        return {
            propertyPrice: parseFloat(document.getElementById('propertyPrice').value),
            moneyAtHand: parseFloat(document.getElementById('moneyAtHand').value),
            loanAmount: parseFloat(document.getElementById('loanAmount').value) || 0,
            interestRate: parseFloat(document.getElementById('interestRate').value),
            loanTenure: parseFloat(document.getElementById('loanTenure').value),
            investmentReturn: parseFloat(document.getElementById('investmentReturn').value)
        };
    }

    calculateResults(data) {
        const results = {
            fullPayOption: this.calculateFullPayOption(data),
            loanOption: this.calculateLoanOption(data),
            comparison: this.compareOptions(data),
            recommendation: this.generateRecommendation(data),
            whatIfScenarios: this.generateWhatIfScenarios(data)
        };

        return results;
    }

    calculateFullPayOption(data) {
        const remainingCash = data.moneyAtHand - data.propertyPrice;
        const investmentValue = remainingCash > 0 ? 
            remainingCash * Math.pow(1 + data.investmentReturn / 100, data.loanTenure) : 0;

        return {
            totalPaid: data.propertyPrice,
            remainingCash: remainingCash,
            investmentValue: investmentValue,
            netWorth: data.propertyPrice + investmentValue
        };
    }

    calculateLoanOption(data) {
        if (data.loanAmount <= 0) {
            return this.calculateFullPayOption(data);
        }

        const monthlyRate = data.interestRate / 100 / 12;
        const totalMonths = data.loanTenure * 12;
        
        // EMI Calculation
        const emi = data.loanAmount * 
            (monthlyRate * Math.pow(1 + monthlyRate, totalMonths)) / 
            (Math.pow(1 + monthlyRate, totalMonths) - 1);

        const totalInterest = (emi * totalMonths) - data.loanAmount;
        const totalPayment = data.loanAmount + totalInterest;
        
        // Remaining cash for investment
        const remainingCash = data.moneyAtHand - (data.propertyPrice - data.loanAmount);
        const investmentValue = remainingCash > 0 ? 
            remainingCash * Math.pow(1 + data.investmentReturn / 100, data.loanTenure) : 0;

        return {
            emi: emi,
            totalInterest: totalInterest,
            totalPayment: totalPayment,
            remainingCash: remainingCash,
            investmentValue: investmentValue,
            netWorth: data.propertyPrice + investmentValue - totalInterest
        };
    }

    compareOptions(data) {
        const fullPay = this.calculateFullPayOption(data);
        const loan = this.calculateLoanOption(data);

        return {
            fullPayNetWorth: fullPay.netWorth,
            loanNetWorth: loan.netWorth,
            difference: loan.netWorth - fullPay.netWorth,
            betterOption: loan.netWorth > fullPay.netWorth ? 'loan' : 'fullPay',
            savings: Math.abs(loan.netWorth - fullPay.netWorth)
        };
    }

    generateRecommendation(data) {
        const comparison = this.compareOptions(data);
        const fullPay = this.calculateFullPayOption(data);
        const loan = this.calculateLoanOption(data);

        let recommendation = '';
        let explanation = '';

        if (comparison.betterOption === 'loan') {
            recommendation = 'Consider taking a home loan and investing the remaining funds';
            explanation = `With this approach, you can potentially increase your net worth by ₹${this.formatNumber(comparison.savings)} over ${data.loanTenure} years while still owning your dream home. The investment returns on your remaining cash can outweigh the loan interest costs.`;
        } else {
            recommendation = 'Consider paying the full amount in cash';
            explanation = `Paying in full cash saves you ₹${this.formatNumber(comparison.savings)} in interest payments and gives you peace of mind with no monthly EMI obligations. You'll own your home outright from day one.`;
        }

        // Additional insights
        let insights = '';
        if (data.loanAmount > 0 && data.loanAmount < data.propertyPrice) {
            const downPayment = data.propertyPrice - data.loanAmount;
            const downPaymentPercentage = ((downPayment / data.propertyPrice) * 100).toFixed(1);
            insights = `Your down payment of ₹${this.formatNumber(downPayment)} (${downPaymentPercentage}%) reduces your loan burden and monthly EMI.`;
        }

        if (data.investmentReturn > data.interestRate) {
            insights += ` Your expected investment return (${data.investmentReturn}%) is higher than the loan interest rate (${data.interestRate}%), which favors the loan + investment strategy.`;
        }

        return {
            recommendation,
            explanation,
            insights
        };
    }

    generateWhatIfScenarios(data) {
        const scenarios = [];

        // Scenario 1: Different interest rates
        const baseLoan = this.calculateLoanOption(data);
        const lowerRate = { ...data, interestRate: Math.max(7.5, data.interestRate - 1) };
        const higherRate = { ...data, interestRate: Math.min(12, data.interestRate + 1) };
        
        const lowerRateLoan = this.calculateLoanOption(lowerRate);
        const higherRateLoan = this.calculateLoanOption(higherRate);

        scenarios.push({
            title: 'Interest Rate Impact',
            description: 'How changing interest rates affect your loan',
            metrics: [
                { label: 'Rate - 1%', value: `₹${this.formatNumber(lowerRateLoan.emi)}`, change: `-${this.formatNumber(baseLoan.emi - lowerRateLoan.emi)}` },
                { label: 'Current Rate', value: `₹${this.formatNumber(baseLoan.emi)}`, change: 'Base' },
                { label: 'Rate + 1%', value: `₹${this.formatNumber(higherRateLoan.emi)}`, change: `+${this.formatNumber(higherRateLoan.emi - baseLoan.emi)}` }
            ]
        });

        // Scenario 2: Different investment returns
        const lowerReturn = { ...data, investmentReturn: Math.max(5, data.investmentReturn - 2) };
        const higherReturn = { ...data, investmentReturn: Math.min(15, data.investmentReturn + 2) };
        
        const lowerReturnFullPay = this.calculateFullPayOption(lowerReturn);
        const higherReturnFullPay = this.calculateFullPayOption(higherReturn);
        const lowerReturnLoan = this.calculateLoanOption(lowerReturn);
        const higherReturnLoan = this.calculateLoanOption(higherReturn);

        scenarios.push({
            title: 'Investment Return Impact',
            description: 'How investment returns affect your wealth',
            metrics: [
                { label: 'Return - 2%', value: `₹${this.formatNumber(lowerReturnLoan.netWorth)}`, change: 'Lower returns' },
                { label: 'Current Return', value: `₹${this.formatNumber(this.calculateLoanOption(data).netWorth)}`, change: 'Base' },
                { label: 'Return + 2%', value: `₹${this.formatNumber(higherReturnLoan.netWorth)}`, change: 'Higher returns' }
            ]
        });

        // Scenario 3: Different loan tenures
        const shorterTenure = { ...data, loanTenure: Math.max(5, data.loanTenure - 5) };
        const longerTenure = { ...data, loanTenure: Math.min(30, data.loanTenure + 5) };
        
        const shorterTenureLoan = this.calculateLoanOption(shorterTenure);
        const longerTenureLoan = this.calculateLoanOption(longerTenure);

        scenarios.push({
            title: 'Loan Tenure Impact',
            description: 'How loan tenure affects your payments',
            metrics: [
                { label: 'Tenure - 5 years', value: `₹${this.formatNumber(shorterTenureLoan.emi)}`, change: 'Higher EMI, less interest' },
                { label: 'Current Tenure', value: `₹${this.formatNumber(baseLoan.emi)}`, change: 'Base' },
                { label: 'Tenure + 5 years', value: `₹${this.formatNumber(longerTenureLoan.emi)}`, change: 'Lower EMI, more interest' }
            ]
        });

        return scenarios;
    }

    displayResults(results) {
        const resultsSection = document.getElementById('resultsSection');
        if (!resultsSection) return;

        resultsSection.innerHTML = this.generateResultsHTML(results);
    }

    generateResultsHTML(results) {
        const fullPay = results.fullPayOption;
        const loan = results.loanOption;
        const comparison = results.comparison;
        const recommendation = results.recommendation;

        return `
            <div class="results-header">
                <h3><i class="fas fa-chart-pie"></i> Financial Comparison Results</h3>
                <p>Detailed analysis of both payment options</p>
            </div>

            <div class="comparison-grid">
                <div class="comparison-card full-pay">
                    <h4><i class="fas fa-money-bill-wave"></i> Full Cash Payment</h4>
                    <div class="metric">
                        <span class="metric-label">Total Amount Paid</span>
                        <span class="metric-value highlight">₹${this.formatNumber(fullPay.totalPaid)}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Remaining Cash</span>
                        <span class="metric-value">₹${this.formatNumber(fullPay.remainingCash)}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Investment Value (${document.getElementById('investmentReturn').value}% return)</span>
                        <span class="metric-value">₹${this.formatNumber(fullPay.investmentValue)}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Net Worth</span>
                        <span class="metric-value highlight">₹${this.formatNumber(fullPay.netWorth)}</span>
                    </div>
                </div>

                <div class="comparison-card loan-option">
                    <h4><i class="fas fa-home"></i> Home Loan Option</h4>
                    <div class="metric">
                        <span class="metric-label">Monthly EMI</span>
                        <span class="metric-value">₹${this.formatNumber(loan.emi)}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Total Interest Paid</span>
                        <span class="metric-value warning">₹${this.formatNumber(loan.totalInterest)}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Total House Payment</span>
                        <span class="metric-value">₹${this.formatNumber(loan.totalPayment)}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Investment Value (${document.getElementById('investmentReturn').value}% return)</span>
                        <span class="metric-value">₹${this.formatNumber(loan.investmentValue)}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Net Worth</span>
                        <span class="metric-value highlight">₹${this.formatNumber(loan.netWorth)}</span>
                    </div>
                </div>
            </div>

            <div class="recommendation-section">
                <h4><i class="fas fa-lightbulb"></i> AI Recommendation</h4>
                <p><strong>${recommendation.recommendation}</strong></p>
                <p>${recommendation.explanation}</p>
                ${recommendation.insights ? `<p><em>${recommendation.insights}</em></p>` : ''}
            </div>

            <div class="what-if-section">
                <h4><i class="fas fa-question-circle"></i> What-If Scenarios</h4>
                <p>Explore how different factors affect your financial outcome</p>
                
                ${results.whatIfScenarios.map(scenario => `
                    <div class="scenario-group" style="margin-top: 1.5rem;">
                        <h5 style="color: #2c3e50; margin-bottom: 1rem;">${scenario.title}</h5>
                        <p style="color: #6c757d; margin-bottom: 1rem;">${scenario.description}</p>
                        <div class="what-if-grid">
                            ${scenario.metrics.map(metric => `
                                <div class="what-if-card">
                                    <h6>${metric.label}</h6>
                                    <div class="value">${metric.value}</div>
                                    <small style="color: #6c757d;">${metric.change}</small>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `).join('')}
            </div>

            <div class="formulas-section" style="background: #f8f9fa; border-radius: 15px; padding: 1.5rem; margin-top: 2rem; border: 1px solid #e9ecef;">
                <h4><i class="fas fa-calculator"></i> Formulas Used</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-top: 1rem;">
                    <div>
                        <h6 style="color: #2c3e50; margin-bottom: 0.5rem;">EMI Calculation</h6>
                        <p style="font-family: monospace; font-size: 0.9rem; color: #6c757d;">
                            EMI = L × [r/12 × (1 + r/12)^(n×12)] / [(1 + r/12)^(n×12) – 1]
                        </p>
                        <small style="color: #6c757d;">Where: L = Loan amount, r = annual interest rate, n = tenure in years</small>
                    </div>
                    <div>
                        <h6 style="color: #2c3e50; margin-bottom: 0.5rem;">Compound Investment</h6>
                        <p style="font-family: monospace; font-size: 0.9rem; color: #6c757d;">
                            Future Value = P × (1 + r/100)^n
                        </p>
                        <small style="color: #6c757d;">Where: P = Principal, r = annual return %, n = years</small>
                    </div>
                </div>
            </div>
        `;
    }

    showResultsSection() {
        const resultsSection = document.getElementById('resultsSection');
        if (resultsSection) {
            resultsSection.style.display = 'block';
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        }
    }

    formatNumber(num) {
        if (isNaN(num) || num === null || num === undefined) return '0';
        return Math.round(num).toLocaleString('en-IN');
    }
}

// Initialize calculator when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new FullPayOrLoanCalculator();
});

// Global functions for form interactions
function toggleFlexibleOptions() {
    // This function can be used for future enhancements
    console.log('Toggle flexible options');
}

function goBackToHome() {
    window.location.href = '../index.html';
}

function goBackToCalculators() {
    window.location.href = 'calculators.html';
}
