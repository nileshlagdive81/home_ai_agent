# Real Estate NLP - Field-Specific Queries Summary

This document provides a comprehensive overview of all the field-specific queries that the NLP system can handle for real estate projects.

## 🏗️ Project Fields

### 1. Project Name
- **Intent**: `GET_DETAILS`
- **Entities**: `PROJECT_NAME`
- **Example Queries**:
  - "What is the name of this project?"
  - "Tell me the project name"
  - "What's this project called?"
  - "Project name please"
  - "What do they call this project?"
  - "Name of the project"
  - "What is the project title?"
  - "Project title please"

### 2. Developer Name
- **Intent**: `GET_DETAILS`
- **Entities**: `DEVELOPER`
- **Example Queries**:
  - "Who is the developer?"
  - "Tell me the developer name"
  - "Which company built this?"
  - "Developer company name"
  - "Who developed this project?"
  - "Name of the builder"
  - "Which builder made this?"
  - "Developer please"

### 3. Locality
- **Intent**: `FILTER_BY_LOCATION`
- **Entities**: `LOCATION`
- **Example Queries**:
  - "Where is this project located?"
  - "What is the locality?"
  - "Which area is this in?"
  - "Location of the project"
  - "What locality is this?"
  - "Area name please"
  - "Which locality?"
  - "Where exactly is this?"

### 4. City
- **Intent**: `FILTER_BY_LOCATION`
- **Entities**: `LOCATION`
- **Example Queries**:
  - "Which city is this in?"
  - "What city is this project?"
  - "City name please"
  - "Which city?"
  - "What's the city?"
  - "City of the project"
  - "In which city?"
  - "City please"

### 5. Property Type
- **Intent**: `FILTER_BY_PROPERTY_TYPE`
- **Entities**: `PROPERTY_TYPE`
- **Example Queries**:
  - "What type of property is this?"
  - "Is this an apartment or villa?"
  - "Property type please"
  - "What kind of property?"
  - "Type of property"
  - "Apartment or villa?"
  - "Which property type?"
  - "Property category"

### 6. Total Units
- **Intent**: `GET_DETAILS`
- **Entities**: `QUANTITY`
- **Example Queries**:
  - "How many units are there?"
  - "Total number of units"
  - "How many flats in total?"
  - "Total units count"
  - "Number of units"
  - "How many units total?"
  - "Units count please"
  - "Total flats"

### 7. Units Per Floor
- **Intent**: `GET_DETAILS`
- **Entities**: `QUANTITY`
- **Example Queries**:
  - "How many units per floor?"
  - "Units on each floor"
  - "Flats per floor"
  - "How many per floor?"
  - "Units per floor count"
  - "Per floor units"
  - "How many on one floor?"
  - "Floor unit count"

### 8. Total Floors
- **Intent**: `GET_DETAILS`
- **Entities**: `QUANTITY`
- **Example Queries**:
  - "How many floors?"
  - "Total number of floors"
  - "How many stories?"
  - "Floor count"
  - "Number of floors"
  - "How many floors total?"
  - "Total stories"
  - "Floor height"

### 9. Project Status
- **Intent**: `GET_DETAILS`
- **Entities**: `STATUS`
- **Example Queries**:
  - "What is the project status?"
  - "Is it ready to move?"
  - "Project completion status"
  - "When will it be ready?"
  - "Construction status"
  - "Is it completed?"
  - "Ready to move?"
  - "Status please"

### 10. Possession Date
- **Intent**: `GET_DETAILS`
- **Entities**: `DATE`
- **Example Queries**:
  - "When can I move in?"
  - "Possession date"
  - "When will it be ready?"
  - "Move in date"
  - "Completion date"
  - "When can I get keys?"
  - "Ready date"
  - "Handover date"

### 11. RERA Number
- **Intent**: `GET_DETAILS`
- **Entities**: `RERA_NUMBER`
- **Example Queries**:
  - "What is the RERA number?"
  - "RERA number please"
  - "RERA registration number"
  - "RERA ID"
  - "RERA number"
  - "Registration number"
  - "RERA please"
  - "RERA details"

### 12. Description
- **Intent**: `GET_DETAILS`
- **Entities**: `DESCRIPTION`
- **Example Queries**:
  - "Tell me about this project"
  - "Project description"
  - "What is this project about?"
  - "Tell me more"
  - "Project details"
  - "What's special about this?"
  - "Project overview"
  - "Description please"

### 13. Highlights
- **Intent**: `GET_DETAILS`
- **Entities**: `FEATURES`
- **Example Queries**:
  - "What are the highlights?"
  - "Project highlights"
  - "Special features"
  - "What's special?"
  - "Key features"
  - "Main attractions"
  - "What stands out?"
  - "Highlights please"

## 🏠 Property Unit Fields

### 1. BHK
- **Intent**: `FILTER_BY_BHK`
- **Entities**: `BHK`
- **Example Queries**:
  - "How many BHK?"
  - "What is the BHK?"
  - "Bedroom count"
  - "How many bedrooms?"
  - "BHK please"
  - "Number of bedrooms"
  - "What BHK is this?"
  - "Bedroom count please"

### 2. Carpet Area
- **Intent**: `GET_DETAILS`
- **Entities**: `AREA`
- **Example Queries**:
  - "What is the carpet area?"
  - "Carpet area please"
  - "How big is it?"
  - "Area size"
  - "Square feet"
  - "What's the area?"
  - "Size of the flat"
  - "Area please"

### 3. Price
- **Intent**: `PRICE_QUERY`
- **Entities**: `PRICE`
- **Example Queries**:
  - "What is the price?"
  - "How much does it cost?"
  - "Price please"
  - "Cost of the property"
  - "What's the price?"
  - "Total cost"
  - "How much?"
  - "Price details"

### 4. Price Per Square Foot
- **Intent**: `PRICE_QUERY`
- **Entities**: `PRICE`
- **Example Queries**:
  - "Price per square foot?"
  - "Rate per sq ft"
  - "Per sq ft price"
  - "Square foot rate"
  - "Price per sq ft please"
  - "Rate per square foot"
  - "Per sq ft cost"
  - "Square foot price"

### 5. Booking Amount
- **Intent**: `PRICE_QUERY`
- **Entities**: `PRICE`
- **Example Queries**:
  - "How much booking amount?"
  - "Booking amount please"
  - "Initial payment"
  - "How much to book?"
  - "Booking payment"
  - "Advance amount"
  - "Initial amount"
  - "Booking cost"

## 🏊 Amenity Fields

### 1. Basic Amenities
- **Intent**: `FILTER_BY_AMENITY`
- **Entities**: `AMENITY`
- **Example Queries**:
  - "What basic amenities are there?"
  - "Basic facilities"
  - "Essential amenities"
  - "Basic features"
  - "What basic things?"
  - "Basic facilities list"
  - "Essential features"
  - "Basic amenities please"

### 2. Luxury Amenities
- **Intent**: `FILTER_BY_AMENITY`
- **Entities**: `AMENITY`
- **Example Queries**:
  - "What luxury amenities?"
  - "Premium facilities"
  - "Luxury features"
  - "High-end amenities"
  - "Premium features"
  - "Luxury facilities"
  - "High-end features"
  - "Luxury amenities please"

### 3. Security Features
- **Intent**: `FILTER_BY_AMENITY`
- **Entities**: `AMENITY`
- **Example Queries**:
  - "What security features?"
  - "Security amenities"
  - "Safety features"
  - "Security facilities"
  - "What security?"
  - "Safety amenities"
  - "Security please"
  - "Security features list"

## 📍 Nearby Places

### 1. Metro Station
- **Intent**: `FILTER_BY_AMENITY`
- **Entities**: `LOCATION`, `DISTANCE`
- **Example Queries**:
  - "Is there metro nearby?"
  - "Metro station distance"
  - "How far is metro?"
  - "Near metro station?"
  - "Metro accessibility"
  - "Metro nearby?"
  - "Metro station please"
  - "Metro distance"

### 2. Hospital
- **Intent**: `FILTER_BY_AMENITY`
- **Entities**: `LOCATION`, `DISTANCE`
- **Example Queries**:
  - "Is there hospital nearby?"
  - "Hospital distance"
  - "How far is hospital?"
  - "Near hospital?"
  - "Hospital accessibility"
  - "Hospital nearby?"
  - "Hospital please"
  - "Hospital distance"

### 3. School
- **Intent**: `FILTER_BY_AMENITY`
- **Entities**: `LOCATION`, `DISTANCE`
- **Example Queries**:
  - "Is there school nearby?"
  - "School distance"
  - "How far is school?"
  - "Near school?"
  - "School accessibility"
  - "School nearby?"
  - "School please"
  - "School distance"

### 4. Shopping Mall
- **Intent**: `FILTER_BY_AMENITY`
- **Entities**: `LOCATION`, `DISTANCE`
- **Example Queries**:
  - "Is there mall nearby?"
  - "Mall distance"
  - "How far is mall?"
  - "Near shopping mall?"
  - "Mall accessibility"
  - "Mall nearby?"
  - "Shopping mall please"
  - "Mall distance"

## 🔍 Simple Search Queries

### 1. By Location
- **Intent**: `SEARCH_PROPERTY`
- **Entities**: `LOCATION`
- **Example Queries**:
  - "Show me projects in Mumbai"
  - "Properties in Delhi"
  - "Flats in Bangalore"
  - "Houses in Pune"
  - "Projects in Hyderabad"
  - "Properties in Chennai"
  - "Flats in Kolkata"
  - "Houses in Ahmedabad"

### 2. By BHK
- **Intent**: `SEARCH_PROPERTY`
- **Entities**: `BHK`
- **Example Queries**:
  - "Show me 2BHK properties"
  - "3BHK flats"
  - "1BHK apartments"
  - "4BHK houses"
  - "2BHK projects"
  - "3BHK properties"
  - "1BHK flats"
  - "4BHK apartments"

### 3. By Price Range
- **Intent**: `SEARCH_PROPERTY`
- **Entities**: `PRICE`
- **Example Queries**:
  - "Properties under 50 lakhs"
  - "Flats under 1 crore"
  - "Houses under 2 crores"
  - "Properties under 100 lakhs"
  - "Affordable properties"
  - "Budget properties"
  - "Cheap properties"
  - "Low cost properties"

### 4. By Status
- **Intent**: `SEARCH_PROPERTY`
- **Entities**: `STATUS`
- **Example Queries**:
  - "Ready to move properties"
  - "Under construction projects"
  - "Completed projects"
  - "New projects"
  - "Ready properties"
  - "Construction projects"
  - "Finished projects"
  - "New properties"

## 🎯 Intent Classification Summary

| Intent | Description | Primary Use Case |
|--------|-------------|------------------|
| `SEARCH_PROPERTY` | Find properties matching criteria | General property search |
| `FILTER_BY_LOCATION` | Filter by city/locality | Location-based search |
| `FILTER_BY_PROPERTY_TYPE` | Filter by property type | Property category search |
| `FILTER_BY_BHK` | Filter by bedroom count | BHK-based search |
| `FILTER_BY_AMENITY` | Filter by amenities | Feature-based search |
| `GET_DETAILS` | Get specific information | Information retrieval |
| `PRICE_QUERY` | Price-related questions | Cost information |
| `COMPARE_PROPERTIES` | Compare multiple projects | Property comparison |
| `BOOK_VIEWING` | Schedule property visits | Appointment booking |

## 🔧 Entity Types Summary

| Entity | Description | Examples |
|--------|-------------|----------|
| `PROJECT_NAME` | Project identification | "Luxury Heights", "Green Valley" |
| `DEVELOPER` | Builder/developer company | "Premium Developers Ltd" |
| `LOCATION` | Geographic location | "Mumbai", "Bandra West" |
| `PROPERTY_TYPE` | Property category | "Apartment", "Villa" |
| `QUANTITY` | Numeric values | "120 units", "30 floors" |
| `STATUS` | Project status | "Ready to move", "Under construction" |
| `DATE` | Temporal information | "June 2024", "Tomorrow" |
| `RERA_NUMBER` | RERA registration | "MahaRERA/A51234/2020" |
| `DESCRIPTION` | Project description | "Premium luxury apartments" |
| `FEATURES` | Project highlights | "Sea View", "Premium Amenities" |
| `BHK` | Bedroom count | "2BHK", "3BHK" |
| `AREA` | Property area | "1200 sq ft", "Carpet area" |
| `PRICE` | Cost information | "50 lakhs", "1 crore" |
| `AMENITY` | Facility features | "Swimming Pool", "Gym" |
| `DISTANCE` | Proximity measurement | "0.5 km", "Nearby" |

## 📊 Training Data Statistics

- **Total Fields Covered**: 25+
- **Total Example Queries**: 200+
- **Intent Categories**: 9
- **Entity Types**: 15
- **Response Templates**: 25+

## 🚀 Usage Examples

### Basic Field Query
```
User: "What is the project name?"
System: "The project name is {project_name}"
Intent: GET_DETAILS
Entities: PROJECT_NAME
```

### Complex Search Query
```
User: "Show me 2BHK properties in Mumbai under 1 crore"
System: "Here are 2BHK properties in Mumbai under 1 crore"
Intent: SEARCH_PROPERTY
Entities: BHK(2), LOCATION(Mumbai), PRICE(1 crore)
```

### Amenity Query
```
User: "Is there metro nearby?"
System: "Metro station is {distance} km away"
Intent: FILTER_BY_AMENITY
Entities: LOCATION(metro), DISTANCE
```

This comprehensive training data ensures that the NLP system can handle queries for every field in the real estate projects, providing accurate intent classification and entity extraction for a seamless user experience.
