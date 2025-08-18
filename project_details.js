// Project Details Page JavaScript
// Handles accordion functionality, modal display, and dynamic content

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initializeAccordion();
    initializeModal();
    initializeViewDetailsButtons();
    initializeContactButtons();
    initializeChatInterface();
    
    // Load property data from URL parameters
    loadPropertyData();
});

// Initialize chat interface functionality
function initializeChatInterface() {
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.querySelector('.send-btn');
    const newChatBtn = document.querySelector('.new-chat-btn');
    
    if (chatInput && sendBtn) {
        // Handle send button click
        sendBtn.addEventListener('click', () => {
            handleChatMessage();
        });
        
        // Handle Enter key press
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleChatMessage();
            }
        });
        
        // Auto-resize textarea
        chatInput.addEventListener('input', () => {
            chatInput.style.height = 'auto';
            chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + 'px';
        });
    }
    
    if (newChatBtn) {
        newChatBtn.addEventListener('click', () => {
            startNewChat();
        });
    }
}

// Handle chat message submission
function handleChatMessage() {
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addUserMessage(message);
    
    // Clear input
    chatInput.value = '';
    chatInput.style.height = 'auto';
    
    // Simulate AI response
    simulateAIResponse(message);
}

// Add user message to chat
function addUserMessage(message) {
    const chatContainer = document.querySelector('.chat-container');
    const userMessage = document.createElement('div');
    userMessage.className = 'user-message';
    userMessage.innerHTML = `
        <div class="message-content">
            <p>${message}</p>
        </div>
    `;
    
    // Insert before the message input
    const messageInput = document.querySelector('.message-input');
    chatContainer.insertBefore(userMessage, messageInput);
    
    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Simulate AI response
async function simulateAIResponse(message) {
    // Fast-path: redirect property-like queries directly to main search page
    const looksLikePropertyFast = /(\bbhk\b|bedroom|apartment|house|flat|property|price|area|location|\bpune\b|\bmumbai\b|baner|hinjewadi|crore|lakh)/i.test(message);
    if (looksLikePropertyFast) {
        window.location.href = `index.html?search=${encodeURIComponent(message)}`;
        return;
    }

    const chatContainer = document.querySelector('.chat-container');
    
    // Add typing indicator
    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'typing-indicator';
    typingIndicator.innerHTML = `
        <div class="typing-dots">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;
    
    const messageInput = document.querySelector('.message-input');
    chatContainer.insertBefore(typingIndicator, messageInput);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    try {
        // Send message to backend for processing
        const response = await fetch('/api/v1/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: message })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        // Remove typing indicator
        if (typingIndicator.parentNode) {
            typingIndicator.parentNode.removeChild(typingIndicator);
        }
        
        // Check if this is a property search query
        if (result.success && result.properties && result.properties.length > 0) {
            // Redirect to main search page quickly
            window.location.href = `index.html?search=${encodeURIComponent(message)}`;
            return;
            
        } else if (result.success && result.message) {
            // General message
            addAIMessage(result);
        } else {
            // No results or error
            const looksLikeProperty = /(\bbhk\b|bedroom|apartment|house|flat|property|price|area|location|\bpune\b|\bmumbai\b|baner|hinjewadi|crore|lakh)/i.test(message);
            if (looksLikeProperty) {
                window.location.href = `index.html?search=${encodeURIComponent(message)}`;
                return;
            }
            addAIMessage({ success: false, message: 'No relevant information found.' });
        }
        
    } catch (error) {
        console.error('Error processing message:', error);
        
        // Remove typing indicator
        if (typingIndicator.parentNode) {
            typingIndicator.parentNode.removeChild(typingIndicator);
        }
        
        // Check if this looks like a property search query
        const isPropertySearch = /(\bbhk\b|bedroom|apartment|house|flat|property|price|area|location|\bpune\b|\bmumbai\b|baner|hinjewadi|crore|lakh)/i.test(message);
        
        if (isPropertySearch) {
            // Property-like query: redirect immediately without showing an error
            window.location.href = `index.html?search=${encodeURIComponent(message)}`;
            return;
        } else {
            // General message - show error
            addAIMessage({
                success: false,
                message: 'I encountered an error processing your request. Please try again or go to the main search page to search for properties.',
                isPropertySearch: false
            });
        }
    }
}

// Add AI message to chat
function addAIMessage(result) {
    const chatContainer = document.querySelector('.chat-container');
    const aiMessage = document.createElement('div');
    aiMessage.className = 'assistant-message';
    
    if (result.success && result.properties && result.properties.length > 0 && result.isPropertySearch) {
        // Property search results - show redirect message
        aiMessage.innerHTML = `
            <div class="message-content">
                <p><strong>${result.message}</strong></p>
                <div class="property-preview">
                    <p>Here's a preview of what you'll find:</p>
                    ${result.properties.slice(0, 3).map(prop => `
                        <div class="preview-item">
                            <strong>${prop.project_name || prop.project || 'Unknown'}</strong> - 
                            ${prop.bhk_count || prop.bhkCount || 'N/A'} BHK, 
                            ₹${(prop.sell_price || prop.sellPrice || 0) / 100000} Lakh
                        </div>
                    `).join('')}
                    ${result.properties.length > 3 ? `<p>... and ${result.properties.length - 3} more properties</p>` : ''}
                </div>
                <p><em>You'll be redirected to the main search page in a few seconds to view all results.</em></p>
            </div>
        `;
    } else if (result.success && result.properties && result.properties.length > 0) {
        // Property search results (fallback)
        aiMessage.innerHTML = `
            <div class="message-content">
                <p><strong>Found ${result.properties.length} properties matching your criteria:</strong></p>
                <div class="property-preview">
                    ${result.properties.slice(0, 3).map(prop => `
                        <div class="preview-item">
                            <strong>${prop.project_name || prop.project || 'Unknown'}</strong> - 
                            ${prop.bhk_count || prop.bhkCount || 'N/A'} BHK, 
                            ₹${(prop.sell_price || prop.sellPrice || 0) / 100000} Lakh
                        </div>
                    `).join('')}
                    ${result.properties.length > 3 ? `<p>... and ${result.properties.length - 3} more properties</p>` : ''}
                </div>
                <p><em>Click <a href="index.html?search=${encodeURIComponent(result.query || '')}" style="color: #2563eb; text-decoration: underline;">here</a> to view all results on the main search page.</em></p>
            </div>
        `;
    } else if (result.isPropertySearch) {
        // Property search with no results or error - show redirect message
        aiMessage.innerHTML = `
            <div class="message-content">
                <p><strong>${result.message}</strong></p>
                <p><em>You'll be redirected to the main search page in a few seconds where you can refine your search.</em></p>
            </div>
        `;
    } else if (result.message) {
        // General message
        aiMessage.innerHTML = `
            <div class="message-content">
                <p>${result.message}</p>
            </div>
        `;
    } else {
        // No results
        aiMessage.innerHTML = `
            <div class="message-content">
                <p>No properties found matching your criteria. Try adjusting your search parameters.</p>
                <p><em>You can also go to the <a href="index.html" style="color: #2563eb; text-decoration: underline;">main search page</a> to explore more options.</em></p>
            </div>
        `;
    }
    
    // Insert before the message input
    const messageInput = document.querySelector('.message-input');
    chatContainer.insertBefore(aiMessage, messageInput);
    
    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Start new chat
function startNewChat() {
    const chatContainer = document.querySelector('.chat-container');
    const messages = chatContainer.querySelectorAll('.user-message, .assistant-message');
    
    // Remove all messages except the initial AI assistant message
    messages.forEach(message => {
        if (!message.querySelector('.ai-assistant')) {
            message.remove();
        }
    });
    
    // Clear input
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.value = '';
        chatInput.style.height = 'auto';
    }
    
    // Scroll to top
    chatContainer.scrollTop = 0;
}

// Accordion functionality for expandable sections
function initializeAccordion() {
    const accordionItems = document.querySelectorAll('.accordion-item');
    
    accordionItems.forEach(item => {
        const header = item.querySelector('.accordion-header');
        const content = item.querySelector('.accordion-content');
        
        header.addEventListener('click', () => {
            const isActive = item.classList.contains('active');
            
            // Close all other accordion items
            accordionItems.forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.classList.remove('active');
                }
            });
            
            // Toggle current item
            if (isActive) {
                item.classList.remove('active');
            } else {
                item.classList.add('active');
            }
        });
    });
}

// Modal functionality for BHK configuration details
function initializeModal() {
    const modal = document.getElementById('bhkModal');
    const closeBtn = document.querySelector('.close-modal');
    
    // Close modal when clicking on close button
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            closeModal();
        });
    }
    
    // Close modal when clicking outside
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal();
            }
        });
    }
    
    // Close modal with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.style.display === 'block') {
            closeModal();
        }
    });
}

// Initialize view details buttons
function initializeViewDetailsButtons() {
    const viewDetailsButtons = document.querySelectorAll('.view-details-btn');
    
    viewDetailsButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const bhkType = button.getAttribute('data-bhk');
            showBHKModal(bhkType);
        });
    });
}

// Initialize contact buttons
function initializeContactButtons() {
    const contactBtn = document.querySelector('.contact-btn');
    const scheduleBtn = document.querySelector('.schedule-btn');
    
    if (contactBtn) {
        contactBtn.addEventListener('click', () => {
            handleContactClick();
        });
    }
    
    if (scheduleBtn) {
        scheduleBtn.addEventListener('click', () => {
            handleScheduleClick();
        });
    }
}

// Show BHK configuration modal
function showBHKModal(bhkType) {
    const modal = document.getElementById('bhkModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalArea = document.getElementById('modalArea');
    const modalPrice = document.getElementById('modalPrice');
    const modalCarpetArea = document.getElementById('modalCarpetArea');
    const modalRoomList = document.getElementById('modalRoomList');
    const modalFeatures = document.getElementById('modalFeatures');
    const modalCtaText = document.getElementById('modalCtaText');
    
    // Get BHK configuration data
    const bhkConfig = getBHKConfiguration(bhkType);
    
    if (bhkConfig) {
        // Update modal content
        modalTitle.textContent = `${bhkType} BHK - ${bhkConfig.title}`;
        modalArea.textContent = `${bhkConfig.area} sq ft`;
        modalPrice.textContent = `${bhkConfig.price} onwards`;
        modalCarpetArea.textContent = `${bhkConfig.area} sq ft carpet area`;
        modalCtaText.textContent = `Interested in this ${bhkType} BHK configuration?`;
        
        // Populate room specifications
        populateRoomList(modalRoomList, bhkConfig.rooms);
        
        // Populate features
        populateFeatures(modalFeatures, bhkConfig.features);
        
        // Show modal
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }
}

// Close modal
function closeModal() {
    const modal = document.getElementById('bhkModal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto'; // Restore scrolling
}

// Get BHK configuration data
function getBHKConfiguration(bhkType) {
    const configurations = {
        '3': {
            title: 'Spacious Luxury',
            area: '1,250',
            price: '₹5.2 Cr',
            rooms: [
                { name: 'Master Bedroom', dimensions: '14\' x 12\'' },
                { name: 'Second Bedroom', dimensions: '12\' x 10\'' },
                { name: 'Third Bedroom', dimensions: '12\' x 10\'' },
                { name: 'Living Room', dimensions: '16\' x 14\'' },
                { name: 'Kitchen', dimensions: '10\' x 8\'' },
                { name: 'Master Bathroom', dimensions: '8\' x 6\'' },
                { name: 'Second Bathroom', dimensions: '6\' x 5\'' },
                { name: 'Balcony', dimensions: '10\' x 4\'' }
            ],
            features: [
                'Premium modular kitchen with granite countertop',
                'Master bedroom with built-in wardrobe',
                'Living area with garden view',
                'Vitrified tile flooring throughout',
                'Multiple balconies with city views',
                'Separate dining area',
                'Attached bathroom in master bedroom',
                'Study area in second bedroom'
            ]
        },
        '4': {
            title: 'Ultimate Prestige',
            area: '1,650',
            price: '₹7.8 Cr',
            rooms: [
                { name: 'Master Bedroom', dimensions: '16\' x 14\'' },
                { name: 'Second Bedroom', dimensions: '14\' x 12\'' },
                { name: 'Third Bedroom', dimensions: '12\' x 10\'' },
                { name: 'Fourth Bedroom', dimensions: '12\' x 10\'' },
                { name: 'Living Room', dimensions: '18\' x 16\'' },
                { name: 'Kitchen', dimensions: '12\' x 10\'' },
                { name: 'Master Bathroom', dimensions: '10\' x 8\'' },
                { name: 'Second Bathroom', dimensions: '8\' x 6\'' },
                { name: 'Third Bathroom', dimensions: '6\' x 5\'' },
                { name: 'Balcony', dimensions: '12\' x 4\'' }
            ],
            features: [
                'Premium modular kitchen with granite countertop',
                'Master bedroom with built-in wardrobe and walk-in closet',
                'Living area with panoramic city & sea views',
                'Premium marble flooring throughout',
                'Private terrace garden',
                'Separate dining area',
                'Entertainment area in living room',
                'Utility area in kitchen',
                'Store room',
                'Jacuzzi in master bathroom'
            ]
        }
    };
    
    return configurations[bhkType];
}

// Populate room list in modal
function populateRoomList(container, rooms) {
    container.innerHTML = '';
    
    rooms.forEach(room => {
        const roomItem = document.createElement('div');
        roomItem.className = 'room-item';
        roomItem.innerHTML = `
            <span>${room.name}</span>
            <span>${room.dimensions}</span>
        `;
        container.appendChild(roomItem);
    });
}

// Populate features in modal
function populateFeatures(container, features) {
    container.innerHTML = '';
    
    features.forEach(feature => {
        const featureItem = document.createElement('div');
        featureItem.className = 'feature-item';
        featureItem.textContent = feature;
        container.appendChild(featureItem);
    });
}

// Handle contact button click
function handleContactClick() {
    // You can implement contact functionality here
    // For now, we'll show an alert
    alert('Contact functionality will be implemented here.\n\nYou can:\n- Add a contact form\n- Integrate with a CRM\n- Add phone number display\n- Add email contact');
}

// Handle schedule appointment button click
function handleScheduleClick() {
    // You can implement scheduling functionality here
    // For now, we'll show an alert
    alert('Schedule Appointment functionality will be implemented here.\n\nYou can:\n- Add a calendar integration\n- Add a booking form\n- Integrate with scheduling services\n- Add availability checking');
}

// Handle call for site visit button click
function handleCallForSiteVisit() {
    // You can implement call functionality here
    // For now, we'll show an alert
    alert('Call for Site Visit functionality will be implemented here.\n\nYou can:\n- Add phone number display\n- Integrate with calling services\n- Add contact form\n- Add WhatsApp integration');
}

// Handle get brochure button click
function handleGetBrochure() {
    // You can implement brochure download functionality here
    // For now, we'll show an alert
    alert('Get Brochure functionality will be implemented here.\n\nYou can:\n- Add PDF download\n- Add email form\n- Integrate with document services\n- Add preview functionality');
}

// Add event listeners to modal action buttons
document.addEventListener('DOMContentLoaded', function() {
    // These need to be added after the modal content is dynamically created
    setTimeout(() => {
        const primaryBtn = document.querySelector('.primary-btn');
        const secondaryBtn = document.querySelector('.secondary-btn');
        
        if (primaryBtn) {
            primaryBtn.addEventListener('click', handleCallForSiteVisit);
        }
        
        if (secondaryBtn) {
            secondaryBtn.addEventListener('click', handleGetBrochure);
        }
    }, 100);
});

// Utility function to format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

// Utility function to format area
function formatArea(area) {
    return `${area.toLocaleString()} sq ft`;
}

// Add smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Add loading states for buttons
function addLoadingState(button, text = 'Loading...') {
    const originalText = button.innerHTML;
    button.innerHTML = `<i class="fas fa-spinner fa-spin"></i> ${text}`;
    button.disabled = true;
    return () => {
        button.innerHTML = originalText;
        button.disabled = false;
    };
}

// Add success/error notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;
    
    // Add notification styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#059669' : type === 'error' ? '#dc2626' : '#2563eb'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        z-index: 10000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 5000);
}

// Load and display property data from URL parameters
function loadPropertyData() {
    console.log('Loading property data from URL...');
    const urlParams = new URLSearchParams(window.location.search);
    const propertyParam = urlParams.get('property');
    
    console.log('URL parameters:', window.location.search);
    console.log('Property parameter:', propertyParam);
    
    if (!propertyParam) {
        console.log('No property data found in URL parameters');
        return;
    }
    
    try {
        const propertyData = JSON.parse(decodeURIComponent(propertyParam));
        console.log('Loaded property data:', propertyData);
        
        // Populate the page with property data
        populatePropertyDetails(propertyData);
        
    } catch (error) {
        console.error('Error parsing property data:', error);
        showNotification('Error loading property details', 'error');
    }
}

// Populate the page with property data
function populatePropertyDetails(property) {
    console.log('Populating property details:', property);
    
    // Extract project name from various possible fields
    let projectName = 'Property';
    if (property.project_name) {
        projectName = property.project_name;
    } else if (property.project) {
        projectName = property.project;
    } else if (property.name) {
        projectName = property.name;
    } else if (property.title) {
        projectName = property.title;
    }
    
    // Update page title
    document.title = `Project Details - ${projectName}`;
    
    // Update header information
    const projectTitle = document.querySelector('.project-title');
    const projectTagline = document.querySelector('.project-tagline');
    const locationSpan = document.querySelector('.location');
    const statusBadge = document.querySelector('.status-badge');
    
    if (projectTitle) projectTitle.textContent = projectName;
    if (projectTagline) projectTagline.textContent = `${property.property_type || 'Property'} in ${property.locality || 'Unknown'}, ${property.city || 'Unknown'}`;
    if (locationSpan) locationSpan.innerHTML = `<i class="fas fa-map-marker-alt"></i> ${property.locality || 'Unknown'}, ${property.city || 'Unknown'}`;
    if (statusBadge) {
        statusBadge.textContent = property.status || 'Available';
        statusBadge.className = `status-badge ${(property.status || 'available').toLowerCase().replace(' ', '-')}`;
    }
    
    // Update key metrics
    const startingPrice = document.querySelector('.metric-card:nth-child(1) .metric-value');
    const pricePerSqft = document.querySelector('.metric-card:nth-child(2) .metric-value');
    const bhkOptions = document.querySelector('.metric-card:nth-child(4) .metric-value');
    
    if (startingPrice) startingPrice.textContent = formatPrice(property.sell_price || property.sellPrice || 0);
    if (pricePerSqft) pricePerSqft.textContent = `₹${(property.price_per_sqft || property.pricePerSqft || 0).toLocaleString()}`;
    if (bhkOptions) bhkOptions.textContent = property.bhk_count || property.bhkCount || '1';
    
    // Update residences section based on BHK count
    updateResidencesSection(property);
    
    // Update amenities section if available
    if (property.amenities && property.amenities.length > 0) {
        updateAmenitiesSection(property.amenities);
    }
    
    // Populate all expandable sections with real data
    populateExpandableSections(property);
}

// Populate all expandable sections with real data from database
function populateExpandableSections(property) {
    // Populate Construction Materials & Specifications
    populateConstructionSpecs(property);
    
    // Populate Environmental & Utility Features
    populateEnvironmentalFeatures(property);
    
    // Populate Expert Review
    populateExpertReview(property);
    
    // Populate Nearby Areas & Connectivity
    populateNearbyConnectivity(property);
    
    // Populate Safety & Security Features
    populateSafetyFeatures(property);
    
    // Populate Project Progress
    populateProgressSection(property);
}

// Populate Construction Materials & Specifications
function populateConstructionSpecs(property) {
    const specsContainer = document.getElementById('construction-specs');
    if (!specsContainer) return;
    
    // Use real data from property or default specifications
    const specs = [
        {
            title: 'Foundation',
            description: property.foundation_specs || 'RCC foundation with standard depth and M25 grade concrete'
        },
        {
            title: 'Structure',
            description: property.structure_specs || 'RCC framed structure with M30 grade concrete and Fe500D steel'
        },
        {
            title: 'Walls',
            description: property.wall_specs || 'Clay bricks with cement mortar, standard thickness'
        },
        {
            title: 'Finishing',
            description: property.finishing_specs || 'Premium quality tiles, paints, and fixtures from reputed brands'
        }
    ];
    
    specsContainer.innerHTML = specs.map(spec => `
        <div class="spec-item">
            <h4>${spec.title}</h4>
            <p>${spec.description}</p>
        </div>
    `).join('');
}

// Populate Environmental & Utility Features
function populateEnvironmentalFeatures(property) {
    const featuresContainer = document.getElementById('environmental-features');
    if (!featuresContainer) return;
    
    // Use real data from property or default features
    const features = [
        {
            icon: 'fa-solar-panel',
            title: 'Solar Power',
            description: property.solar_power || 'Solar panels for energy efficiency'
        },
        {
            icon: 'fa-recycle',
            title: 'Water Recycling',
            description: property.water_recycling || 'STP plant for grey water treatment'
        },
        {
            icon: 'fa-leaf',
            title: 'Green Building',
            description: property.green_certification || 'Environmentally friendly construction'
        }
    ];
    
    featuresContainer.innerHTML = features.map(feature => `
        <div class="feature-item">
            <i class="fas ${feature.icon}"></i>
            <h4>${feature.title}</h4>
            <p>${feature.description}</p>
        </div>
    `).join('');
}

// Populate Expert Review
function populateExpertReview(property) {
    const reviewContainer = document.getElementById('expert-review');
    if (!reviewContainer) return;
    
    // Use real data from property or default review
    const rating = property.expert_rating || 4.5;
    const stars = '★'.repeat(Math.floor(rating)) + '☆'.repeat(5 - Math.floor(rating));
    
    reviewContainer.innerHTML = `
        <div class="expert-rating">
            <div class="stars">${stars}</div>
            <span class="rating-text">${rating}/5.0</span>
        </div>
        <p><strong>Architectural Excellence:</strong> ${property.architectural_review || 'Modern design with optimal space utilization and natural light.'}</p>
        <p><strong>Construction Quality:</strong> ${property.construction_review || 'Premium materials and workmanship meeting international standards.'}</p>
        <p><strong>Investment Potential:</strong> ${property.investment_review || 'High ROI potential due to prime location and quality construction.'}</p>
    `;
}

// Populate Nearby Areas & Connectivity
function populateNearbyConnectivity(property) {
    const connectivityContainer = document.getElementById('nearby-connectivity');
    if (!connectivityContainer) return;
    
    // Use real data from property or default connectivity info
    const connectivity = [
        {
            icon: 'fa-subway',
            title: 'Metro Station',
            description: property.metro_distance || 'Metro station nearby'
        },
        {
            icon: 'fa-shopping-bag',
            title: 'Shopping',
            description: property.shopping_distance || 'Shopping centers in vicinity'
        },
        {
            icon: 'fa-hospital',
            title: 'Healthcare',
            description: property.healthcare_distance || 'Hospitals and clinics nearby'
        },
        {
            icon: 'fa-graduation-cap',
            title: 'Education',
            description: property.education_distance || 'Schools and colleges in area'
        }
    ];
    
    connectivityContainer.innerHTML = connectivity.map(item => `
        <div class="connectivity-item">
            <i class="fas ${item.icon}"></i>
            <h4>${item.title}</h4>
            <p>${item.description}</p>
        </div>
    `).join('');
}

// Populate Safety & Security Features
function populateSafetyFeatures(property) {
    const safetyContainer = document.getElementById('safety-content');
    if (!safetyContainer) return;
    
    // Use real data from property or default safety features
    const securityFeatures = property.security_features || ['CCTV Surveillance', 'Fire Alarm System', 'Access Control'];
    const emergencyFeatures = property.emergency_features || ['Fire Staircase', 'Refuge Areas', 'Fire Extinguishers'];
    
    safetyContainer.innerHTML = `
        <div class="safety-column">
            <h3>Security Systems</h3>
            <ul class="safety-list">
                ${securityFeatures.map(feature => `<li><i class="fas fa-check"></i> ${feature}</li>`).join('')}
            </ul>
        </div>
        <div class="safety-column">
            <h3>Emergency Features</h3>
            <ul class="safety-list">
                ${emergencyFeatures.map(feature => `<li><i class="fas fa-check"></i> ${feature}</li>`).join('')}
            </ul>
        </div>
        <div class="safety-note">
            <p><strong>Important:</strong> ${property.safety_note || 'All security systems are monitored 24/7 by trained personnel. Emergency response protocols are in place.'}</p>
        </div>
    `;
}

// Populate Project Progress Section
function populateProgressSection(property) {
    const progressContainer = document.querySelector('.progress-container');
    if (!progressContainer) return;
    
    // Use real data from property or default progress
    const progressData = {
        overallProgress: property.overall_progress || 75,
        timeline: property.timeline_months || 18,
        remaining: property.remaining_months || 6,
        phases: property.construction_phases || [
            { name: 'Foundation', status: 'completed' },
            { name: 'Structure', status: 'completed' },
            { name: 'Interiors', status: 'in-progress' },
            { name: 'Handover', status: 'pending' }
        ]
    };
    
    // Update progress summary
    const summaryItems = progressContainer.querySelectorAll('.summary-value');
    if (summaryItems.length >= 3) {
        summaryItems[0].textContent = `${progressData.overallProgress}%`;
        summaryItems[1].textContent = progressData.timeline;
        summaryItems[2].textContent = progressData.remaining;
    }
    
    // Update progress steps
    const progressSteps = progressContainer.querySelectorAll('.progress-step');
    progressSteps.forEach((step, index) => {
        if (index < progressData.phases.length) {
            const phase = progressData.phases[index];
            const stepLabel = step.querySelector('.step-label');
            if (stepLabel) {
                stepLabel.textContent = phase.name;
            }
            
            // Update status classes
            step.className = `progress-step ${phase.status}`;
        }
    });
}

// Update residences section based on property data
function updateResidencesSection(property) {
    const residencesGrid = document.querySelector('.residences-grid');
    
    if (!residencesGrid) return;
    
    // Clear existing residences
    residencesGrid.innerHTML = '';
    
    // Create multiple BHK configurations based on property data
    const bhkConfigs = generateBHKConfigurations(property);
    
    bhkConfigs.forEach(config => {
        const residenceCard = createResidenceCard(config);
        residencesGrid.appendChild(residenceCard);
    });
    
    // Initialize slider functionality
    initializeResidencesSlider();
}

// Generate multiple BHK configurations for the project
function generateBHKConfigurations(property) {
    const baseArea = property.carpet_area || 1000;
    const basePrice = property.sell_price || 25000000;
    const basePricePerSqft = property.price_per_sqft || 18000;
    
    const configurations = [
        {
            bhk_count: 1,
            title: 'COMPACT LIVING',
            area: Math.round(baseArea * 0.6),
            price: Math.round(basePrice * 0.6),
            pricePerSqft: basePricePerSqft,
            features: ['Efficient space utilization', 'Modern kitchen design', 'Balcony with city view'],
            property_type: property.property_type || 'Apartment',
            locality: property.locality || 'Unknown',
            city: property.city || 'Unknown'
        },
        {
            bhk_count: 2,
            title: 'FAMILY COMFORT',
            area: Math.round(baseArea * 0.8),
            price: Math.round(basePrice * 0.8),
            pricePerSqft: basePricePerSqft,
            features: ['Two spacious bedrooms', 'Separate dining area', 'Balcony access'],
            property_type: property.property_type || 'Apartment',
            locality: property.locality || 'Unknown',
            city: property.city || 'Unknown'
        },
        {
            bhk_count: 3,
            title: 'SPACIOUS LUXURY',
            area: baseArea,
            price: basePrice,
            pricePerSqft: basePricePerSqft,
            features: ['Three spacious bedrooms', 'Separate dining area', 'Multiple balconies with city views'],
            property_type: property.property_type || 'Apartment',
            locality: property.locality || 'Unknown',
            city: property.city || 'Unknown'
        },
        {
            bhk_count: 4,
            title: 'ULTIMATE PRESTIGE',
            area: Math.round(baseArea * 1.3),
            price: Math.round(basePrice * 1.3),
            pricePerSqft: basePricePerSqft,
            features: ['Four luxurious bedrooms', 'Premium finishes', 'Private terrace garden'],
            property_type: property.property_type || 'Apartment',
            locality: property.locality || 'Unknown',
            city: property.city || 'Unknown'
        }
    ];
    
    return configurations;
}

// Create a residence card for the property
function createResidenceCard(config) {
    const card = document.createElement('div');
    card.className = 'residence-card';
    
    const bhkText = `${config.bhk_count} BHK`;
    const areaText = `${config.area.toLocaleString()} sq ft`;
    const priceText = formatPrice(config.price);
    
    card.innerHTML = `
        <div class="card-header">
            <h3>${config.title}</h3>
            <span class="bhk-config">${bhkText}</span>
        </div>
        <div class="card-content">
            <div class="area-info">
                <span class="area-value">${areaText}</span>
            </div>
            <ul class="features-list">
                <li>${bhkText} configuration</li>
                <li>${config.area} sq ft carpet area</li>
                <li>Located in ${config.locality}, ${config.city}</li>
            </ul>
            <div class="price-info">
                <span class="price">${priceText} onwards</span>
            </div>
            <button class="view-details-btn" data-bhk="${config.bhk_count}">
                View Details
            </button>
        </div>
    `;
    
    // Add click event for the view details button
    const viewDetailsBtn = card.querySelector('.view-details-btn');
    viewDetailsBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const bhkType = viewDetailsBtn.getAttribute('data-bhk');
        showBHKModal(bhkType);
    });
    
    return card;
}

// Initialize residences slider functionality
function initializeResidencesSlider() {
    const residencesGrid = document.querySelector('.residences-grid');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    
    if (!residencesGrid || !prevBtn || !nextBtn) return;
    
    let currentIndex = 0;
    const cardWidth = 350 + 24; // card width + gap
    const visibleCards = Math.floor(residencesGrid.parentElement.offsetWidth / cardWidth);
    const totalCards = residencesGrid.children.length;
    
    // Update button states
    function updateButtonStates() {
        prevBtn.disabled = currentIndex === 0;
        nextBtn.disabled = currentIndex >= totalCards - visibleCards;
    }
    
    // Slide to specific index
    function slideToIndex(index) {
        currentIndex = Math.max(0, Math.min(index, totalCards - visibleCards));
        const translateX = -currentIndex * cardWidth;
        residencesGrid.style.transform = `translateX(${translateX}px)`;
        updateButtonStates();
    }
    
    // Initialize button states
    updateButtonStates();
    
    // Store functions globally for onclick handlers
    window.slideResidences = function(direction) {
        if (direction === 'prev' && currentIndex > 0) {
            slideToIndex(currentIndex - 1);
        } else if (direction === 'next' && currentIndex < totalCards - visibleCards) {
            slideToIndex(currentIndex + 1);
        }
    };
}

// Update amenities section with property amenities
function updateAmenitiesSection(amenities) {
    const amenitiesGrid = document.querySelector('.amenities-grid');
    if (!amenitiesGrid) return;
    
    // Clear existing amenities
    amenitiesGrid.innerHTML = '';
    
    // Add property amenities
    amenities.forEach(amenity => {
        const amenityCard = document.createElement('div');
        amenityCard.className = 'amenity-card';
        
        // Map amenity names to icons
        const iconMap = {
            'gym': 'fa-dumbbell',
            'parking': 'fa-car',
            'swimming pool': 'fa-swimming-pool',
            'garden': 'fa-seedling',
            'security': 'fa-shield-alt',
            'lift': 'fa-arrow-up',
            'balcony': 'fa-home',
            'concierge': 'fa-concierge-bell',
            'pool': 'fa-swimming-pool',
            'spa': 'fa-spa',
            'theater': 'fa-film',
            'wine cellar': 'fa-wine-bottle',
            'garage': 'fa-warehouse',
            'fireplace': 'fa-fire',
            'patio': 'fa-umbrella-beach',
            'laundry': 'fa-tshirt',
            'storage': 'fa-box'
        };
        
        const iconClass = iconMap[amenity.toLowerCase()] || 'fa-star';
        
        amenityCard.innerHTML = `
            <div class="amenity-icon">
                <i class="fas ${iconClass}"></i>
            </div>
            <h3>${amenity.charAt(0).toUpperCase() + amenity.slice(1)}</h3>
            <p>Available</p>
        `;
        
        amenitiesGrid.appendChild(amenityCard);
    });
}

// Utility function to format price in Indian format
function formatPrice(price) {
    if (!price || price === 0) return 'Price on request';
    
    const priceInLakhs = price / 100000; // Convert rupees to lakhs
    if (priceInLakhs >= 100) {
        return `₹${(priceInLakhs / 100).toFixed(1)} Cr`;
    } else {
        return `₹${priceInLakhs.toFixed(0)} Lakh`;
    }
}

// Go back to search results page
function goBack() {
    // Check if we came from the search page
    if (document.referrer && document.referrer.includes('index.html')) {
        window.history.back();
    } else {
        // If no referrer or came from elsewhere, go to main page
        window.location.href = 'index.html';
    }
}

// Export functions for potential external use
window.ProjectDetails = {
    showBHKModal,
    closeModal,
    showNotification,
    handleContactClick,
    handleScheduleClick,
    loadPropertyData,
    populatePropertyDetails,
    populateExpandableSections,
    populateConstructionSpecs,
    populateEnvironmentalFeatures,
    populateExpertReview,
    populateNearbyConnectivity,
    populateSafetyFeatures,
    populateProgressSection,
    generateBHKConfigurations,
    initializeResidencesSlider,
    goBack
};
