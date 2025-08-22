// Full Pay or Home Loan Calculator - Lean & Clean

class FullPayOrLoanCalculator {
    constructor() {
        this.initializeSliders();
        this.calculateAndDisplay();
    }

    initializeSliders() {
        // Property Price Slider
        const propertyPriceSlider = document.getElementById('propertyPrice');
        const propertyPriceValue = document.getElementById('propertyPriceValue');
        propertyPriceSlider.addEventListener('input', (e) => {
            propertyPriceValue.textContent = this.formatNumber(e.target.value);
            this.updateYourContributionMin(); // Update contribution limits when property price changes
            this.calculateAndDisplay();
        });

        // Available Cash Slider
        const moneyAtHandSlider = document.getElementById('moneyAtHand');
        const moneyAtHandValue = document.getElementById('moneyAtHandValue');
        moneyAtHandSlider.addEventListener('input', (e) => {
            moneyAtHandValue.textContent = this.formatNumber(e.target.value);
            this.updateYourContributionMin(); // Update contribution limits when cash changes
            this.validateDownPayment();
            this.calculateAndDisplay();
        });

        // Your Contribution Slider (Downpayment)
        const yourContributionSlider = document.getElementById('yourContribution');
        const yourContributionValue = document.getElementById('yourContributionValue');
        yourContributionSlider.addEventListener('input', (e) => {
            yourContributionValue.textContent = this.formatNumber(e.target.value);
            this.updateLoanAmount();
            this.calculateAndDisplay();
        });

        // Loan Amount Slider - Now read-only, automatically calculated
        // const loanAmountSlider = document.getElementById('loanAmount');
        // const loanAmountValue = document.getElementById('loanAmountValue');
        // loanAmountSlider.addEventListener('input', (e) => {
        //     loanAmountValue.textContent = this.formatNumber(e.target.value);
        //     this.calculateAndDisplay();
        // });

        // Interest Rate Slider
        const interestRateSlider = document.getElementById('interestRate');
        const interestRateValue = document.getElementById('interestRateValue');
        interestRateSlider.addEventListener('input', (e) => {
            interestRateValue.textContent = e.target.value;
            this.calculateAndDisplay();
        });

        // Loan Tenure Slider
        const loanTenureSlider = document.getElementById('loanTenure');
        const loanTenureValue = document.getElementById('loanTenureValue');
        loanTenureSlider.addEventListener('input', (e) => {
            loanTenureValue.textContent = e.target.value;
            this.calculateAndDisplay();
        });

        // Investment Growth Slider
        const investmentGrowthSlider = document.getElementById('investmentGrowth');
        const investmentGrowthValue = document.getElementById('investmentGrowthValue');
        investmentGrowthSlider.addEventListener('input', (e) => {
            investmentGrowthValue.textContent = e.target.value;
            this.calculateAndDisplay();
        });

        // Rent Checkbox and Slider
        const rentCheckbox = document.getElementById('rentCheckbox');
        const rentSliderContainer = document.getElementById('rentSliderContainer');
        const rentSlider = document.getElementById('rent');
        const rentValue = document.getElementById('rentValue');
        
        // Handle checkbox change
        rentCheckbox.addEventListener('change', (e) => {
            if (e.target.checked) {
                rentSliderContainer.classList.remove('hidden');
            } else {
                rentSliderContainer.classList.add('hidden');
            }
            this.calculateAndDisplay();
        });
        
        // Handle rent slider change
        rentSlider.addEventListener('input', (e) => {
            rentValue.textContent = e.target.value;
            this.calculateAndDisplay();
        });

        // House Rate Increase Slider
        const houseRateIncreaseSlider = document.getElementById('houseRateIncrease');
        const houseRateIncreaseValue = document.getElementById('houseRateIncreaseValue');
        houseRateIncreaseSlider.addEventListener('input', (e) => {
            houseRateIncreaseValue.textContent = e.target.value;
            this.calculateAndDisplay();
        });

        // Set initial values and validation
        this.setInitialValues();
        this.updateYourContributionMin();
        this.validateDownPayment();
    }

    setInitialValues() {
        const propertyPrice = parseInt(document.getElementById('propertyPrice').value);
        const availableCash = parseInt(document.getElementById('moneyAtHand').value);
        
        // Set Your Contribution to 20% of property price (minimum downpayment)
        const minContribution = Math.round(propertyPrice * 0.2);
        const maxContribution = Math.max(minContribution, availableCash);
        
        // Always start with minimum contribution (20% of property price)
        const initialContribution = minContribution;
        
        const yourContributionSlider = document.getElementById('yourContribution');
        yourContributionSlider.value = initialContribution;
        document.getElementById('yourContributionValue').textContent = this.formatNumber(initialContribution);
        
        // Loan amount is auto-calculated, no need to display separately
    }

    updateYourContributionMin() {
        const propertyPrice = parseInt(document.getElementById('propertyPrice').value);
        const availableCash = parseInt(document.getElementById('moneyAtHand').value);
        const yourContributionSlider = document.getElementById('yourContribution');
        const minContribution = Math.round(propertyPrice * 0.2); // 20% minimum downpayment
        
        // Your contribution max = Available cash (but not less than minimum)
        const maxContribution = Math.max(minContribution, availableCash);
        
        yourContributionSlider.min = minContribution;
        yourContributionSlider.max = maxContribution;
        
        // Always reset to 20% of property price when property price changes
        yourContributionSlider.value = minContribution;
        document.getElementById('yourContributionValue').textContent = this.formatNumber(minContribution);
        
        // Always ensure loan amount is recalculated
        this.updateLoanAmount();
    }

    updateLoanAmount() {
        // Loan amount is auto-calculated in collectSliderData, no UI update needed
        return;
    }

    validateDownPayment() {
        const propertyPrice = parseInt(document.getElementById('propertyPrice').value);
        const availableCash = parseInt(document.getElementById('moneyAtHand').value);
        const minDownpayment = Math.round(propertyPrice * 0.2);
        const validationMessage = document.getElementById('validationMessage');
        const validationText = document.getElementById('validationText');
        
        if (availableCash < minDownpayment) {
            validationText.textContent = `You need at least ₹${this.formatNumber(minDownpayment)} for the mandatory 20% downpayment. Current cash: ₹${this.formatNumber(availableCash)}`;
            validationMessage.style.display = 'flex';
        } else {
            validationMessage.style.display = 'none';
        }
        
        // Also validate that loan amount + your contribution equals property price
        // this.validateTotalEqualsPrice(); // Removed - no longer needed
    }

    // validateTotalEqualsPrice function removed - no longer needed since loan amount is auto-calculated

    calculateAndDisplay() {
        console.log('calculateAndDisplay called');
        // Ensure loan amount is always correct before calculations
        this.updateLoanAmount();
        
        const data = this.collectSliderData();
        console.log('Collected data:', data);
        const results = this.calculateResults(data);
        console.log('Calculated results:', results);
        this.displayResults(results);
    }

    collectSliderData() {
        const propertyPrice = parseInt(document.getElementById('propertyPrice').value);
        const yourContribution = parseInt(document.getElementById('yourContribution').value);
        
        return {
            propertyPrice: propertyPrice,
            availableCash: parseInt(document.getElementById('moneyAtHand').value),
            yourContribution: yourContribution,
            loanAmount: propertyPrice - yourContribution, // Calculate loan amount
            interestRate: parseFloat(document.getElementById('interestRate').value),
            loanTenure: parseInt(document.getElementById('loanTenure').value),
            investmentGrowth: parseFloat(document.getElementById('investmentGrowth').value),
            houseRateIncrease: parseFloat(document.getElementById('houseRateIncrease').value),
            rentPercentage: parseFloat(document.getElementById('rent').value)
        };
    }

    calculateResults(data) {
        const mainOption = this.calculateFullPayOption(data);
        const recommendation = this.generateRecommendation(data);

        return {
            mainOption,
            recommendation
        };
    }

    calculateFullPayOption(data) {
        // Cash left after home purchase = Available cash - Your contribution
        const cashLeft = data.availableCash - data.yourContribution;
        
        // Loan component = Property value - Your contribution
        const loanComponent = data.propertyPrice - data.yourContribution;
        
        // Calculate EMI for the loan component
        const monthlyRate = data.interestRate / 100 / 12;
        const totalMonths = data.loanTenure * 12;
        const emi = loanComponent > 0 ? 
            loanComponent * (monthlyRate * Math.pow(1 + monthlyRate, totalMonths)) / 
            (Math.pow(1 + monthlyRate, totalMonths) - 1) : 0;
        
        // Total Interest = EMI * 12 * Loan Tenure
        const totalInterest = emi * 12 * data.loanTenure;
        
        // Total Paid = Purchase Price + Total Interest
        const totalPaid = data.propertyPrice + totalInterest;
        
        // Debug logging for Total Paid
        console.log('=== TOTAL PAID CALCULATION DEBUG ===');
        console.log('EMI:', emi);
        console.log('Monthly Interest:', emi * 12);
        console.log('Total Interest:', totalInterest);
        console.log('Property Price:', data.propertyPrice);
        console.log('Total Paid:', totalPaid);
        console.log('=====================================');
        
        // Investment value using compound interest formula
        const investmentValue = cashLeft > 0 ? 
            cashLeft * Math.pow(1 + data.investmentGrowth / 100, data.loanTenure) : 0;

        // Rent calculations (only if giving on rent)
        const isGivingOnRent = document.getElementById('rentCheckbox').checked;
        const initialRentAmount = isGivingOnRent ? data.propertyPrice * (data.rentPercentage / 100) : 0;
        const totalRentIncome = isGivingOnRent ? initialRentAmount * ((Math.pow(1.05, data.loanTenure) - 1) / 0.05) : 0; // 5% YOY increase

        // Property appreciation using compound interest formula
        const propertyAppreciation = data.propertyPrice * Math.pow(1 + data.houseRateIncrease / 100, data.loanTenure);

        // Gain/Loss from purchasing property = Property Appreciation - Total Paid (should not include rent)
        const gainLossFromProperty = propertyAppreciation - totalPaid;
        
        // Debug logging
        console.log('=== GAIN/LOSS CALCULATION DEBUG ===');
        console.log('Property Price:', data.propertyPrice);
        console.log('House Rate Increase:', data.houseRateIncrease + '%');
        console.log('Loan Tenure:', data.loanTenure + ' years');
        console.log('Property Appreciation:', propertyAppreciation);
        console.log('Total Paid:', totalPaid);
        console.log('Gain/Loss (without rent):', gainLossFromProperty);
        console.log('=====================================');

        // Final Net Worth = Gain/Loss from Property + Rent Income + Investment Value
        const finalNetWorth = gainLossFromProperty + totalRentIncome + investmentValue;
        
        console.log('=== FINAL NET WORTH CALCULATION DEBUG ===');
        console.log('Gain/Loss from Property:', gainLossFromProperty);
        console.log('Total Rent Income:', totalRentIncome);
        console.log('Investment Value:', investmentValue);
        console.log('Final Net Worth:', finalNetWorth);
        console.log('==========================================');

        return {
            propertyPrice: data.propertyPrice,
            availableCash: data.availableCash,
            yourContribution: data.yourContribution,
            cashLeft: cashLeft,
            loanComponent: loanComponent,
            emi: emi,
            loanTenure: data.loanTenure,
            totalInterest: totalInterest,
            totalPaid: totalPaid,
            initialRentAmount: initialRentAmount,
            totalRentIncome: totalRentIncome,
            propertyAppreciation: propertyAppreciation,
            gainLossFromProperty: gainLossFromProperty,
            investmentValue: investmentValue,
            finalNetWorth: finalNetWorth
        };
    }





    generateRecommendation(data) {
        const mainOption = this.calculateFullPayOption(data);

        let recommendation = '';
        let explanation = '';

        if (mainOption.finalNetWorth > 0) {
            recommendation = 'Property investment looks favorable';
            explanation = `Your property investment strategy shows a positive net worth of ₹${this.formatNumber(mainOption.finalNetWorth)} after ${data.loanTenure} years.`;
        } else {
            recommendation = 'Consider alternative investment strategies';
            explanation = `Your current scenario shows a negative net worth of ₹${this.formatNumber(Math.abs(mainOption.finalNetWorth))} after ${data.loanTenure} years.`;
        }

        // Additional insights
        let insights = '';
        if (data.investmentGrowth > data.interestRate) {
            insights += ` Your expected investment return (${data.investmentGrowth}%) is higher than the loan interest rate (${data.interestRate}%), which helps offset loan costs.`;
        }

        if (data.houseRateIncrease > 0) {
            insights += ` With an average ${data.houseRateIncrease}% annual property appreciation, your property value will grow significantly over ${data.loanTenure} years.`;
        }

        return {
            recommendation,
            explanation,
            insights
        };
    }

    displayResults(results) {
        console.log('displayResults called with:', results);
        const resultsSection = document.getElementById('resultsSection');
        console.log('resultsSection element:', resultsSection);
        if (!resultsSection) {
            console.error('Results section not found!');
            return;
        }

        const htmlContent = this.generateResultsHTML(results);
        console.log('Generated HTML length:', htmlContent.length);
        resultsSection.innerHTML = htmlContent;
        console.log('Results displayed successfully');
    }

        generateResultsHTML(results) {
        const mainOption = results.mainOption;
        const recommendation = results.recommendation;

        return `
            <div class="results-header">
                <h3><i class="fas fa-chart-pie"></i> Property Investment Analysis</h3>
                <p>Real-time analysis of your property investment strategy</p>
            </div>

            <div class="main-results">
                <div class="results-card">
                    <h4><i class="fas fa-home"></i> Investment Details</h4>
                    <div class="metric">
                        <span class="metric-label">Property Price</span>
                        <span class="metric-value">₹${this.formatNumber(mainOption.propertyPrice)}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Available Cash</span>
                        <span class="metric-value">₹${this.formatNumber(mainOption.availableCash)}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Your Contribution</span>
                        <span class="metric-value">₹${this.formatNumber(mainOption.yourContribution)}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Cash Left</span>
                        <span class="metric-value">₹${this.formatNumber(mainOption.cashLeft)}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Loan Component</span>
                        <span class="metric-value">₹${this.formatNumber(mainOption.loanComponent)}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">EMI</span>
                        <span class="metric-value">₹${this.formatNumber(mainOption.emi)}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Loan Tenure</span>
                        <span class="metric-value">${mainOption.loanTenure} years</span>
                    </div>
                    ${mainOption.initialRentAmount > 0 ? `
                    <div class="metric">
                        <span class="metric-label">Rent Amount</span>
                        <span class="metric-value highlight">₹${this.formatNumber(mainOption.initialRentAmount)}</span>
                    </div>
                    ` : ''}
                    <div class="metric">
                        <span class="metric-label">Total Interest Paid</span>
                        <span class="metric-value warning">₹${this.formatNumber(mainOption.totalInterest)}</span>
                    </div>
                </div>

                <div class="summary-section">
                    <h4><i class="fas fa-calculator"></i> Summary after ${mainOption.loanTenure} years</h4>
                    <div class="metric">
                        <span class="metric-label">Total Paid (Loan amount + Interest)</span>
                        <span class="metric-value">₹${this.formatNumber(mainOption.totalPaid)}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Probable House Price</span>
                        <span class="metric-value highlight">₹${this.formatNumber(mainOption.propertyAppreciation)}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Gain/Loss from Purchasing Property (Home Value - Total Paid)</span>
                        <span class="metric-value ${mainOption.gainLossFromProperty >= 0 ? 'highlight' : 'warning'}">₹${this.formatNumber(mainOption.gainLossFromProperty)}</span>
                    </div>
                    ${mainOption.totalRentIncome > 0 ? `
                    <div class="metric">
                        <span class="metric-label">Rent Income (5% YOY increase)</span>
                        <span class="metric-value highlight">₹${this.formatNumber(mainOption.totalRentIncome)}</span>
                    </div>
                    ` : ''}
                    <div class="metric">
                        <span class="metric-label">Investment Value (Cash in hand)</span>
                        <span class="metric-value">₹${this.formatNumber(mainOption.investmentValue)}</span>
                    </div>
                    <div class="metric final-result">
                        <span class="metric-label">Final Net Worth (Home + Investment):</span>
                        <span class="metric-value ${mainOption.finalNetWorth >= 0 ? 'highlight' : 'warning'}">₹${this.formatNumber(mainOption.finalNetWorth)}</span>
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
                <h4><i class="fas fa-question-circle"></i> Key Insights</h4>
                <div class="what-if-grid">
                    <div class="what-if-card">
                        <h6>Investment Growth</h6>
                        <div class="value">${document.getElementById('investmentGrowth').value}%</div>
                        <small>Annual return rate</small>
                    </div>
                    <div class="what-if-card">
                        <h6>Property Appreciation</h6>
                        <div class="value">${document.getElementById('houseRateIncrease').value}%</div>
                        <small>Annual growth rate</small>
                    </div>
                    <div class="what-if-card">
                        <h6>Interest Rate</h6>
                        <div class="value">${document.getElementById('interestRate').value}%</div>
                        <small>Loan interest rate</small>
                    </div>
                </div>
            </div>
        `;
    }

    formatNumber(num) {
        if (isNaN(num) || num === null || num === undefined) return '0';
        
        // Convert to number and round to 2 decimal places
        const roundedNum = Math.round(parseFloat(num) * 100) / 100;
        
        // Handle negative numbers
        const isNegative = roundedNum < 0;
        const absNum = Math.abs(roundedNum);
        
        // Convert to lakhs and crores format with 2 decimal places
        if (absNum >= 10000000) { // 1 crore = 10,000,000
            const crores = absNum / 10000000;
            return (isNegative ? '-' : '') + crores.toFixed(2) + ' cr';
        } else if (absNum >= 100000) { // 1 lakh = 100,000
            const lakhs = absNum / 100000;
            return (isNegative ? '-' : '') + lakhs.toFixed(2) + ' lakhs';
        } else {
            // For numbers less than 1 lakh, use regular formatting with 2 decimals
            const numStr = absNum.toFixed(2);
            let formatted = '';
            const parts = numStr.split('.');
            const wholePart = parts[0];
            const decimalPart = parts[1];
            
            if (wholePart.length <= 3) {
                formatted = wholePart;
            } else {
                // Last 3 digits
                formatted = wholePart.substring(wholePart.length - 3);
                
                // Remaining digits in groups of 2 from right to left
                for (let i = wholePart.length - 3; i > 0; i -= 2) {
                    const start = Math.max(0, i - 2);
                    const group = wholePart.substring(start, i);
                    formatted = group + ',' + formatted;
                }
            }
            
            // Add decimal part
            formatted = formatted + '.' + decimalPart;
            
            return (isNegative ? '-' : '') + formatted;
        }
    }
}

// Initialize calculator when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new FullPayOrLoanCalculator();
});

// Global functions
function goBackToHome() {
    window.location.href = '../index.html';
}

function goBackToCalculators() {
    window.location.href = 'calculators.html';
}
