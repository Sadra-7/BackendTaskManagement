#!/usr/bin/env python3
"""
Simple test for board access
"""

import sys
import os
import requests
import json

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_board_access_simple():
    """Test board access with API calls"""
    print("🔍 TESTING BOARD ACCESS")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Server is running: {response.json()}")
    except Exception as e:
        print(f"❌ Server not running: {e}")
        return False
    
    # Test 2: Check debug endpoint
    try:
        response = requests.get(f"{base_url}/boards/debug/my-boards")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Debug endpoint working:")
            print(f"  User: {data['user_email']}")
            print(f"  Owned boards: {len(data['owned_boards'])}")
            print(f"  Member boards: {len(data['member_boards'])}")
            print(f"  Memberships: {len(data['memberships'])}")
            
            if data['owned_boards']:
                print(f"  Owned boards:")
                for board in data['owned_boards']:
                    print(f"    - {board['title']} (ID: {board['id']})")
            
            if data['member_boards']:
                print(f"  Member boards:")
                for board in data['member_boards']:
                    print(f"    - {board['title']} (ID: {board['id']})")
            
            if data['memberships']:
                print(f"  Memberships:")
                for membership in data['memberships']:
                    print(f"    - Board ID: {membership['board_id']}, Role: {membership['role']}")
        else:
            print(f"❌ Debug endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Debug endpoint error: {e}")
    
    # Test 3: Check all boards endpoint
    try:
        response = requests.get(f"{base_url}/boards/all")
        if response.status_code == 200:
            boards = response.json()
            print(f"✅ All boards endpoint working: {len(boards)} boards")
            for board in boards:
                print(f"  - {board['title']} (ID: {board['id']})")
        else:
            print(f"❌ All boards endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ All boards endpoint error: {e}")
    
    print(f"\n🎯 RECOMMENDATIONS:")
    print(f"1. Check if the user has board memberships")
    print(f"2. Verify the boards endpoint is working")
    print(f"3. Check frontend API calls")
    
    return True

if __name__ == "__main__":
    test_board_access_simple()
