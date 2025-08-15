#!/usr/bin/env python3
"""
Script to check what endpoints are available on the backend
"""

import requests

def check_backend_endpoints():
    """Check what endpoints are available on the backend"""
    print("🔍 CHECKING BACKEND ENDPOINTS")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    # Test common endpoints
    endpoints = [
        "/",
        "/docs",
        "/openapi.json",
        "/search",
        "/api/search",
        "/properties",
        "/api/properties"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            print(f"   📍 {endpoint}: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ {endpoint}: Connection Error (Backend not running)")
        except Exception as e:
            print(f"   ❌ {endpoint}: Error - {e}")
    
    # Test POST to search endpoint
    print(f"\n2️⃣ TESTING POST TO SEARCH ENDPOINTS:")
    print("-" * 40)
    
    search_endpoints = [
        "/search",
        "/api/search",
        "/properties/search"
    ]
    
    for endpoint in search_endpoints:
        try:
            response = requests.post(
                f"{base_url}{endpoint}",
                json={"query": "test"},
                headers={"Content-Type": "application/json"}
            )
            print(f"   📍 POST {endpoint}: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ POST {endpoint}: Connection Error (Backend not running)")
        except Exception as e:
            print(f"   ❌ POST {endpoint}: Error - {e}")

if __name__ == "__main__":
    check_backend_endpoints()
