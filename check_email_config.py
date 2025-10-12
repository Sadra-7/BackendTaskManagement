#!/usr/bin/env python3
"""
Check email configuration
"""

import sys
import os
from dotenv import load_dotenv

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_email_config():
    """Check email configuration"""
    print("🔍 CHECKING EMAIL CONFIGURATION")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check .env file exists
    env_file = ".env"
    if not os.path.exists(env_file):
        print(f"❌ .env file not found!")
        print(f"💡 Create a .env file with:")
        print(f"   EMAIL_USERNAME=your-email@gmail.com")
        print(f"   EMAIL_PASSWORD=your-app-password")
        return False
    
    print(f"✅ .env file found")
    
    # Check email credentials
    email_username = os.getenv("EMAIL_USERNAME")
    email_password = os.getenv("EMAIL_PASSWORD")
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    print(f"\n📋 Current Configuration:")
    print(f"  EMAIL_USERNAME: {email_username}")
    print(f"  EMAIL_PASSWORD: {'*' * len(email_password) if email_password else 'NOT SET'}")
    print(f"  FRONTEND_URL: {frontend_url}")
    
    if not email_username:
        print(f"❌ EMAIL_USERNAME not set")
        return False
    
    if not email_password:
        print(f"❌ EMAIL_PASSWORD not set")
        return False
    
    print(f"✅ Email credentials found")
    
    # Check if it's a Gmail account
    if "@gmail.com" in email_username:
        print(f"✅ Gmail account detected")
        print(f"💡 Make sure you're using an App Password, not your regular password")
        print(f"   To create App Password:")
        print(f"   1. Go to Google Account settings")
        print(f"   2. Security > 2-Step Verification")
        print(f"   3. App passwords > Generate")
        print(f"   4. Use the generated password")
    else:
        print(f"⚠️  Non-Gmail account detected")
        print(f"💡 Make sure your email provider supports SMTP")
    
    return True

if __name__ == "__main__":
    check_email_config()
