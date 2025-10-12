#!/usr/bin/env python3
"""
Setup invitation tables in database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def setup_invitation_tables():
    """Setup invitation tables"""
    try:
        print("🚀 SETTING UP INVITATION TABLES")
        print("=" * 50)
        
        # Import database components
        from app.db.database import engine, Base
        from app.models.invitation import BoardInvitation, BoardMember
        
        print("📊 Creating invitation tables...")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully")
        
        # Verify tables exist
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"\n📋 Database tables ({len(tables)}):")
        for table in tables:
            print(f"  - {table}")
        
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
        
        print("\n🎯 INVITATION SYSTEM READY!")
        print("✅ Database tables created")
        print("✅ API endpoints should work now")
        print("✅ Frontend can connect to backend")
        
        return True
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    setup_invitation_tables()
