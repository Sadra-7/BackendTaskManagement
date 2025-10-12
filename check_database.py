#!/usr/bin/env python3
"""
Check database tables
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_database():
    """Check if database tables exist"""
    try:
        from app.db.database import engine
        from sqlalchemy import inspect
        
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print("🔍 DATABASE TABLES CHECK")
        print("=" * 40)
        print(f"Total tables: {len(tables)}")
        
        for table in tables:
            print(f"✅ {table}")
        
        # Check for invitation tables
        if 'board_invitations' in tables:
            print("\n✅ BoardInvitation table exists")
        else:
            print("\n❌ BoardInvitation table missing")
            
        if 'board_members' in tables:
            print("✅ BoardMember table exists")
        else:
            print("❌ BoardMember table missing")
        
        # Check if we need to create tables
        if 'board_invitations' not in tables or 'board_members' not in tables:
            print("\n🔧 CREATING MISSING TABLES...")
            from app.db.database import Base
            Base.metadata.create_all(bind=engine)
            print("✅ Tables created successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return False

if __name__ == "__main__":
    check_database()
