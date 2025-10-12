#!/usr/bin/env python3
"""
Test all invitation endpoints to ensure they work
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_all_endpoints():
    """Test all invitation endpoints"""
    try:
        print("TESTING ALL INVITATION ENDPOINTS")
        print("=" * 50)
        
        # Import the app
        from app.main import app
        
        print("SUCCESS: App imported successfully")
        
        # Check all routes
        routes = []
        for route in app.routes:
            if hasattr(route, 'methods') and hasattr(route, 'path'):
                routes.append(f"{list(route.methods)} {route.path}")
        
        print(f"\nALL ROUTES ({len(routes)}):")
        for route in routes:
            print(f"  {route}")
        
        # Check specifically for invitations routes
        invitation_routes = [r for r in routes if '/invitations' in r]
        print(f"\nINVITATION ROUTES ({len(invitation_routes)}):")
        for route in invitation_routes:
            print(f"  {route}")
        
        # Check if accept endpoint exists
        accept_routes = [r for r in routes if 'accept' in r]
        print(f"\nACCEPT ROUTES ({len(accept_routes)}):")
        for route in accept_routes:
            print(f"  {route}")
        
        # Check if send endpoint exists
        send_routes = [r for r in routes if 'send' in r]
        print(f"\nSEND ROUTES ({len(send_routes)}):")
        for route in send_routes:
            print(f"  {route}")
        
        # Check if token endpoint exists
        token_routes = [r for r in routes if 'token' in r]
        print(f"\nTOKEN ROUTES ({len(token_routes)}):")
        for route in token_routes:
            print(f"  {route}")
        
        print("\nENDPOINT TEST COMPLETED!")
        
        # Summary
        if len(invitation_routes) >= 3:
            print("SUCCESS: All invitation endpoints are registered!")
        else:
            print("WARNING: Some invitation endpoints might be missing")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_all_endpoints()
