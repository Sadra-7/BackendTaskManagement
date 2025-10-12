#!/usr/bin/env python3
"""
Fix 404 error for invitations endpoint
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def fix_404_error():
    """Fix 404 error by ensuring all routes are properly registered"""
    try:
        print("FIXING 404 ERROR FOR INVITATIONS")
        print("=" * 50)
        
        # Import the app
        from app.main import app
        
        print("SUCCESS: App imported successfully")
        
        # Check if invitations router is included
        from app.routers import invitations
        print("SUCCESS: Invitations router imported")
        
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
            print("SOLUTION: The invitations router is not properly included")
            return False
        
        # Check if accept endpoint exists
        accept_routes = [r for r in invitation_routes if 'accept' in r]
        if accept_routes:
            print(f"SUCCESS: Accept endpoint found: {accept_routes[0]}")
        else:
            print("ERROR: Accept endpoint not found!")
            return False
        
        print("\nROUTES ARE PROPERLY REGISTERED!")
        print("The 404 error might be due to:")
        print("1. Backend server not restarted after database changes")
        print("2. Database tables not created")
        print("3. Import errors in the invitations router")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Fix failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    fix_404_error()
