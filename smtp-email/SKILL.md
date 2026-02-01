---
name: smtp-email
description: "Send emails via SMTP protocol. Use when Claude needs to send emails programmatically for: (1) Sending notifications or alerts, (2) Sending reports or data exports, (3) Automated email sending tasks, (4) Email-based automation workflows."
---

# SMTP Email

Send emails programmatically via SMTP protocol using Python scripts.

## Quick Start

### 1. Configure Email Credentials

Copy the example configuration and fill in your credentials:

```bash
cd scripts
cp config.example.py config.py
# Edit config.py with your SMTP credentials
```

Or set environment variables:

```bash
export SMTP_USER="your-username"
export SMTP_PASSWORD="your-password"
export SMTP_FROM="your-email@example.com"
```

### 2. Send Email

```bash
python3 scripts/send_email.py <to_email> <subject> <body> [from_email] [attachments]
```

## Usage Examples

### Basic Email

```bash
python3 scripts/send_email.py "recipient@example.com" "Hello" "This is a test email"
```

### Email with Custom Sender

```bash
python3 scripts/send_email.py "recipient@example.com" "Report" "Here is the report" "sender@example.com"
```

### Email with Attachments

```bash
python3 scripts/send_email.py "recipient@example.com" "Files" "Please find attached" "sender@example.com" "file1.pdf,file2.txt"
```

### Email from Shell Script

```bash
#!/bin/bash
TO="recipient@example.com"
SUBJECT="Daily Report"
BODY=$(cat report.txt)

python3 scripts/send_email.py "$TO" "$SUBJECT" "$BODY"
```

### Email from Python Code

```python
import subprocess

subprocess.run([
    "python3", "scripts/send_email.py",
    "recipient@example.com",
    "Alert",
    "Server is down!"
])
```

## Email Monitor

The `email_monitor.py` script listens for incoming emails and processes them automatically (similar to an AI email assistant).

### Start Monitor

```bash
# Configure environment variables first
export IMAP_USER="your-email@example.com"
export IMAP_PASSWORD="your-password"
export NOTIFY_EMAIL="notification@example.com"
export MASTER_EMAIL="master@example.com"
export ALLOWED_SENDERS="master@example.com,trusted@example.com"

# Start monitor
python3 scripts/email_monitor.py
```

### Configuration

See `scripts/config.example.py` for all configuration options:

| Variable | Description |
|----------|-------------|
| `SMTP_SERVER/SMTP_PORT` | SMTP server configuration |
| `SMTP_USER/SMTP_PASSWORD` | SMTP authentication |
| `SMTP_FROM` | Default sender email |
| `IMAP_SERVER/IMAP_PORT` | IMAP server for monitor |
| `IMAP_USER/IMAP_PASSWORD` | IMAP authentication |
| `NOTIFY_EMAIL` | CC address for notifications |
| `MASTER_EMAIL` | Email that can execute tasks immediately |
| `ALLOWED_SENDERS` | List of allowed sender emails |

## Scripts Reference

### send_email.py

Send emails via SMTP.

```bash
python3 scripts/send_email.py <to_email> <subject> <body> [from_email] [attachments]
```

**Features:**
- UTF-8 encoding support
- Multiple attachments (comma-separated)
- Configurable via environment variables or config.py
- SMTP_SSL (port 465) or STARTTLS (port 587)

### email_monitor.py

Monitor inbox and process incoming emails automatically.

**Features:**
- Listens for unread emails
- Whitelist-based sender control
- Master/authorized user levels
- Automatic reply and notification
- Task logging

## Configuration Priority

Configuration is loaded in this order:

1. **config.py** - If exists, use values from file
2. **Environment Variables** - Fall back to environment
3. **Defaults** - Use built-in defaults (incomplete, must provide credentials)

## Security Notes

- **Never commit config.py** to version control
- **Never hardcode credentials** in scripts
- **Use environment variables** for production deployments
- **Keep .gitignore** up to date

## Troubleshooting

### Authentication Failed

```
Error: 535 Authentication failed
```

**Solution:** Check username/password and SMTP_FROM email match.

### Connection Timeout

```
Error: Timeout connecting to server
```

**Solution:** Check firewall and SMTP server port (465/587).

### Config Not Found

```
ValueError: SMTP_USER not configured
```

**Solution:** Create config.py from config.example.py or set environment variables.
