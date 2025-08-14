# 🏠 **UPDATED Property Card to Database Field Mappings - V2**

## ✅ **Database Changes Made**

### **Price Field Consolidation:**
- **REMOVED**: `properties.price_lakhs` and `properties.price_crores`
- **ADDED**: `properties.sell_price` (DECIMAL(15,2)) - stores price in rupees
- **BENEFIT**: Single field for easier queries and calculations

### **Media Support Added:**
- **NEW TABLE**: `project_media` - supports images and videos
- **FEATURES**: File paths, categories, primary images, metadata

---

## 🎯 **Updated Property Card Field Mappings**

| **Property Card Field** | **Frontend Display** | **Database Source** | **Table** | **Mapping Type** |
|-------------------------|---------------------|---------------------|-----------|------------------|
| **Status Tag** | "Available", "New Listing", "Premium" | `properties.status` | `properties` | Direct |
| **Image Display** | Project image or placeholder icon | `project_media.file_path` WHERE `is_primary = TRUE` | `project_media` | Join via `project_id` |
| **Image Counter** | "1/4", "1/5" | `COUNT(*)` from `project_media` WHERE `project_id = X` | `project_media` | Aggregate query |
| **Price Main** | ₹85 Lakh, ₹1.2 Cr | `properties.sell_price` | `properties` | **UPDATED: Single field** |
| **Price Per Sqft** | ₹8,500/sq ft | `properties.sell_price` ÷ `properties.carpet_area_sqft` | `properties` | **UPDATED: Calculated from sell_price** |
| **Property Specs** | "2 BHK • 2 Bath • 1,200 sq ft • Apartment" | Multiple fields | Multiple tables | Complex join |
| **Locality & City** | "Baner, Pune" | `locations.locality` + `locations.city` | `locations` | Direct |
| **Amenities** | ["Gym", "Parking", "Pet-friendly"] | `project_amenities` + `amenities.name` | Join tables | Join via `project_id` |
| **Project Name** | "Lodha Park" (with asterisks) | `projects.name` | `projects` | Direct |

---

## 🔍 **Updated Database Query for Property Cards**

```sql
-- Main query to get property data for cards with NEW sell_price field
SELECT 
    -- Project information
    p.id as project_id,
    p.name as project_name,
    p.project_status,
    p.project_type,
    
    -- Property details (UPDATED: using sell_price)
    pr.id as property_id,
    pr.bhk_count,
    pr.carpet_area_sqft,
    pr.sell_price,                    -- NEW: Single price field in rupees
    pr.status as property_status,
    pr.floor_number,
    
    -- Location info
    l.city,
    l.locality,
    l.area,
    l.state,
    
    -- Media information
    pm.file_path as primary_image_path,
    pm.file_type as primary_media_type,
    COUNT(pm_all.id) as total_media_count,
    COUNT(CASE WHEN pm_all.file_type = 'image' THEN 1 END) as image_count,
    COUNT(CASE WHEN pm_all.file_type = 'video' THEN 1 END) as video_count,
    
    -- Amenities count
    COUNT(DISTINCT pa.amenity_id) as amenities_count,
    
    -- Developer info
    d.name as developer_name
    
FROM projects p
JOIN properties pr ON p.id = pr.project_id
JOIN locations l ON p.id = l.id
LEFT JOIN project_media pm ON p.id = pm.project_id AND pm.is_primary = TRUE
LEFT JOIN project_media pm_all ON p.id = pm_all.project_id AND pm_all.is_active = TRUE
LEFT JOIN project_amenities pa ON p.id = pa.project_id
LEFT JOIN amenities a ON pa.amenity_id = a.id
LEFT JOIN developers d ON p.developer_id = d.id

WHERE pr.status = 'Available'
GROUP BY p.id, p.name, p.project_status, p.project_type,
         pr.id, pr.bhk_count, pr.carpet_area_sqft, pr.sell_price, 
         pr.status, pr.floor_number,
         l.city, l.locality, l.area, l.state,
         pm.file_path, pm.file_type, d.name;
```

---

## 🧠 **Enhanced NLP Logic for Price Intent Detection**

### **Price Intent Patterns Supported:**

#### **1. Under/Below/Less Than:**
- "Show me properties under 50 lakhs"
- "Properties below 2 crore"
- "Houses less than 1.5 cr"
- **NLP Logic**: Extracts amount and unit, converts to lakhs, sets filter

#### **2. Above/More Than/Over:**
- "Properties above 100 lakhs"
- "Houses more than 3 crore"
- "Apartments over 75 lakhs"
- **NLP Logic**: Extracts amount and unit, converts to lakhs, sets filter

#### **3. Price Range:**
- "Properties between 50 lakhs and 2 crore"
- "Houses in range 1-3 crore"
- **NLP Logic**: Sets price range filter

#### **4. Unit Recognition:**
- **Lakh/Lac**: Direct conversion
- **Crore/Cr**: Multiply by 100
- **Million**: Multiply by 10
- **K**: Divide by 100

### **Example NLP Queries:**
```
User: "Show me 2 BHK apartments under 1 crore in Pune"
NLP Processing:
- BHK: 2 → Filter: "2 BHK"
- Price: 1 crore → Filter: "Under ₹100 Lakh"
- Location: Pune → Filter: "Pune"
```

---

## 💰 **Price Formatting Logic (Frontend)**

### **From sell_price (rupees) to Display:**

```javascript
// Format price in Indian format (lakhs/crores) from sellPrice in rupees
const formatPrice = (sellPrice) => {
    const priceInLakhs = sellPrice / 100000; // Convert rupees to lakhs
    if (priceInLakhs >= 100) {
        return `₹${(priceInLakhs / 100).toFixed(1)} Cr`;
    } else {
        return `₹${priceInLakhs.toFixed(0)} Lakh`;
    }
};

// Examples:
// sellPrice: 8500000 → "₹85 Lakh"
// sellPrice: 25000000 → "₹2.5 Cr"
// sellPrice: 45000000 → "₹4.5 Cr"
```

### **Price Per Sqft Calculation:**

```javascript
// Calculate price per sqft from sell_price and carpet_area_sqft
const pricePerSqft = property.sellPrice / property.carpet_area_sqft;

// Format price per sqft
const formatPricePerSqft = (pricePerSqft) => {
    const priceInLakhs = pricePerSqft / 100000;
    if (priceInLakhs >= 1) {
        return `₹${priceInLakhs.toFixed(2)} Lakh/sq ft`;
    } else {
        const priceInThousands = pricePerSqft / 1000;
        return `₹${priceInThousands.toFixed(1)} K/sq ft`;
    }
};
```

---

## 🎬 **Media Support Features**

### **Image Support:**
- ✅ JPEG, PNG, WebP formats
- ✅ Multiple categories (exterior, interior, floor plan, amenity)
- ✅ Primary image designation
- ✅ Alt text for accessibility
- ✅ Sort order for galleries

### **Video Support:**
- ✅ MP4, WebM, MOV formats
- ✅ Video tours and walkthroughs
- ✅ Duration tracking
- ✅ Thumbnail generation (future enhancement)

### **File Storage Structure:**
```
images/
└── projects/
    ├── lodha-park/
    │   ├── main.jpg          # Primary image
    │   ├── exterior-1.jpg    # Exterior views
    │   ├── interior-1.jpg    # Interior views
    │   ├── floor-plan.pdf    # Floor plans
    │   └── video-tour.mp4    # Video tours
    └── ...
```

---

## 🚀 **Benefits of Updated Structure**

### **Database Benefits:**
- **✅ Simplified**: Single price field instead of two
- **✅ Consistent**: All prices stored in same unit (rupees)
- **✅ Calculable**: Easy to perform price-based queries and calculations
- **✅ Scalable**: No need to manage separate lakh/crore fields

### **NLP Benefits:**
- **✅ Enhanced**: Better price intent detection
- **✅ Flexible**: Supports multiple price units and formats
- **✅ Accurate**: Proper conversion between units
- **✅ User-friendly**: Natural language queries work seamlessly

### **Frontend Benefits:**
- **✅ Cleaner**: Single price field to work with
- **✅ Consistent**: Uniform price formatting across all cards
- **✅ Maintainable**: Easier to update price logic
- **✅ Performance**: No need to handle multiple price fields

---

## 📋 **Next Steps Available**

1. **Create API endpoints** to fetch properties with new `sell_price` field
2. **Update backend models** to use the new field structure
3. **Test NLP queries** with various price formats
4. **Add more price patterns** (budget ranges, specific amounts)
5. **Implement actual database queries** instead of sample data

---

## 💡 **Key Takeaways**

- **Database**: Consolidated price fields into single `sell_price` field
- **NLP**: Enhanced price intent detection with unit conversion
- **Frontend**: Updated price formatting logic for new field structure
- **Media**: Added comprehensive image and video support
- **Performance**: Better indexing and query optimization

Your real estate application now has a cleaner, more maintainable price structure with enhanced NLP capabilities for price-based queries!

