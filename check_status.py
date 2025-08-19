#!/usr/bin/env python3
"""
Real Estate Application Status Checker
Checks if all components (backend, frontend, NLP) are running correctly
"""

import requests
import time
import sys

def check_backend():
    """Check if backend server is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend Server: RUNNING (http://localhost:8000)")
            return True
        else:
            print(f"❌ Backend Server: ERROR - Status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend Server: NOT RUNNING - {e}")
        return False

def check_frontend():
    """Check if frontend server is running"""
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend Server: RUNNING (http://localhost:3000)")
            return True
        else:
            print(f"❌ Frontend Server: ERROR - Status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend Server: NOT RUNNING - {e}")
        return False

def test_nlp_functionality():
    """Test NLP functionality with a sample query"""
    try:
        query = "Show me 2 BHK apartments in Pune"
        response = requests.post(
            "http://localhost:8000/api/v1/search/nlp",
            data={"query": query},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ NLP Engine: WORKING")
            print(f"   Query: {data.get('query', 'N/A')}")
            print(f"   Intent: {data.get('intent', 'N/A')}")
            print(f"   Results: {data.get('results_count', 0)} properties found")
            return True
        else:
            print(f"❌ NLP Engine: ERROR - Status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ NLP Engine: NOT RESPONDING - {e}")
        return False

def main():
    """Main status check function"""
    print("🏠 Real Estate Application Status Check")
    print("=" * 50)
    
    backend_ok = check_backend()
    frontend_ok = check_frontend()
    nlp_ok = test_nlp_functionality()
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    
    if all([backend_ok, frontend_ok, nlp_ok]):
        print("🎉 All systems are running correctly!")
        print("\n🌐 Access your application:")
        print("   Frontend: http://localhost:3000")
        print("   Backend API: http://localhost:8000")
        print("   API Docs: http://localhost:8000/docs")
        return 0
    else:
        print("⚠️  Some components are not working properly.")
        print("\n🔧 Troubleshooting:")
        if not backend_ok:
            print("   - Check if backend server is running")
            print("   - Run: cd backend && python main.py")
        if not frontend_ok:
            print("   - Check if frontend server is running")
            print("   - Run: python -m http.server 3000")
        if not nlp_ok:
            print("   - Check backend logs for NLP errors")
        return 1

if __name__ == "__main__":
    sys.exit(main())
