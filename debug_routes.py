#!/usr/bin/env python3
"""
Debug routes to find the 404 issue
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_routes():
    """Debug routes to find the 404 issue"""
    try:
        print("DEBUGGING ROUTES")
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
        
        # Check if the route is properly registered
        if not invitation_routes:
            print("ERROR: No invitation routes found!")
            print("The invitations router is not properly included")
            return False
        
        if not accept_routes:
            print("ERROR: No accept routes found!")
            print("The accept endpoint is not registered")
            return False
        
        print("\nROUTES DEBUG COMPLETED!")
        return True
        
    except Exception as e:
        print(f"ERROR: Debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_routes()
