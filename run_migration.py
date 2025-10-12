#!/usr/bin/env python3
"""
Run database migration for invitation tables
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import engine, Base
from app.models.invitation import BoardInvitation, BoardMember

def run_migration():
    """Create invitation tables"""
    try:
        print("🔧 Running database migration...")
        
        # Create all tables (including new ones)
        Base.metadata.create_all(bind=engine)
        
        print("✅ Database migration completed successfully!")
        print("✅ BoardInvitation table created")
        print("✅ BoardMember table created")
        
        return True
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    run_migration()
