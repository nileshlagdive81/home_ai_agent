// Sample property data with updated sell_price field
const sampleProperties = [
    {
        id: 1,
        status: "Available",
        imagePath: "images/projects/lodha-park.jpg",
        imageCount: "1/4",
        sellPrice: 8500000, // in rupees (85 lakhs)
        pricePerSqft: 8500, // in rupees per sqft
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

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners
    sendBtn.addEventListener('click', handleChatMessage);
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleChatMessage();
        }
    });

    // Add click handlers for search cards
    document.querySelectorAll('.search-card').forEach(card => {
        card.addEventListener('click', function() {
            const searchText = this.querySelector('p').textContent;
            searchProperties(searchText);
        });
    });

    // Add click handler for contact button
    document.querySelector('.contact-btn').addEventListener('click', function() {
        handleContactClick();
    });
});

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
    // Search properties based on message immediately
    searchProperties(message);
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
        // Call the backend NLP API
        const response = await fetch('http://localhost:8000/api/v1/search/nlp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `query=${encodeURIComponent(query)}`
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
            
            // Update filters based on extracted entities
            updateFiltersFromQuery(query, data.extracted_entities);
        } else {
            // No results found
            propertyGrid.innerHTML = `
                <div class="no-results">
                    <i class="fas fa-search"></i>
                    <h3>No properties found</h3>
                    <p>Your search for "${query}" returned no results.</p>
                    <p>Try adjusting your search criteria:</p>
                    <ul>
                        <li>Check spelling of location names</li>
                        <li>Try different price ranges</li>
                        <li>Use different BHK configurations</li>
                    </ul>
                </div>
            `;
        }
        
        // Log the NLP processing details for debugging
        console.log('NLP Query:', query);
        console.log('NLP Intent:', data.intent);
        console.log('NLP Confidence:', data.confidence);
        console.log('Extracted Entities:', data.extracted_entities);
        console.log('Results Count:', data.results_count);
        
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
    
    // Scroll to top of results
    searchResults.scrollIntoView({ behavior: 'smooth' });
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
    const locality = property.locality || 'Unknown';
    const city = property.city || 'Unknown';
    const projectName = property.project_name || property.project || 'Unknown';
    const status = property.status || 'Available';
    
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
    
    // Format price per sqft in lakhs
    const formatPricePerSqft = (pricePerSqft) => {
        if (!pricePerSqft || pricePerSqft === 0) return 'Price/sq ft on request';
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
        if (bhkCount && propertyType) {
            return `${bhkCount} BHK • ${propertyType}`;
        } else if (bhkCount) {
            return `${bhkCount} BHK`;
        } else if (propertyType) {
            return propertyType;
        }
        return 'Specifications not available';
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
            <div class="property-price">
                <div class="price-main">${formatPrice(sellPrice)}</div>
                <div class="price-per-sqft">${formatPricePerSqft(pricePerSqft)}</div>
            </div>
            <div class="property-specs">${createSpecs()}</div>
            <div class="property-locality">${locality}, ${city}</div>
            <div class="property-amenities">
                <span class="amenity-tag">Basic Amenities</span>
            </div>
            <div class="project-name" style="user-select: none; -webkit-user-select: none; -moz-user-select: none; -ms-user-select: none;">${createProjectName(projectName)}</div>
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
    
    // BHK detection
    if (extractedEntities && extractedEntities.BHK) {
        filters[2].textContent = extractedEntities.BHK;
    } else if (queryLower.includes('2-bedroom') || queryLower.includes('2 bed') || queryLower.includes('2bhk')) {
        filters[2].textContent = '2 BHK';
    } else if (queryLower.includes('3-bedroom') || queryLower.includes('3 bed') || queryLower.includes('3bhk')) {
        filters[2].textContent = '3 BHK';
    } else if (queryLower.includes('1-bedroom') || queryLower.includes('1 bed') || queryLower.includes('1bhk')) {
        filters[2].textContent = '1 BHK';
    } else if (queryLower.includes('4-bedroom') || queryLower.includes('4 bed') || queryLower.includes('4bhk')) {
        filters[2].textContent = '4 BHK';
    }
    
    // Enhanced price intent detection
    if (extractedEntities && extractedEntities.Price) {
        filters[3].textContent = extractedEntities.Price;
    } else if (queryLower.includes('under') || queryLower.includes('below') || queryLower.includes('less than')) {
        // Extract price from query
        const priceMatch = queryLower.match(/(\d+(?:\.\d+)?)\s*(lakh|lac|cr|crore|million|k)/i);
        if (priceMatch) {
            const amount = parseFloat(priceMatch[1]);
            const unit = priceMatch[2].toLowerCase();
            
            let priceInLakhs;
            if (unit === 'cr' || unit === 'crore') {
                priceInLakhs = amount * 100;
            } else if (unit === 'million') {
                priceInLakhs = amount * 10;
            } else if (unit === 'k') {
                priceInLakhs = amount / 100;
            } else {
                priceInLakhs = amount;
            }
            
            filters[3].textContent = `Under ₹${priceInLakhs} Lakh`;
        } else {
            filters[3].textContent = 'Price Filter Applied';
        }
    } else if (queryLower.includes('above') || queryLower.includes('more than') || queryLower.includes('over')) {
        const priceMatch = queryLower.match(/(\d+(?:\.\d+)?)\s*(lakh|lac|cr|crore|million|k)/i);
        if (priceMatch) {
            const amount = parseFloat(priceMatch[1]);
            const unit = priceMatch[2].toLowerCase();
            
            let priceInLakhs;
            if (unit === 'cr' || unit === 'crore') {
                priceInLakhs = amount * 100;
            } else if (unit === 'million') {
                priceInLakhs = amount * 10;
            } else if (unit === 'k') {
                priceInLakhs = amount / 100;
            } else {
                priceInLakhs = amount;
            }
            
            filters[3].textContent = `Above ₹${priceInLakhs} Lakh`;
        } else {
            filters[3].textContent = 'Price Filter Applied';
        }
    } else if (queryLower.includes('between') || queryLower.includes('range')) {
        filters[3].textContent = 'Price Range Applied';
    }
    
    // Property type detection
    if (extractedEntities && extractedEntities.PropertyType) {
        filters[4].textContent = extractedEntities.PropertyType;
    } else if (queryLower.includes('apartment') || queryLower.includes('flat')) {
        // Could add property type filter here
    } else if (queryLower.includes('house') || queryLower.includes('villa')) {
        // Could add property type filter here
    }
    
    // Location detection
    if (extractedEntities && extractedEntities.Location) {
        filters[0].textContent = extractedEntities.Location;
    } else if (queryLower.includes('pune') || queryLower.includes('mumbai') || queryLower.includes('bangalore')) {
        filters[0].textContent = queryLower.match(/(pune|mumbai|bangalore)/i)[0];
    }
    
    if (extractedEntities && extractedEntities.Locality) {
        filters[1].textContent = extractedEntities.Locality;
    } else if (queryLower.includes('baner') || queryLower.includes('hinjewadi') || queryLower.includes('wakad')) {
        filters[1].textContent = queryLower.match(/(baner|hinjewadi|wakad)/i)[0];
    }
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
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
});


