#!/usr/bin/env python3
"""
Detailed email debugging script
"""

import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
import traceback

# Load environment variables
load_dotenv()

def debug_email():
    """Debug email configuration step by step"""
    print("🔍 DETAILED EMAIL DEBUGGING")
    print("=" * 50)
    
    # Step 1: Check .env file
    print("\n📁 Step 1: Checking .env file...")
    env_file = os.path.exists('.env')
    print(f"   .env file exists: {'✅ Yes' if env_file else '❌ No'}")
    
    if not env_file:
        print("❌ .env file not found! Please create it first.")
        return False
    
    # Step 2: Check environment variables
    print("\n🔧 Step 2: Checking environment variables...")
    username = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")
    
    print(f"   EMAIL_USERNAME: {'✅ Set' if username else '❌ Not set'}")
    print(f"   EMAIL_PASSWORD: {'✅ Set' if password else '❌ Not set'}")
    
    if username:
        print(f"   Username value: {username}")
    if password:
        print(f"   Password length: {len(password)} characters")
        print(f"   Password starts with: {password[:3]}...")
    
    if not username or not password:
        print("❌ Missing email credentials!")
        return False
    
    # Step 3: Test Gmail connection
    print("\n🌐 Step 3: Testing Gmail SMTP connection...")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        print("   ✅ Connected to Gmail SMTP server")
        
        server.starttls()
        print("   ✅ TLS encryption started")
        
        server.login(username, password)
        print("   ✅ Gmail authentication successful")
        
        # Step 4: Send test email
        print("\n📤 Step 4: Sending test email...")
        msg = MIMEText("This is a test email from Task Manager. If you receive this, your email system is working!")
        msg['Subject'] = "Task Manager Email Test"
        msg['From'] = username
        msg['To'] = username
        
        server.sendmail(username, username, msg.as_string())
        print("   ✅ Email sent successfully!")
        
        server.quit()
        print("   ✅ Connection closed")
        
        print("\n🎉 SUCCESS! Email system is working!")
        print("📬 Check your email inbox (including spam folder)")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Gmail authentication failed: {e}")
        print("\n🔧 Possible solutions:")
        print("1. Check your Gmail App Password")
        print("2. Make sure 2-Factor Authentication is enabled")
        print("3. Generate a new App Password")
        return False
        
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"   Error type: {type(e).__name__}")
        print(f"   Full traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_email()
