/**
 * Reusable Chat Component JavaScript - Updated for Knowledge Queries & Property Search
 * This file provides consistent chat functionality across all pages
 * Includes property search without page refresh and knowledge query popups
 */

class ChatComponent {
    constructor() {
        console.log('🚀 ChatComponent constructor called');
        
        // Check if already initialized
        if (this.initialized) {
            console.log('⚠️ ChatComponent already initialized, skipping');
            return;
        }
        
        this.initialized = true;
        
        // Initialize immediately since HTML is guaranteed to be loaded
        console.log('✅ Initializing chat component...');
        this.initializeChat();
        this.setupEventListeners();
        this.setupPopupEventListeners();
        this.setupImagePath();
        
        // Test if elements are accessible
        requestAnimationFrame(() => {
            console.log('🧪 Testing DOM element accessibility...');
            const testInput = document.getElementById('chatInput');
            const testBtn = document.getElementById('sendBtn');
            console.log('Test - Chat input:', testInput);
            console.log('Test - Send button:', testBtn);
            
            if (testInput && testBtn) {
                console.log('✅ All elements are accessible');
            } else {
                console.error('❌ Some elements are not accessible');
            }
        });
    }

    initializeChat() {
        console.log('🔧 Initializing chat...');
        
        // Auto-resize textarea
        const chatInput = document.getElementById('chatInput');
        if (chatInput) {
            console.log('✅ Chat input found, setting up event listeners');
            
            chatInput.addEventListener('input', () => {
                chatInput.style.height = 'auto';
                chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + 'px';
            });

            // Handle Enter key
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    console.log('⏎ Enter key pressed, calling handleSendMessage');
                    this.handleSendMessage();
                }
            });
        } else {
            console.error('❌ Chat input not found during initialization');
        }
    }

    setupEventListeners() {
        console.log('🔧 Setting up event listeners...');
        
        const sendBtn = document.getElementById('sendBtn');
        if (sendBtn) {
            console.log('✅ Send button found, setting up click listener');
            sendBtn.addEventListener('click', () => {
                console.log('🖱️ Send button clicked, calling handleSendMessage');
                this.handleSendMessage();
            });
        } else {
            console.error('❌ Send button not found');
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
        console.log('📤 handleSendMessage called');
        
        const chatInput = document.getElementById('chatInput');
        console.log('🔍 Chat input element:', chatInput);
        
        if (!chatInput) {
            console.error('❌ chatInput element not found');
            return;
        }

        const message = chatInput.value.trim();
        console.log('📝 Message value:', message);
        
        if (!message) {
            console.log('⚠️ Empty message, not sending');
            return;
        }

        console.log('✅ Sending message:', message);

        // Add user message to chat FIRST
        console.log('💬 About to add user message to chat');
        this.addMessageToChat(message, 'user');
        console.log('✅ User message added to chat');

        // Clear input AFTER adding message
        chatInput.value = '';
        chatInput.style.height = 'auto';
        console.log('🧹 Input cleared');

        // Check if it's a property search query and handle it
        if (this.isPropertySearchQuery(message)) {
            console.log('🏠 Property search detected, calling searchProperties directly');
            // Call the existing searchProperties function instead of navigating
            if (typeof searchProperties === 'function') {
                searchProperties(message);
            } else {
                console.error('❌ searchProperties function not found');
            }
        } else {
            console.log('💡 Knowledge query detected, processing for popup response');
            // Process the message to get a response and show it in popup
            try {
                const response = await this.processMessage(message);
                this.showQueryPopup(message, response);
            } catch (error) {
                console.error('Error processing knowledge query:', error);
            }
        }
    }

    addMessageToChat(message, sender) {
        const aiAssistant = document.querySelector('.ai-assistant');
        if (!aiAssistant) {
            console.error('ai-assistant element not found');
            return;
        }

        // Ensure message is a string
        if (typeof message !== 'string') {
            console.warn('addMessageToChat received non-string message:', message);
            message = String(message || '');
        }

        console.log(`Adding ${sender} message:`, message);

        // For user messages, always add them below the "Agent: Kavya" message
        if (sender === 'user') {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'user-message';
            
            const messageContent = document.createElement('div');
            messageContent.className = 'message-content';
            messageContent.textContent = message;
            
            messageDiv.appendChild(messageContent);
            aiAssistant.appendChild(messageDiv);
            
            console.log(`User message added to chat. Total messages:`, aiAssistant.children.length);
            
            // Scroll to bottom with smooth animation
            setTimeout(() => {
                aiAssistant.scrollTop = aiAssistant.scrollHeight;
                console.log('Scrolled to bottom');
            }, 100);
        }
        // For now, ignore assistant messages
    }

    parseResponse(response) {
        // Ensure response is a string before parsing
        if (typeof response !== 'string') {
            console.warn('parseResponse received non-string response:', response);
            return String(response || '');
        }
        
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
        const lowerMessage = message.toLowerCase();
        
        // First check if it's a knowledge query (should not be treated as property search)
        const knowledgePatterns = [
            'what is', 'how to', 'tell me about', 'explain', 'define', 'meaning of',
            'what are', 'how do', 'can you explain', 'i want to know about'
        ];
        
        if (knowledgePatterns.some(pattern => lowerMessage.includes(pattern))) {
            return false; // This is a knowledge query, not a property search
        }
        
        // Then check for property-specific keywords
        const propertyKeywords = [
            'bhk', 'apartment', 'house', 'property', 'flat', 'villa', 'pune', 'mumbai', 'bangalore',
            'delhi', 'chennai', 'hyderabad', 'kolkata', 'ahmedabad', 'price', 'cost', 'area',
            'sq ft', 'sqft', 'square feet', 'bedroom', 'bedrooms', 'location', 'locality'
        ];
        
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
        // Navigate to home page for property search since results are always displayed there
        this.navigateToHomePageForSearch(message);
        return `Searching for "${message}"...`;
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

        // Keep only the first message (which should be "I am Kavya")
        const firstMessage = aiAssistant.children[0];
        aiAssistant.innerHTML = '';
        if (firstMessage) {
            aiAssistant.appendChild(firstMessage);
        }
    }

    // Method to setup image path dynamically based on current page
    setupImagePath() {
        const imageElement = document.getElementById('kavyaImage');
        if (!imageElement) return;

        // Determine the correct image path based on current page location
        const currentPath = window.location.pathname;
        let imagePath = '';

        if (currentPath.includes('/calculators/')) {
            // We're on a calculator page, need to go up one level
            imagePath = '../images/Kavya.JPG';
        } else {
            // We're on the home page or other pages
            imagePath = 'images/Kavya.JPG';
        }

        imageElement.src = imagePath;
        console.log('Set image path to:', imagePath);
        
        // Add error handling for image loading
        imageElement.onerror = function() {
            console.error('Failed to load image from:', imagePath);
            // Try alternative path
            const altPath = imagePath.includes('../') ? 'images/Kavya.JPG' : '../images/Kavya.JPG';
            console.log('Trying alternative path:', altPath);
            imageElement.src = altPath;
        };
        
        imageElement.onload = function() {
            console.log('Image loaded successfully from:', imagePath);
        };
    }

    // Reusable method to navigate to home page for property search
    navigateToHomePageForSearch(searchQuery) {
        // Encode the search query for URL
        const encodedQuery = encodeURIComponent(searchQuery);
        
        // Navigate to home page with search query
        const homePageUrl = this.getHomePageUrl();
        const searchUrl = `${homePageUrl}?search=${encodedQuery}`;
        
        console.log('Navigating to home page for search:', searchUrl);
        
        // Navigate to home page
        window.location.href = searchUrl;
    }

    // Helper method to get the correct home page URL
    getHomePageUrl() {
        const currentPath = window.location.pathname;
        
        if (currentPath.includes('/calculators/')) {
            // We're on a calculator page, need to go up one level
            return '../index.html';
        } else {
            // We're on the home page or other pages
            return 'index.html';
        }
    }
    
    // Test method to verify functionality
    testChatFunctionality() {
        console.log('🧪 Testing chat functionality...');
        
        // Test if we can find the elements
        const chatInput = document.getElementById('chatInput');
        const sendBtn = document.getElementById('sendBtn');
        const aiAssistant = document.querySelector('.ai-assistant');
        
        console.log('Test results:');
        console.log('- Chat input:', chatInput);
        console.log('- Send button:', sendBtn);
        console.log('- AI assistant:', aiAssistant);
        
        // Test if we can add a message
        if (aiAssistant) {
            console.log('✅ Testing message addition...');
            this.addMessageToChat('Test message from console', 'user');
        }
        
        return {
            chatInput: !!chatInput,
            sendBtn: !!sendBtn,
            aiAssistant: !!aiAssistant
        };
    }
}

// Chat component initialization is now handled by index.html
// This prevents duplicate initialization and ensures proper sequencing

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ChatComponent;
}

// Global test function for debugging
window.testChat = function() {
    if (window.chatComponentInstance) {
        return window.chatComponentInstance.testChatFunctionality();
    } else {
        console.error('❌ ChatComponent not initialized');
        return null;
    }
};
