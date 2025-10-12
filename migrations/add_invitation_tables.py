"""
Migration script to add invitation and board member tables
Run this script to create the new tables in your database
"""

from sqlalchemy import create_engine, text
from app.db.database import Base, engine
from app.models.invitation import BoardInvitation, BoardMember
import os

def run_migration():
    """Create the new tables for invitations and board members"""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Migration completed successfully!")
        print("📋 Created tables:")
        print("   - board_invitations")
        print("   - board_members")
        print("\n🔧 Next steps:")
        print("1. Set up your email configuration in .env file")
        print("2. Update your frontend to use the new invitation endpoints")
        print("3. Test the invitation flow")
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        raise

if __name__ == "__main__":
    run_migration()
