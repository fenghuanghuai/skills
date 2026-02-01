#!/usr/bin/env python3
"""
Email Monitor - Listen for incoming emails and process tasks

Configuration via environment variables or config.py (see config.example.py)
"""
import imaplib
import email
from email.header import decode_header
import time
import json
import subprocess
import os
from datetime import datetime
import re

# Default configuration
DEFAULT_IMAP_SERVER = "imap.2925.com"
DEFAULT_IMAP_PORT = 993
DEFAULT_TASK_LOG = "/tmp/email_tasks.log"

# Try to load from config.py, otherwise use environment variables
try:
    from config import (
        IMAP_SERVER, IMAP_PORT, IMAP_USER, IMAP_PASSWORD,
        NOTIFY_EMAIL, MASTER_EMAIL, ALLOWED_SENDERS, TASK_LOG
    )
except ImportError:
    IMAP_SERVER = os.getenv("IMAP_SERVER", DEFAULT_IMAP_SERVER)
    IMAP_PORT = int(os.getenv("IMAP_PORT", str(DEFAULT_IMAP_PORT)))
    IMAP_USER = os.getenv("IMAP_USER", "")
    IMAP_PASSWORD = os.getenv("IMAP_PASSWORD", "")
    NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL", "")
    MASTER_EMAIL = os.getenv("MASTER_EMAIL", "")
    TASK_LOG = os.getenv("TASK_LOG", DEFAULT_TASK_LOG)

    # Parse allowed senders from environment (comma-separated)
    allowed_senders_str = os.getenv("ALLOWED_SENDERS", "")
    ALLOWED_SENDERS = [s.strip() for s in allowed_senders_str.split(',') if s.strip()]

def validate_config():
    """Validate that required configuration is present"""
    if not IMAP_USER:
        raise ValueError("IMAP_USER not configured")
    if not IMAP_PASSWORD:
        raise ValueError("IMAP_PASSWORD not configured")
    if not NOTIFY_EMAIL:
        raise ValueError("NOTIFY_EMAIL not configured")
    if not MASTER_EMAIL:
        raise ValueError("MASTER_EMAIL not configured")
    if not ALLOWED_SENDERS:
        raise ValueError("ALLOWED_SENDERS not configured")

def decode_email_header(header):
    """Decode email header"""
    if not header:
        return ""
    decoded = []
    for part, encoding in decode_header(header):
        if isinstance(part, bytes):
            decoded.append(part.decode(encoding if encoding else 'utf-8', errors='ignore'))
        else:
            decoded.append(str(part))
    return ''.join(decoded)

def extract_email_body(msg):
    """Extract email body from message"""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if "attachment" in content_disposition:
                continue

            try:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or 'utf-8'
                    body += payload.decode(charset, errors='ignore')
            except:
                pass
    else:
        try:
            payload = msg.get_payload(decode=True)
            if payload:
                charset = msg.get_content_charset() or 'utf-8'
                body = payload.decode(charset, errors='ignore')
        except:
            body = msg.get_payload(decode=True) or ""

    # Clean up HTML tags if present
    body = re.sub(r'<[^>]+>', '', body)
    return body.strip()

def send_reply(to_email, subject, body, original_message_id=None):
    """Send reply email"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    send_email_script = os.path.join(script_dir, "send_email.py")

    cc_header = f"CC: {NOTIFY_EMAIL}"
    full_body = f"{cc_header}\n\n原始邮件ID: {original_message_id}\n\n{body}"

    cmd = [
        "python3", send_email_script,
        to_email,
        f"Re: {subject}",
        full_body
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"发送回复失败: {e.stderr}")
        return False

def log_task(from_email, subject, body):
    """Log task to file"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "from": from_email,
        "subject": subject,
        "body": body
    }
    with open(TASK_LOG, "a") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

def extract_email_address(email_string):
    """Extract email address from string like "Name <email@domain.com>" """
    if '<' in email_string and '>' in email_string:
        return email_string.split('<')[1].split('>')[0]
    return email_string.strip()

def is_allowed_sender(from_email):
    """Check if sender is in allowed list"""
    sender_email = extract_email_address(from_email)
    return sender_email in ALLOWED_SENDERS

def is_master_sender(from_email):
    """Check if sender is the master (can execute tasks immediately)"""
    sender_email = extract_email_address(from_email)
    return sender_email == MASTER_EMAIL

def notify_master(from_email, subject, body, message_id):
    """Send notification to master about new email from allowed sender"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    send_email_script = os.path.join(script_dir, "send_email.py")

    notify_body = f"""收到新邮件通知！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

发件人: {from_email}
主题: {subject}
时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

内容:
{body[:300]}{'...' if len(body) > 300 else ''}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

请指示是否要回复或处理此邮件。

贾维斯 (AI 助手)
"""

    cmd = [
        "python3", send_email_script,
        NOTIFY_EMAIL,
        f"[通知] 收到 {extract_email_address(from_email)} 的邮件",
        notify_body
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"通知主人失败: {e.stderr}")
        return False

def process_task(from_email, subject, body, message_id):
    """Process task from email"""
    log_entry = f"\n{'='*60}\n"
    log_entry += f"新任务接收: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    log_entry += f"发件人: {from_email}\n"
    log_entry += f"主题: {subject}\n"
    log_entry += f"内容:\n{body}\n"
    log_entry += f"{'='*60}\n"

    print(log_entry)
    log_task(from_email, subject, body)

    # Check if sender is allowed
    if not is_allowed_sender(from_email):
        print(f"发件人不在白名单，忽略: {from_email}")
        return

    # If it's the master, process immediately
    if is_master_sender(from_email):
        reply_body = f"""任务已收到，正在处理中...

任务详情:
- 发件人: {from_email}
- 主题: {subject}
- 内容: {body[:200]}{'...' if len(body) > 200 else ''}

贾维斯 (AI 助手)
"""
        send_reply(from_email, subject, reply_body, message_id)
    else:
        # For other allowed senders, notify master and send acknowledgment
        notify_master(from_email, subject, body, message_id)

        reply_body = f"""收到你的邮件！

我已经将你的邮件转告给广怀，等待他的处理指示。

贾维斯 (AI 助手)
"""
        send_reply(from_email, subject, reply_body, message_id)

def monitor_emails():
    """Monitor for new emails"""
    validate_config()

    print(f"贾维斯邮件监听启动...")
    print(f"IMAP 服务器: {IMAP_SERVER}:{IMAP_PORT}")
    print(f"监听邮箱: {IMAP_USER}")
    print(f"抄送地址: {NOTIFY_EMAIL}")
    print(f"主人邮箱: {MASTER_EMAIL}")
    print(f"任务日志: {TASK_LOG}")
    print("-" * 60)

    processed_emails = set()

    try:
        # Connect to IMAP
        server = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        server.login(IMAP_USER, IMAP_PASSWORD)
        server.select('INBOX')

        print("✅ 已连接到邮箱，开始监听...")

        last_unseen_count = 0

        while True:
            try:
                # Get inbox status to check for new unread emails
                server.select('INBOX')
                typ, status_data = server.status('INBOX', '(MESSAGES UNSEEN)')

                if typ == 'OK':
                    status_text = status_data[0].decode()
                    match = re.search(r'UNSEEN\s+(\d+)', status_text)
                    if match:
                        unseen_count = int(match.group(1))

                        # Check for new unread emails
                        if unseen_count > last_unseen_count:
                            print(f"\n📬 检测到 {unseen_count - last_unseen_count} 封新邮件！")

                        # Get total messages
                        match_total = re.search(r'MESSAGES\s+(\d+)', status_text)
                        if match_total:
                            total_messages = int(match_total.group(1))

                            # Fetch recent emails (last 20)
                            start_seq = max(1, total_messages - 19)
                            end_seq = total_messages

                            typ, data = server.fetch(f'{start_seq}:{end_seq}', '(FLAGS BODY.PEEK[])')

                            if typ == 'OK':
                                # Process emails in reverse order (newest first)
                                for response in reversed(data):
                                    if not isinstance(response, tuple):
                                        continue

                                    raw_response = response[0]
                                    raw_email = response[1]

                                    # Check if email is unseen
                                    is_unseen = b'\\Seen' not in raw_response

                                    if is_unseen:
                                        seq_match = re.search(b'(\d+)\s+\(FLAGS', raw_response)
                                        if seq_match:
                                            seq_num = seq_match.group(1).decode()

                                            if seq_num in processed_emails:
                                                continue

                                            try:
                                                msg = email.message_from_bytes(raw_email)

                                                from_email = decode_email_header(msg.get('From', ''))
                                                subject = decode_email_header(msg.get('Subject', '(无主题)'))
                                                message_id = msg.get('Message-ID', '')

                                                body = extract_email_body(msg)

                                                process_task(from_email, subject, body, message_id)

                                                processed_emails.add(seq_num)

                                                # Mark as read
                                                server.store(seq_num, '+FLAGS', '\\Seen')

                                            except Exception as e:
                                                print(f"处理邮件 {seq_num} 时出错: {e}")

                # Update last unseen count
                typ, status_data = server.status('INBOX', '(UNSEEN)')
                if typ == 'OK':
                    status_text = status_data[0].decode()
                    match = re.search(r'UNSEEN\s+(\d+)', status_text)
                    if match:
                        last_unseen_count = int(match.group(1))

                # Wait before next check (30 seconds)
                time.sleep(30)

            except Exception as e:
                print(f"监听出错: {e}, 5秒后重试...")
                time.sleep(5)
                # Reconnect
                try:
                    server.close()
                    server.logout()
                except:
                    pass
                server = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
                server.login(IMAP_USER, IMAP_PASSWORD)
                server.select('INBOX')

    except KeyboardInterrupt:
        print("\n监听已停止")
    except Exception as e:
        print(f"严重错误: {e}")
    finally:
        try:
            server.close()
            server.logout()
        except:
            pass

if __name__ == "__main__":
    monitor_emails()
