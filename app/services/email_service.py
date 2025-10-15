import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@taskmanager.com")
        self.from_name = os.getenv("FROM_NAME", "Task Manager")
    
    def send_invitation_email(
        self, 
        invitee_email: str, 
        inviter_name: str, 
        board_title: str, 
        invitation_link: str,
        role: str
    ) -> bool:
        """
        Send board invitation email to user
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"You're invited to collaborate on '{board_title}'"
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = invitee_email
            
            # Create HTML content
            html_content = self._create_invitation_html(
                inviter_name, 
                board_title, 
                invitation_link, 
                role
            )
            
            # Create plain text content
            text_content = self._create_invitation_text(
                inviter_name, 
                board_title, 
                invitation_link, 
                role
            )
            
            # Attach parts
            text_part = MIMEText(text_content, 'plain')
            html_part = MIMEText(html_content, 'html')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Invitation email sent to {invitee_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send invitation email to {invitee_email}: {str(e)}")
            return False
    
    def _create_invitation_html(
        self, 
        inviter_name: str, 
        board_title: str, 
        invitation_link: str, 
        role: str
    ) -> str:
        """Create HTML content for invitation email"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Board Invitation</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f4f4f4;
                }}
                .container {{
                    background: white;
                    border-radius: 10px;
                    padding: 30px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .logo {{
                    font-size: 28px;
                    font-weight: bold;
                    color: #0079bf;
                    margin-bottom: 10px;
                }}
                .title {{
                    font-size: 24px;
                    color: #1e293b;
                    margin-bottom: 20px;
                }}
                .content {{
                    margin-bottom: 30px;
                }}
                .board-info {{
                    background: #f8fafc;
                    border-left: 4px solid #0079bf;
                    padding: 20px;
                    margin: 20px 0;
                    border-radius: 5px;
                }}
                .board-title {{
                    font-size: 20px;
                    font-weight: bold;
                    color: #1e293b;
                    margin-bottom: 10px;
                }}
                .role-badge {{
                    display: inline-block;
                    background: #0079bf;
                    color: white;
                    padding: 5px 15px;
                    border-radius: 20px;
                    font-size: 14px;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }}
                .cta-button {{
                    display: inline-block;
                    background: linear-gradient(135deg, #0079bf 0%, #0052cc 100%);
                    color: white;
                    padding: 15px 30px;
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: bold;
                    font-size: 16px;
                    margin: 20px 0;
                    transition: all 0.3s ease;
                }}
                .cta-button:hover {{
                    background: linear-gradient(135deg, #0052cc 0%, #003d99 100%);
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(0, 121, 191, 0.3);
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #e2e8f0;
                    color: #64748b;
                    font-size: 14px;
                }}
                .warning {{
                    background: #fef3c7;
                    border: 1px solid #f59e0b;
                    color: #92400e;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">📋 Task Manager</div>
                    <h1 class="title">You're Invited!</h1>
                </div>
                
                <div class="content">
                    <p>Hello!</p>
                    <p><strong>{inviter_name}</strong> has invited you to collaborate on a board.</p>
                    
                    <div class="board-info">
                        <div class="board-title">📌 {board_title}</div>
                        <p>Role: <span class="role-badge">{role.title()}</span></p>
                    </div>
                    
                    <p>Click the button below to accept the invitation and start collaborating:</p>
                    
                    <div style="text-align: center;">
                        <a href="{invitation_link}" class="cta-button">Accept Invitation</a>
                    </div>
                    
                    <div class="warning">
                        <strong>⚠️ Important:</strong> This invitation will expire in 7 days. 
                        If you don't have an account, you'll be prompted to create one.
                    </div>
                    
                    <p>If the button doesn't work, you can copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; color: #0079bf;">{invitation_link}</p>
                </div>
                
                <div class="footer">
                    <p>This invitation was sent by {inviter_name} via Task Manager.</p>
                    <p>If you didn't expect this invitation, you can safely ignore this email.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_invitation_text(
        self, 
        inviter_name: str, 
        board_title: str, 
        invitation_link: str, 
        role: str
    ) -> str:
        """Create plain text content for invitation email"""
        return f"""
        You're Invited to Collaborate!
        
        Hello!
        
        {inviter_name} has invited you to collaborate on the board "{board_title}".
        
        Role: {role.title()}
        
        To accept this invitation, click the link below:
        {invitation_link}
        
        This invitation will expire in 7 days.
        If you don't have an account, you'll be prompted to create one.
        
        If you didn't expect this invitation, you can safely ignore this email.
        
        Best regards,
        Task Manager Team
        """
    
    def send_welcome_email(self, user_email: str, user_name: str) -> bool:
        """Send welcome email to new user"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Welcome to Task Manager!"
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = user_email
            
            html_content = f"""
            <html>
            <body>
                <h1>Welcome to Task Manager!</h1>
                <p>Hello {user_name},</p>
                <p>Welcome to Task Manager! You can now start creating and managing your boards.</p>
                <p>Happy collaborating!</p>
            </body>
            </html>
            """
            
            text_content = f"""
            Welcome to Task Manager!
            
            Hello {user_name},
            
            Welcome to Task Manager! You can now start creating and managing your boards.
            
            Happy collaborating!
            """
            
            text_part = MIMEText(text_content, 'plain')
            html_part = MIMEText(html_content, 'html')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send welcome email to {user_email}: {str(e)}")
            return False

# Global email service instance
email_service = EmailService()





