# app/utils/send_email.py
from email.header import Header
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")

EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(to_email: str, subject: str, body: str):
    print(f"DEBUG: Starting email send to {to_email}")
    print(f"DEBUG: Using email: {EMAIL_USERNAME}")
    print(f"DEBUG: SMTP host: {EMAIL_HOST}:{EMAIL_PORT}")
    
    msg = MIMEMultipart()
    msg["From"] = f"Nik Tick <{EMAIL_USERNAME}>"
    msg["To"] = to_email
    msg["Subject"] = Header(subject, "utf-8")

    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        print(f"DEBUG: Connecting to SMTP server...")
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        print(f"DEBUG: Starting TLS...")
        server.starttls()
        print(f"DEBUG: Logging in with {EMAIL_USERNAME}...")
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        print(f"DEBUG: Sending email...")
        server.sendmail(EMAIL_USERNAME, to_email, msg.as_string())
        print(f"DEBUG: Closing connection...")
        server.quit()
        print(f"DEBUG: Email sent successfully!")
    except Exception as e:
        print(f"ERROR: Email sending failed: {e}")
        print(f"ERROR: Exception type: {type(e).__name__}")
        import traceback
        print(f"ERROR: Traceback: {traceback.format_exc()}")
        raise