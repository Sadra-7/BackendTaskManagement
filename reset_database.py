#!/usr/bin/env python3
"""
Database Reset Script
This script will completely reset the database by dropping all tables and recreating them.
"""

import os
import sys
from sqlalchemy import create_engine, text
from app.db.database import SQLALCHEMY_DATABASE_URL, Base
from app.models.user import User, UserRole
from app.utils.hashing import hash_password

def reset_database():
    """Reset the database by dropping all tables and recreating them."""
    
    print("🔄 Starting database reset...")
    
    # Create engine
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    try:
        # Drop all tables
        print("🗑️  Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        
        # Create all tables
        print("🏗️  Creating all tables...")
        Base.metadata.create_all(bind=engine)
        
        # Create superadmin user
        print("👤 Creating superadmin user...")
        from sqlalchemy.orm import sessionmaker
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        try:
            superadmin_email = "sadra.amini1006@gmail.com"
            new_superadmin = User(
                username="superadmin",
                email=superadmin_email,
                hashed_password=hash_password("admin1234"),
                role=UserRole.SUPERADMIN
            )
            db.add(new_superadmin)
            db.commit()
            print(f"✅ Superadmin created -> Email: {superadmin_email} | Password: admin1234")
        except Exception as e:
            print(f"⚠️  Superadmin creation failed: {e}")
        finally:
            db.close()
        
        print("✅ Database reset completed successfully!")
        print("📊 All data has been cleared and tables recreated.")
        print("🔑 Superadmin credentials:")
        print("   Email: sadra.amini1006@gmail.com")
        print("   Password: admin1234")
        
    except Exception as e:
        print(f"❌ Database reset failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    reset_database()


