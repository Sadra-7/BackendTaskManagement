#!/usr/bin/env python3
"""
Verify email delivery and check for common issues
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

def verify_email_delivery():
    """Verify email delivery with different approaches"""
    print("📧 VERIFYING EMAIL DELIVERY")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    email_username = os.getenv("EMAIL_USERNAME")
    email_password = os.getenv("EMAIL_PASSWORD")
    
    print(f"📋 Using email: {email_username}")
    
    # Test 1: Send simple test email
    print(f"\n🔍 Test 1: Simple Email")
    try:
        msg = MIMEMultipart()
        msg["From"] = f"Nik Tick <{email_username}>"
        msg["To"] = "s.amini8585@gmail.com"
        msg["Subject"] = Header("TaskManager Test - Simple", "utf-8")
        
        body = """
        This is a simple test email from TaskManager.
        
        If you receive this, the basic email system is working.
        
        Best regards,
        Nik Tick
        """
        
        msg.attach(MIMEText(body, "plain", "utf-8"))
        
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_username, email_password)
        server.sendmail(email_username, "s.amini8585@gmail.com", msg.as_string())
        server.quit()
        
        print(f"✅ Simple email sent successfully!")
        
    except Exception as e:
        print(f"❌ Simple email failed: {e}")
        return False
    
    # Test 2: Send HTML email
    print(f"\n🔍 Test 2: HTML Email")
    try:
        msg = MIMEMultipart()
        msg["From"] = f"Nik Tick <{email_username}>"
        msg["To"] = "s.amini8585@gmail.com"
        msg["Subject"] = Header("TaskManager Test - HTML", "utf-8")
        
        html_body = """
        <html>
        <body>
        <h2>TaskManager Test Email</h2>
        <p>This is an HTML test email from TaskManager.</p>
        <p>If you receive this, the HTML email system is working.</p>
        <p><strong>Test Link:</strong> <a href="http://localhost:3000">Visit TaskManager</a></p>
        <br>
        <p>Best regards,<br>Nik Tick</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, "html", "utf-8"))
        
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_username, email_password)
        server.sendmail(email_username, "s.amini8585@gmail.com", msg.as_string())
        server.quit()
        
        print(f"✅ HTML email sent successfully!")
        
    except Exception as e:
        print(f"❌ HTML email failed: {e}")
        return False
    
    # Test 3: Send invitation-style email
    print(f"\n🔍 Test 3: Invitation Email")
    try:
        msg = MIMEMultipart()
        msg["From"] = f"Nik Tick <{email_username}>"
        msg["To"] = "s.amini8585@gmail.com"
        msg["Subject"] = Header("TaskManager Board Invitation - Test", "utf-8")
        
        # Add headers to avoid spam
        msg["X-Mailer"] = "TaskManager"
        msg["X-Priority"] = "3"
        
        body = """
        You have been invited to join a board in TaskManager!
        
        Board: Test Board
        Invited by: Test User
        
        Click the link below to accept the invitation:
        http://localhost:3000/board/10/invite/test-token-123
        
        This invitation will expire in 7 days.
        
        Best regards,
        Nik Tick
        TaskManager Team
        """
        
        msg.attach(MIMEText(body, "plain", "utf-8"))
        
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_username, email_password)
        server.sendmail(email_username, "s.amini8585@gmail.com", msg.as_string())
        server.quit()
        
        print(f"✅ Invitation email sent successfully!")
        
    except Exception as e:
        print(f"❌ Invitation email failed: {e}")
        return False
    
    print(f"\n🎯 EMAIL DELIVERY VERIFICATION COMPLETE")
    print(f"📧 Check your inbox: s.amini8585@gmail.com")
    print(f"📧 Also check spam folder!")
    print(f"📧 Look for these subjects:")
    print(f"   - TaskManager Test - Simple")
    print(f"   - TaskManager Test - HTML")
    print(f"   - TaskManager Board Invitation - Test")
    
    print(f"\n💡 TROUBLESHOOTING TIPS:")
    print(f"1. Check spam/junk folder")
    print(f"2. Check 'All Mail' folder in Gmail")
    print(f"3. Check if emails are being filtered")
    print(f"4. Try sending to a different email address")
    print(f"5. Check Gmail security settings")
    
    return True

if __name__ == "__main__":
    verify_email_delivery()
