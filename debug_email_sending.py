#!/usr/bin/env python3
"""
Debug email sending in the invitation system
"""

import sys
import os
import requests
import json

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_email_sending():
    """Debug email sending"""
    print("🔍 DEBUGGING EMAIL SENDING")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Server is running: {response.json()}")
    except Exception as e:
        print(f"❌ Server not running: {e}")
        return False
    
    # Test 2: Check email configuration
    try:
        response = requests.get(f"{base_url}/boards/debug/my-boards")
        if response.status_code == 200:
            print(f"✅ Debug endpoint working")
        else:
            print(f"❌ Debug endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Debug endpoint error: {e}")
    
    # Test 3: Try to send an invitation
    print(f"\n📧 Testing invitation sending...")
    
    # You'll need to provide a valid JWT token here
    # For now, let's just check if the endpoint exists
    try:
        response = requests.post(f"{base_url}/invitations/send", 
                               json={
                                   "board_id": 1,
                                   "invitee_email": "s.amini8585@gmail.com",
                                   "role": "member"
                               },
                               headers={"Authorization": "Bearer YOUR_TOKEN_HERE"})
        
        if response.status_code == 200:
            print(f"✅ Invitation endpoint working")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Invitation endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Invitation endpoint error: {e}")
    
    print(f"\n💡 TROUBLESHOOTING STEPS:")
    print(f"1. Check if .env file has correct email credentials")
    print(f"2. Make sure Gmail App Password is used (not regular password)")
    print(f"3. Check backend logs for email errors")
    print(f"4. Test email sending manually")
    
    return True

if __name__ == "__main__":
    debug_email_sending()
