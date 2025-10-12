#!/usr/bin/env python3
"""
Comprehensive email testing script
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

def test_email_comprehensive():
    """Test email configuration and sending"""
    print("📧 COMPREHENSIVE EMAIL TEST")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Get email credentials
    email_username = os.getenv("EMAIL_USERNAME")
    email_password = os.getenv("EMAIL_PASSWORD")
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    print(f"📋 Email Configuration:")
    print(f"  Username: {email_username}")
    print(f"  Password: {'*' * len(email_password) if email_password else 'NOT SET'}")
    print(f"  Frontend URL: {frontend_url}")
    
    if not email_username or not email_password:
        print("❌ Email credentials not found in .env file")
        print("💡 Make sure your .env file contains:")
        print("   EMAIL_USERNAME=your-email@gmail.com")
        print("   EMAIL_PASSWORD=your-app-password")
        return False
    
    # Test 1: Test SMTP connection
    print(f"\n🔍 Testing SMTP Connection...")
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        print("✅ SMTP connection established")
        
        # Test login
        server.login(email_username, email_password)
        print("✅ SMTP login successful")
        server.quit()
        
    except Exception as e:
        print(f"❌ SMTP connection failed: {e}")
        print("💡 Common issues:")
        print("   - Wrong email/password")
        print("   - Need to use App Password (not regular password)")
        print("   - 2FA not enabled")
        print("   - Less secure apps not allowed")
        return False
    
    # Test 2: Send test email
    print(f"\n📤 Sending Test Email...")
    try:
        # Create test email
        msg = MIMEMultipart()
        msg["From"] = f"Nik Tick <{email_username}>"
        msg["To"] = "s.amini8585@gmail.com"
        msg["Subject"] = Header("Test Email from TaskManager", "utf-8")
        
        body = """
        This is a test email from TaskManager.
        
        If you receive this, the email system is working correctly!
        
        Best regards,
        Nik Tick
        """
        
        msg.attach(MIMEText(body, "plain", "utf-8"))
        
        # Send email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_username, email_password)
        server.sendmail(email_username, "s.amini8585@gmail.com", msg.as_string())
        server.quit()
        
        print("✅ Test email sent successfully!")
        print("📧 Check your inbox: s.amini8585@gmail.com")
        
    except Exception as e:
        print(f"❌ Test email failed: {e}")
        return False
    
    # Test 3: Test invitation email format
    print(f"\n📧 Testing Invitation Email Format...")
    try:
        # Create invitation email
        msg = MIMEMultipart()
        msg["From"] = f"Nik Tick <{email_username}>"
        msg["To"] = "s.amini8585@gmail.com"
        msg["Subject"] = Header("Invitation to join board: Test Board", "utf-8")
        
        invite_link = f"{frontend_url}/board/1/invite/test-token-123"
        body = f"""
        You have been invited to join the board "Test Board" by Test User.
        
        Click the link below to accept the invitation:
        {invite_link}
        
        This invitation will expire in 7 days.
        """
        
        msg.attach(MIMEText(body, "plain", "utf-8"))
        
        # Send invitation email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_username, email_password)
        server.sendmail(email_username, "s.amini8585@gmail.com", msg.as_string())
        server.quit()
        
        print("✅ Invitation email sent successfully!")
        print("📧 Check your inbox for the invitation email")
        
    except Exception as e:
        print(f"❌ Invitation email failed: {e}")
        return False
    
    print(f"\n🎯 EMAIL SYSTEM STATUS: WORKING")
    print(f"✅ All email tests passed!")
    print(f"📧 Check your inbox for the test emails")
    
    return True

if __name__ == "__main__":
    test_email_comprehensive()
