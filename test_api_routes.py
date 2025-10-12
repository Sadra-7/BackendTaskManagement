#!/usr/bin/env python3
"""
Test API routes to debug 404 error
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_api_routes():
    """Test API routes to debug 404 error"""
    try:
        print("TESTING API ROUTES")
        print("=" * 50)
        
        # Import the app
        from app.main import app
        
        print("SUCCESS: App imported successfully")
        
        # Check routes
        routes = []
        for route in app.routes:
            if hasattr(route, 'methods') and hasattr(route, 'path'):
                routes.append(f"{list(route.methods)} {route.path}")
        
        print(f"\nFOUND {len(routes)} ROUTES:")
        for route in routes:
            print(f"  {route}")
        
        # Check specifically for invitations routes
        invitation_routes = [r for r in routes if '/invitations' in r]
        print(f"\nINVITATION ROUTES ({len(invitation_routes)}):")
        for route in invitation_routes:
            print(f"  {route}")
        
        if not invitation_routes:
            print("ERROR: No invitation routes found!")
            return False
        
        # Check if accept endpoint exists
        accept_routes = [r for r in invitation_routes if 'accept' in r]
        if accept_routes:
            print(f"SUCCESS: Accept endpoint found: {accept_routes[0]}")
        else:
            print("ERROR: Accept endpoint not found!")
            return False
        
        print("\nAPI ROUTES TEST COMPLETED!")
        return True
        
    except Exception as e:
        print(f"ERROR: Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_api_routes()
