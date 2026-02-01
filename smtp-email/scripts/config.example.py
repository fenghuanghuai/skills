#!/usr/bin/env python3
"""
Email Configuration Template

Copy this file to config.py and fill in your actual credentials.
DO NOT commit config.py to version control.
"""

# SMTP Configuration
SMTP_SERVER = "smtp.2925.com"
SMTP_PORT = 465  # 465 for SMTP_SSL, 587 for SMTP with STARTTLS
SMTP_USER = "your-username"
SMTP_PASSWORD = "your-password"
SMTP_FROM = "your-email@2925.com"

# IMAP Configuration (for email monitor)
IMAP_SERVER = "imap.2925.com"
IMAP_PORT = 993
IMAP_USER = "your-username"
IMAP_PASSWORD = "your-password"

# Email Monitor Settings
NOTIFY_EMAIL = "notification@example.com"  # CC address for notifications
MASTER_EMAIL = "master@example.com"       # Email that can execute tasks immediately

# Allowed senders (can send emails to trigger tasks)
ALLOWED_SENDERS = [
    "master@example.com",
    "trusted@example.com"
]

# Task log file
TASK_LOG = "/tmp/email_tasks.log"
