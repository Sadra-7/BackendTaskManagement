#!/usr/bin/env python3
"""
Test email configuration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_email_config():
    """Test email configuration"""
    try:
        print("TESTING EMAIL CONFIGURATION")
        print("=" * 50)
        
        # Check environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        email_username = os.getenv("EMAIL_USERNAME")
        email_password = os.getenv("EMAIL_PASSWORD")
        frontend_url = os.getenv("FRONTEND_URL")
        
        print(f"EMAIL_USERNAME: {email_username}")
        print(f"EMAIL_PASSWORD: {'*' * len(email_password) if email_password else 'NOT SET'}")
        print(f"FRONTEND_URL: {frontend_url}")
        
        if not email_username:
            print("ERROR: EMAIL_USERNAME not set")
            return False
        
        if not email_password:
            print("ERROR: EMAIL_PASSWORD not set")
            return False
        
        # Test email sending
        from app.utils.send_email import send_email
        
        test_email = "s.amini8585@gmail.com"
        subject = "Test Email from Task Manager"
        body = "This is a test email to verify email configuration."
        
        print(f"\nSending test email to {test_email}...")
        send_email(test_email, subject, body)
        print("SUCCESS: Test email sent successfully!")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Email test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_email_config()
