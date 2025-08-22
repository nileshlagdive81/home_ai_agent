/**
 * Reusable Chat Component JavaScript
 * This file provides consistent chat functionality across all pages
 * Includes property search and navigation to search results
 */

class ChatComponent {
    constructor() {
        this.initializeChat();
        this.setupEventListeners();
        this.setupPopupEventListeners();
    }

    initializeChat() {
        // Auto-resize textarea
        const chatInput = document.getElementById('chatInput');
        if (chatInput) {
            chatInput.addEventListener('input', () => {
                chatInput.style.height = 'auto';
                chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + 'px';
            });

            // Handle Enter key
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.handleSendMessage();
                }
            });
        }
    }

    setupEventListeners() {
        const sendBtn = document.getElementById('sendBtn');
        if (sendBtn) {
            sendBtn.addEventListener('click', () => {
                this.handleSendMessage();
            });
        }
    }

    setupPopupEventListeners() {
        const popupClose = document.getElementById('popupClose');
        const backToChatBtn = document.getElementById('backToChatBtn');
        const popup = document.getElementById('queryPopup');

        if (popupClose) {
            popupClose.addEventListener('click', () => {
                this.hidePopup();
            });
        }

        if (backToChatBtn) {
            backToChatBtn.addEventListener('click', () => {
                this.hidePopup();
            });
        }

        // Close popup when clicking outside
        if (popup) {
            popup.addEventListener('click', (e) => {
                if (e.target === popup) {
                    this.hidePopup();
                }
            });
        }

        // Close popup with Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isPopupVisible()) {
                this.hidePopup();
            }
        });
    }

    async handleSendMessage() {
        const chatInput = document.getElementById('chatInput');
        if (!chatInput) return;

        const message = chatInput.value.trim();
        if (!message) return;

        // Clear input
        chatInput.value = '';
        chatInput.style.height = 'auto';

        // Add user message to chat
        this.addMessageToChat(message, 'user');

        // Show typing indicator
        this.showTypingIndicator();

        try {
            // Process the message and get response
            const response = await this.processMessage(message);
            
            // Hide typing indicator
            this.hideTypingIndicator();
            
            // Add AI response to chat
            this.addMessageToChat(response, 'assistant');

            // Show non-property queries in popup (property searches are handled by searchProperties function)
            if (!this.isPropertySearchQuery(message)) {
                this.showQueryPopup(message, response);
            }

        } catch (error) {
            console.error('Error processing message:', error);
            this.hideTypingIndicator();
            this.addMessageToChat('Sorry, I encountered an error. Please try again.', 'assistant');
        }
    }

    addMessageToChat(message, sender) {
        const aiAssistant = document.querySelector('.ai-assistant');
        if (!aiAssistant) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = sender === 'user' ? 'user-message' : 'assistant-message';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        if (sender === 'user') {
            messageContent.textContent = message;
        } else {
            // Parse markdown-like content for AI responses
            messageContent.innerHTML = this.parseResponse(message);
        }
        
        messageDiv.appendChild(messageContent);
        aiAssistant.appendChild(messageDiv);
        
        // Scroll to bottom
        aiAssistant.scrollTop = aiAssistant.scrollHeight;
    }

    parseResponse(response) {
        // Simple markdown parsing for AI responses
        return response
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
    }

    showTypingIndicator() {
        const aiAssistant = document.querySelector('.ai-assistant');
        if (!aiAssistant) return;

        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = `
            <span>AI is typing</span>
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        
        aiAssistant.appendChild(typingDiv);
        aiAssistant.scrollTop = aiAssistant.scrollHeight;
    }

    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    async processMessage(message) {
        // Check if it's a property search query
        if (this.isPropertySearchQuery(message)) {
            return this.generatePropertySearchResponse(message);
        }

        // Check if it's a calculator-related query
        if (this.isCalculatorQuery(message)) {
            return this.generateCalculatorResponse(message);
        }

        // Default response for other queries
        return this.generateDefaultResponse(message);
    }

    isPropertySearchQuery(message) {
        const propertyKeywords = [
            'bhk', 'apartment', 'house', 'property', 'flat', 'villa', 'pune', 'mumbai', 'bangalore',
            'delhi', 'chennai', 'hyderabad', 'kolkata', 'ahmedabad', 'price', 'cost', 'area',
            'sq ft', 'sqft', 'square feet', 'bedroom', 'bedrooms', 'location', 'locality'
        ];
        
        const lowerMessage = message.toLowerCase();
        return propertyKeywords.some(keyword => lowerMessage.includes(keyword));
    }

    isCalculatorQuery(message) {
        const calculatorKeywords = [
            'calculate', 'emi', 'loan', 'affordability', 'roi', 'investment', 'mortgage',
            'down payment', 'interest rate', 'tenure', 'monthly payment'
        ];
        
        const lowerMessage = message.toLowerCase();
        return calculatorKeywords.some(keyword => lowerMessage.includes(keyword));
    }

    generatePropertySearchResponse(message) {
        // Call the existing searchProperties function on the home page
        if (typeof searchProperties === 'function') {
            searchProperties(message);
            return `Searching for "${message}"...`;
        } else {
            // Fallback if not on home page
            return `I understand you're looking for properties. Please use the search on our home page to find "${message}".`;
        }
    }

    generateCalculatorResponse(message) {
        return `I can help you with calculations! You can use our calculators to find EMI, affordability, ROI, and more. Would you like me to show you the calculators page?`;
    }

    generateDefaultResponse(message) {
        // Enhanced responses for common non-property queries
        const lowerMessage = message.toLowerCase();
        
        if (lowerMessage.includes('rental yield') || lowerMessage.includes('rent yield')) {
            return this.generateRentalYieldResponse(message);
        } else if (lowerMessage.includes('rera') || lowerMessage.includes('real estate regulation')) {
            return this.generateReraResponse(message);
        } else if (lowerMessage.includes('emi') || lowerMessage.includes('loan calculation')) {
            return this.generateEmiResponse(message);
        } else if (lowerMessage.includes('affordability') || lowerMessage.includes('how much can i afford')) {
            return this.generateAffordabilityResponse(message);
        } else if (lowerMessage.includes('roi') || lowerMessage.includes('return on investment')) {
            return this.generateRoiResponse(message);
        } else {
            return `Thank you for your question about "${message}". I'm here to help with real estate queries, property searches, and financial calculations. Feel free to ask me anything specific about properties, loans, or real estate in general.`;
        }
    }

    generateRentalYieldResponse(message) {
        return {
            title: "Rental Yield Information",
            content: `
                <h3>🏠 Rental Yield in Pune, Karve Nagar</h3>
                <p><strong>Current Average Rental Yield:</strong> 3.5% - 4.2% annually</p>
                
                <h3>📊 What is Rental Yield?</h3>
                <p>Rental yield is the annual rental income as a percentage of the property's current market value.</p>
                
                <h3>💰 Calculation Example:</h3>
                <ul>
                    <li>Property Value: ₹1 Crore</li>
                    <li>Monthly Rent: ₹35,000</li>
                    <li>Annual Rent: ₹4,20,000</li>
                    <li>Rental Yield: 4.2%</li>
                </ul>
                
                <h3>📍 Karve Nagar Specifics:</h3>
                <ul>
                    <li><strong>1 BHK:</strong> ₹15,000 - ₹25,000/month (3.2% - 3.8% yield)</li>
                    <li><strong>2 BHK:</strong> ₹25,000 - ₹40,000/month (3.5% - 4.2% yield)</li>
                    <li><strong>3 BHK:</strong> ₹40,000 - ₹60,000/month (3.8% - 4.5% yield)</li>
                </ul>
                
                <h3>💡 Factors Affecting Rental Yield:</h3>
                <ul>
                    <li>Property age and condition</li>
                    <li>Location and connectivity</li>
                    <li>Nearby amenities and infrastructure</li>
                    <li>Market demand and supply</li>
                    <li>Property type (apartment, villa, etc.)</li>
                </ul>
                
                <p><em>Note: These are approximate values. For accurate current rates, please consult with local real estate agents or check recent rental agreements in the area.</em></p>
            `
        };
    }

    generateReraResponse(message) {
        return {
            title: "RERA Information",
            content: `
                <h3>🏛️ Real Estate (Regulation and Development) Act, 2016</h3>
                <p>RERA is a comprehensive law that regulates the real estate sector and protects homebuyers' interests.</p>
                
                <h3>🛡️ Key Protections for Homebuyers:</h3>
                <ul>
                    <li><strong>Project Registration:</strong> All projects must be registered with RERA</li>
                    <li><strong>Transparency:</strong> Developers must disclose project details and timelines</li>
                    <li><strong>Escrow Account:</strong> 70% of payments must be kept in escrow</li>
                    <li><strong>Compensation:</strong> Penalties for delays and false promises</li>
                </ul>
                
                <h3>📋 What to Check Before Buying:</h3>
                <ul>
                    <li>RERA registration number</li>
                    <li>Project completion timeline</li>
                    <li>Land ownership and approvals</li>
                    <li>Construction quality standards</li>
                </ul>
            `
        };
    }

    generateEmiResponse(message) {
        return {
            title: "EMI Calculation Guide",
            content: `
                <h3>💰 Understanding EMI (Equated Monthly Installment)</h3>
                <p>EMI is the fixed monthly payment you make to repay your home loan.</p>
                
                <h3>🧮 EMI Formula:</h3>
                <p><strong>EMI = P × r × (1 + r)^n / ((1 + r)^n - 1)</strong></p>
                <ul>
                    <li><strong>P:</strong> Principal amount (loan amount)</li>
                    <li><strong>r:</strong> Monthly interest rate (annual rate ÷ 12)</li>
                    <li><strong>n:</strong> Total number of months</li>
                </ul>
                
                <h3>📊 Example Calculation:</h3>
                <ul>
                    <li>Loan Amount: ₹50 Lakhs</li>
                    <li>Interest Rate: 8.5% per annum</li>
                    <li>Loan Tenure: 20 years (240 months)</li>
                    <li>Monthly EMI: ₹43,391</li>
                </ul>
                
                <h3>💡 Tips to Reduce EMI:</h3>
                <ul>
                    <li>Increase down payment</li>
                    <li>Choose longer tenure</li>
                    <li>Compare interest rates</li>
                    <li>Consider prepayment options</li>
                </ul>
            `
        };
    }

    generateAffordabilityResponse(message) {
        return {
            title: "Home Affordability Guide",
            content: `
                <h3>🏠 How Much Home Can You Afford?</h3>
                <p>Your home affordability depends on your income, expenses, and financial situation.</p>
                
                <h3>📊 General Guidelines:</h3>
                <ul>
                    <li><strong>Monthly EMI:</strong> Should not exceed 40-50% of your monthly income</li>
                    <li><strong>Down Payment:</strong> Typically 20-30% of property value</li>
                    <li><strong>Total Debt:</strong> Should not exceed 60% of your income</li>
                </ul>
                
                <h3>💰 Affordability Calculator:</h3>
                <p>Use our <strong>Home Affordability Calculator</strong> to get a precise estimate based on your:</p>
                <ul>
                    <li>Monthly income</li>
                    <li>Existing expenses</li>
                    <li>Down payment amount</li>
                    <li>Preferred loan tenure</li>
                    <li>Current interest rates</li>
                </ul>
                
                <h3>💡 Smart Tips:</h3>
                <ul>
                    <li>Keep emergency funds (6-12 months of expenses)</li>
                    <li>Consider additional costs (maintenance, taxes, insurance)</li>
                    <li>Factor in future income growth</li>
                    <li>Don't stretch beyond your comfort zone</li>
                </ul>
            `
        };
    }

    generateRoiResponse(message) {
        return {
            title: "ROI in Real Estate",
            content: `
                <h3>📈 Return on Investment (ROI) in Real Estate</h3>
                <p>ROI measures the profitability of your real estate investment.</p>
                
                <h3>🧮 ROI Calculation:</h3>
                <p><strong>ROI = ((Current Value - Purchase Price) + Rental Income) / Purchase Price × 100</strong></p>
                
                <h3>💰 Example Calculation:</h3>
                <ul>
                    <li>Purchase Price: ₹1 Crore</li>
                    <li>Current Value: ₹1.2 Crores</li>
                    <li>Rental Income (5 years): ₹20 Lakhs</li>
                    <li>ROI: 40% over 5 years</li>
                    <li>Annual ROI: 8%</li>
                </ul>
                
                <h3>📊 Factors Affecting ROI:</h3>
                <ul>
                    <li><strong>Location:</strong> Prime areas typically have higher appreciation</li>
                    <li><strong>Infrastructure:</strong> Metro, highways, malls boost value</li>
                    <li><strong>Economic Growth:</strong> City development affects property prices</li>
                    <li><strong>Property Type:</strong> Apartments vs villas have different ROI patterns</li>
                </ul>
                
                <h3>💡 Investment Strategies:</h3>
                <ul>
                    <li>Long-term holding (5-10 years minimum)</li>
                    <li>Rental income to cover EMI</li>
                    <li>Diversify across different locations</li>
                    <li>Regular property maintenance</li>
                </ul>
            `
        };
    }



    showQueryPopup(query, response) {
        const popup = document.getElementById('queryPopup');
        const popupTitle = document.getElementById('popupTitle');
        const popupBody = document.getElementById('popupBody');

        if (!popup || !popupTitle || !popupBody) return;

        // Check if response is an object with title and content
        if (typeof response === 'object' && response.title && response.content) {
            popupTitle.textContent = response.title;
            popupBody.innerHTML = response.content;
        } else {
            // Handle string responses
            popupTitle.textContent = "Query Response";
            popupBody.innerHTML = `<p>${response}</p>`;
        }

        // Show popup with animation
        popup.classList.add('show');
        
        // Prevent body scroll when popup is open
        document.body.style.overflow = 'hidden';
    }

    hidePopup() {
        const popup = document.getElementById('queryPopup');
        if (popup) {
            popup.classList.remove('show');
            // Restore body scroll
            document.body.style.overflow = 'auto';
        }
    }

    isPopupVisible() {
        const popup = document.getElementById('queryPopup');
        return popup && popup.classList.contains('show');
    }

    // Method to set placeholder text dynamically
    setPlaceholder(placeholder) {
        const chatInput = document.getElementById('chatInput');
        if (chatInput) {
            chatInput.placeholder = placeholder;
        }
    }

    // Method to clear chat history
    clearChat() {
        const aiAssistant = document.querySelector('.ai-assistant');
        if (!aiAssistant) return;

        // Keep the initial message
        const initialMessage = aiAssistant.querySelector('.assistant-message');
        aiAssistant.innerHTML = '';
        if (initialMessage) {
            aiAssistant.appendChild(initialMessage);
        }
    }
}

// Initialize chat component when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatComponent();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ChatComponent;
}
