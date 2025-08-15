#!/usr/bin/env python3
"""
Simple script to explore Delhi data structure
"""

from backend.database import get_db
from backend.models import Location, Project, Property, ProjectLocation

def explore_delhi_data():
    """Explore Delhi data structure"""
    db = next(get_db())
    
    print("🔍 Exploring Delhi Data Structure:")
    print("=" * 50)
    
    # Check Delhi locations
    delhi_locations = db.query(Location).filter(Location.city.ilike('%Delhi%')).all()
    print(f"\n📍 Delhi Locations Found: {len(delhi_locations)}")
    for loc in delhi_locations:
        print(f"  • {loc.locality}, {loc.city} (Area: {loc.area}, Pincode: {loc.pincode})")
    
    # Check Delhi projects
    delhi_projects = db.query(Project).join(ProjectLocation).join(Location).filter(Location.city.ilike('%Delhi%')).all()
    print(f"\n🏢 Delhi Projects Found: {len(delhi_projects)}")
    for proj in delhi_projects:
        print(f"  • {proj.name} (Developer ID: {proj.developer_id})")
    
    # Check Delhi properties
    delhi_properties = db.query(Property).join(Project).join(ProjectLocation).join(Location).filter(Location.city.ilike('%Delhi%')).all()
    print(f"\n🏠 Delhi Properties Found: {len(delhi_properties)}")
    for prop in delhi_properties:
        print(f"  • {prop.bhk_count} BHK • {prop.property_type} • ₹{prop.sell_price:,}")
    
    # Check property types and BHK configurations
    print(f"\n🏗️ Property Types in Delhi:")
    property_types = db.query(Property.property_type).join(Project).join(ProjectLocation).join(Location).filter(Location.city.ilike('%Delhi%')).distinct().all()
    for pt in property_types:
        if pt[0]:
            print(f"  • {pt[0]}")
    
    print(f"\n🛏️ BHK Configurations in Delhi:")
    bhk_configs = db.query(Property.bhk_count).join(Project).join(ProjectLocation).join(Location).filter(Location.city.ilike('%Delhi%')).distinct().all()
    for bhk in sorted(bhk_configs):
        if bhk[0]:
            print(f"  • {bhk[0]} BHK")
    
    # Check price ranges
    print(f"\n💰 Price Ranges in Delhi:")
    prices = db.query(Property.sell_price).join(Project).join(ProjectLocation).join(Location).filter(Location.city.ilike('%Delhi%')).all()
    if prices:
        min_price = min(p[0] for p in prices if p[0])
        max_price = max(p[0] for p in prices if p[0])
        print(f"  • Min: ₹{min_price:,} ({min_price/100000:.1f} Lakh)")
        print(f"  • Max: ₹{max_price:,} ({max_price/100000:.1f} Lakh)")
    
    # Check nearby places if the table exists
    try:
        from backend.models import NearbyPlace
        print(f"\n🚇 Nearby Places for Delhi Projects:")
        delhi_nearby = db.query(NearbyPlace).join(Project).join(ProjectLocation).join(Location).filter(Location.city.ilike('%Delhi%')).distinct().all()
        for nearby in delhi_nearby[:10]:  # Show first 10
            print(f"  • {nearby.name} ({nearby.category})")
    except ImportError:
        print(f"\n🚇 Nearby Places table not available")
    
    print(f"\n" + "=" * 50)
    print("💡 Search Suggestions for Delhi:")
    print("  • Try: '2 BHK in Rajouri Garden'")
    print("  • Try: 'Properties under 1 crore in Delhi'")
    print("  • Try: '3 BHK apartments in Dwarka'")
    print("  • Try: 'Luxury properties in South Delhi'")

if __name__ == "__main__":
    explore_delhi_data()
