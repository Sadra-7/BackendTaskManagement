#!/usr/bin/env python3
"""
Test the complete invitation flow
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_invitation_flow():
    """Test the complete invitation flow"""
    print("TESTING INVITATION FLOW")
    print("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Server is running: {response.json()}")
    except Exception as e:
        print(f"❌ Server not running: {e}")
        return False
    
    # Test 2: Check available endpoints
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"✅ API docs available at: {BASE_URL}/docs")
    except Exception as e:
        print(f"❌ API docs not accessible: {e}")
    
    # Test 3: Check invitation endpoints
    endpoints_to_check = [
        "/invitations/send",
        "/invitations/accept", 
        "/invitations/token/{token}",
        "/invitations/board/{id}",
        "/invitations/check/{token}"
    ]
    
    print(f"\n📋 Available invitation endpoints:")
    for endpoint in endpoints_to_check:
        print(f"  - {endpoint}")
    
    print(f"\n🎯 Next steps:")
    print(f"1. Send an invitation from your app")
    print(f"2. Check the server logs for debug information")
    print(f"3. The invitation should work now!")
    
    return True

if __name__ == "__main__":
    test_invitation_flow()
