#!/usr/bin/env python3
"""
Debug API endpoints to check if invitations router is working
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_endpoints():
    """Debug API endpoints"""
    try:
        print("🔍 DEBUGGING API ENDPOINTS")
        print("=" * 50)
        
        # Import the app
        from app.main import app
        
        print("✅ App imported successfully")
        
        # Check routes
        routes = []
        for route in app.routes:
            if hasattr(route, 'methods') and hasattr(route, 'path'):
                routes.append(f"{list(route.methods)} {route.path}")
        
        print(f"\n📋 Found {len(routes)} routes:")
        for route in routes:
            print(f"  {route}")
        
        # Check specifically for invitations routes
        invitation_routes = [r for r in routes if '/invitations' in r]
        print(f"\n🎯 Invitation routes ({len(invitation_routes)}):")
        for route in invitation_routes:
            print(f"  {route}")
        
        if not invitation_routes:
            print("❌ No invitation routes found!")
            return False
        
        # Check if accept endpoint exists
        accept_routes = [r for r in invitation_routes if 'accept' in r]
        if accept_routes:
            print(f"✅ Accept endpoint found: {accept_routes[0]}")
        else:
            print("❌ Accept endpoint not found!")
            return False
        
        print("\n🎉 API endpoints debug completed!")
        return True
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_endpoints()
