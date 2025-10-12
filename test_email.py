#!/usr/bin/env python3
"""
Test email configuration and send a test email
"""

import os
from dotenv import load_dotenv
from app.utils.send_email import send_email

# Load environment variables
load_dotenv()

def test_email_configuration():
    """Test email configuration"""
    print("🔧 Testing Email Configuration...")
    
    # Check environment variables
    email_username = os.getenv("EMAIL_USERNAME")
    email_password = os.getenv("EMAIL_PASSWORD")
    
    print(f"📧 EMAIL_USERNAME: {'✅ Set' if email_username else '❌ Not set'}")
    print(f"🔑 EMAIL_PASSWORD: {'✅ Set' if email_password else '❌ Not set'}")
    
    if not email_username or not email_password:
        print("\n❌ Email configuration is incomplete!")
        print("Please set the following environment variables:")
        print("EMAIL_USERNAME=your-email@gmail.com")
        print("EMAIL_PASSWORD=your-app-password")
        return False
    
    return True

def send_test_email():
    """Send a test email"""
    print("\n📤 Sending test email...")
    
    try:
        send_email(
            to_email="test@example.com",  # Replace with your email
            subject="Test Email from Task Manager",
            body="This is a test email to verify email configuration is working."
        )
        print("✅ Test email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Task Manager Email Test")
    print("=" * 40)
    
    if test_email_configuration():
        print("\n📧 Configuration looks good!")
        print("To test email sending, update the email address in this script and run again.")
    else:
        print("\n❌ Please fix the configuration first.")
