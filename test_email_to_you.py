#!/usr/bin/env python3
"""
Test email to specific address
"""

import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

# Load environment variables
load_dotenv()

def test_email_to_you():
    """Test email to specific address"""
    try:
        print("🔧 Testing Email Configuration...")
        
        # Get credentials
        username = os.getenv("EMAIL_USERNAME")
        password = os.getenv("EMAIL_PASSWORD")
        
        print(f"📧 From: {username}")
        print(f"📬 To: s.amini8585@gmail.com")
        print(f"🔑 Password: {'*' * len(password) if password else 'None'}")
        
        if not username or not password:
            print("❌ Email credentials not found in .env file!")
            return False
        
        # Create message
        msg = MIMEText("Hello! This is a test email from Task Manager. If you receive this, the email system is working perfectly!")
        msg['Subject'] = "Task Manager Email Test - SUCCESS!"
        msg['From'] = "Nik Tick <" + username + ">"
        msg['To'] = "s.amini8585@gmail.com"
        
        print("📤 Sending test email...")
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(username, password)
        server.sendmail(username, "s.amini8585@gmail.com", msg.as_string())
        server.quit()
        
        print("✅ Email sent successfully!")
        print("📬 Check s.amini8585@gmail.com for the test message.")
        print("📧 Also check spam/junk folder if you don't see it in inbox.")
        return True
        
    except Exception as e:
        print(f"❌ Email failed: {e}")
        print("\n🔍 Possible issues:")
        print("1. Check your Gmail App Password")
        print("2. Make sure 2-Factor Authentication is enabled")
        print("3. Verify your .env file has correct credentials")
        print("4. Check if Gmail account is locked")
        return False

if __name__ == "__main__":
    print("🚀 Task Manager Email Test")
    print("=" * 40)
    test_email_to_you()
