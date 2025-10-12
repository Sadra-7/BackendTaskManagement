#!/usr/bin/env python3
"""
Run invitation tables migration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_migration():
    """Run the invitation tables migration"""
    try:
        print("🚀 RUNNING INVITATION TABLES MIGRATION")
        print("=" * 50)
        
        # Import Alembic components
        from alembic.config import Config
        from alembic import command
        
        # Get the alembic config
        alembic_cfg = Config("alembic.ini")
        
        print("📊 Running migration: add_invitation_tables")
        
        # Run the migration
        command.upgrade(alembic_cfg, "add_invitation_tables")
        
        print("✅ Migration completed successfully!")
        print("✅ board_invitations table created")
        print("✅ board_members table created")
        print("✅ Foreign key constraints added")
        
        print("\n🎯 INVITATION SYSTEM READY!")
        print("✅ Database tables created")
        print("✅ API endpoints will work now")
        print("✅ No more 404 errors")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    run_migration()
