#!/usr/bin/env python3
"""
Test invitation system to debug the 404 error
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_invitation_system():
    """Test invitation system"""
    try:
        print("🧪 TESTING INVITATION SYSTEM")
        print("=" * 50)
        
        # Test imports
        print("📦 Testing imports...")
        try:
            from app.models.invitation import BoardInvitation, BoardMember
            print("✅ Invitation models imported")
        except Exception as e:
            print(f"❌ Failed to import invitation models: {e}")
            return False
        
        try:
            from app.routers.invitations import router
            print("✅ Invitations router imported")
        except Exception as e:
            print(f"❌ Failed to import invitations router: {e}")
            return False
        
        # Test database connection
        print("\n🗄️ Testing database...")
        try:
            from app.db.database import SessionLocal
            db = SessionLocal()
            print("✅ Database connection successful")
            
            # Check if tables exist
            from sqlalchemy import inspect
            inspector = inspect(db.bind)
            tables = inspector.get_table_names()
            print(f"📊 Found {len(tables)} tables: {tables}")
            
            # Check for invitation tables
            if 'board_invitations' in tables:
                print("✅ board_invitations table exists")
            else:
                print("❌ board_invitations table missing")
                return False
                
            if 'board_members' in tables:
                print("✅ board_members table exists")
            else:
                print("❌ board_members table missing")
                return False
            
            db.close()
        except Exception as e:
            print(f"❌ Database test failed: {e}")
            return False
        
        # Test API endpoints
        print("\n🌐 Testing API endpoints...")
        try:
            from app.main import app
            print("✅ FastAPI app imported")
            
            # Check routes
            routes = []
            for route in app.routes:
                if hasattr(route, 'methods') and hasattr(route, 'path'):
                    routes.append(f"{list(route.methods)} {route.path}")
            
            invitation_routes = [r for r in routes if '/invitations' in r]
            print(f"🎯 Found {len(invitation_routes)} invitation routes:")
            for route in invitation_routes:
                print(f"  {route}")
            
            if not invitation_routes:
                print("❌ No invitation routes found!")
                return False
                
        except Exception as e:
            print(f"❌ API test failed: {e}")
            return False
        
        print("\n🎉 Invitation system test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_invitation_system()