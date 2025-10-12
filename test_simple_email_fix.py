#!/usr/bin/env python3
"""
Simple email test to fix the issue
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

def test_simple_email():
    """Test email sending with detailed debugging"""
    print("📧 SIMPLE EMAIL TEST")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    email_username = os.getenv("EMAIL_USERNAME")
    email_password = os.getenv("EMAIL_PASSWORD")
    
    print(f"📋 Configuration:")
    print(f"  Username: {email_username}")
    print(f"  Password: {'*' * len(email_password) if email_password else 'NOT SET'}")
    
    if not email_username or not email_password:
        print("❌ Email credentials not found!")
        return False
    
    try:
        print(f"\n🔍 Testing SMTP connection...")
        
        # Create email
        msg = MIMEMultipart()
        msg["From"] = f"Nik Tick <{email_username}>"
        msg["To"] = "s.amini8585@gmail.com"
        msg["Subject"] = Header("Test Email from TaskManager", "utf-8")
        
        body = """
        This is a test email from TaskManager.
        
        If you receive this, the email system is working!
        
        Best regards,
        Nik Tick
        """
        
        msg.attach(MIMEText(body, "plain", "utf-8"))
        
        print(f"📤 Sending email...")
        
        # Connect and send
        server = smtplib.SMTP("smtp.gmail.com", 587)
        print(f"✅ Connected to SMTP server")
        
        server.starttls()
        print(f"✅ TLS started")
        
        server.login(email_username, email_password)
        print(f"✅ Login successful")
        
        server.sendmail(email_username, "s.amini8585@gmail.com", msg.as_string())
        print(f"✅ Email sent successfully")
        
        server.quit()
        print(f"✅ Connection closed")
        
        print(f"\n🎯 EMAIL SENT SUCCESSFULLY!")
        print(f"📧 Check your inbox: s.amini8585@gmail.com")
        print(f"📧 Also check spam folder!")
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print(f"💡 Make sure you're using Gmail App Password, not regular password")
        return False
        
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_simple_email()
