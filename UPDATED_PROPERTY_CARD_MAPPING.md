# 🏠 **UPDATED Property Card to Database Field Mappings**

## ✅ **Database Tables Available**

| **Table Name** | **Purpose** | **Key Fields** |
|----------------|-------------|----------------|
| `projects` | Main project information | `id`, `name`, `project_status`, `project_type` |
| `properties` | Individual property units | `id`, `bhk_count`, `carpet_area_sqft`, `price_lakhs`, `status` |
| `locations` | City, locality, area info | `city`, `locality`, `area`, `state` |
| `amenities` | Available amenities | `name`, `category` |
| `project_amenities` | Amenity mapping | `project_id`, `amenity_id`, `available` |
| `project_media` | **NEW: Images & Videos** | `file_path`, `file_type`, `media_category`, `is_primary` |
| `developers` | Developer information | `name`, `description` |

---

## 🎯 **Property Card Field Mappings**

### **1. Status Tag**
- **Frontend Display**: "Available", "New Listing", "Premium"
- **Database Source**: `properties.status`
- **Mapping**: Direct field access

### **2. Image Display**
- **Frontend Display**: Project image or placeholder icon
- **Database Source**: `project_media.file_path` WHERE `is_primary = TRUE`
- **Fallback**: Building icon placeholder if no image exists
- **Mapping**: Join via `project_id`

### **3. Image Counter**
- **Frontend Display**: "1/4", "1/5"
- **Database Source**: `COUNT(*)` from `project_media` WHERE `project_id = X`
- **Mapping**: Aggregate query

### **4. Price Main**
- **Frontend Display**: ₹85 Lakh, ₹1.2 Cr
- **Database Source**: `properties.price_lakhs` + `properties.price_crores`
- **Mapping**: Conditional logic (show crores if ≥100 lakhs)

### **5. Price Per Sqft**
- **Frontend Display**: ₹8,500/sq ft
- **Database Source**: `properties.price_lakhs` ÷ `properties.carpet_area_sqft`
- **Mapping**: Calculated field

### **6. Property Specs**
- **Frontend Display**: "2 BHK • 2 Bath • 1,200 sq ft • Apartment"
- **Database Source**: Multiple tables
- **Mapping**: Complex join
  - BHK: `properties.bhk_count`
  - Area: `properties.carpet_area_sqft`
  - Type: `projects.project_type`

### **7. Locality & City**
- **Frontend Display**: "Baner, Pune"
- **Database Source**: `locations.locality` + `locations.city`
- **Mapping**: Direct field access

### **8. Amenities**
- **Frontend Display**: ["Gym", "Parking", "Pet-friendly"]
- **Database Source**: `project_amenities` + `amenities.name`
- **Mapping**: Join via `project_id`

### **9. Project Name**
- **Frontend Display**: "Lodha Park" (with asterisks)
- **Database Source**: `projects.name`
- **Mapping**: Direct field access + frontend formatting

---

## 🔍 **Complete Database Query for Property Cards**

```sql
-- Main query to get property data for cards with media support
SELECT 
    -- Project information
    p.id as project_id,
    p.name as project_name,
    p.project_status,
    p.project_type,
    
    -- Property details
    pr.id as property_id,
    pr.bhk_count,
    pr.carpet_area_sqft,
    pr.price_lakhs,
    pr.price_crores,
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
JOIN locations l ON p.id = l.id  -- Assuming location relationship
LEFT JOIN project_media pm ON p.id = pm.project_id AND pm.is_primary = TRUE
LEFT JOIN project_media pm_all ON p.id = pm_all.project_id AND pm_all.is_active = TRUE
LEFT JOIN project_amenities pa ON p.id = pa.project_id
LEFT JOIN amenities a ON pa.amenity_id = a.id
LEFT JOIN developers d ON p.developer_id = d.id

WHERE pr.status = 'Available'
GROUP BY p.id, p.name, p.project_status, p.project_type,
         pr.id, pr.bhk_count, pr.carpet_area_sqft, pr.price_lakhs, 
         pr.price_crores, pr.status, pr.floor_number,
         l.city, l.locality, l.area, l.state,
         pm.file_path, pm.file_type, d.name;
```

---

## 📁 **File Storage Structure**

```
images/
└── projects/
    ├── lodha-park/
    │   ├── main.jpg          # Primary image
    │   ├── exterior-1.jpg    # Exterior views
    │   ├── interior-1.jpg    # Interior views
    │   ├── floor-plan.pdf    # Floor plans
    │   └── video-tour.mp4    # Video tours
    ├── dlf-cyber-city/
    │   ├── main.jpg
    │   └── ...
    └── prestige-tech-park/
        ├── main.jpg
        └── ...
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

### **File Management:**
- ✅ Relative path storage
- ✅ File size tracking
- ✅ MIME type detection
- ✅ Active/inactive status
- ✅ Featured media designation

---

## 🚀 **Next Steps**

1. **Create API endpoints** to fetch properties with media
2. **Update frontend** to use real database data
3. **Implement image loading** with fallback placeholders
4. **Add video support** for property tours
5. **Create media upload** functionality for admins

---

## 💡 **Benefits of This Structure**

- **Scalable**: Supports unlimited media per project
- **Organized**: Clear categorization and sorting
- **Flexible**: Works with images, videos, and documents
- **Performance**: Indexed for fast queries
- **Maintainable**: Clear separation of concerns
