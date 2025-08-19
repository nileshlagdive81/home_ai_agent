// Home Affordability Calculator JavaScript

class AffordabilityCalculator {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 5;
        this.formData = {};
        this.initializeCalculator();
    }

    initializeCalculator() {
        this.bindEvents();
        this.initializeFormData();
        this.updateProgress();
        this.updateNavigationButtons();
    }

    bindEvents() {
        // Bind form input events for live updates
        this.bindFormInputs();
        
        // Bind navigation events
        document.querySelectorAll('.step').forEach(step => {
            step.addEventListener('click', (e) => {
                const stepNumber = parseInt(e.target.dataset.step);
                this.goToStep(stepNumber);
            });
        });
        
        // Bind modal close on outside click
        document.getElementById('calculatorModal').addEventListener('click', (e) => {
            if (e.target.id === 'calculatorModal') {
                this.closeCalculatorModal();
            }
        });
        
        // Bind escape key to close modal
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && document.getElementById('calculatorModal').classList.contains('show')) {
                this.closeCalculatorModal();
            }
        });
    }

    bindFormInputs() {
        // Bind all form inputs to update live results
        const inputs = document.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                this.updateFormDataFromInputs();
                this.calculateLiveResults();
            });
            input.addEventListener('change', () => {
                this.updateFormDataFromInputs();
                this.calculateLiveResults();
            });
        });
    }

    initializeFormData() {
        this.formData = {
            // Profile
            residentType: 'indian',
            employmentType: 'salaried',
            age: 30,
            city: 'mumbai',
            dependents: 0,
            loanRequired: true,
            
            // Income
            grossIncome: 0,
            netIncome: 0,
            variablePay: 0,
            otherIncome: 0,
            incomeStability: 'medium',
            
            // Obligations
            existingEMIs: 0,
            creditCardPayments: 0,
            rent: 0,
            schoolFees: 0,
            otherExpenses: 0,
            
            // Credit
            cibilScore: 'good',
            
            // Preferences
            propertyType: 'apartment',
            preferredBHK: 2,
            downPayment: 0,
            loanTenure: 20
        };
        
        this.bindFormEvents();
    }

    populateFormFields() {
        // Populate form fields with default values
        Object.keys(this.formData).forEach(key => {
            const element = document.getElementById(key);
            if (element) {
                if (element.type === 'number') {
                    element.value = this.formData[key];
                } else if (element.tagName === 'SELECT') {
                    element.value = this.formData[key];
                }
            }
        });
    }

    nextStep() {
        if (this.currentStep < this.totalSteps) {
            this.currentStep++;
            this.showCurrentStep();
            this.updateProgress();
            this.updateNavigationButtons();
        }
    }

    previousStep() {
        if (this.currentStep > 1) {
            this.currentStep--;
            this.showCurrentStep();
            this.updateProgress();
            this.updateNavigationButtons();
        }
    }

    goToStep(stepNumber) {
        if (stepNumber >= 1 && stepNumber <= this.totalSteps) {
            this.currentStep = stepNumber;
            this.showCurrentStep();
            this.updateProgress();
            this.updateNavigationButtons();
        }
    }

    showCurrentStep() {
        // Hide all sections
        document.querySelectorAll('.form-section').forEach(section => {
            section.classList.remove('active');
        });
        
        // Show current section
        const currentSection = document.getElementById(this.getSectionId(this.currentStep));
        if (currentSection) {
            currentSection.classList.add('active');
        }
        
        // Update step indicators
        document.querySelectorAll('.step').forEach((step, index) => {
            step.classList.remove('active');
            if (index + 1 === this.currentStep) {
                step.classList.add('active');
            }
        });
    }

    getSectionId(stepNumber) {
        const sections = [
            'profileSection',
            'incomeSection', 
            'obligationsSection',
            'creditSection',
            'preferencesSection'
        ];
        return sections[stepNumber - 1];
    }

    updateProgress() {
        const progressPercentage = (this.currentStep / this.totalSteps) * 100;
        document.getElementById('progressFill').style.width = progressPercentage + '%';
    }

    updateNavigationButtons() {
        // Navigation buttons are now in each section, so this method is simplified
        // The buttons are handled directly in the HTML with onclick events
    }

    updateFormDataFromInputs() {
        // Update form data from current input values
        Object.keys(this.formData).forEach(key => {
            const element = document.getElementById(key);
            if (element) {
                if (element.type === 'number') {
                    this.formData[key] = parseFloat(element.value) || 0;
                } else {
                    this.formData[key] = element.value;
                }
            }
        });
        
        // Debug: Log the updated form data
        console.log('Form data updated:', this.formData);
    }

    calculateLiveResults() {
        console.log('Calculating live results...');
        const results = this.calculateAffordability();
        console.log('Live results calculated:', results);
        this.displayLiveResults(results);
    }

    displayLiveResults(results) {
        // Update summary
        document.getElementById('maxHomePrice').textContent = `₹${this.formatNumber(results.maxHomePrice)}`;
        document.getElementById('maxLoanAmount').textContent = results.noLoanRequired ? 'No Loan Required' : `₹${this.formatNumber(results.maxLoanAmount)}`;
        document.getElementById('monthlyEMI').textContent = results.noLoanRequired ? 'No EMI' : `₹${this.formatNumber(results.monthlyEMI)}`;
        
        // Update FOIR meter
        const foirMeter = document.getElementById('foirMeter');
        const foirStatus = document.getElementById('foirStatus');
        const foirValue = document.getElementById('foirValue');
        
        if (results.noLoanRequired) {
            foirMeter.style.width = '0%';
            foirStatus.textContent = 'Not Applicable';
            foirStatus.setAttribute('data-status', 'excellent');
            foirValue.textContent = '0%';
        } else {
            const foirPercentage = Math.min(results.foir, 100);
            foirMeter.style.width = `${foirPercentage}%`;
            foirValue.textContent = `${results.foir.toFixed(1)}%`;
            
            // Set FOIR status and color
            let status, color;
            if (results.foir <= 30) {
                status = 'Excellent';
                color = 'excellent';
            } else if (results.foir <= 40) {
                status = 'Good';
                color = 'good';
            } else if (results.foir <= 50) {
                status = 'Fair';
                color = 'fair';
            } else {
                status = 'Poor';
                color = 'poor';
            }
            
            foirStatus.textContent = status;
            foirStatus.setAttribute('data-status', color);
        }
        
        // Update FOIR breakdown
        document.getElementById('monthlyIncomeDisplay').textContent = this.formatNumber(results.monthlyIncome);
        document.getElementById('monthlyObligationsDisplay').textContent = this.formatNumber(results.monthlyObligations);
        
        // Update readiness meter
        const readinessScore = this.calculateReadinessScore(results);
        const readinessMeter = document.getElementById('readinessMeter');
        const readinessStatus = document.getElementById('readinessStatus');
        const readinessValue = document.getElementById('readinessValue');
        
        readinessMeter.style.width = `${readinessScore}%`;
        readinessValue.textContent = `${readinessScore}%`;
        
        if (readinessScore >= 80) {
            readinessStatus.textContent = 'Excellent';
            readinessStatus.style.color = '#10b981';
        } else if (readinessScore >= 60) {
            readinessStatus.textContent = 'Good';
            readinessStatus.style.color = '#10b981';
        } else if (readinessScore >= 40) {
            readinessStatus.textContent = 'Fair';
            readinessStatus.style.color = '#fbbf24';
        } else {
            readinessStatus.textContent = 'Poor';
            readinessStatus.style.color = '#ef4444';
        }
        
        // Update advice
        this.updateAdvice(results, readinessScore);
        
        // Show detailed breakdown
        this.showDetailedBreakdown(results);
    }

    calculateAffordability() {
        // Calculate total monthly income
        const monthlyIncome = this.formData.netIncome + (this.formData.variablePay / 12) + this.formData.otherIncome;
        
        // Calculate total monthly obligations
        const monthlyObligations = this.formData.existingEMIs + this.formData.creditCardPayments + 
                                  this.formData.rent + (this.formData.schoolFees / 12) + this.formData.otherExpenses;
        
        // If no loan required, affordability is just down payment
        if (!this.formData.loanRequired) {
            return {
                maxHomePrice: this.formData.downPayment,
                maxLoanAmount: 0,
                monthlyEMI: 0,
                foir: 0,
                interestRate: 0,
                downPayment: this.formData.downPayment,
                stampDuty: 0,
                registrationCharges: 0,
                documentHandling: 0,
                otherExpenses: 0,
                totalAdditionalExpenses: 0,
                basePrice: this.formData.downPayment,
                monthlyIncome: Math.round(monthlyIncome),
                monthlyObligations: Math.round(monthlyObligations),
                noLoanRequired: true
            };
        }
        
        // Calculate FOIR (Fixed Obligations to Income Ratio)
        const foir = monthlyIncome > 0 ? (monthlyObligations / monthlyIncome) * 100 : 0;
        
        // Determine interest rate based on CIBIL score
        let interestRate = 8.5; // Base rate
        switch(this.formData.cibilScore) {
            case 'excellent': interestRate = 7.5; break;
            case 'good': interestRate = 8.5; break;
            case 'fair': interestRate = 9.5; break;
            case 'poor': interestRate = 11.0; break;
        }
        
        // Calculate maximum EMI (50% of net income - existing obligations)
        const maxEMI = Math.max(0, (monthlyIncome * 0.5) - monthlyObligations);
        
        // Calculate loan tenure in months
        const tenureMonths = this.formData.loanTenure * 12;
        
        // Calculate maximum loan amount using EMI formula
        const monthlyRate = interestRate / 12 / 100;
        const maxLoanAmount = maxEMI * ((Math.pow(1 + monthlyRate, tenureMonths) - 1) / 
                                       (monthlyRate * Math.pow(1 + monthlyRate, tenureMonths)));
        
        // Calculate additional expenses
        const basePrice = maxLoanAmount + this.formData.downPayment;
        const stampDuty = basePrice * 0.05; // 5% stamp duty
        const registrationCharges = basePrice * 0.01; // 1% registration
        const documentHandling = basePrice * 0.01; // 1% document handling
        const otherExpenses = basePrice * 0.02; // 2% for other expenses (GST, etc.)
        
        const totalAdditionalExpenses = stampDuty + registrationCharges + documentHandling + otherExpenses;
        
        // Final affordability = loan + down payment - additional expenses
        const maxHomePrice = basePrice - totalAdditionalExpenses;
        
        return {
            maxHomePrice: Math.round(maxHomePrice),
            maxLoanAmount: Math.round(maxLoanAmount),
            monthlyEMI: Math.round(maxEMI),
            foir: foir,
            interestRate: interestRate,
            downPayment: this.formData.downPayment,
            stampDuty: Math.round(stampDuty),
            registrationCharges: Math.round(registrationCharges),
            documentHandling: Math.round(documentHandling),
            otherExpenses: Math.round(otherExpenses),
            totalAdditionalExpenses: Math.round(totalAdditionalExpenses),
            basePrice: Math.round(basePrice),
            monthlyIncome: Math.round(monthlyIncome),
            monthlyObligations: Math.round(monthlyObligations),
            noLoanRequired: false
        };
    }

    getInterestRate() {
        // Base interest rates based on CIBIL score
        const baseRates = {
            'excellent': 8.5,
            'good': 9.0,
            'fair': 9.5,
            'poor': 10.5
        };
        
        let rate = baseRates[this.formData.cibilScore] || 9.0;
        
        // Adjustments based on employment type
        if (this.formData.employmentType === 'self-employed') rate += 0.5;
        if (this.formData.employmentType === 'business') rate += 0.75;
        
        // Adjustments based on income stability
        if (this.formData.incomeStability === 'low') rate += 0.5;
        if (this.formData.incomeStability === 'high') rate -= 0.25;
        
        return rate;
    }

    calculateReadinessScore(results) {
        let score = 0;
        
        // Income stability (25 points)
        if (this.formData.incomeStability === 'high') score += 25;
        else if (this.formData.incomeStability === 'medium') score += 15;
        else score += 5;
        
        // CIBIL score (25 points)
        if (this.formData.cibilScore === 'excellent') score += 25;
        else if (this.formData.cibilScore === 'good') score += 20;
        else if (this.formData.cibilScore === 'fair') score += 10;
        else score += 5;
        
        // Down payment (25 points)
        const downPaymentPercentage = results.maxHomePrice > 0 ? 
            this.formData.downPayment / results.maxHomePrice : 0;
        if (downPaymentPercentage >= 0.2) score += 25;
        else if (downPaymentPercentage >= 0.15) score += 20;
        else if (downPaymentPercentage >= 0.10) score += 15;
        else score += 10;
        
        // Age factor (25 points) - Better age range for home buying
        if (this.formData.age >= 28 && this.formData.age <= 45) score += 25; // Prime age for home buying
        else if (this.formData.age >= 25 && this.formData.age <= 50) score += 20; // Good age range
        else if (this.formData.age >= 22 && this.formData.age <= 55) score += 15; // Acceptable range
        else score += 10; // Too young or too old
        
        return Math.min(score, 100);
    }

    getFOIRStatus(foir) {
        if (foir <= 0.3) return 'Excellent';
        if (foir <= 0.4) return 'Good';
        if (foir <= 0.5) return 'Fair';
        return 'Poor';
    }

    getReadinessStatus(score) {
        if (score >= 80) return 'Excellent';
        if (score >= 60) return 'Good';
        if (score >= 40) return 'Fair';
        return 'Needs Improvement';
    }

    updateAdvice(results, readinessScore) {
        const adviceContainer = document.getElementById('adviceContainer');
        let adviceHTML = '';
        
        if (results.noLoanRequired) {
            adviceHTML = `
                <div class="advice-item success">
                    <i class="fas fa-check-circle"></i>
                    <strong>Cash Purchase Advantage:</strong> You can purchase a home without taking on debt, which eliminates EMI burden and interest costs.
                </div>
                <div class="advice-item info">
                    <i class="fas fa-info-circle"></i>
                    <strong>Consider:</strong> You might be able to afford a larger home if you're open to taking a small loan for the difference.
                </div>
            `;
        } else {
            // FOIR-based advice
            if (results.foir <= 30) {
                adviceHTML += `
                    <div class="advice-item success">
                        <i class="fas fa-check-circle"></i>
                        <strong>Excellent FOIR:</strong> Your debt-to-income ratio is very healthy. You're in a great position for loan approval.
                    </div>
                `;
            } else if (results.foir <= 40) {
                adviceHTML += `
                    <div class="advice-item success">
                        <i class="fas fa-check-circle"></i>
                        <strong>Good FOIR:</strong> Your debt-to-income ratio is within acceptable limits. Loan approval chances are high.
                    </div>
                `;
            } else if (results.foir <= 50) {
                adviceHTML += `
                    <div class="advice-item warning">
                        <i class="fas fa-exclamation-triangle"></i>
                        <strong>Fair FOIR:</strong> Your debt-to-income ratio is approaching the limit. Consider reducing existing obligations.
                    </div>
                `;
            } else {
                adviceHTML += `
                    <div class="advice-item warning">
                        <i class="fas fa-exclamation-triangle"></i>
                        <strong>High FOIR:</strong> Your debt-to-income ratio is too high. Focus on reducing existing debt before applying.
                    </div>
                `;
            }
            
            // Loan amount advice
            if (results.maxLoanAmount > 0) {
                adviceHTML += `
                    <div class="advice-item info">
                        <i class="fas fa-info-circle"></i>
                        <strong>Loan Amount:</strong> You can qualify for a loan of ₹${this.formatNumber(results.maxLoanAmount)} based on your income and obligations.
                    </div>
                `;
            } else {
                adviceHTML += `
                    <div class="advice-item warning">
                        <i class="fas fa-exclamation-triangle"></i>
                        <strong>Loan Qualification:</strong> Your current obligations are too high relative to your income. Consider reducing debt first.
                    </div>
                `;
            }
        }
        
        // Readiness score advice
        if (readinessScore >= 80) {
            adviceHTML += `
                <div class="advice-item success">
                    <i class="fas fa-star"></i>
                    <strong>Excellent Readiness:</strong> You're in an excellent position to buy a home. All factors are favorable.
                </div>
            `;
        } else if (readinessScore >= 60) {
            adviceHTML += `
                <div class="advice-item success">
                    <i class="fas fa-thumbs-up"></i>
                    <strong>Good Readiness:</strong> You're well-positioned to buy a home. Minor improvements could boost your score further.
                </div>
            `;
        } else if (readinessScore >= 40) {
            adviceHTML += `
                <div class="advice-item warning">
                    <i class="fas fa-exclamation-triangle"></i>
                    <strong>Fair Readiness:</strong> You have some areas to improve before buying. Focus on building savings and improving credit.
                </div>
            `;
        } else {
            adviceHTML += `
                <div class="advice-item warning">
                    <i class="fas fa-exclamation-triangle"></i>
                    <strong>Low Readiness:</strong> Consider waiting to improve your financial position before buying a home.
                </div>
            `;
        }
        
        adviceContainer.innerHTML = adviceHTML;
    }

    getAdviceIcon(type) {
        const icons = {
            'success': 'fa-check-circle',
            'warning': 'fa-exclamation-triangle',
            'info': 'fa-info-circle'
        };
        return icons[type] || 'fa-info-circle';
    }

    calculateFinalResults() {
        const results = this.calculateAffordability();
        
        // Close the modal
        this.closeCalculatorModal();
        
        // Show results section
        document.getElementById('resultsSection').style.display = 'block';
        
        // Update all results displays
        this.displayLiveResults(results);
        
        // Show detailed breakdown in right panel
        this.showDetailedBreakdown(results);
        
        // Scroll to results
        document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
    }

    openCalculatorModal() {
        document.getElementById('calculatorModal').classList.add('show');
        document.body.style.overflow = 'hidden';
    }

    closeCalculatorModal() {
        document.getElementById('calculatorModal').classList.remove('show');
        document.body.style.overflow = 'auto';
    }

    resetCalculator() {
        // Reset form data
        this.initializeFormData();
        
        // Hide results section
        document.getElementById('resultsSection').style.display = 'none';
        
        // Reset progress
        this.currentStep = 1;
        this.updateProgress();
        this.showCurrentStep();
        
        // Open modal again
        this.openCalculatorModal();
    }

    showDetailedBreakdown(results) {
        let breakdownSection = document.getElementById('calculationDetails');
        
        if (results.noLoanRequired) {
            breakdownSection.innerHTML = `
                <div class="breakdown-card">
                    <h4><i class="fas fa-home"></i> Cash Purchase Breakdown</h4>
                    
                    <div class="breakdown-section">
                        <h5>Purchase Details</h5>
                        <div class="breakdown-item">
                            <span>Available Cash:</span>
                            <strong>₹${this.formatNumber(results.downPayment)}</strong>
                        </div>
                        <div class="breakdown-item">
                            <span>Maximum Home Price:</span>
                            <strong>₹${this.formatNumber(results.maxHomePrice)}</strong>
                        </div>
                    </div>
                    
                    <div class="breakdown-section">
                        <h5>Income & Expenses</h5>
                        <div class="breakdown-item">
                            <span>Monthly Income:</span>
                            <strong>₹${this.formatNumber(results.monthlyIncome)}</strong>
                        </div>
                        <div class="breakdown-item">
                            <span>Monthly Obligations:</span>
                            <strong>₹${this.formatNumber(results.monthlyObligations)}</strong>
                        </div>
                    </div>
                    
                    <div class="breakdown-section final-result">
                        <h5>Cash Purchase Summary</h5>
                        <div class="breakdown-item highlight">
                            <span>You can purchase a home worth:</span>
                            <strong>₹${this.formatNumber(results.maxHomePrice)}</strong>
                        </div>
                        <p style="color: #9ca3af; font-size: 14px; margin-top: 1rem;">
                            Since no loan is required, your affordability is limited to your available cash amount.
                        </p>
                    </div>
                </div>
            `;
            return;
        }
        
        breakdownSection.innerHTML = `
            <div class="breakdown-card">
                <h4><i class="fas fa-calculator"></i> Calculation Breakdown</h4>
                
                <div class="breakdown-section">
                    <h5>Interest Rate & Loan Details</h5>
                    <div class="breakdown-item">
                        <span>Annual Interest Rate:</span>
                        <strong>${results.interestRate}%</strong>
                    </div>
                    <div class="breakdown-item">
                        <span>Loan Tenure:</span>
                        <strong>${this.formData.loanTenure} Years</strong>
                    </div>
                    <div class="breakdown-item">
                        <span>Maximum Loan Amount:</span>
                        <strong>₹${this.formatNumber(results.maxLoanAmount)}</strong>
                    </div>
                    <div class="breakdown-item">
                        <span>Monthly EMI:</span>
                        <strong>₹${this.formatNumber(results.monthlyEMI)}</strong>
                    </div>
                </div>
                
                <div class="breakdown-section">
                    <h5>Down Payment & Base Price</h5>
                    <div class="breakdown-item">
                        <span>Your Down Payment:</span>
                        <strong>₹${this.formatNumber(results.downPayment)}</strong>
                    </div>
                    <div class="breakdown-item">
                        <span>Base Price (Loan + Down Payment):</span>
                        <strong>₹${this.formatNumber(results.basePrice)}</strong>
                    </div>
                </div>
                
                <div class="breakdown-section">
                    <h5>Additional Expenses</h5>
                    <div class="breakdown-item">
                        <span>Stamp Duty (5%):</span>
                        <strong>₹${this.formatNumber(results.stampDuty)}</strong>
                    </div>
                    <div class="breakdown-item">
                        <span>Registration Charges (1%):</span>
                        <strong>₹${this.formatNumber(results.registrationCharges)}</strong>
                    </div>
                    <div class="breakdown-item">
                        <span>Document Handling (1%):</span>
                        <strong>₹${this.formatNumber(results.documentHandling)}</strong>
                    </div>
                    <div class="breakdown-item">
                        <span>Other Expenses (2%):</span>
                        <strong>₹${this.formatNumber(results.otherExpenses)}</strong>
                    </div>
                    <div class="breakdown-item total-expenses">
                        <span>Total Additional Expenses:</span>
                        <strong>₹${this.formatNumber(results.totalAdditionalExpenses)}</strong>
                    </div>
                </div>
                
                <div class="breakdown-section final-result">
                    <h5>Final Affordability</h5>
                    <div class="breakdown-item highlight">
                        <span>Maximum Home Price:</span>
                        <strong>₹${this.formatNumber(results.maxHomePrice)}</strong>
                    </div>
                </div>
            </div>
        `;
    }

    openPropertySearch() {
        // Generate property search links for external portals
        const city = this.formData.city;
        const budget = this.formData.maxHomePrice;
        const bhk = this.formData.preferredBHK;
        
        const searchLinks = this.generatePropertySearchLinks(city, budget, bhk);
        this.showPropertySearchModal(searchLinks);
    }

    generatePropertySearchLinks(city, budget, bhk) {
        const budgetInLakhs = Math.round(budget / 100000);
        const cityName = city.charAt(0).toUpperCase() + city.slice(1);
        
        return {
            '99acres': `https://www.99acres.com/property-in-${city}-${bhk}-bhk-residential-for-sale-${budgetInLakhs}lac-${budgetInLakhs + 10}lac`,
            'magicbricks': `https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=${bhk}&proptype=Multistorey-Apartment&cityName=${cityName}&budget=${budgetInLakhs}L-${budgetInLakhs + 10}L`,
            'nobroker': `https://www.nobroker.in/property-for-sale-${city}/${bhk}-bhk-apartment-for-sale`
        };
    }

    showPropertySearchModal(searchLinks) {
        // Create and show modal with property search links
        const modal = document.createElement('div');
        modal.className = 'property-search-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <h3>Search Properties on</h3>
                <div class="search-links">
                    <a href="${searchLinks['99acres']}" target="_blank" class="search-link">
                        <i class="fas fa-external-link-alt"></i> 99acres
                    </a>
                    <a href="${searchLinks['magicbricks']}" target="_blank" class="search-link">
                        <i class="fas fa-external-link-alt"></i> Magicbricks
                    </a>
                    <a href="${searchLinks['nobroker']}" target="_blank" class="search-link">
                        <i class="fas fa-external-link-alt"></i> NoBroker
                    </a>
                </div>
                <button onclick="this.parentElement.parentElement.remove()" class="btn btn-primary">Close</button>
            </div>
        `;
        
        document.body.appendChild(modal);
    }

    formatNumber(num) {
        if (num >= 10000000) {
            return (num / 10000000).toFixed(1) + ' Cr';
        } else if (num >= 100000) {
            return (num / 100000).toFixed(1) + ' L';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(1) + ' K';
        }
        return num.toString();
    }

    bindFormEvents() {
        // Profile
        document.getElementById('residentType').addEventListener('change', (e) => {
            this.formData.residentType = e.target.value;
        });
        
        document.getElementById('employmentType').addEventListener('change', (e) => {
            this.formData.employmentType = e.target.value;
        });
        
        document.getElementById('age').addEventListener('input', (e) => {
            this.formData.age = parseInt(e.target.value) || 0;
        });
        
        document.getElementById('city').addEventListener('change', (e) => {
            this.formData.city = e.target.value;
        });
        
        document.getElementById('dependents').addEventListener('input', (e) => {
            this.formData.dependents = parseInt(e.target.value) || 0;
        });
        
        document.getElementById('loanRequired').addEventListener('change', (e) => {
            this.formData.loanRequired = e.target.checked;
            this.updateLoanFieldsVisibility();
        });
        
        // Income
        document.getElementById('grossIncome').addEventListener('input', (e) => {
            this.formData.grossIncome = parseInt(e.target.value) || 0;
            this.updateLiveResults();
        });
        
        document.getElementById('netIncome').addEventListener('input', (e) => {
            this.formData.netIncome = parseInt(e.target.value) || 0;
            this.updateLiveResults();
        });
        
        document.getElementById('variablePay').addEventListener('input', (e) => {
            this.formData.variablePay = parseInt(e.target.value) || 0;
            this.updateLiveResults();
        });
        
        document.getElementById('otherIncome').addEventListener('input', (e) => {
            this.formData.otherIncome = parseInt(e.target.value) || 0;
            this.updateLiveResults();
        });
        
        document.getElementById('incomeStability').addEventListener('change', (e) => {
            this.formData.incomeStability = e.target.value;
        });
        
        // Obligations
        document.getElementById('existingEMIs').addEventListener('input', (e) => {
            this.formData.existingEMIs = parseInt(e.target.value) || 0;
            this.updateLiveResults();
        });
        
        document.getElementById('creditCardPayments').addEventListener('input', (e) => {
            this.formData.creditCardPayments = parseInt(e.target.value) || 0;
            this.updateLiveResults();
        });
        
        document.getElementById('rent').addEventListener('input', (e) => {
            this.formData.rent = parseInt(e.target.value) || 0;
            this.updateLiveResults();
        });
        
        document.getElementById('schoolFees').addEventListener('input', (e) => {
            this.formData.schoolFees = parseInt(e.target.value) || 0;
            this.updateLiveResults();
        });
        
        document.getElementById('otherExpenses').addEventListener('input', (e) => {
            this.formData.otherExpenses = parseInt(e.target.value) || 0;
            this.updateLiveResults();
        });
        
        // Credit
        document.getElementById('cibilScore').addEventListener('change', (e) => {
            this.formData.cibilScore = e.target.value;
        });
        
        // Preferences
        document.getElementById('propertyType').addEventListener('change', (e) => {
            this.formData.propertyType = e.target.value;
        });
        
        document.getElementById('preferredBHK').addEventListener('change', (e) => {
            this.formData.preferredBHK = parseInt(e.target.value) || 2;
        });
        
        document.getElementById('downPayment').addEventListener('input', (e) => {
            this.formData.downPayment = parseInt(e.target.value) || 0;
            this.updateLiveResults();
        });
        
        document.getElementById('loanTenure').addEventListener('change', (e) => {
            this.formData.loanTenure = parseInt(e.target.value) || 20;
        });
        
        this.populateFormFields();
    }
    
    updateLoanFieldsVisibility() {
        const loanFields = document.querySelectorAll('.loan-dependent-field');
        const isLoanRequired = this.formData.loanRequired;
        
        loanFields.forEach(field => {
            if (isLoanRequired) {
                field.style.display = 'block';
            } else {
                field.style.display = 'none';
            }
        });
    }
}

// Initialize calculator when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.calculator = new AffordabilityCalculator();
});

// Global functions for button clicks
function nextStep() {
    if (window.calculator) {
        window.calculator.nextStep();
    }
}

function previousStep() {
    if (window.calculator) {
        window.calculator.previousStep();
    }
}

function calculateAffordability() {
    if (window.calculator) {
        window.calculator.calculateFinalResults();
    }
}

function openPropertySearch() {
    if (window.calculator) {
        window.calculator.openPropertySearch();
    }
}

function openCalculatorModal() {
    if (window.calculator) {
        window.calculator.openCalculatorModal();
    }
}

function closeCalculatorModal() {
    if (window.calculator) {
        window.calculator.closeCalculatorModal();
    }
}

function resetCalculator() {
    if (window.calculator) {
        window.calculator.resetCalculator();
    }
}
