# Property Images Directory

This directory contains property images for the Real Estate Search Application.

## Structure
```
images/
├── projects/           # Project-specific property images
│   ├── lodha-park.jpg
│   ├── godrej-properties.jpg
│   ├── mahindra-lifespaces.jpg
│   ├── kolte-patil.jpg
│   ├── purvankara.jpg
│   └── sobha-developers.jpg
└── placeholder-property.jpg  # Fallback image when project image not found
```

## Image Requirements
- **Format**: JPG or PNG
- **Size**: Recommended 400x300 pixels or larger
- **Aspect Ratio**: 4:3 or 16:9
- **File Size**: Keep under 500KB for web performance

## Fallback System
- If a project image is not found, the system will show `placeholder-property.jpg`
- If no placeholder exists, it will show a colored background with an icon

## Database Storage
- Store only the image path in the database (e.g., "images/projects/lodha-park.jpg")
- Do NOT store the actual image binary data in the database
- Images are served from the file system for better performance

## Adding New Images
1. Place the image file in the appropriate directory
2. Update the database with the correct image path
3. Ensure the image follows the size and format requirements
