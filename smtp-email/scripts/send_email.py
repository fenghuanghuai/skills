#!/usr/bin/env python3
"""
Send Email via SMTP

Usage:
    python3 send_email.py <to_email> <subject> <body> [from_email] [attachment1,attachment2,...]

Configuration:
    Set environment variables (SMTP_USER, SMTP_PASSWORD, SMTP_FROM)
    Or create config.py from config.example.py
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import sys

# Default configuration (can be overridden by environment variables or config.py)
DEFAULT_SMTP_SERVER = "smtp.2925.com"
DEFAULT_SMTP_PORT = 465

# Try to load from config.py, otherwise use defaults or environment variables
try:
    from config import (
        SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM
    )
except ImportError:
    SMTP_SERVER = os.getenv("SMTP_SERVER", DEFAULT_SMTP_SERVER)
    SMTP_PORT = int(os.getenv("SMTP_PORT", str(DEFAULT_SMTP_PORT)))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM = os.getenv("SMTP_FROM", "")

def validate_config():
    """Validate that required configuration is present"""
    if not SMTP_USER:
        raise ValueError(
            "SMTP_USER not configured. Set environment variable or create config.py "
            "from config.example.py"
        )
    if not SMTP_PASSWORD:
        raise ValueError(
            "SMTP_PASSWORD not configured. Set environment variable or create config.py "
            "from config.example.py"
        )
    if not SMTP_FROM:
        raise ValueError(
            "SMTP_FROM not configured. Set environment variable or create config.py "
            "from config.example.py"
        )

def send_email(to_email, subject, body, from_email=None, attachments=None):
    """Send email via SMTP"""
    validate_config()

    try:
        msg = MIMEMultipart()
        msg['From'] = from_email or SMTP_FROM
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        if attachments:
            for attachment_path in attachments.split(',') if isinstance(attachments, str) else attachments:
                if os.path.exists(attachment_path):
                    with open(attachment_path, 'rb') as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename="{os.path.basename(attachment_path)}"'
                    )
                    msg.attach(part)
                else:
                    print(f"Warning: Attachment not found: {attachment_path}")

        if SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=30)
        else:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30)
            server.starttls()

        server.login(SMTP_USER, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(from_email or SMTP_FROM, to_email, text)
        server.quit()
        print(f"✅ Email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

def main():
    if len(sys.argv) < 4:
        print("Usage: send_email.py <to_email> <subject> <body> [from_email] [attachment1,attachment2,...]")
        print()
        print("Configuration:")
        print("  Set environment variables: SMTP_USER, SMTP_PASSWORD, SMTP_FROM")
        print("  Or create config.py from config.example.py")
        sys.exit(1)

    to_email = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    from_email = sys.argv[4] if len(sys.argv) > 4 else None
    attachments = sys.argv[5] if len(sys.argv) > 5 else None

    success = send_email(to_email, subject, body, from_email, attachments)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
