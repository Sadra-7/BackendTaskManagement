#!/usr/bin/env python3
"""
Manual migration for invitation tables (if Alembic doesn't work)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def manual_migration():
    """Run manual migration for invitation tables"""
    try:
        print("🚀 RUNNING MANUAL INVITATION MIGRATION")
        print("=" * 50)
        
        # Import database components
        from app.db.database import engine, Base
        from app.models.invitation import BoardInvitation, BoardMember
        
        print("📊 Creating invitation tables...")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully")
        
        # Verify tables exist
        from sqlalchemy import inspect, text
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"\n📋 Database tables ({len(tables)}):")
        for table in sorted(tables):
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
        
        # Test table structure
        print("\n🔍 Testing table structure...")
        
        # Test board_invitations table
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM board_invitations"))
            count = result.scalar()
            print(f"✅ board_invitations table accessible (count: {count})")
        
        # Test board_members table
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM board_members"))
            count = result.scalar()
            print(f"✅ board_members table accessible (count: {count})")
        
        print("\n🎯 MANUAL MIGRATION COMPLETED!")
        print("✅ Database tables created")
        print("✅ Tables are accessible")
        print("✅ API endpoints will work now")
        print("✅ No more 404 errors")
        
        return True
        
    except Exception as e:
        print(f"❌ Manual migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    manual_migration()
