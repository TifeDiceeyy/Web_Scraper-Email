#!/usr/bin/env python3
"""
Send notifications via Telegram or Email when businesses reply
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()


def send_telegram_notification(message):
    """
    Send notification via Telegram Bot

    Args:
        message: str - Message to send

    Returns:
        bool - True if sent successfully

    Raises:
        ValueError: If Telegram credentials not configured
    """
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        raise ValueError(
            "Telegram not configured. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env"
        )

    try:
        import requests

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }

        response = requests.post(url, data=data, timeout=10)

        if response.status_code == 200:
            print(f"✅ Telegram notification sent")
            return True
        else:
            print(f"⚠️  Telegram API error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to send Telegram notification: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error sending Telegram: {e}")
        return False


def send_email_notification(subject, body, to_email=None):
    """
    Send notification via email

    Args:
        subject: str - Email subject
        body: str - Email body
        to_email: str - Recipient (default: from NOTIFICATION_EMAIL env var)

    Returns:
        bool - True if sent successfully

    Raises:
        ValueError: If email not configured
    """
    if not to_email:
        to_email = os.getenv("NOTIFICATION_EMAIL")

    if not to_email:
        raise ValueError(
            "Email not configured. Set NOTIFICATION_EMAIL in .env"
        )

    try:
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        import smtplib

        # Get Gmail credentials from env
        gmail_address = os.getenv("GMAIL_ADDRESS")
        gmail_password = os.getenv("GMAIL_APP_PASSWORD")

        if not gmail_address or not gmail_password:
            raise ValueError(
                "Gmail not configured. Set GMAIL_ADDRESS and GMAIL_APP_PASSWORD in .env"
            )

        # Create message
        msg = MIMEMultipart()
        msg['From'] = gmail_address
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Send via Gmail SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(gmail_address, gmail_password)
            server.send_message(msg)

        print(f"✅ Email notification sent to {to_email}")
        return True

    except smtplib.SMTPException as e:
        print(f"❌ SMTP error sending notification: {e}")
        return False
    except Exception as e:
        print(f"❌ Failed to send email notification: {e}")
        return False


def notify_reply_received(business_name, reply_preview, reply_from):
    """
    Send notification when a business replies

    Args:
        business_name: str
        reply_preview: str - First 200 chars of reply
        reply_from: str - Email address that replied

    Returns:
        bool - True if notification sent
    """
    notification_method = os.getenv("NOTIFICATION_METHOD", "").lower()

    if notification_method == "telegram":
        message = f"""
🎉 <b>New Reply Received!</b>

<b>Business:</b> {business_name}
<b>From:</b> {reply_from}

<b>Preview:</b>
{reply_preview}

Check your Google Sheet for full details.
"""
        return send_telegram_notification(message)

    elif notification_method == "email":
        subject = f"🎉 Reply from {business_name}"
        body = f"""
New Reply Received!

Business: {business_name}
From: {reply_from}

Preview:
{reply_preview}

Check your Google Sheet for full details and respond.
"""
        return send_email_notification(subject, body)

    else:
        print(f"⚠️  Notification method not configured: '{notification_method}'")
        print("   Set NOTIFICATION_METHOD to 'telegram' or 'email' in .env")
        return False


def notify_campaign_complete(total_sent, campaign_type):
    """
    Send notification when email campaign completes

    Args:
        total_sent: int
        campaign_type: str (general_help or specific_automation)

    Returns:
        bool - True if notification sent
    """
    notification_method = os.getenv("NOTIFICATION_METHOD", "").lower()

    strategy_name = "General Help" if campaign_type == "general_help" else "Specific Automation"

    if notification_method == "telegram":
        message = f"""
✅ <b>Campaign Complete!</b>

<b>Emails Sent:</b> {total_sent}
<b>Strategy:</b> {strategy_name}

Now monitor for replies with /track-responses
"""
        return send_telegram_notification(message)

    elif notification_method == "email":
        subject = f"✅ Campaign Complete - {total_sent} emails sent"
        body = f"""
Campaign Complete!

Emails Sent: {total_sent}
Strategy: {strategy_name}

Your emails have been sent successfully. Now you can track responses.
"""
        return send_email_notification(subject, body)

    else:
        return False


def test_telegram():
    """Test Telegram notification"""
    try:
        message = """
🧪 <b>Test Notification</b>

This is a test from your Business Outreach System.

If you see this, Telegram notifications are working! ✅
"""
        result = send_telegram_notification(message)
        if result:
            print("✅ Telegram test successful!")
        else:
            print("❌ Telegram test failed - check your bot token and chat ID")
    except Exception as e:
        print(f"❌ Telegram test failed: {e}")


def test_email():
    """Test email notification"""
    try:
        subject = "🧪 Test Notification from Outreach System"
        body = """
This is a test email from your Business Outreach Automation System.

If you received this, email notifications are working correctly!

✅ Test Successful
"""
        result = send_email_notification(subject, body)
        if result:
            print("✅ Email test successful!")
        else:
            print("❌ Email test failed - check your Gmail credentials")
    except Exception as e:
        print(f"❌ Email test failed: {e}")


if __name__ == "__main__":
    print("="*60)
    print("NOTIFICATION SYSTEM TEST")
    print("="*60)

    method = os.getenv("NOTIFICATION_METHOD", "").lower()

    if method == "telegram":
        print("\n📱 Testing Telegram notifications...")
        test_telegram()
    elif method == "email":
        print("\n📧 Testing Email notifications...")
        test_email()
    else:
        print("\n⚠️  NOTIFICATION_METHOD not set in .env")
        print("   Set it to 'telegram' or 'email' and try again")
        print("\nTesting both methods anyway...\n")
        print("📱 Testing Telegram:")
        try:
            test_telegram()
        except:
            print("   (Skipped - not configured)")
        print("\n📧 Testing Email:")
        try:
            test_email()
        except:
            print("   (Skipped - not configured)")
