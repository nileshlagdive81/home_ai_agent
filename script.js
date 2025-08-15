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

// Header scroll effect
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners
    sendBtn.addEventListener('click', handleChatMessage);
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleChatMessage();
        }
    });

    // Add focus/blur event listeners for suggestive placeholder
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

    // Add click handlers for search cards
    document.querySelectorAll('.search-card').forEach(card => {
        card.addEventListener('click', function() {
            const searchText = this.querySelector('p').textContent;
            searchProperties(searchText);
        });
    });

    // Add click handler for New Query button
    document.querySelector('.new-chat-btn').addEventListener('click', function() {
        handleNewQuery();
    });

    // Add click handler for contact button
    document.querySelector('.contact-btn').addEventListener('click', function() {
        handleContactClick();
    });
    
    // Set initial suggestive placeholder
    updateSuggestivePlaceholder();
});

// Function to update the suggestive placeholder
function updateSuggestivePlaceholder() {
    const suggestion = generateSuggestiveQueries(globalFilterState);
    chatInput.placeholder = suggestion;
}

// Handle chat messages
function handleChatMessage() {
    const message = chatInput.value.trim();
    if (message) {
        // Add user message to chat
        addUserMessage(message);
        // Simulate AI response
        simulateAIResponse(message);
        chatInput.value = '';
    }
}

// Simulate AI response and search
function simulateAIResponse(message) {
    const messageLower = message.toLowerCase().trim();
    
    // Check if message is a casual greeting or non-property query
    const casualMessages = [
        'hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening',
        'how are you', 'thanks', 'thank you', 'bye', 'goodbye', 'see you',
        'ok', 'okay', 'yes', 'no', 'maybe', 'sure', 'alright'
    ];
    
    // Check if message contains property-related keywords
    const propertyKeywords = [
        'bhk', 'bedroom', 'apartment', 'house', 'property', 'flat', 'villa',
        'pune', 'mumbai', 'bangalore', 'baner', 'hinjewadi', 'wakad', 'thane',
        'price', 'crore', 'lakh', 'sqft', 'sq ft', 'square feet',
        'gym', 'parking', 'pool', 'garden', 'security', 'lift',
        'available', 'luxury', 'premium', 'new', 'ready', 'under construction'
    ];
    
    const isCasualMessage = casualMessages.some(casual => messageLower === casual);
    const hasPropertyKeywords = propertyKeywords.some(keyword => messageLower.includes(keyword));
    
    if (isCasualMessage && !hasPropertyKeywords) {
        // Handle casual messages with friendly responses
        addAIMessage(`Hello! 👋 I'm here to help you find your perfect property. Try asking me about properties, like:<br>
• "2 BHK apartments in Pune"<br>
• "Properties under 1 crore"<br>
• "Homes with gym facility"`);
    } else {
        // Search properties for property-related queries
        searchProperties(message);
    }
}

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
    chatInput.value = '';
    
    // Update suggestive placeholder
    updateSuggestivePlaceholder();
    
    // Don't scroll - keep header visible
    // window.scrollTo({ top: 0, behavior: 'smooth' });
    
    console.log('New Query completed - state reset');
}



// Add AI message to chat
function addAIMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'assistant-message';
    messageDiv.innerHTML = `
        <div class="message-icon">
            <i class="fas fa-check"></i>
        </div>
        <p>${message}</p>
    `;
    
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
    // Hide landing content and show search results
    landingContent.style.display = 'none';
    searchResults.style.display = 'block';
    
    // Show filters bar
    document.getElementById('filtersBar').style.display = 'flex';
    
    // Show loading state
    resultCount.textContent = 'Searching...';
    propertyGrid.innerHTML = '<div class="loading">🔍 Processing your query...</div>';
    
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
        
        // Update result count with actual results
        resultCount.textContent = data.results_count;
        
        // Display the actual results from the API
        if (data.results && data.results.length > 0) {
            displayProperties(data.results);
            
            // Update filters based on extracted entities and maintain state
            updateFiltersFromQuery(query, data.extracted_entities);
        } else {
            // No results found - provide AI-powered suggestions
            const suggestions = generateAISuggestions(query, globalFilterState);
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
        resultCount.textContent = sampleProperties.length;
        displayProperties(sampleProperties);
        
        // Show error message
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
    
    // Don't scroll - keep header visible
    // searchResults.scrollIntoView({ behavior: 'smooth' });
}

// Display properties in the grid
function displayProperties(properties) {
    propertyGrid.innerHTML = '';
    
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
    
    // Global price formatting function for consistency
    window.formatPriceForDisplay = (sellPrice) => {
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
    
    card.innerHTML = `
        <div class="property-image">
            <div class="status-tag">${status}</div>
            <div class="image-placeholder">
                <i class="fas fa-building"></i>
            </div>
            <div class="image-counter">1/1</div>
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
    const queryLower = query.toLowerCase();
    
    console.log('Updating filters with extracted entities:', extractedEntities);
    
    // Prepare new filter values to update state
    const newFilters = {};
    
    // City detection (filter[0]) - Persistent filter
    if (extractedEntities && extractedEntities.city) {
        const cityValue = extractedEntities.city.charAt(0).toUpperCase() + extractedEntities.city.slice(1);
        filters[0].textContent = cityValue;
        newFilters.city = extractedEntities.city.toLowerCase();
    } else if (queryLower.includes('pune') || queryLower.includes('mumbai') || queryLower.includes('bangalore')) {
        const cityMatch = queryLower.match(/(pune|mumbai|bangalore)/i);
        if (cityMatch) {
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
        filters[1].textContent = capitalizedLocality;
        newFilters.locality = extractedEntities.locality.toLowerCase();
    } else if (queryLower.includes('baner') || queryLower.includes('hinjewadi') || queryLower.includes('wakad') || 
               queryLower.includes('thane west') || queryLower.includes('bandra west') || queryLower.includes('viman nagar')) {
        const localityMatch = queryLower.match(/(baner|hinjewadi|wakad|thane west|bandra west|viman nagar)/i);
        if (localityMatch) {
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
        filters[2].textContent = `${extractedEntities.bhk} BHK`;
        newFilters.bhk = extractedEntities.bhk.toString();
    } else if (queryLower.includes('2-bedroom') || queryLower.includes('2 bed') || queryLower.includes('2bhk')) {
        filters[2].textContent = '2 BHK';
        newFilters.bhk = '2';
    } else if (queryLower.includes('3-bedroom') || queryLower.includes('3 bed') || queryLower.includes('3bhk')) {
        filters[2].textContent = '3 BHK';
        newFilters.bhk = '3';
    } else if (queryLower.includes('1-bedroom') || queryLower.includes('1 bed') || queryLower.includes('1bhk')) {
        filters[2].textContent = '1 BHK';
        newFilters.bhk = '1';
    } else if (queryLower.includes('4-bedroom') || queryLower.includes('4 bed') || queryLower.includes('4bhk')) {
        filters[2].textContent = '4 BHK';
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
        
        if (priceDisplay) {
            filters[3].textContent = priceDisplay;
        }
    }
    
    // Carpet area detection (filter[4]) - Replaceable filter
    if (extractedEntities && extractedEntities.carpet_area) {
        const areaText = extractedEntities.carpet_area.toLowerCase();
        let areaDisplay = '';
        
        if (areaText.includes('less than') || areaText.includes('under') || areaText.includes('below')) {
            const areaMatch = areaText.match(/(\d+)\s*sqft/i);
            if (areaMatch) {
                const areaValue = parseInt(areaMatch[1]);
                areaDisplay = `Under ${areaValue} sq ft`;
                newFilters.carpet_area = `under ${areaValue} sqft`;
            }
        } else if (areaText.includes('more than') || areaText.includes('above') || areaText.includes('over')) {
            const areaMatch = areaText.match(/(\d+)\s*sqft/i);
            if (areaMatch) {
                const areaValue = parseInt(areaMatch[1]);
                areaDisplay = `Above ${areaValue} sq ft`;
                newFilters.carpet_area = `above ${areaValue} sqft`;
            }
        }
        
        if (areaDisplay) {
            filters[4].textContent = areaDisplay;
        }
    }
    
    // Amenities detection (filter[5]) - Accumulative filter (OR logic)
    if (extractedEntities && extractedEntities.amenities && extractedEntities.amenities.length > 0) {
        const amenities = extractedEntities.amenities;
        // Update display to show all accumulated amenities
        const allAmenities = [...globalFilterState.amenities, ...amenities];
        const uniqueAmenities = [...new Set(allAmenities)];
        filters[5].textContent = uniqueAmenities.map(a => a.charAt(0).toUpperCase() + a.slice(1)).join(', ');
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
        
        if (foundAmenities.length > 0) {
            // Update display to show all accumulated amenities
            const allAmenities = [...globalFilterState.amenities, ...foundAmenities];
            const uniqueAmenities = [...new Set(allAmenities)];
            filters[5].textContent = uniqueAmenities.map(a => a.charAt(0).toUpperCase() + a.slice(1)).join(', ');
            newFilters.amenities = foundAmenities;
        }
    } else {
        // If no new amenities found, still update display with existing ones
        if (globalFilterState.amenities.length > 0) {
            filters[5].textContent = globalFilterState.amenities.map(a => a.charAt(0).toUpperCase() + a.slice(1)).join(', ');
        }
    }
    
    // Status detection (filter[6]) - Replaceable filter
    if (extractedEntities && extractedEntities.status) {
        const statusValue = extractedEntities.status.charAt(0).toUpperCase() + extractedEntities.status.slice(1);
        filters[6].textContent = statusValue;
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
        if (foundStatus) {
            const statusValue = foundStatus.charAt(0).toUpperCase() + foundStatus.slice(1);
            filters[6].textContent = statusValue;
            newFilters.status = foundStatus.toLowerCase();
        }
    }
    
    // ROI detection (filter[7]) - Replaceable filter
    if (extractedEntities && extractedEntities.roi) {
        filters[7].textContent = extractedEntities.roi;
        newFilters.roi = extractedEntities.roi;
    }
    
    // Update global filter state
    updateFilterState(newFilters);
    
    // Refresh amenities display to show accumulated values
    if (globalFilterState.amenities.length > 0) {
        const amenitiesDisplay = globalFilterState.amenities.map(a => a.charAt(0).toUpperCase() + a.slice(1)).join(', ');
        filters[5].textContent = amenitiesDisplay;
    }
    
    // Update suggestive placeholder based on new filter state
    updateSuggestivePlaceholder();
    
    console.log('Filters updated successfully');
    console.log('New filter state:', globalFilterState);
}

// Show property details (placeholder for future enhancement)
function showPropertyDetails(property) {
    alert(`Property Details: ${property.specs}\nPrice: ${property.price}\nAddress: ${property.address}`);
    // In a real application, this would open a modal or navigate to a detail page
}

// Handle contact button click
function handleContactClick() {
    // You can customize this to show contact form, open modal, or navigate to contact page
    alert('Contact Us\n\nPhone: +91 98765 43210\nEmail: info@prontohomes.com\nAddress: Pune, Maharashtra\n\nWe\'ll get back to you within 24 hours!');
}

// New chat functionality
document.querySelector('.new-chat-btn').addEventListener('click', function() {
    // Clear chat and reset to landing page
    landingContent.style.display = 'block';
    searchResults.style.display = 'none';
    
    // Hide filters bar
    document.getElementById('filtersBar').style.display = 'none';
    
    // Clear ALL chat messages including the initial AI message
    const aiAssistant = document.querySelector('.ai-assistant');
    const allMessages = aiAssistant.querySelectorAll('.assistant-message, .user-message');
    allMessages.forEach(msg => msg.remove());
    
    // Reset filters
    const filters = document.querySelectorAll('.filter-value');
    filters.forEach(filter => filter.textContent = '—');
    
    // Clear chat input
    chatInput.value = '';
    
    // Don't scroll - keep header visible
    // window.scrollTo({ top: 0, behavior: 'smooth' });
});

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


