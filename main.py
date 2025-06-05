import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

# Load from .env in the current directory
load_dotenv()

# Read variables from .env
smtp_server = os.getenv('smtp_server')
smtp_port = int(os.getenv('smtp_port', 587))
smtp_user = os.getenv('smtp_username')
smtp_password = os.getenv('smtp_password')
receiver_emails = os.getenv('receiver_email', '').split(',')

# Format receiver list
receiver_emails = [email.strip() for email in receiver_emails if email.strip()]
if not receiver_emails:
    raise ValueError("No valid receiver_email found in .env")

# Build message
msg = MIMEText("✅ This is a test email from your SMTP setup script.")
msg["Subject"] = "Airflow SMTP Test"
msg["From"] = smtp_user
msg["To"] = ', '.join(receiver_emails)

try:
    # Connect to SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.sendmail(smtp_user, receiver_emails, msg.as_string())
    server.quit()
    print("✅ Email sent successfully to:", receiver_emails)
except Exception as e:
    print("❌ Failed to send email.")
    print("Error:", e)
