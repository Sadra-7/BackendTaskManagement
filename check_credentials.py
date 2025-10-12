#!/usr/bin/env python3
"""
Check email credentials
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_credentials():
    """Check if email credentials are properly set"""
    print("🔍 CHECKING EMAIL CREDENTIALS")
    print("=" * 40)
    
    username = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")
    
    print(f"📧 EMAIL_USERNAME: {username}")
    print(f"🔑 EMAIL_PASSWORD: {'*' * len(password) if password else 'None'}")
    
    if not username:
        print("❌ EMAIL_USERNAME is not set!")
        return False
        
    if not password:
        print("❌ EMAIL_PASSWORD is not set!")
        return False
    
    # Check if it looks like a Gmail App Password
    if len(password) != 16:
        print(f"⚠️  Password length is {len(password)}, should be 16 characters")
        print("   This might not be a Gmail App Password")
    
    if not password.isalnum():
        print("⚠️  Password contains non-alphanumeric characters")
        print("   Gmail App Passwords should only contain letters and numbers")
    
    print("\n✅ Credentials are set!")
    print("\n🔧 If emails still don't work, try:")
    print("1. Generate a new Gmail App Password")
    print("2. Make sure 2-Factor Authentication is enabled")
    print("3. Check if your Gmail account is locked")
    
    return True

if __name__ == "__main__":
    check_credentials()
