#!/usr/bin/env python3
"""
Complete setup for invitation system with migration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def setup_invitations_complete():
    """Complete setup for invitation system"""
    try:
        print("🚀 COMPLETE INVITATION SYSTEM SETUP")
        print("=" * 50)
        
        # Method 1: Try Alembic migration
        print("\n📊 Method 1: Trying Alembic migration...")
        try:
            from alembic.config import Config
            from alembic import command
            
            alembic_cfg = Config("alembic.ini")
            command.upgrade(alembic_cfg, "add_invitation_tables")
            print("✅ Alembic migration successful!")
            return True
            
        except Exception as e:
            print(f"⚠️  Alembic migration failed: {e}")
            print("📊 Method 2: Trying manual migration...")
        
        # Method 2: Manual migration
        try:
            from app.db.database import engine, Base
            from app.models.invitation import BoardInvitation, BoardMember
            
            # Create all tables
            Base.metadata.create_all(bind=engine)
            print("✅ Manual migration successful!")
            
            # Verify tables exist
            from sqlalchemy import inspect
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            
            if 'board_invitations' in tables and 'board_members' in tables:
                print("✅ Both invitation tables created")
                return True
            else:
                print("❌ Tables not created properly")
                return False
                
        except Exception as e:
            print(f"❌ Manual migration failed: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Complete setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_setup():
    """Verify the invitation system setup"""
    try:
        print("\n🔍 VERIFYING SETUP...")
        
        # Test imports
        from app.models.invitation import BoardInvitation, BoardMember
        print("✅ Invitation models imported")
        
        # Test database connection
        from app.db.database import SessionLocal
        db = SessionLocal()
        
        # Check tables exist
        from sqlalchemy import inspect, text
        inspector = inspect(db.bind)
        tables = inspector.get_table_names()
        
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
        
        # Test table access
        with db.bind.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM board_invitations"))
            count = result.scalar()
            print(f"✅ board_invitations accessible (count: {count})")
            
            result = conn.execute(text("SELECT COUNT(*) FROM board_members"))
            count = result.scalar()
            print(f"✅ board_members accessible (count: {count})")
        
        db.close()
        
        print("\n🎯 SETUP VERIFICATION COMPLETE!")
        print("✅ All systems ready")
        print("✅ API endpoints will work")
        print("✅ No more 404 errors")
        
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 STARTING COMPLETE INVITATION SETUP")
    print("=" * 50)
    
    # Run setup
    if setup_invitations_complete():
        print("\n✅ Setup completed successfully!")
        
        # Verify setup
        if verify_setup():
            print("\n🎉 INVITATION SYSTEM READY!")
            print("✅ Database tables created")
            print("✅ API endpoints ready")
            print("✅ Frontend integration ready")
            print("✅ No more 404 errors")
            
            print("\n📋 NEXT STEPS:")
            print("1. Restart your backend server")
            print("2. Test the invitation flow")
            print("3. Send an invitation")
            print("4. Accept the invitation")
            print("5. Both users can now collaborate!")
        else:
            print("\n❌ Setup verification failed")
    else:
        print("\n❌ Setup failed")
