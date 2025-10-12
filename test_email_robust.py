#!/usr/bin/env python3
"""
Robust email test with better formatting
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

def test_robust_email():
    """Test email with better formatting to avoid spam"""
    print("📧 ROBUST EMAIL TEST")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    email_username = os.getenv("EMAIL_USERNAME")
    email_password = os.getenv("EMAIL_PASSWORD")
    
    if not email_username or not email_password:
        print("❌ Email credentials not found!")
        return False
    
    try:
        # Create email with better formatting
        msg = MIMEMultipart()
        msg["From"] = f"Nik Tick <{email_username}>"
        msg["To"] = "s.amini8585@gmail.com"
        msg["Subject"] = Header("TaskManager Board Invitation", "utf-8")
        
        # Add headers to avoid spam
        msg["X-Mailer"] = "TaskManager"
        msg["X-Priority"] = "3"
        
        # Create HTML body
        html_body = """
        <html>
        <body>
        <h2>You have been invited to join a board!</h2>
        <p>Hello,</p>
        <p>You have been invited to join a board in TaskManager.</p>
        <p><strong>Board:</strong> Test Board</p>
        <p><strong>Invited by:</strong> Test User</p>
        <br>
        <p>Click the link below to accept the invitation:</p>
        <p><a href="http://localhost:3000/board/10/invite/test-token" style="background-color: #0079bf; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Accept Invitation</a></p>
        <br>
        <p>This invitation will expire in 7 days.</p>
        <br>
        <p>Best regards,<br>Nik Tick<br>TaskManager Team</p>
        </body>
        </html>
        """
        
        # Create plain text version
        text_body = """
        You have been invited to join a board!
        
        Board: Test Board
        Invited by: Test User
        
        Click the link below to accept the invitation:
        http://localhost:3000/board/10/invite/test-token
        
        This invitation will expire in 7 days.
        
        Best regards,
        Nik Tick
        TaskManager Team
        """
        
        # Attach both versions
        msg.attach(MIMEText(text_body, "plain", "utf-8"))
        msg.attach(MIMEText(html_body, "html", "utf-8"))
        
        print(f"📤 Sending robust email...")
        
        # Connect and send
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_username, email_password)
        server.sendmail(email_username, "s.amini8585@gmail.com", msg.as_string())
        server.quit()
        
        print(f"✅ Robust email sent successfully!")
        print(f"📧 Check your inbox: s.amini8585@gmail.com")
        print(f"📧 Also check spam folder!")
        
        return True
        
    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False

if __name__ == "__main__":
    test_robust_email()
