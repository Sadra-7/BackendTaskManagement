#!/usr/bin/env python3
"""
Simple email test script
"""

import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

# Load environment variables
load_dotenv()

def test_email():
    """Test email configuration"""
    try:
        print("🔧 Testing Email Configuration...")
        
        # Get credentials
        username = os.getenv("EMAIL_USERNAME")
        password = os.getenv("EMAIL_PASSWORD")
        
        print(f"📧 Username: {username}")
        print(f"🔑 Password: {'*' * len(password) if password else 'None'}")
        
        if not username or not password:
            print("❌ Email credentials not found in .env file!")
            return False
        
        # Create message
        msg = MIMEText("Test email from Task Manager - Email system is working!")
        msg['Subject'] = "Test Email from Task Manager"
        msg['From'] = username
        msg['To'] = username  # Send to yourself
        
        print("📤 Sending test email...")
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(username, password)
        server.sendmail(username, username, msg.as_string())
        server.quit()
        
        print("✅ Email sent successfully!")
        print("📬 Check your email inbox for the test message.")
        return True
        
    except Exception as e:
        print(f"❌ Email failed: {e}")
        print("\n🔍 Possible issues:")
        print("1. Check your Gmail App Password")
        print("2. Make sure 2-Factor Authentication is enabled")
        print("3. Verify your .env file has correct credentials")
        return False

if __name__ == "__main__":
    print("🚀 Task Manager Email Test")
    print("=" * 40)
    test_email()
