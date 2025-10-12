#!/usr/bin/env python3
"""
Test sending email to different addresses
"""

import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from dotenv import load_dotenv

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_different_emails():
    """Test sending to different email addresses"""
    print("📧 TESTING DIFFERENT EMAIL ADDRESSES")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    email_username = os.getenv("EMAIL_USERNAME")
    email_password = os.getenv("EMAIL_PASSWORD")
    
    # Test email addresses
    test_emails = [
        "s.amini8585@gmail.com",
        "sadra.amini1006@gmail.com",  # Your other email
        email_username  # Send to yourself
    ]
    
    for test_email in test_emails:
        print(f"\n📤 Testing email to: {test_email}")
        
        try:
            msg = MIMEMultipart()
            msg["From"] = f"Nik Tick <{email_username}>"
            msg["To"] = test_email
            msg["Subject"] = Header(f"TaskManager Test - {test_email}", "utf-8")
            
            body = f"""
            This is a test email from TaskManager.
            
            Sent to: {test_email}
            From: {email_username}
            
            If you receive this, the email system is working!
            
            Best regards,
            Nik Tick
            """
            
            msg.attach(MIMEText(body, "plain", "utf-8"))
            
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(email_username, email_password)
            server.sendmail(email_username, test_email, msg.as_string())
            server.quit()
            
            print(f"✅ Email sent successfully to {test_email}")
            
        except Exception as e:
            print(f"❌ Email failed to {test_email}: {e}")
    
    print(f"\n🎯 EMAIL TESTING COMPLETE")
    print(f"📧 Check all email addresses for test emails")
    print(f"📧 Also check spam folders")
    
    return True

if __name__ == "__main__":
    test_different_emails()
