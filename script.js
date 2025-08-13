// Sample property data
const sampleProperties = [
    {
        id: 1,
        status: "Available",
        imageClass: "blue",
        imageIcon: "fas fa-building",
        imageCount: "1/4",
        price: "$1,850/month",
        pricePerSqft: "$1.54/sqft",
        specs: "2 bed • 2 bath • 1,200 sq ft • Apartment",
        address: "123 Main Street, Downtown District, NY 10001",
        project: "Project: Sky",
        amenities: ["Gym", "Parking", "Pet-friendly"],
        moreAmenities: 3
    },
    {
        id: 2,
        status: "New Listing",
        imageClass: "green",
        imageIcon: "fas fa-home",
        imageCount: "1/4",
        price: "$2,400/month",
        pricePerSqft: "$1.33/sqft",
        specs: "3 bed • 2 bath • 1,800 sq ft • House",
        address: "456 Oak Avenue, Suburban Area, NY 10002",
        project: "Project: Gre",
        amenities: ["Garden", "Garage", "Fireplace"],
        moreAmenities: 2
    },
    {
        id: 3,
        status: "Premium",
        imageClass: "yellow",
        imageIcon: "fas fa-city",
        imageCount: "1/5",
        price: "$4,500/month",
        pricePerSqft: "$1.80/sqft",
        specs: "3 bed • 3 bath • 2,500 sq ft • Penthouse",
        address: "789 Park Avenue, City Center, NY 10003",
        project: "Project: Man",
        amenities: ["Balcony", "Concierge", "Pool"],
        moreAmenities: 3
    },
    {
        id: 4,
        status: "Available",
        imageClass: "blue",
        imageIcon: "fas fa-building",
        imageCount: "1/3",
        price: "$1,600/month",
        pricePerSqft: "$1.20/sqft",
        specs: "1 bed • 1 bath • 800 sq ft • Studio",
        address: "321 Elm Street, Arts District, NY 10004",
        project: "Project: Urban",
        amenities: ["Gym", "Laundry", "Storage"],
        moreAmenities: 1
    },
    {
        id: 5,
        status: "Featured",
        imageClass: "green",
        imageIcon: "fas fa-home",
        imageCount: "1/6",
        price: "$3,200/month",
        pricePerSqft: "$1.45/sqft",
        specs: "4 bed • 3 bath • 2,200 sq ft • Townhouse",
        address: "654 Pine Street, Historic District, NY 10005",
        project: "Project: Heritage",
        amenities: ["Garden", "Patio", "Fireplace", "Garage"],
        moreAmenities: 2
    },
    {
        id: 6,
        status: "Luxury",
        imageClass: "yellow",
        imageIcon: "fas fa-crown",
        imageCount: "1/8",
        price: "$8,500/month",
        pricePerSqft: "$2.50/sqft",
        specs: "5 bed • 4 bath • 3,400 sq ft • Mansion",
        address: "987 Luxury Lane, Exclusive Area, NY 10006",
        project: "Project: Elite",
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
function searchProperties(query) {
    // Hide landing content and show search results
    landingContent.style.display = 'none';
    searchResults.style.display = 'block';
    
    // Show filters bar
    document.getElementById('filtersBar').style.display = 'flex';
    
    // Update result count
    resultCount.textContent = sampleProperties.length;
    
    // Display properties
    displayProperties(sampleProperties);
    
    // Update filters based on query (simplified)
    updateFiltersFromQuery(query);
    
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
    
    // Modify project name to add *** after 4th character
    const modifiedProject = property.project.length > 4 
        ? property.project.substring(0, 4) + '***' + property.project.substring(4)
        : property.project + '***';
    
    card.innerHTML = `
        <div class="property-image ${property.imageClass}">
            <div class="status-tag">${property.status}</div>
            <i class="${property.imageIcon}"></i>
            <div class="image-counter">${property.imageCount}</div>
        </div>
        <div class="property-details">
            <div class="property-price">
                <div class="price-main">${property.price}</div>
                <div class="price-per-sqft">${property.pricePerSqft}</div>
            </div>
            <div class="property-specs">${property.specs}</div>
            <div class="property-address">${property.address}</div>
            <div class="project-name">${modifiedProject}</div>
            <div class="property-amenities">
                ${property.amenities.map(amenity => 
                    `<span class="amenity-tag">${amenity}</span>`
                ).join('')}
                <span class="amenity-more">+${property.moreAmenities} more</span>
            </div>
        </div>
    `;
    
    // Add click handler for property card
    card.addEventListener('click', () => {
        showPropertyDetails(property);
    });
    
    return card;
}

// Update filters based on search query
function updateFiltersFromQuery(query) {
    const filters = document.querySelectorAll('.filter-value');
    
    // Simple keyword matching for demo purposes
    if (query.toLowerCase().includes('2-bedroom') || query.toLowerCase().includes('2 bed')) {
        filters[2].textContent = '2 BHK'; // BHK filter
    }
    if (query.toLowerCase().includes('under $2000')) {
        filters[3].textContent = 'Under $2000'; // Price filter
    }
    if (query.toLowerCase().includes('apartment')) {
        // Could add property type filter here
    }
}

// Show property details (placeholder for future enhancement)
function showPropertyDetails(property) {
    alert(`Property Details: ${property.specs}\nPrice: ${property.price}\nAddress: ${property.address}`);
    // In a real application, this would open a modal or navigate to a detail page
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


