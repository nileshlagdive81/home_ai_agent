// Sample property data with updated sell_price field
const sampleProperties = [
    {
        id: 1,
        status: "Available",
        imagePath: "images/projects/lodha-park.jpg",
        imageCount: "1/4",
        sellPrice: 8500000, // in rupees (85 lakhs)
        pricePerSqft: 8500, // in rupees per sqft
        carpetArea: 1200, // in sq ft
        specs: "2 BHK • 2 Bath • 1,200 sq ft • Apartment",
        locality: "Baner",
        city: "Pune",
        project: "Lodha Park",
        amenities: ["Gym", "Parking", "Pet-friendly"],
        moreAmenities: 3
    },
    {
        id: 2,
        status: "New Listing",
        imagePath: "images/projects/godrej-properties.jpg",
        imageCount: "1/4",
        sellPrice: 12000000, // in rupees (120 lakhs)
        pricePerSqft: 9200, // in rupees per sqft
        carpetArea: 1800, // in sq ft
        specs: "3 BHK • 2 Bath • 1,800 sq ft • House",
        locality: "Hinjewadi",
        city: "Pune",
        project: "Godrej Properties",
        amenities: ["Garden", "Garage", "Fireplace"],
        moreAmenities: 2
    },
    {
        id: 3,
        status: "Premium",
        imagePath: "images/projects/mahindra-lifespaces.jpg",
        imageCount: "1/5",
        sellPrice: 25000000, // in rupees (250 lakhs)
        pricePerSqft: 12500, // in rupees per sqft
        carpetArea: 2500, // in sq ft
        specs: "3 BHK • 3 Bath • 2,500 sq ft • Penthouse",
        locality: "Koregaon Park",
        city: "Pune",
        project: "Mahindra Lifespaces",
        amenities: ["Balcony", "Concierge", "Pool"],
        moreAmenities: 3
    },
    {
        id: 4,
        status: "Available",
        imagePath: "images/projects/kolte-patil.jpg",
        imageCount: "1/3",
        sellPrice: 6500000, // in rupees (65 lakhs)
        pricePerSqft: 7200, // in rupees per sqft
        carpetArea: 800, // in sq ft
        specs: "1 BHK • 1 Bath • 800 sq ft • Studio",
        locality: "Wakad",
        city: "Pune",
        project: "Kolte Patil",
        amenities: ["Gym", "Laundry", "Storage"],
        moreAmenities: 1
    },
    {
        id: 5,
        status: "Featured",
        imagePath: "images/projects/purvankara.jpg",
        imageCount: "1/6",
        sellPrice: 18000000, // in rupees (180 lakhs)
        pricePerSqft: 9800, // in rupees per sqft
        carpetArea: 2200, // in sq ft
        specs: "4 BHK • 3 Bath • 2,200 sq ft • Townhouse",
        locality: "Baner",
        city: "Pune",
        project: "Purvankara",
        amenities: ["Garden", "Patio", "Fireplace", "Garage"],
        moreAmenities: 2
    },
    {
        id: 6,
        status: "Luxury",
        imagePath: "images/projects/sobha-developers.jpg",
        imageCount: "1/8",
        sellPrice: 45000000, // in rupees (450 lakhs)
        pricePerSqft: 18500, // in rupees per sqft
        specs: "5 BHK • 4 Bath • 3,400 sq ft • Mansion",
        locality: "Koregaon Park",
        city: "Pune",
        project: "Sobha Developers",
        amenities: ["Pool", "Gym", "Spa", "Theater", "Wine Cellar"],
        moreAmenities: 4
    }
];



// Static search queries - no rotation needed
const staticSearchQueries = {
    size: "2 BHK apartments under 1 crore in Pune",
    budget: "Properties under 50 lakhs in Pune",
    locality: "Homes in Baner, Pune", 
    status: "Ready to move properties in Pune"
};

// Global search state
let isSearchActive = false;

// DOM elements
const landingContent = document.getElementById('landingContent');
const searchResults = document.getElementById('searchResults');
const propertyGrid = document.getElementById('propertyGrid');
const resultCount = document.getElementById('resultCount');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.querySelector('.send-btn');
const header = document.querySelector('.header');

// Global filter state management
let globalFilterState = {
    city: null,
    locality: null,
    bhk: null,
    price: null,
    carpet_area: null,
    amenities: [],
    status: null,
    roi: null
};

// Header scroll effect - only on home page
if (document.querySelector('.main-content .search-header')) {
    window.addEventListener('scroll', () => {
        const header = document.querySelector('.main-header');
        if (header && window.scrollY > 50) {
            header.classList.add('scrolled');
        } else if (header) {
            header.classList.remove('scrolled');
        }
    });
}

// Helper: safely get the chat input textarea element on any page
function getChatInputElement() {
    const byId = document.getElementById('chatInput');
    if (byId) return byId;
    const inContainer = document.querySelector('.message-input textarea');
    if (inContainer) return inContainer;
    return null;
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the home page (has search functionality)
    const isHomePage = document.querySelector('.main-content .search-header');
    
    // Initialize chat functionality on ALL pages
    const sendBtn = document.querySelector('.send-btn');
    const chatInput = getChatInputElement();
    
    if (sendBtn && chatInput) {
        sendBtn.addEventListener('click', handleChatMessage);
        chatInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault(); // Prevent new line
                handleChatMessage();
            }
        });
        
        // Auto-resize textarea
        chatInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 200) + 'px';
        });

        // Add focus/blur event listeners for suggestive placeholder (only on home page)
        if (isHomePage) {
            chatInput.addEventListener('focus', function() {
                // Clear placeholder when user focuses on input
                this.placeholder = '';
            });
            
            chatInput.addEventListener('blur', function() {
                // Restore suggestive placeholder when user leaves input
                if (this.value.trim() === '') {
                    updateSuggestivePlaceholder();
                }
            });
        }
    }
    
    if (isHomePage) {
        // Check for search parameter in URL (for redirects from project details page)
        checkURLSearchParameter();
        
        // Initialize static search boxes
        initializeStaticSearchBoxes();
        
        // Initialize static search boxes
        initializeStaticSearchBoxes();

        // Add click handler for New Query button
        const newChatBtn = document.querySelector('.new-chat-btn');
        if (newChatBtn) {
            newChatBtn.addEventListener('click', function() {
                // Clear chat and reset to landing page
                const landingContent = document.querySelector('.landing-content');
                const searchResults = document.querySelector('.search-results');
                const filtersBar = document.getElementById('filtersBar');
                const aiAssistant = document.querySelector('.ai-assistant');
                const filters = document.querySelectorAll('.filter-value');
                
                if (landingContent && searchResults) {
                    landingContent.style.display = 'block';
                    searchResults.style.display = 'none';
                }
                
                if (filtersBar) {
                    filtersBar.style.display = 'none';
                }
                
                // Clear ALL chat messages including the initial AI message
                if (aiAssistant) {
                    const allMessages = aiAssistant.querySelectorAll('.assistant-message, .user-message');
                    allMessages.forEach(msg => msg.remove());
                }
                
                // Reset filters
                if (filters.length > 0) {
                    filters.forEach(filter => filter.textContent = '—');
                }
                
                // Clear chat input
                const chatInput = getChatInputElement();
                if (chatInput) {
                    chatInput.value = '';
                }
                
                // Call handleNewQuery for additional functionality
                handleNewQuery();
            });
        }
        
        // Set initial suggestive placeholder
        updateSuggestivePlaceholder();
    }
});

// Check for search parameter in URL and perform search if found
function checkURLSearchParameter() {
    const urlParams = new URLSearchParams(window.location.search);
    const searchQuery = urlParams.get('search');
    
    if (searchQuery) {
        console.log('Found search parameter in URL:', searchQuery);
        
        // Set the search query in the chat input
        const chatInput = getChatInputElement();
        if (chatInput) {
            chatInput.value = searchQuery;
        }
        
        // Perform the search automatically
        setTimeout(() => {
            handleChatMessage();
        }, 500);
        
        // Clear the search parameter from URL to prevent re-searching on refresh
        const newUrl = window.location.pathname;
        window.history.replaceState({}, document.title, newUrl);
    }
}



// Update search box content with static queries
function updateSearchBoxContent(category) {
    const searchCards = document.querySelectorAll('.search-card');
    
    // Safety check - only proceed if search cards exist
    if (searchCards.length === 0) {
        return;
    }
    
    let targetCard;
    
    switch(category) {
        case 'size':
            targetCard = searchCards[0];
            break;
        case 'budget':
            targetCard = searchCards[1];
            break;
        case 'locality':
            targetCard = searchCards[2];
            break;
        case 'status':
            targetCard = searchCards[3];
            break;
    }
    
    if (targetCard) {
        const staticQuery = staticSearchQueries[category];
        const titleElement = targetCard.querySelector('h3');
        const descElement = targetCard.querySelector('p');
        
        if (titleElement && descElement && staticQuery) {
            // Set static title and description
            titleElement.textContent = category.charAt(0).toUpperCase() + category.slice(1);
            descElement.textContent = staticQuery;
            
            // Update onclick to use static query
            targetCard.onclick = () => searchProperties(staticQuery);
        }
    }
}

// Initialize static search boxes (no rotation needed)
function initializeStaticSearchBoxes() {
    // Only initialize if search cards exist (home page)
    if (document.querySelectorAll('.search-card').length > 0) {
        updateSearchBoxContent('size');
        updateSearchBoxContent('budget');
        updateSearchBoxContent('locality');
        updateSearchBoxContent('status');
    }
}

// Function to update the suggestive placeholder
function updateSuggestivePlaceholder() {
    const chatInput = getChatInputElement();
    if (chatInput) {
        const suggestion = generateSuggestiveQueries(globalFilterState);
        chatInput.placeholder = suggestion;
    }
}

// Handle chat messages
function handleChatMessage() {
    const chatInput = getChatInputElement();
    if (chatInput) {
        const message = chatInput.value.trim();
        if (message) {
            // Add user message to chat
            addUserMessage(message);
            // Simulate AI response
            simulateAIResponse(message);
            chatInput.value = '';
        }
    }
}

// Simulate AI response and search
async function simulateAIResponse(message) {
    const messageLower = message.toLowerCase().trim();
    
    // Check if message contains system-generated text that should not be processed
    const systemGeneratedPatterns = [
        'found properties matching criteria', 'searching for properties', 'processing your query',
        'knowledge base - all available queries', 'complete knowledge base', 'showing sample properties'
    ];
    
    // Check if this is a system-generated message that shouldn't be processed
    const isSystemGenerated = systemGeneratedPatterns.some(pattern => messageLower.includes(pattern));
    if (isSystemGenerated) {
        console.log('🚫 Ignoring system-generated text:', message);
        return; // Don't process system-generated text
    }
    

    
    // Check if message is a casual greeting or non-property query
    const casualMessages = [
        'hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening',
        'how are you', 'thanks', 'thank you', 'bye', 'goodbye', 'see you',
        'ok', 'okay', 'yes', 'no', 'maybe', 'sure', 'alright'
    ];
    
    // Check message characteristics
    const isCasualMessage = casualMessages.some(casual => messageLower === casual);
    
    if (isCasualMessage) {
        // Handle casual messages with friendly responses
        addAIMessage(`Hello! 👋 I'm here to help you find your perfect property. Try asking me:<br><br>
<strong>🏠 Property Search Examples:</strong><br>
• "2 BHK apartments in Pune"<br>
• "Properties under 1 crore"<br>
• "Homes with gym facility"<br>
• "3 BHK houses in Baner"<br>
• "Luxury properties above 2 crore"`);
    } else {
        // All other messages are treated as property searches
        console.log('🏠 Processing as Property Search:', message);
        searchProperties(message);
    }
}

// Handle knowledge base queries - COMMENTED OUT FOR NOW
/*
async function handleKnowledgeQuery(message) {
    try {
        // Show typing indicator
        addAIMessage(`
            <div class="typing-indicator">🤔 Let me search my knowledge base...</div>
        `);
        
        console.log('🔍 Calling knowledge base API for:', message);
        
        // Call the knowledge base API
        const formData = new FormData();
        formData.append('query', message);
        
        const apiUrl = 'http://localhost:8000/api/v1/knowledge/query';
        console.log('🌐 API URL:', apiUrl);
        
        const response = await fetch(apiUrl, {
            method: 'POST',
            body: formData
        });
        
        console.log('📡 API Response Status:', response.status);
        console.log('📡 API Response Headers:', response.headers);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('📊 API Response Data:', result);
        
        // Remove typing indicator
        removeTypingIndicator();
        
        if (result.success) {
            // Display knowledge answer in the right panel
            displayKnowledgeInRightPanel(result);
        } else {
            // Display suggestions if no exact match found
            addAIMessage(`
                <div class="knowledge-no-match">
                    <p>${result.message}</p>
                    <div class="knowledge-suggestions">
                        <strong>💡 Try asking about:</strong><br>
                        ${result.suggestions.map(q => `• "${q}"`).join('<br>')}
                    </div>
                </div>
            `);
        }
        
    } catch (error) {
        console.error('❌ Error querying knowledge base:', error);
        console.error('❌ Error details:', {
            message: error.message,
            stack: error.stack,
            name: error.name
        });
        
        removeTypingIndicator();
        addAIMessage(`
            <div class="knowledge-error">
                <p><strong>❌ Error Details:</strong> ${error.message}</p>
                <p>This usually means:</p>
                <ul>
                    <li>Backend server is not running</li>
                    <li>Network connectivity issue</li>
                    <li>API endpoint changed</li>
                </ul>
                <p><strong>💡 Troubleshooting:</strong></p>
                <ul>
                    <li>Make sure backend server is running on port 8000</li>
                    <li>Check if you can access <a href="http://localhost:8000/docs" target="_blank">http://localhost:8000/docs</a></li>
                    <li>Try refreshing the page</li>
                </ul>
            </div>
        `);
    }
}
*/

// Remove typing indicator - COMMENTED OUT FOR NOW
/*
function removeTypingIndicator() {
    const typingIndicator = document.querySelector('.typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Show knowledge modal
function showKnowledgeModal(result) {
    const modal = document.getElementById('knowledgeModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');
    
    // Set modal title
    modalTitle.textContent = `${result.category.replace('_', ' ').toUpperCase()} - ${Math.round(result.confidence * 100)}% Match`;
    
    // Set modal content
    modalBody.innerHTML = `
        <div class="knowledge-content">
            ${result.answer}
        </div>
        <div class="knowledge-suggestions">
            <strong>💡 Related questions you might ask:</strong><br>
            • "What is built up area?"<br>
            • "How to buy property in India?"<br>
            • "What is ROI in real estate?"<br>
            • "Tell me about RERA"
        </div>
    `;
    
    // Show modal
    modal.style.display = 'block';
    
    // Knowledge answer is now displayed directly in chat, no need for additional message
}

// Close knowledge modal
function closeKnowledgeModal() {
    const modal = document.getElementById('knowledgeModal');
    modal.style.display = 'none';
}

// Display knowledge answer in the right panel
function displayKnowledgeInRightPanel(result) {
    // Hide landing content and show search results
    const landingContent = document.getElementById('landingContent');
    const searchResults = document.getElementById('searchResults');
    const propertyGrid = document.getElementById('propertyGrid');
    const resultCount = document.getElementById('resultCount');
    const filtersBar = document.getElementById('filtersBar');
    
    if (!landingContent || !searchResults || !propertyGrid) return;
    
    // Hide landing page and show search results area
    landingContent.style.display = 'none';
    searchResults.style.display = 'block';
    
    // Hide the filters bar for knowledge queries
    if (filtersBar) {
        filtersBar.style.display = 'none';
    }
    
    // Clear the result count text for knowledge queries
    if (resultCount) {
        resultCount.textContent = '';
    }
    
    // Clear existing content and show knowledge
    propertyGrid.innerHTML = '';
    
    // Create knowledge display
    const knowledgeDiv = document.createElement('div');
    knowledgeDiv.className = 'knowledge-display';
    knowledgeDiv.innerHTML = `
        <div class="knowledge-panel">
            <div class="knowledge-panel-header">
                <h3>📚 Knowledge Base</h3>
                <span class="knowledge-category-badge">${result.category.replace('_', ' ').toUpperCase()}</span>
            </div>
            <div class="knowledge-panel-content">
                ${result.answer}
            </div>
            <div class="knowledge-panel-footer">
                <button class="btn btn-secondary" onclick="showMoreKnowledgeTopics()">
                    <i class="fas fa-arrow-left"></i> Back to Topics
                </button>
                <button class="btn btn-primary" onclick="clearKnowledgeDisplay()">
                    <i class="fas fa-search"></i> Back to Property Search
                </button>
            </div>
        </div>
    `;
    
    propertyGrid.appendChild(knowledgeDiv);
}

// Clear knowledge display and show property search
function clearKnowledgeDisplay() {
    const landingContent = document.getElementById('landingContent');
    const searchResults = document.getElementById('searchResults');
    const propertyGrid = document.getElementById('propertyGrid');
    const filtersBar = document.getElementById('filtersBar');
    
    if (!landingContent || !searchResults || !propertyGrid) return;
    
    // Show landing page
    landingContent.style.display = 'block';
    searchResults.style.display = 'none';
    
    // Clear any knowledge content
    propertyGrid.innerHTML = '';
    
    // Show filters bar when returning to property search
    if (filtersBar) {
        filtersBar.style.display = 'flex';
    }
}

// Show more knowledge topics
function showMoreKnowledgeTopics() {
    const propertyGrid = document.getElementById('propertyGrid');
    const resultCount = document.getElementById('resultCount');
    const filtersBar = document.getElementById('filtersBar');
    if (!propertyGrid) return;
    
    // Hide the filters bar for knowledge topics
    if (filtersBar) {
        filtersBar.style.display = 'none';
    }
    
    // Clear the result count text for knowledge topics
    if (resultCount) {
        resultCount.textContent = '';
    }
    
    propertyGrid.innerHTML = `
        <div class="knowledge-topics">
            <h3>📚 Complete Knowledge Base - All Available Queries</h3>
            <p class="knowledge-intro">Click on any question to get detailed answers from our comprehensive real estate knowledge base.</p>
            
            <div class="knowledge-categories">
                <!-- Terminology Section -->
                <div class="knowledge-category">
                    <h4><i class="fas fa-book"></i> 📖 Terminology & Definitions</h4>
                    <div class="query-list">
                        <div class="query-item" onclick="askKnowledgeQuestion('What is carpet area?')">
                            <i class="fas fa-question-circle"></i>
                            What is carpet area?
                        </div>
                        <div class="query-item" onclick="askKnowledgeQuestion('What is built up area?')">
                            <i class="fas fa-question-circle"></i>
                            What is built up area?
                        </div>
                        <div class="query-item" onclick="askKnowledgeQuestion('What is super built up area?')">
                            <i class="fas fa-question-circle"></i>
                            What is super built up area?
                        </div>
                        <div class="query-item" onclick="askKnowledgeQuestion('What is BHK?')">
                            <i class="fas fa-question-circle"></i>
                            What is BHK?
                        </div>
                        <div class="query-item" onclick="askKnowledgeQuestion('What is ROI in real estate?')">
                            <i class="fas fa-question-circle"></i>
                            What is ROI in real estate?
                        </div>
                    </div>
                </div>
                
                <!-- Legal & Regulatory Section -->
                <div class="knowledge-category">
                    <h4><i class="fas fa-gavel"></i> ⚖️ Legal & Regulatory</h4>
                    <div class="query-list">
                        <div class="query-item" onclick="askKnowledgeQuestion('What is RERA?')">
                            <i class="fas fa-question-circle"></i>
                            What is RERA?
                        </div>
                        <div class="query-item" onclick="askKnowledgeQuestion('What documents needed for home loan?')">
                            <i class="fas fa-question-circle"></i>
                            What documents needed for home loan?
                        </div>
                        <div class="query-item" onclick="askKnowledgeQuestion('What is stamp duty?')">
                            <i class="fas fa-question-circle"></i>
                            What is stamp duty?
                        </div>
                        <div class="query-item" onclick="askKnowledgeQuestion('What is GST in real estate?')">
                            <i class="fas fa-question-circle"></i>
                            What is GST in real estate?
                        </div>
                    </div>
                </div>
                
                <!-- Processes Section -->
                <div class="knowledge-category">
                    <h4><i class="fas fa-cogs"></i> 🔄 Processes & Procedures</h4>
                    <div class="query-list">
                        <div class="query-item" onclick="askKnowledgeQuestion('How to buy property in India?')">
                            <i class="fas fa-question-circle"></i>
                            How to buy property in India?
                        </div>
                        <div class="query-item" onclick="askKnowledgeQuestion('How to apply for home loan?')">
                            <i class="fas fa-question-circle"></i>
                            How to apply for home loan?
                        </div>
                        <div class="query-item" onclick="askKnowledgeQuestion('How to check property documents?')">
                            <i class="fas fa-question-circle"></i>
                            How to check property documents?
                        </div>
                        <div class="query-item" onclick="askKnowledgeQuestion('What document to check for buying a flat?')">
                            <i class="fas fa-question-circle"></i>
                            What document to check for buying a flat?
                        </div>
                    </div>
                </div>
                
                <!-- Investment Section -->
                <div class="knowledge-category">
                    <h4><i class="fas fa-chart-line"></i> 💰 Investment & Analysis</h4>
                    <div class="query-list">
                        <div class="query-item" onclick="askKnowledgeQuestion('Is real estate good investment?')">
                            <i class="fas fa-question-circle"></i>
                            Is real estate good investment?
                        </div>
                        <div class="query-item" onclick="askKnowledgeQuestion('How to calculate rental yield?')">
                            <i class="fas fa-question-circle"></i>
                            How to calculate rental yield?
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="knowledge-footer">
                <button class="btn btn-primary" onclick="clearKnowledgeDisplay()">
                    <i class="fas fa-search"></i> Back to Property Search
                </button>
                <p class="knowledge-note">💡 <strong>Pro Tip:</strong> You can also ask these questions in natural language in the chat box!</p>
            </div>
        </div>
    `;
}

// Ask a knowledge question from topic cards
function askKnowledgeQuestion(question) {
    // Add user message to chat
    addUserMessage(question);
    
    // Process the knowledge query
    handleKnowledgeQuery(question);
}
*/

// Close modal when clicking outside - COMMENTED OUT FOR NOW
/*
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('knowledgeModal');
    
    modal.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeKnowledgeModal();
        }
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && modal.style.display === 'block') {
            closeKnowledgeModal();
        }
    });
});
*/

// Filter state management functions
function updateFilterState(newFilters) {
    // Update global filter state with new values
    Object.keys(newFilters).forEach(key => {
        if (newFilters[key] !== null && newFilters[key] !== undefined) {
            if (key === 'amenities') {
                // For amenities, accumulate (OR logic) - only add new ones
                if (Array.isArray(newFilters[key])) {
                    // Add new amenities to existing ones
                    newFilters[key].forEach(amenity => {
                        if (!globalFilterState[key].includes(amenity.toLowerCase())) {
                            globalFilterState[key].push(amenity.toLowerCase());
                        }
                    });
                } else {
                    // Add single amenity if not already present
                    if (!globalFilterState[key].includes(newFilters[key].toLowerCase())) {
                        globalFilterState[key].push(newFilters[key].toLowerCase());
                    }
                }
            } else {
                // For other filters, replace (except city which is constant)
                if (key !== 'city') {
                    globalFilterState[key] = newFilters[key];
                }
            }
        }
    });
    
    console.log('Updated global filter state:', globalFilterState);
}

function clearAllFilters() {
    globalFilterState = {
        city: null,
        locality: null,
        bhk: null,
        price: null,
        carpet_area: null,
        amenities: [],
        status: null,
        roi: null
    };
    
    // Reset all filter displays
    const filters = document.querySelectorAll('.filter-value');
    filters.forEach(filter => filter.textContent = '—');
    
    // Update suggestive placeholder
    updateSuggestivePlaceholder();
}

function buildQueryWithFilters(userQuery) {
    // Build a comprehensive query that includes existing filters
    let enhancedQuery = userQuery;
    
    if (globalFilterState.city) {
        enhancedQuery += ` in ${globalFilterState.city}`;
    }
    
    if (globalFilterState.bhk) {
        enhancedQuery += ` ${globalFilterState.bhk} BHK`;
    }
    
    if (globalFilterState.locality) {
        enhancedQuery += ` in ${globalFilterState.locality}`;
    }
    
    if (globalFilterState.price) {
        enhancedQuery += ` ${globalFilterState.price}`;
    }
    
    if (globalFilterState.carpet_area) {
        enhancedQuery += ` ${globalFilterState.carpet_area}`;
    }
    
    if (globalFilterState.amenities.length > 0) {
        // Capitalize amenities for better display
        const capitalizedAmenities = globalFilterState.amenities.map(amenity => 
            amenity.charAt(0).toUpperCase() + amenity.slice(1)
        );
        enhancedQuery += ` with ${capitalizedAmenities.join(' and ')}`;
    }
    
    if (globalFilterState.status) {
        enhancedQuery += ` ${globalFilterState.status}`;
    }
    
    if (globalFilterState.roi) {
        enhancedQuery += ` ${globalFilterState.roi}`;
    }
    
    return enhancedQuery;
}

// AI-powered suggestions for no results
function generateAISuggestions(query, filterState) {
    const suggestions = [];
    
    if (filterState.price) {
        suggestions.push("💰 Try increasing your budget - properties in this area might be priced higher");
    }
    
    if (filterState.carpet_area) {
        suggestions.push("📏 Consider properties with larger carpet area - your current requirement might be too specific");
    }
    
    if (filterState.amenities && filterState.amenities.length > 0) {
        suggestions.push("🏠 Try searching with fewer amenities - some properties might not have all requested facilities");
    }
    
    if (filterState.locality) {
        suggestions.push("📍 Explore nearby localities - similar properties might be available in adjacent areas");
    }
    
    if (filterState.bhk) {
        suggestions.push("🏘️ Consider different BHK configurations - try 1 BHK or 4+ BHK if available");
    }
    
    // Default suggestions
    if (suggestions.length === 0) {
        suggestions.push("🔍 Check spelling of location names");
        suggestions.push("💰 Try different price ranges");
        suggestions.push("🏘️ Use different BHK configurations");
        suggestions.push("📍 Search in different localities within the same city");
    }
    
    return suggestions;
}

// Check if query has meaningful filters or search criteria
function hasMeaningfulFilters(query) {
    if (!query || query.trim() === '') return false;
    
    const queryLower = query.toLowerCase().trim();
    
    // Check for location terms
    const locationTerms = ['pune', 'mumbai', 'bangalore', 'baner', 'hinjewadi', 'wakad', 'thane', 'bandra', 'viman nagar'];
    const hasLocation = locationTerms.some(term => queryLower.includes(term));
    
    // Check for property type terms
    const propertyTypeTerms = ['bhk', 'bedroom', 'apartment', 'house', 'flat', 'villa', 'property'];
    const hasPropertyType = propertyTypeTerms.some(term => queryLower.includes(term));
    
    // Check for price terms
    const priceTerms = ['price', 'crore', 'lakh', 'budget', 'under', 'above', 'less than', 'more than'];
    const hasPrice = priceTerms.some(term => queryLower.includes(term));
    
    // Check for size terms
    const sizeTerms = ['sqft', 'sq ft', 'square feet', 'carpet area', 'built up', 'super built up'];
    const hasSize = sizeTerms.some(term => queryLower.includes(term));
    
    // Check for amenity terms
    const amenityTerms = ['gym', 'parking', 'pool', 'garden', 'security', 'lift', 'swimming', 'concierge', 'spa'];
    const hasAmenity = amenityTerms.some(term => queryLower.includes(term));
    
    // Check for status terms
    const statusTerms = ['available', 'ready', 'under construction', 'new launch', 'premium', 'luxury'];
    const hasStatus = statusTerms.some(term => queryLower.includes(term));
    
    // Check for specific numbers (BHK, price, area)
    const hasNumbers = /\d+/.test(queryLower);
    
    // Return true if at least one meaningful filter is present
    return hasLocation || hasPropertyType || hasPrice || hasSize || hasAmenity || hasStatus || hasNumbers;
}

// Generate AI-powered suggestive queries for input placeholder
function generateSuggestiveQueries(filterState) {
    const suggestions = [];
    
    // Base suggestions based on current filter state
    if (filterState.city) {
        if (filterState.bhk) {
            if (filterState.price) {
                // City + BHK + Price set
                suggestions.push(`Properties in ${filterState.city} with ${filterState.bhk} BHK ${filterState.price}`);
                suggestions.push(`Show me ${filterState.bhk} BHK in ${filterState.city} ${filterState.price}`);
            } else {
                // City + BHK set
                suggestions.push(`${filterState.bhk} BHK properties in ${filterState.city} under 2 crore`);
                suggestions.push(`Show me ${filterState.bhk} BHK apartments in ${filterState.city}`);
            }
        } else {
            // Only city set
            suggestions.push(`2 BHK apartments in ${filterState.city} under 1 crore`);
            suggestions.push(`3 BHK houses in ${filterState.city} above 50 lakhs`);
            suggestions.push(`Luxury properties in ${filterState.city} above 2 crore`);
        }
    } else {
        // No filters set - general suggestions
        suggestions.push("2 BHK apartments under 1 crore in Pune");
        suggestions.push("3 BHK houses above 50 lakhs in Mumbai");
        suggestions.push("Properties in Baner area");
        suggestions.push("Luxury homes above 2 crore");
    }
    
    // Add amenity-based suggestions if amenities exist
    if (filterState.amenities && filterState.amenities.length > 0) {
        const amenityText = filterState.amenities.join(' and ');
        if (filterState.city) {
            suggestions.push(`Properties in ${filterState.city} with ${amenityText}`);
        } else {
            suggestions.push(`Homes with ${amenityText} in Pune`);
        }
    }
    
    // Add locality-based suggestions if locality exists
    if (filterState.locality) {
        if (filterState.city) {
            suggestions.push(`Properties in ${filterState.locality}, ${filterState.city}`);
        } else {
            suggestions.push(`Homes in ${filterState.locality} area`);
        }
    }
    
    // Return a random suggestion
    return suggestions[Math.floor(Math.random() * suggestions.length)];
}

// Handle New Query button click
function handleNewQuery() {
    console.log('New Query clicked - clearing all filters and resetting state');
    
    // Clear all filters
    clearAllFilters();
    
    // Clear chat messages
    const aiAssistant = document.querySelector('.ai-assistant');
    const userMessages = aiAssistant.querySelectorAll('.user-message');
    const aiMessages = aiAssistant.querySelectorAll('.assistant-message');
    
    // Remove all messages
    userMessages.forEach(msg => msg.remove());
    aiMessages.forEach(msg => msg.remove());
    
    // Add the initial AI message with query suggestions
    addAIMessage(`Try these natural language queries:<br>
• "2 BHK apartments under 1 crore in Pune"<br>
• "3 BHK houses above 50 lakhs"<br>
• "Properties in Baner area"<br>
• "Luxury homes above 2 crore"`);
    
    // Hide search results and show landing page
    searchResults.style.display = 'none';
    landingContent.style.display = 'block';
    
    // Hide filters bar
    document.getElementById('filtersBar').style.display = 'none';
    
    // Clear chat input
    const chatInput = document.querySelector('.message-input');
    if (chatInput) {
        chatInput.value = '';
    }
    
    // Update suggestive placeholder
    updateSuggestivePlaceholder();
    
            // Mark search as inactive
        isSearchActive = false;
    
    // Don't scroll - keep header visible
    // window.scrollTo({ top: 0, behavior: 'smooth' });
    
    console.log('New Query completed - state reset');
}



// Add AI message to chat
function addAIMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'assistant-message';
    messageDiv.innerHTML = `<p>${message}</p>`;
    
    const aiAssistant = document.querySelector('.ai-assistant');
    aiAssistant.appendChild(messageDiv);
    
    // Scroll to bottom
    aiAssistant.scrollTop = aiAssistant.scrollHeight;
}

// Add user message to chat
function addUserMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'user-message';
    messageDiv.innerHTML = `
        <p>${message}</p>
    `;
    
    const aiAssistant = document.querySelector('.ai-assistant');
    aiAssistant.appendChild(messageDiv);
    
    // Scroll to bottom
    aiAssistant.scrollTop = aiAssistant.scrollHeight;
}

// Search properties function
async function searchProperties(query) {
    // Set search as active
    isSearchActive = true;
    
    // Check if we're on the home page (has search functionality)
    const isHomePage = document.querySelector('.main-content .search-header');
    
    // If not on home page, redirect to home page with search query
    if (!isHomePage) {
        console.log('🚀 Redirecting to home page for property search:', query);
        const encodedQuery = encodeURIComponent(query);
        window.location.href = `index.html?search=${encodedQuery}`;
        return;
    }
    
    // Check if there are any meaningful filters or search criteria
    const hasValidFilters = hasMeaningfulFilters(query);
    
    if (!hasValidFilters) {
        // Show message that at least one parameter is needed
        if (propertyGrid) {
            propertyGrid.innerHTML = `
                <div class="no-filters-message">
                    <i class="fas fa-info-circle"></i>
                    <h3>Please specify search criteria</h3>
                    <p>To search for properties, please provide at least one of the following:</p>
                    <ul>
                        <li><strong>Location:</strong> City, locality, or area</li>
                        <li><strong>Property Type:</strong> BHK, apartment, house, villa</li>
                        <li><strong>Price Range:</strong> Budget in lakhs or crores</li>
                        <li><strong>Size:</strong> Carpet area in sq ft</li>
                        <li><strong>Amenities:</strong> Gym, parking, pool, etc.</li>
                    </ul>
                    <p><strong>Examples:</strong></p>
                    <ul>
                        <li>"2 BHK apartments in Pune"</li>
                        <li>"Properties under 1 crore"</li>
                        <li>"Homes with gym in Baner"</li>
                        <li>"3 BHK above 50 lakhs"</li>
                    </ul>
                </div>
            `;
        }
        
        // Hide filters bar and result count for no-filter searches
        const filtersBar = document.getElementById('filtersBar');
        if (filtersBar) {
            filtersBar.style.display = 'none';
        }
        if (resultCount) {
            resultCount.textContent = '';
        }
        
        // Show search results area but with the no-filters message
        if (landingContent && searchResults) {
            landingContent.style.display = 'none';
            searchResults.style.display = 'block';
        }
        
        // Mark search as completed
        isSearchActive = false;
        return;
    }
    
    // Hide landing content and show search results
    if (landingContent && searchResults) {
        landingContent.style.display = 'none';
        searchResults.style.display = 'block';
    }
    
    // Show filters bar
    const filtersBar = document.getElementById('filtersBar');
    if (filtersBar) {
        filtersBar.style.display = 'flex';
    }
    
    // Show loading state
    if (resultCount) {
        resultCount.textContent = 'Searching...';
    }
    if (propertyGrid) {
        propertyGrid.innerHTML = '<div class="loading">🔍 Processing your query...</div>';
    }
    
    try {
        // Build enhanced query with existing filters
        const enhancedQuery = buildQueryWithFilters(query);
        console.log('Enhanced Query:', enhancedQuery);
        console.log('Current Filter State:', globalFilterState);
        
        // Call the backend NLP API
        const response = await fetch('http://localhost:8000/api/v1/search/nlp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `query=${encodeURIComponent(enhancedQuery)}`
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Display the actual results from the API
        if (data.results && data.results.length > 0) {
            // Update result count with actual results
            if (resultCount) {
                resultCount.textContent = `Found ${data.results_count} properties matching your criteria`;
            }
            displayProperties(data.results);
            
            // Update filters based on extracted entities and maintain state
            updateFiltersFromQuery(query, data.extracted_entities);
        } else {
            // No results found - hide result count completely and provide AI-powered suggestions
            if (resultCount) {
                resultCount.style.display = 'none';
            }
            const suggestions = generateAISuggestions(query, globalFilterState);
            if (propertyGrid) {
                propertyGrid.innerHTML = `
                    <div class="no-results">
                        <i class="fas fa-search"></i>
                        <h3>No properties found</h3>
                        <p>Your search for "${enhancedQuery}" returned no results.</p>
                        <div class="ai-suggestions">
                            <h4>💡 AI Suggestions:</h4>
                            <ul>
                                ${suggestions.map(suggestion => `<li>${suggestion}</li>`).join('')}
                            </ul>
                        </div>
                    </div>
                `;
            }
        }
        
        // Log the NLP processing details for debugging
        console.log('Original Query:', query);
        console.log('Enhanced Query:', enhancedQuery);
        console.log('NLP Intent:', data.intent);
        console.log('NLP Confidence:', data.confidence);
        console.log('Extracted Entities:', data.extracted_entities);
        console.log('Results Count:', data.results_count);
        console.log('Updated Filter State:', globalFilterState);
        
    } catch (error) {
        console.error('Error calling NLP API:', error);
        
        // Fallback to sample data if API fails
        if (resultCount) {
            resultCount.textContent = sampleProperties.length;
        }
        displayProperties(sampleProperties);
        
        // Show error message
        if (propertyGrid) {
            propertyGrid.innerHTML = `
                <div class="error-message">
                    <i class="fas fa-exclamation-triangle"></i>
                    <h3>API Error</h3>
                    <p>Could not connect to NLP search service.</p>
                    <p>Showing sample properties instead.</p>
                    <button onclick="searchProperties('${query}')" class="retry-btn">Retry</button>
                </div>
            `;
        }
    } finally {
        // Mark search as completed
        isSearchActive = false;
    }
    
    // Don't scroll - keep header visible
    // searchResults.scrollIntoView({ behavior: 'smooth' });
}

// Display properties in the grid
function displayProperties(properties) {
    if (!propertyGrid) return;
    
    propertyGrid.innerHTML = '';
    
    // Ensure result count is visible when showing properties
    if (resultCount) {
        resultCount.style.display = 'block';
    }
    
    properties.forEach(property => {
        const propertyCard = createPropertyCard(property);
        propertyGrid.appendChild(propertyCard);
    });
}

// Create property card element
function createPropertyCard(property) {
    const card = document.createElement('div');
    card.className = 'property-card';
    
    // Handle both API response format and sample data format
    const sellPrice = property.sell_price || property.sellPrice || 0;
    const pricePerSqft = property.price_per_sqft || property.pricePerSqft || 0;
    const propertyType = property.property_type || property.propertyType || 'Property';
    const bhkCount = property.bhk_count || property.bhkCount || 0;
    const carpetArea = property.carpet_area_sqft || property.carpetArea || 0;
    
    // Handle nested location structure from API
    let locality, city;
    if (property.location && property.location.locality) {
        locality = property.location.locality;
        city = property.location.city;
    } else {
        locality = property.locality || 'Unknown';
        city = property.city || 'Unknown';
    }
    
    const projectName = property.project_name || (property.project ? property.project.name : 'Unknown') || property.project || 'Unknown';
    const status = property.status || 'Available';
    
    // Use actual amenities from data if available, otherwise generate
    let allAmenities;
    if (property.amenities && Array.isArray(property.amenities) && property.amenities.length > 0) {
        allAmenities = property.amenities;
    } else {
        // Generate amenities based on property type and BHK
        const generatedAmenities = [];
        if (bhkCount >= 2) generatedAmenities.push('Parking');
        if (bhkCount >= 3) generatedAmenities.push('Gym', 'Garden');
        if (propertyType && propertyType.toLowerCase().includes('apartment')) {
            generatedAmenities.push('Lift', 'Security');
        }
        if (propertyType && propertyType.toLowerCase().includes('villa')) {
            generatedAmenities.push('Garden', 'Parking', 'Security');
        }
        if (generatedAmenities.length === 0) generatedAmenities.push('Basic Amenities');
        allAmenities = generatedAmenities;
    }
    
    const visibleAmenities = allAmenities.slice(0, 3);
    const hiddenAmenities = allAmenities.slice(3);
    
    // Format price in Indian format (lakhs/crores) from sellPrice in rupees
    const formatPrice = (sellPrice) => {
        if (!sellPrice || sellPrice === 0) return 'Price on request';
        const priceInLakhs = sellPrice / 100000; // Convert rupees to lakhs
        if (priceInLakhs >= 100) {
            return `₹${(priceInLakhs / 100).toFixed(1)} Cr`;
        } else {
            return `₹${priceInLakhs.toFixed(0)} Lakh`;
        }
    };
    
    // Format price per carpet area
    const formatPricePerCarpetArea = (pricePerSqft) => {
        if (!pricePerSqft || pricePerSqft === 0) return 'Price/carpet area on request';
        const priceInLakhs = pricePerSqft / 100000; // Convert to lakhs
        if (priceInLakhs >= 1) {
            return `₹${priceInLakhs.toFixed(2)} Lakh/sq ft`;
        } else {
            const priceInThousands = pricePerSqft / 1000;
            return `₹${priceInThousands.toFixed(1)} K/sq ft`;
        }
    };
    
    // Create project name with first 4 characters + asterisks (non-copyable)
    const createProjectName = (projectName) => {
        if (!projectName || projectName === 'Unknown') return 'Unknown***';
        if (projectName.length > 4) {
            const firstFour = projectName.substring(0, 4);
            const remaining = projectName.substring(4);
            return `${firstFour}${'*'.repeat(remaining.length)}`;
        }
        return projectName + '***';
    };
    
    // Create specs string from API data
    const createSpecs = () => {
        let specs = '';
        if (bhkCount) {
            specs += `${bhkCount} BHK`;
        }
        if (carpetArea && carpetArea > 0) {
            if (specs) specs += ' | ';
            specs += `${carpetArea} sq ft`;
        }
        if (propertyType && propertyType !== 'Property') {
            if (specs) specs += ' | ';
            specs += propertyType;
        }
        return specs || 'Specifications not available';
    };
    
    // Handle media display
    let imageDisplay = '';
    let imageCounter = '1/1';
    
    if (property.media && property.media.primary_image) {
        // Use real image from database
        imageDisplay = `<img src="${property.media.primary_image}" alt="${projectName}" class="property-real-image">`;
        imageCounter = `1/${property.media.total_count || 1}`;
    } else {
        // Fallback to placeholder
        imageDisplay = `
            <div class="image-placeholder">
                <i class="fas fa-building"></i>
            </div>
        `;
        imageCounter = '1/1';
    }
    
    card.innerHTML = `
        <div class="property-image">
            <div class="status-tag">${status}</div>
            ${imageDisplay}
            <div class="image-counter">${imageCounter}</div>
        </div>
        <div class="property-details">
            <div class="project-name" style="user-select: none; -webkit-user-select: none; -moz-user-select: none; -ms-user-select: none; font-size: 18px; font-weight: 600; color: #fff; margin-bottom: 16px;">${createProjectName(projectName)}</div>
            <div class="property-price">
                <div class="price-main">${formatPrice(sellPrice)}</div>
                <div class="price-per-sqft">${formatPricePerCarpetArea(pricePerSqft)}</div>
            </div>
            <div class="property-specs">${createSpecs()}</div>
            <div class="property-locality">${locality}, ${city}</div>
            <div class="property-amenities">
                ${visibleAmenities.map(amenity => `<span class="amenity-tag">${amenity}</span>`).join('')}
                ${hiddenAmenities.length > 0 ? `
                    <span class="amenity-count" onclick="toggleAmenities(this, ${JSON.stringify(hiddenAmenities).replace(/"/g, '&quot;')})" style="cursor: pointer; color: #3b82f6;">
                        +${hiddenAmenities.length} more
                    </span>
                ` : ''}
            </div>
        </div>
    `;
    
    // Add click handler for property card
    card.addEventListener('click', () => {
        showPropertyDetails(property);
    });
    
    return card;
}

// Enhanced NLP logic for price intent detection and filter updates
function updateFiltersFromQuery(query, extractedEntities) {
    const filters = document.querySelectorAll('.filter-value');
    if (!filters || filters.length === 0) return;
    
    const queryLower = query.toLowerCase();
    
    console.log('Updating filters with extracted entities:', extractedEntities);
    
    // Prepare new filter values to update state
    const newFilters = {};
    
    // City detection (filter[0]) - Persistent filter
    if (extractedEntities && extractedEntities.city) {
        const cityValue = extractedEntities.city.charAt(0).toUpperCase() + extractedEntities.city.slice(1);
        if (filters[0]) filters[0].textContent = cityValue;
        newFilters.city = extractedEntities.city.toLowerCase();
    } else if (queryLower.includes('pune') || queryLower.includes('mumbai') || queryLower.includes('bangalore')) {
        const cityMatch = queryLower.match(/(pune|mumbai|bangalore)/i);
        if (cityMatch && filters[0]) {
            const cityValue = cityMatch[0].charAt(0).toUpperCase() + cityMatch[0].slice(1);
            filters[0].textContent = cityValue;
            newFilters.city = cityMatch[0].toLowerCase();
        }
    }
    
    // Locality detection (filter[1]) - Replaceable filter
    if (extractedEntities && extractedEntities.locality) {
        const localityWords = extractedEntities.locality.split(' ');
        const capitalizedLocality = localityWords.map(word => 
            word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');
        if (filters[1]) filters[1].textContent = capitalizedLocality;
        newFilters.locality = extractedEntities.locality.toLowerCase();
    } else if (queryLower.includes('baner') || queryLower.includes('hinjewadi') || queryLower.includes('wakad') || 
               queryLower.includes('thane west') || queryLower.includes('bandra west') || queryLower.includes('viman nagar')) {
        const localityMatch = queryLower.match(/(baner|hinjewadi|wakad|thane west|bandra west|viman nagar)/i);
        if (localityMatch && filters[1]) {
            const localityWords = localityMatch[0].split(' ');
            const capitalizedLocality = localityWords.map(word => 
                word.charAt(0).toUpperCase() + word.slice(1)
            ).join(' ');
            filters[1].textContent = capitalizedLocality;
            newFilters.locality = localityMatch[0].toLowerCase();
        }
    }
    
    // BHK detection (filter[2]) - Persistent filter
    if (extractedEntities && extractedEntities.bhk) {
        if (filters[2]) filters[2].textContent = `${extractedEntities.bhk} BHK`;
        newFilters.bhk = extractedEntities.bhk.toString();
    } else if (queryLower.includes('2-bedroom') || queryLower.includes('2 bed') || queryLower.includes('2bhk')) {
        if (filters[2]) filters[2].textContent = '2 BHK';
        newFilters.bhk = '2';
    } else if (queryLower.includes('3-bedroom') || queryLower.includes('3 bed') || queryLower.includes('3bhk')) {
        if (filters[2]) filters[2].textContent = '3 BHK';
        newFilters.bhk = '3';
    } else if (queryLower.includes('1-bedroom') || queryLower.includes('1 bed') || queryLower.includes('1bhk')) {
        if (filters[2]) filters[2].textContent = '1 BHK';
        newFilters.bhk = '1';
    } else if (queryLower.includes('4-bedroom') || queryLower.includes('4 bed') || queryLower.includes('4bhk')) {
        if (filters[2]) filters[2].textContent = '4 BHK';
        newFilters.bhk = '4';
    }
    
    // Price detection (filter[3]) - Replaceable filter
    if (extractedEntities && extractedEntities.price_range) {
        const priceText = extractedEntities.price_range.toLowerCase();
        let priceDisplay = '';
        
        if (priceText.includes('under') || priceText.includes('below') || priceText.includes('less than')) {
            const priceMatch = priceText.match(/(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)/i);
            if (priceMatch) {
                const amount = parseFloat(priceMatch[1]);
                const unit = priceMatch[2].toLowerCase();
                
                if (unit === 'cr' || unit === 'crore' || unit === 'crores') {
                    priceDisplay = `Under ₹${amount} Cr`;
                    newFilters.price = `under ${amount} crore`;
                } else {
                    if (amount >= 100) {
                        const crores = (amount / 100).toFixed(1);
                        priceDisplay = `Under ₹${crores} Cr`;
                        newFilters.price = `under ${crores} crore`;
                    } else {
                        priceDisplay = `Under ₹${amount} Lakh`;
                        newFilters.price = `under ${amount} lakh`;
                    }
                }
            }
        } else if (priceText.includes('above') || priceText.includes('more than') || priceText.includes('over')) {
            const priceMatch = priceText.match(/(\d+(?:\.\d+)?)\s*(cr|crore|crores|lakh|lakhs)/i);
            if (priceMatch) {
                const amount = parseFloat(priceMatch[1]);
                const unit = priceMatch[2].toLowerCase();
                
                if (unit === 'cr' || unit === 'crore' || unit === 'crores') {
                    priceDisplay = `Above ₹${amount} Cr`;
                    newFilters.price = `above ${amount} crore`;
                } else {
                    if (amount >= 100) {
                        const crores = (amount / 100).toFixed(1);
                        priceDisplay = `Above ₹${crores} Cr`;
                        newFilters.price = `above ${crores} crore`;
                    } else {
                        priceDisplay = `Above ₹${amount} Lakh`;
                        newFilters.price = `above ${amount} lakh`;
                    }
                }
            }
        }
        
        if (priceDisplay && filters[3]) {
            filters[3].textContent = priceDisplay;
        }
    }
    
    // Carpet area detection (filter[4]) - Replaceable filter
    if (extractedEntities && extractedEntities.carpet_area) {
        console.log('🔍 Carpet area entity found:', extractedEntities.carpet_area);
        console.log('🔍 Full extracted entities:', extractedEntities);
        
        // Use area_value if available (more reliable), otherwise parse from text
        let areaValue = null;
        let areaOperator = null;
        
        if (extractedEntities.area_value) {
            areaValue = extractedEntities.area_value;
            areaOperator = extractedEntities.area_operator || '=';
        } else {
            // Fallback to parsing from text
            const areaText = extractedEntities.carpet_area.toLowerCase();
            
            // Handle various area patterns with better regex
            if (areaText.includes('less than') || areaText.includes('under') || areaText.includes('below')) {
                const areaMatch = areaText.match(/(\d+)(?:\s*sqft|\s*square\s*feet|\s*area)?/i);
                if (areaMatch) {
                    areaValue = parseInt(areaMatch[1]);
                    areaOperator = '<';
                }
            } else if (areaText.includes('more than') || areaText.includes('above') || areaText.includes('over')) {
                const areaMatch = areaText.match(/(\d+)(?:\s*sqft|\s*square\s*feet|\s*area)?/i);
                if (areaMatch) {
                    areaValue = parseInt(areaMatch[1]);
                    areaOperator = '>';
                }
            } else if (areaText.includes('between') || areaText.includes('to') || areaText.includes('-')) {
                // Handle range patterns like "1000-1500 sqft" or "between 1000 to 1500"
                const rangeMatch = areaText.match(/(\d+)(?:\s*[-to]\s*|\s+to\s+)(\d+)(?:\s*sqft|\s*square\s*feet|\s*area)?/i);
                if (rangeMatch) {
                    const minArea = parseInt(rangeMatch[1]);
                    const maxArea = parseInt(rangeMatch[2]);
                    areaValue = `${minArea}-${maxArea}`;
                    areaOperator = 'BETWEEN';
                }
            } else {
                // Fallback: try to extract just the number and assume it's an exact match
                const exactMatch = areaText.match(/(\d+)(?:\s*sqft|\s*square\s*feet|\s*area)?/i);
                if (exactMatch) {
                    areaValue = parseInt(exactMatch[1]);
                    areaOperator = '=';
                }
            }
        }
        
        // Generate display text based on operator and value
        let areaDisplay = '';
        if (areaValue && areaOperator) {
            if (areaOperator === '<') {
                areaDisplay = `Under ${areaValue} sq ft`;
                newFilters.carpet_area = `under ${areaValue} sqft`;
            } else if (areaOperator === '>') {
                areaDisplay = `Above ${areaValue} sq ft`;
                newFilters.carpet_area = `above ${areaValue} sqft`;
            } else if (areaOperator === 'BETWEEN') {
                areaDisplay = `${areaValue} sq ft`;
                newFilters.carpet_area = `${areaValue} sqft`;
            } else {
                areaDisplay = `${areaValue} sq ft`;
                newFilters.carpet_area = `${areaValue} sqft`;
            }
        }
        
        if (areaDisplay && filters[4]) {
            filters[4].textContent = areaDisplay;
        }
    }
    
    // Amenities detection (filter[5]) - Accumulative filter (OR logic)
    if (extractedEntities && extractedEntities.amenities && extractedEntities.amenities.length > 0) {
        const amenities = extractedEntities.amenities;
        // Update display to show all accumulated amenities
        const allAmenities = [...globalFilterState.amenities, ...amenities];
        const uniqueAmenities = [...new Set(allAmenities)];
        if (filters[5]) {
            filters[5].textContent = uniqueAmenities.map(a => a.charAt(0).toUpperCase() + a.slice(1)).join(', ');
        }
        newFilters.amenities = amenities;
    } else if (queryLower.includes('gym') || queryLower.includes('parking') || queryLower.includes('pool') || 
               queryLower.includes('garden') || queryLower.includes('security') || queryLower.includes('lift') ||
               queryLower.includes('swimming pool') || queryLower.includes('concierge') || queryLower.includes('spa')) {
        // Enhanced amenity detection
        const amenityPatterns = [
            'gym', 'parking', 'pool', 'garden', 'security', 'lift', 
            'swimming pool', 'concierge', 'spa', 'fireplace', 'balcony'
        ];
        
        const foundAmenities = [];
        amenityPatterns.forEach(pattern => {
            if (queryLower.includes(pattern)) {
                foundAmenities.push(pattern);
            }
        });
        
        if (foundAmenities.length > 0 && filters[5]) {
            // Update display to show all accumulated amenities
            const allAmenities = [...globalFilterState.amenities, ...foundAmenities];
            const uniqueAmenities = [...new Set(allAmenities)];
            filters[5].textContent = uniqueAmenities.map(a => a.charAt(0).toUpperCase() + a.slice(1)).join(', ');
            newFilters.amenities = foundAmenities;
        }
    } else {
        // If no new amenities found, still update display with existing ones
        if (globalFilterState.amenities.length > 0 && filters[5]) {
            filters[5].textContent = globalFilterState.amenities.map(a => a.charAt(0).toUpperCase() + a.slice(1)).join(', ');
        }
    }
    
    // Status detection (filter[6]) - Replaceable filter
    if (extractedEntities && extractedEntities.status) {
        const statusValue = extractedEntities.status.charAt(0).toUpperCase() + extractedEntities.status.slice(1);
        if (filters[6]) filters[6].textContent = statusValue;
        newFilters.status = extractedEntities.status.toLowerCase();
    } else if (queryLower.includes('available') || queryLower.includes('ready to move') || 
               queryLower.includes('under construction') || queryLower.includes('new launch') ||
               queryLower.includes('premium') || queryLower.includes('luxury') || 
               queryLower.includes('featured') || queryLower.includes('sold')) {
        // Enhanced status detection from query
        const statusPatterns = [
            'available', 'ready to move', 'under construction', 'new launch',
            'premium', 'luxury', 'featured', 'sold'
        ];
        
        const foundStatus = statusPatterns.find(pattern => queryLower.includes(pattern));
        if (foundStatus && filters[6]) {
            const statusValue = foundStatus.charAt(0).toUpperCase() + foundStatus.slice(1);
            filters[6].textContent = statusValue;
            newFilters.status = foundStatus.toLowerCase();
        }
    }
    
    // ROI detection (filter[7]) - Replaceable filter
    if (extractedEntities && extractedEntities.roi && filters[7]) {
        filters[7].textContent = extractedEntities.roi;
        newFilters.roi = extractedEntities.roi;
    }
    
    // Update global filter state
    updateFilterState(newFilters);
    
    // Refresh amenities display to show accumulated values
    if (globalFilterState.amenities.length > 0 && filters[5]) {
        const amenitiesDisplay = globalFilterState.amenities.map(a => a.charAt(0).toUpperCase() + a.slice(1)).join(', ');
        filters[5].textContent = amenitiesDisplay;
    }
    
    // Update suggestive placeholder based on new filter state
    updateSuggestivePlaceholder();
    
    console.log('Filters updated successfully');
    console.log('New filter state:', globalFilterState);
}

// Show property details by navigating to project details page
function showPropertyDetails(property) {
    console.log('Property clicked:', property);
    
    // Prepare the property data for the details page
    const propertyData = {
        id: property.project_id || property.project?.id || property.id, // Use project_id for amenities API
        project_name: property.project_name || property.project || 'Unknown',
        status: property.status || 'Available',
        sell_price: property.sell_price || property.sellPrice || 0,
        price_per_sqft: property.price_per_sqft || property.pricePerSqft || 0,
        bhk_count: property.bhk_count || property.bhkCount || 0,
        carpet_area: property.carpet_area_sqft || property.carpetArea || 0,
        property_type: property.property_type || property.propertyType || 'Property',
        locality: property.location?.locality || property.locality || 'Unknown',
        city: property.location?.city || property.city || 'Unknown',
        amenities: property.amenities || [],
        description: property.description || ''
    };
    
    console.log('Prepared property data:', propertyData);
    
    // Encode the data and navigate to project details page
    const encodedData = encodeURIComponent(JSON.stringify(propertyData));
    console.log('Encoded data:', encodedData);
    window.location.href = `project_details.html?property=${encodedData}`;
}



// New chat functionality - moved to DOMContentLoaded event handler

// Toggle amenities visibility
function toggleAmenities(element, hiddenAmenities) {
    if (element.textContent.includes('more')) {
        // Show all amenities
        const amenitiesContainer = element.parentElement;
        hiddenAmenities.forEach(amenity => {
            const amenityTag = document.createElement('span');
            amenityTag.className = 'amenity-tag';
            amenityTag.textContent = amenity;
            amenitiesContainer.insertBefore(amenityTag, element);
        });
        element.textContent = 'Show less';
        element.style.color = '#ef4444';
    } else {
        // Hide additional amenities
        const amenitiesContainer = element.parentElement;
        const amenityTags = amenitiesContainer.querySelectorAll('.amenity-tag');
        // Keep only first 3 amenities
        for (let i = 3; i < amenityTags.length; i++) {
            amenityTags[i].remove();
        }
        element.textContent = `+${hiddenAmenities.length} more`;
        element.style.color = '#3b82f6';
    }
}



