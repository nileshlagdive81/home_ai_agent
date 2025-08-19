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
                    ${result.properties.slice(0, 3).map(prop => {
                        let projectName = 'Unknown';
                        if (prop.project_name) {
                            if (typeof prop.project_name === 'object' && prop.project_name.name) {
                                projectName = prop.project_name.name;
                            } else if (typeof prop.project_name === 'string') {
                                projectName = prop.project_name;
                            }
                        } else if (prop.project) {
                            if (typeof prop.project === 'object' && prop.project.name) {
                                projectName = prop.project.name;
                            } else if (typeof prop.project === 'string') {
                                projectName = prop.project;
                            }
                        }
                        return `
                            <div class="preview-item">
                                <strong>${projectName}</strong> - 
                                ${prop.bhk_count || prop.bhkCount || 'N/A'} BHK, 
                                ₹${(prop.sell_price || prop.sellPrice || 0) / 100000} Lakh
                            </div>
                        `;
                    }).join('')}
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
                    ${result.properties.slice(0, 3).map(prop => {
                        let projectName = 'Unknown';
                        if (prop.project_name) {
                            if (typeof prop.project_name === 'object' && prop.project_name.name) {
                                projectName = prop.project_name.name;
                            } else if (typeof prop.project_name === 'string') {
                                projectName = prop.project_name;
                            }
                        } else if (prop.project) {
                            if (typeof prop.project === 'object' && prop.project.name) {
                                projectName = prop.project.name;
                            } else if (typeof prop.project === 'string') {
                                projectName = prop.project;
                            }
                        }
                        return `
                            <div class="preview-item">
                                <strong>${projectName}</strong> - 
                                ${prop.bhk_count || prop.bhkCount || 'N/A'} BHK, 
                                ₹${(prop.sell_price || prop.sellPrice || 0) / 100000} Lakh
                            </div>
                        `;
                    }).join('')}
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
    
    // Initialize media modal
    const mediaModal = document.getElementById('mediaModal');
    const mediaModalCloseBtn = mediaModal?.querySelector('.media-close-btn');
    
    if (mediaModalCloseBtn) {
        mediaModalCloseBtn.addEventListener('click', () => {
            closeMediaModal();
        });
    }
    
    if (mediaModal) {
        mediaModal.addEventListener('click', (e) => {
            if (e.target === mediaModal) {
                closeMediaModal();
            }
        });
    }
    
    // Close media modal with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && mediaModal?.style.display === 'block') {
            closeMediaModal();
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
function showBHKModal(bhkData) {
    console.log('Showing BHK modal for:', bhkData);
    
    const modal = document.getElementById('bhkModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalArea = document.getElementById('modalArea');
    const modalPrice = document.getElementById('modalPrice');
    const modalCarpetArea = document.getElementById('modalCarpetArea');
    const modalRoomList = document.getElementById('modalRoomList');
    const modalFeatures = document.getElementById('modalFeatures');
    const modalCtaText = document.getElementById('modalCtaText');
    
    // Update modal title
    modalTitle.textContent = `${bhkData.bhk_count} BHK Configuration Details`;
    
    // Update area and price information
    modalArea.textContent = `${bhkData.carpet_area_sqft} sq ft`;
    modalPrice.textContent = `₹${(bhkData.sell_price / 10000000).toFixed(1)} Cr onwards`;
    modalCarpetArea.textContent = `${bhkData.carpet_area_sqft} sq ft carpet area`;
    
    // Update CTA text
    modalCtaText.textContent = `Interested in this ${bhkData.bhk_count} BHK configuration?`;
    
    // Display floor plan if available
    displayFloorPlan(bhkData.floor_plan_url);
    
    // Populate room specifications
    populateRoomSpecifications(bhkData.room_specifications || []);
    
    // Populate features
    populateModalFeatures(bhkData);
    
    // Show the modal
    modal.style.display = 'block';
}

// Display floor plan in the modal
function displayFloorPlan(floorPlanUrl) {
    const floorPlanDisplay = document.getElementById('floorPlanDisplay');
    const floorPlanPlaceholder = document.getElementById('floorPlanPlaceholder');
    const floorPlanImage = document.getElementById('floorPlanImage');
    
    if (floorPlanUrl) {
        // Show floor plan image
        floorPlanImage.src = floorPlanUrl;
        floorPlanImage.style.display = 'block';
        floorPlanPlaceholder.style.display = 'none';
    } else {
        // Show placeholder
        floorPlanImage.style.display = 'none';
        floorPlanPlaceholder.style.display = 'block';
    }
}

// Load and display project media (images and videos)
async function loadProjectMedia(projectId) {
    try {
        console.log('Loading media for project:', projectId);
        
        if (!projectId) {
            console.log('No project ID provided for media loading');
            return;
        }
        
        // Fetch media from the API
        const response = await fetch(`http://localhost:8000/api/v1/projects/${projectId}/media`);
        console.log('Media response status:', response.status);
        
        if (response.ok) {
            const mediaData = await response.json();
            console.log('Fetched media data:', mediaData);
            
            if (mediaData.success && mediaData.media && mediaData.media.length > 0) {
                // Show project tour section
                const projectTourSection = document.getElementById('projectTourSection');
                projectTourSection.style.display = 'block';
                
                // Show unified media slider
                const mediaSliderContainer = document.getElementById('mediaSliderContainer');
                mediaSliderContainer.style.display = 'block';
                
                // Display all media in unified slider
                displayUnifiedMedia(mediaData.media);
            }
        } else {
            console.log('Media response not ok:', response.statusText);
        }
        
    } catch (error) {
        console.error('Error loading project media:', error);
    }
}

// Display unified media in single slider
function displayUnifiedMedia(mediaItems) {
    const mediaSlides = document.getElementById('mediaSlides');
    
    mediaSlides.innerHTML = '';
    
    mediaItems.forEach((media, index) => {
        const mediaSlide = document.createElement('div');
        mediaSlide.className = 'media-slide';
        mediaSlide.onclick = () => openMediaModal(media.file_type, media.file_path, media.alt_text || `Project ${media.file_type}`);
        
        if (media.file_type === 'video') {
            mediaSlide.innerHTML = `
                <video src="${media.file_path}" preload="metadata">
                    Your browser does not support the video tag.
                </video>
                <div class="media-caption">${media.alt_text || 'Project Video'}</div>
            `;
        } else {
            mediaSlide.innerHTML = `
                <img src="${media.file_path}" alt="${media.alt_text}" loading="lazy">
                <div class="media-caption">${media.alt_text || 'Project Image'}</div>
            `;
        }
        
        mediaSlides.appendChild(mediaSlide);
    });
}

// Open media modal for bigger view
function openMediaModal(type, src, caption) {
    const mediaModal = document.getElementById('mediaModal');
    const mediaModalContent = document.getElementById('mediaModalContent');
    
    if (type === 'video') {
        mediaModalContent.innerHTML = `
            <video controls autoplay>
                <source src="${src}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        `;
    } else {
        mediaModalContent.innerHTML = `
            <img src="${src}" alt="${caption}">
        `;
    }
    
    mediaModal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

// Close media modal
function closeMediaModal() {
    const mediaModal = document.getElementById('mediaModal');
    mediaModal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Unified media slider navigation
function slideMedia(direction) {
    const mediaSlides = document.getElementById('mediaSlides');
    const slideWidth = 280 + 16; // slide width + gap
    
    if (direction === 'prev') {
        mediaSlides.scrollLeft -= slideWidth;
    } else {
        mediaSlides.scrollLeft += slideWidth;
    }
}

// Populate room specifications in the modal
function populateRoomSpecifications(roomSpecs) {
    const modalRoomList = document.getElementById('modalRoomList');
    
    if (!roomSpecs || roomSpecs.length === 0) {
        // Show default room specifications if none provided
        modalRoomList.innerHTML = `
            <div class="room-item">
                <h4>Living Room</h4>
                <p>Spacious living area with natural light</p>
            </div>
            <div class="room-item">
                <h4>Master Bedroom</h4>
                <p>Large bedroom with attached bathroom</p>
            </div>
            <div class="room-item">
                <h4>Kitchen</h4>
                <p>Modern kitchen with utility area</p>
            </div>
        `;
        return;
    }
    
    modalRoomList.innerHTML = '';
    
    roomSpecs.forEach(room => {
        const roomItem = document.createElement('div');
        roomItem.className = 'room-item';
        
        roomItem.innerHTML = `
            <h4>${room.room_name}</h4>
            <p>${room.room_type} - ${room.area_sqft} sq ft</p>
            ${room.features ? `<p>Features: ${room.features.join(', ')}</p>` : ''}
        `;
        
        modalRoomList.appendChild(roomItem);
    });
}

// Populate modal features
function populateModalFeatures(bhkData) {
    const modalFeatures = document.getElementById('modalFeatures');
    
    // Use real features from BHK data or generate based on BHK count
    let features = [];
    
    if (bhkData.features && bhkData.features.length > 0) {
        // Use real features from database
        features = bhkData.features;
    } else {
        // Generate features based on BHK count and property type
        features = generateFeaturesForBHK(bhkData.bhk_count, bhkData.property_type);
    }
    
    modalFeatures.innerHTML = '';
    
    features.forEach(feature => {
        const featureItem = document.createElement('div');
        featureItem.className = 'feature-item';
        
        featureItem.innerHTML = `
            <i class="fas fa-check"></i>
            <span>${feature}</span>
        `;
        
        modalFeatures.appendChild(featureItem);
    });
}

// Generate features based on BHK count and property type
function generateFeaturesForBHK(bhkCount, propertyType = 'Apartment') {
    const baseFeatures = ['Modern Design', 'Quality Finishes'];
    
    if (bhkCount <= 1) {
        return [
            ...baseFeatures,
            'Efficient Space Utilization',
            'Modern Kitchen Design',
            'Balcony Access',
            'Built-in Storage',
            'Attached Bathroom'
        ];
    } else if (bhkCount <= 2) {
        return [
            ...baseFeatures,
            'Spacious Bedrooms',
            'Separate Dining Area',
            'Multiple Balconies',
            'Built-in Wardrobes',
            'Modular Kitchen',
            'Attached Bathrooms'
        ];
    } else if (bhkCount <= 3) {
        return [
            ...baseFeatures,
            'Large Master Bedroom',
            'Separate Living & Dining',
            'Multiple Balconies with Views',
            'Premium Kitchen with Island',
            'Walk-in Wardrobe',
            'Attached Bathrooms',
            'Study Area'
        ];
    } else {
        return [
            ...baseFeatures,
            'Luxurious Master Suite',
            'Separate Living & Dining',
            'Private Terrace Garden',
            'Premium Kitchen with Butler Pantry',
            'Walk-in Wardrobes',
            'Attached Bathrooms',
            'Study/Home Office',
            'Entertainment Area',
            'Utility Room'
        ];
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
async function loadPropertyData() {
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
        
        // For nearby places functionality, use the property ID directly as project ID
        // This ensures we can fetch nearby places data without complex matching logic
        propertyData.project_id = propertyData.id;
        
        // Fetch amenities data for this project
        if (propertyData.id) {
            try {
                console.log('Fetching amenities for project ID:', propertyData.id);
                const amenitiesResponse = await fetch(`http://localhost:8000/api/v1/projects/${propertyData.id}/amenities`);
                console.log('Amenities response status:', amenitiesResponse.status);
                if (amenitiesResponse.ok) {
                    const amenitiesData = await amenitiesResponse.json();
                    console.log('Fetched amenities data:', amenitiesData);
                    if (amenitiesData.success && amenitiesData.amenities) {
                        propertyData.amenities = amenitiesData.amenities.map(a => a.name);
                        console.log('Updated property data with amenities:', propertyData.amenities);
                    }
                } else {
                    console.log('Amenities response not ok:', amenitiesResponse.statusText);
                }
            } catch (error) {
                console.log('Could not fetch amenities, using defaults:', error);
            }
        } else {
            console.log('No project ID found in property data');
        }
        
        // Populate the page with property data
        populatePropertyDetails(propertyData);
        
        // Load and display project media
        await loadProjectMedia(propertyData.id);
        
    } catch (error) {
        console.error('Error parsing property data:', error);
        showNotification('Error loading property details', 'error');
    }
}

// Populate property details on the page
function populatePropertyDetails(property) {
    console.log('populatePropertyDetails called with property:', property);
    console.log('Property amenities:', property.amenities);
    
    // Extract project name safely
    let projectName = 'Property';
    if (typeof property.project_name === 'object' && property.project_name?.name) {
        projectName = property.project_name.name;
    } else if (typeof property.project === 'object' && property.project?.name) {
        projectName = property.project.name;
    } else if (typeof property.project_name === 'string') {
        projectName = property.project_name;
    } else if (typeof property.project === 'string') {
        projectName = property.project;
    }
    
    // Extract locality safely
    let locality = '';
    if (typeof property.locality === 'object' && property.locality?.name) {
        locality = property.locality.name;
    } else if (typeof property.locality === 'string') {
        locality = property.locality;
    }
    
    // Extract city safely
    let city = '';
    if (typeof property.city === 'object' && property.city?.name) {
        city = property.city.name;
    } else if (typeof property.city === 'string') {
        city = property.city;
    }
    
    // Extract status safely
    let status = '';
    if (typeof property.status === 'object' && property.status?.name) {
        status = property.status.name;
    } else if (typeof property.status === 'string') {
        status = property.status;
    }
    
    // Extract RERA number safely
    let reraNumber = '';
    if (typeof property.rera_number === 'object' && property.rera_number?.number) {
        reraNumber = property.rera_number.number;
    } else if (typeof property.rera_number === 'string') {
        reraNumber = property.rera_number;
    }
    
    console.log('Extracted values - Project Name:', projectName, 'Locality:', locality, 'City:', city, 'Status:', status, 'RERA:', reraNumber);
    
    // Update project title and tagline
    const projectTitle = document.querySelector('.project-title');
    const projectTagline = document.querySelector('.project-tagline');
    const locationSpan = document.querySelector('.location-span');
    const statusBadge = document.querySelector('.status-badge');
    const reraNumberSpan = document.querySelector('.rera-number');
    
    if (projectTitle) projectTitle.textContent = projectName || 'Property Details';
    if (projectTagline) projectTagline.textContent = property.description || 'Premium residential project';
    if (locationSpan) locationSpan.textContent = `${locality}, ${city}`;
    if (statusBadge) statusBadge.textContent = status || 'Available';
    if (reraNumberSpan) reraNumberSpan.textContent = reraNumber || 'RERA Number Pending';
    
    // Update metrics
    const startingPrice = document.querySelector('#starting-price');
    const pricePerSqft = document.querySelector('#price-per-sqft');
    const totalUnits = document.querySelector('.metric-card:nth-child(3) .metric-value');
    const totalFloors = document.querySelector('.metric-card:nth-child(4) .metric-value');
    
    if (startingPrice) startingPrice.textContent = formatPrice(property.sell_price || property.starting_price || property.startingPrice || 0);
    if (pricePerSqft) pricePerSqft.textContent = `₹${(property.price_per_sqft || property.pricePerSqft || 0).toLocaleString()}`;
    if (totalUnits) totalUnits.textContent = property.total_units || property.project?.total_units || 'N/A';
    if (totalFloors) totalFloors.textContent = property.total_floors || property.project?.total_floors || 'N/A';
    
    // Update residences section based on BHK count
    updateResidencesSection(property);
    
    // Update amenities section if available
    console.log('About to call updateAmenitiesSection with:', property.amenities);
    if (property.amenities && property.amenities.length > 0) {
        updateAmenitiesSection(property.amenities);
    } else {
        console.log('No amenities found in property, using default amenities');
        updateAmenitiesSection([]);
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
            description: property.foundation_specs || property.construction_specs?.foundation || 'RCC foundation with standard depth and M25 grade concrete'
        },
        {
            title: 'Structure',
            description: property.structure_specs || property.construction_specs?.structure || 'RCC framed structure with M30 grade concrete and Fe500D steel'
        },
        {
            title: 'Walls',
            description: property.wall_specs || property.construction_specs?.walls || 'Clay bricks with cement mortar, standard thickness'
        },
        {
            title: 'Finishing',
            description: property.finishing_specs || property.construction_specs?.finishing || 'Premium quality tiles, paints, and fixtures from reputed brands'
        },
        {
            title: 'Electrical',
            description: property.electrical_specs || property.construction_specs?.electrical || 'Standard electrical fittings with safety switches'
        },
        {
            title: 'Plumbing',
            description: property.plumbing_specs || property.construction_specs?.plumbing || 'CPVC pipes with modern fixtures'
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
            description: property.solar_power || property.environmental_features?.solar_power || 'Solar panels for energy efficiency'
        },
        {
            icon: 'fa-recycle',
            title: 'Water Recycling',
            description: property.water_recycling || property.environmental_features?.water_recycling || 'STP plant for grey water treatment'
        },
        {
            icon: 'fa-leaf',
            title: 'Green Building',
            description: property.green_certification || property.environmental_features?.green_certification || 'Environmentally friendly construction'
        },
        {
            icon: 'fa-wind',
            title: 'Natural Ventilation',
            description: property.natural_ventilation || property.environmental_features?.natural_ventilation || 'Cross-ventilation design for natural air flow'
        },
        {
            icon: 'fa-seedling',
            title: 'Landscaping',
            description: property.landscaping || property.environmental_features?.landscaping || 'Green spaces and gardens for better environment'
        },
        {
            icon: 'fa-tint',
            title: 'Rainwater Harvesting',
            description: property.rainwater_harvesting || property.environmental_features?.rainwater_harvesting || 'Rainwater collection and storage system'
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
    const rating = property.expert_rating || property.expert_review?.rating || 4.5;
    const stars = '★'.repeat(Math.floor(rating)) + '☆'.repeat(5 - Math.floor(rating));
    
    reviewContainer.innerHTML = `
        <div class="expert-rating">
            <div class="stars">${stars}</div>
            <span class="rating-text">${rating}/5.0</span>
        </div>
        <p><strong>Architectural Excellence:</strong> ${property.architectural_review || property.expert_review?.architectural || 'Modern design with optimal space utilization and natural light.'}</p>
        <p><strong>Construction Quality:</strong> ${property.construction_review || property.expert_review?.construction_quality || 'Premium materials and workmanship meeting international standards.'}</p>
        <p><strong>Investment Potential:</strong> ${property.investment_review || property.expert_review?.investment_potential || 'High ROI potential due to prime location and quality construction.'}</p>
        <p><strong>Location Analysis:</strong> ${property.location_review || property.expert_review?.location_analysis || 'Prime location with excellent connectivity and future growth potential.'}</p>
        <p><strong>Market Position:</strong> ${property.market_position || property.expert_review?.market_position || 'Competitive pricing with strong market demand in the area.'}</p>
    `;
}

// Populate Nearby Areas & Connectivity
async function populateNearbyConnectivity(property) {
    const connectivityContainer = document.getElementById('nearby-connectivity');
    if (!connectivityContainer) return;
    
    try {
        // Fetch nearby places from the API
        const projectId = property.project?.id || property.project_id;
        
        if (!projectId) {
            // Fallback to default connectivity info
            populateDefaultConnectivity(property);
            return;
        }
        
        const response = await fetch(`http://localhost:8000/api/v1/projects/${projectId}/nearby-places`);
        
        if (!response.ok) {
            throw new Error(`Failed to fetch nearby places: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success && data.nearby_places) {
            // Display real nearby places data
            displayNearbyPlaces(data.nearby_places, connectivityContainer);
        } else {
            // Fallback to default connectivity info
            populateDefaultConnectivity(property);
        }
    } catch (error) {
        console.error('Error fetching nearby places:', error);
        // Fallback to default connectivity info
        populateDefaultConnectivity(property);
    }
}

// Display nearby places with real data
function displayNearbyPlaces(nearbyPlaces, container) {
    // Define icons for different place types
    const placeIcons = {
        'School': 'fa-graduation-cap',
        'College': 'fa-university',
        'University': 'fa-university',
        'Hospital': 'fa-hospital',
        'Metro Station': 'fa-subway',
        'Railway Station': 'fa-train',
        'Mall': 'fa-shopping-bag',
        'Shopping Center': 'fa-shopping-cart',
        'Market': 'fa-store',
        'Park': 'fa-tree',
        'Gym': 'fa-dumbbell',
        'Restaurant': 'fa-utensils',
        'Cinema': 'fa-film',
        'Bank': 'fa-university',
        'ATM': 'fa-credit-card',
        'Post Office': 'fa-envelope',
        'Police Station': 'fa-shield-alt',
        'Fire Station': 'fa-fire-extinguisher',
        'Airport': 'fa-plane',
        'Library': 'fa-book',
        'Sports Complex': 'fa-futbol',
        'Temple': 'fa-pray',
        'Bus Stand': 'fa-bus'
    };
    
    // Convert to array and sort by category
    const placesArray = Object.entries(nearbyPlaces).map(([category, places]) => ({
        category,
        places: places.sort((a, b) => a.distance_km - b.distance_km) // Sort by distance
    }));
    
    // Sort categories by priority
    const categoryPriority = ['Metro Station', 'School', 'Hospital', 'Mall', 'Railway Station', 'College', 'University', 'Park', 'Gym', 'Restaurant', 'Bank', 'ATM', 'Post Office', 'Police Station', 'Fire Station', 'Airport', 'Library', 'Sports Complex', 'Temple', 'Bus Stand'];
    
    placesArray.sort((a, b) => {
        const aPriority = categoryPriority.indexOf(a.category);
        const bPriority = categoryPriority.indexOf(b.category);
        return (aPriority === -1 ? 999 : aPriority) - (bPriority === -1 ? 999 : bPriority);
    });
    
    container.innerHTML = placesArray.map(categoryData => `
        <div class="connectivity-category">
            <h4 class="category-title">
                <i class="fas ${placeIcons[categoryData.category] || 'fa-map-marker-alt'}"></i>
                ${categoryData.category}
            </h4>
            <div class="places-list">
                ${categoryData.places.map(place => `
                    <div class="place-item">
                        <span class="place-name">${place.place_name}</span>
                        <span class="place-distance">${place.distance_km} km</span>
                        ${place.walking_distance ? '<span class="walking-badge">🚶 Walking</span>' : ''}
                    </div>
                `).join('')}
            </div>
        </div>
    `).join('');
}

// Fallback to default connectivity info
function populateDefaultConnectivity(property) {
    const connectivityContainer = document.getElementById('nearby-connectivity');
    if (!connectivityContainer) return;
    
    // Use real data from property or default connectivity info with distances in KMs
    const connectivity = [
        {
            icon: 'fa-subway',
            title: 'Metro Station',
            description: property.metro_distance ? `${property.metro_distance} KM` : property.nearby_connectivity?.metro || 'Metro station nearby'
        },
        {
            icon: 'fa-shopping-bag',
            title: 'Shopping',
            description: property.shopping_distance ? `${property.shopping_distance} KM` : property.nearby_connectivity?.shopping || 'Shopping centers in vicinity'
        },
        {
            icon: 'fa-hospital',
            title: 'Healthcare',
            description: property.healthcare_distance ? `${property.healthcare_distance} KM` : property.nearby_connectivity?.healthcare || 'Hospitals and clinics nearby'
        },
        {
            icon: 'fa-graduation-cap',
            title: 'Education',
            description: property.education_distance ? `${property.education_distance} KM` : property.nearby_connectivity?.education || 'Schools and colleges in area'
        },
        {
            icon: 'fa-plane',
            title: 'Airport',
            description: property.airport_distance ? `${property.airport_distance} KM` : property.nearby_connectivity?.airport || 'Airport connectivity available'
        },
        {
            icon: 'fa-train',
            title: 'Railway Station',
            description: property.railway_distance ? `${property.railway_distance} KM` : property.nearby_connectivity?.railway || 'Railway station nearby'
        },
        {
            icon: 'fa-bus',
            title: 'Bus Stand',
            description: property.bus_distance ? `${property.bus_distance} KM` : property.nearby_connectivity?.bus || 'Bus stand in vicinity'
        },
        {
            icon: 'fa-utensils',
            title: 'Restaurants',
            description: property.restaurant_distance ? `${property.restaurant_distance} KM` : property.nearby_connectivity?.restaurants || 'Restaurants and cafes nearby'
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
    const securityFeatures = property.security_features || property.safety_features?.security || ['CCTV Surveillance', 'Fire Alarm System', 'Access Control'];
    const emergencyFeatures = property.emergency_features || property.safety_features?.emergency || ['Fire Staircase', 'Refuge Areas', 'Fire Extinguishers'];
    const safetyFeatures = property.safety_features?.general || ['Child-safe railings', 'Non-slip flooring', 'Emergency lighting'];
    
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
        <div class="safety-column">
            <h3>General Safety</h3>
            <ul class="safety-list">
                ${safetyFeatures.map(feature => `<li><i class="fas fa-check"></i> ${feature}</li>`).join('')}
            </ul>
        </div>
        ${property.safety_note || property.safety_features?.note ? `
        <div class="safety-note">
            <p><strong>Important:</strong> ${property.safety_note || property.safety_features?.note}</p>
        </div>
        ` : ''}
    `;
}

// Populate Project Progress Section
function populateProgressSection(property) {
    const progressContainer = document.querySelector('.progress-container');
    if (!progressContainer) return;
    
    // Use real data from property or default progress
    const progressData = {
        overallProgress: property.overall_progress || property.project_progress?.overall || 75,
        timeline: property.timeline_months || property.project_progress?.timeline || 18,
        remaining: property.remaining_months || property.project_progress?.remaining || 6,
        phases: property.construction_phases || property.project_progress?.phases || [
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
async function updateResidencesSection(property) {
    const residencesGrid = document.querySelector('.residences-grid');
    
    if (!residencesGrid) return;
    
    // Clear existing residences
    residencesGrid.innerHTML = '';
    
    // Create multiple BHK configurations based on property data
    const bhkConfigs = await generateBHKConfigurations(property);
    
    bhkConfigs.forEach(config => {
        const residenceCard = createResidenceCard(config);
        residencesGrid.appendChild(residenceCard);
    });
    
    // Initialize slider functionality
    initializeResidencesSlider();
}

// Generate multiple BHK configurations for the project
async function generateBHKConfigurations(property) {
    try {
        // Fetch real BHK configurations from the API
        const projectId = property.project_id || property.id;
        if (!projectId) {
            console.log('No project ID available for fetching BHK configurations');
            return generateDefaultBHKConfigurations(property);
        }
        
        const response = await fetch(`http://localhost:8000/api/v1/projects/${projectId}/property-configurations`);
        if (response.ok) {
            const data = await response.json();
            if (data.success && data.configurations) {
                console.log('Fetched real BHK configurations:', data.configurations);
                return data.configurations.map(config => ({
                    ...config,
                    title: getBHKTitle(config.bhk_count),
                    pricePerSqft: config.sell_price && config.carpet_area_sqft ? 
                        (config.sell_price / config.carpet_area_sqft) : null,
                    features: getDefaultFeatures(config.bhk_count),
                    property_type: config.property_type || 'Apartment',
                    locality: property.locality || 'Unknown',
                    city: property.city || 'Unknown'
                }));
            }
        }
        
        console.log('Failed to fetch BHK configurations, using defaults');
        return generateDefaultBHKConfigurations(property);
        
    } catch (error) {
        console.error('Error fetching BHK configurations:', error);
        return generateDefaultBHKConfigurations(property);
    }
}

// Generate default BHK configurations as fallback
function generateDefaultBHKConfigurations(property) {
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

// Get BHK title based on BHK count
function getBHKTitle(bhkCount) {
    switch (bhkCount) {
        case 1: return 'COMPACT LIVING';
        case 1.5: return 'COMPACT PLUS';
        case 2: return 'FAMILY COMFORT';
        case 2.5: return 'FAMILY PLUS';
        case 3: return 'SPACIOUS LUXURY';
        case 3.5: return 'LUXURY PLUS';
        case 4: return 'ULTIMATE PRESTIGE';
        default: return `${bhkCount} BHK CONFIGURATION`;
    }
}

// Get default features based on BHK count
function getDefaultFeatures(bhkCount) {
    const baseFeatures = ['Modern design', 'Quality finishes', 'Balcony access'];
    
    if (bhkCount <= 1) {
        return [...baseFeatures, 'Efficient space utilization', 'Modern kitchen design'];
    } else if (bhkCount <= 2) {
        return [...baseFeatures, 'Spacious bedrooms', 'Separate dining area'];
    } else if (bhkCount <= 3) {
        return [...baseFeatures, 'Multiple bedrooms', 'Separate dining area', 'Multiple balconies'];
    } else {
        return [...baseFeatures, 'Luxurious bedrooms', 'Premium finishes', 'Private terrace garden'];
    }
}

// Create a residence card for the property
function createResidenceCard(config) {
    const card = document.createElement('div');
    card.className = 'residence-card';
    
    const bhkText = `${config.bhk_count} BHK`;
    // Use real data if available, fallback to calculated values
    const areaText = config.carpet_area_sqft ? 
        `${config.carpet_area_sqft.toLocaleString()} sq ft` : 
        `${(config.area || 0).toLocaleString()} sq ft`;
    const priceText = config.sell_price ? 
        formatPrice(config.sell_price) : 
        formatPrice(config.price || 0);
    
    // Check if floor plan is available
    const hasFloorPlan = config.floor_plan_url;
    const floorPlanBadge = hasFloorPlan ? 
        '<span class="floor-plan-badge">📐 Floor Plan Available</span>' : 
        '<span class="floor-plan-badge unavailable">📐 Floor Plan Coming Soon</span>';
    
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
                <li>${areaText} carpet area</li>
                <li>Located in ${config.locality}, ${config.city}</li>
            </ul>
            <div class="floor-plan-info">
                ${floorPlanBadge}
            </div>
            <div class="price-info">
                <span class="price">${priceText} onwards</span>
            </div>
            <button class="view-details-btn" data-bhk="${config.bhk_count}" data-config='${JSON.stringify(config)}'>
                View Details
            </button>
        </div>
    `;
    
    // Add click event for the view details button
    const viewDetailsBtn = card.querySelector('.view-details-btn');
    viewDetailsBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const bhkType = viewDetailsBtn.getAttribute('data-bhk');
        const configData = JSON.parse(viewDetailsBtn.getAttribute('data-config'));
        showBHKModal(configData);
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
    console.log('updateAmenitiesSection called with:', amenities);
    const amenitiesGrid = document.querySelector('.amenities-grid');
    console.log('amenitiesGrid found:', amenitiesGrid);
    if (!amenitiesGrid) return;
    
    // Clear existing amenities
    amenitiesGrid.innerHTML = '';
    
    // Use real amenities from property or default ones
    const allAmenities = amenities && amenities.length > 0 ? amenities : [
        'Gym', 'Parking', 'Swimming Pool', 'Garden', 'Security', 'Lift', 
        'Balcony', 'Concierge', 'Spa', 'Theater', 'Wine Cellar', 'Garage', 
        'Fireplace', 'Patio', 'Laundry', 'Storage', 'Kids Play Area', 
        'Party Hall', 'Indoor Games', 'Outdoor Sports', 'Restaurant', 'Bank',
        'ATM', 'Medical Center', 'Library', 'Business Center', 'Guest House'
    ];
    
    console.log('All amenities to display:', allAmenities);
    
    // Add property amenities
    allAmenities.forEach(amenity => {
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
            'storage': 'fa-box',
            'kids play area': 'fa-child',
            'party hall': 'fa-birthday-cake',
            'indoor games': 'fa-gamepad',
            'outdoor sports': 'fa-futbol',
            'restaurant': 'fa-utensils',
            'bank': 'fa-university',
            'atm': 'fa-credit-card',
            'medical center': 'fa-hospital',
            'library': 'fa-book',
            'business center': 'fa-briefcase',
            'guest house': 'fa-bed'
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
    
    console.log('Amenities section updated with', allAmenities.length, 'amenities');
    
    // Note: Amenities section will be expanded by default via CSS
    // The accordion functionality will handle expanding/collapsing
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
    goBack,
    // New Project Tour functions
    openMediaModal,
    closeMediaModal,
    slideMedia,
    displayUnifiedMedia
};
