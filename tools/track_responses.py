#!/usr/bin/env python3
"""
Track email responses from Gmail
"""

import os
import time
from datetime import datetime
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
from pathlib import Path
import requests
from .upload_to_sheets import get_sheets_service

load_dotenv()

# Gmail API scopes
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_gmail_service():
    """Get authenticated Gmail service"""

    creds = None
    token_path = Path(__file__).parent.parent / "gmail_token.pickle"
    creds_file = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')

    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, GMAIL_SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)


def get_sent_businesses():
    """Get all businesses with Status = "Sent" """

    try:
        service = get_sheets_service()
        spreadsheet_id = os.getenv('GOOGLE_SPREADSHEET_ID')

        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='A2:N'
        ).execute()

        rows = result.get('values', [])

        sent_businesses = []
        for i, row in enumerate(rows, start=2):
            while len(row) < 14:
                row.append('')

            status = row[9] if len(row) > 9 else ''

            if status.lower() == 'sent':
                business = {
                    'row_number': i,
                    'name': row[0],
                    'email': row[2],
                    'date_sent': row[11] if len(row) > 11 else ''
                }
                sent_businesses.append(business)

        return sent_businesses

    except Exception as error:
        print(f"❌ Error getting sent businesses: {error}")
        return []


def check_for_reply(gmail_service, business_email, date_sent):
    """Check if we received a reply from this business"""

    try:
        # Search for emails from this address received after we sent our email
        query = f'from:{business_email}'

        results = gmail_service.users().messages().list(
            userId='me',
            q=query,
            maxResults=5
        ).execute()

        messages = results.get('messages', [])

        if not messages:
            return None

        # Get the most recent message
        msg_id = messages[0]['id']
        message = gmail_service.users().messages().get(
            userId='me',
            id=msg_id,
            format='full'
        ).execute()

        # Extract email body
        if 'parts' in message['payload']:
            parts = message['payload']['parts']
            data = parts[0]['body'].get('data', '')
        else:
            data = message['payload']['body'].get('data', '')

        # Decode body
        import base64
        if data:
            body = base64.urlsafe_b64decode(data).decode('utf-8')
            return body[:500]  # First 500 chars

        return None

    except Exception as error:
        print(f"   ⚠️  Could not check reply: {error}")
        return None


def update_reply_status(row_number, response_text):
    """Update sheet with reply info"""

    try:
        service = get_sheets_service()
        spreadsheet_id = os.getenv('GOOGLE_SPREADSHEET_ID')

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        range_name = f'J{row_number}:N{row_number}'
        values = [['Replied', '', '', now, response_text]]

        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body={'values': values}
        ).execute()

    except Exception as error:
        print(f"   ⚠️  Could not update reply status: {error}")


def send_notification(business_name, response_preview):
    """Send notification about new reply"""

    notification_method = os.getenv('NOTIFICATION_METHOD', 'telegram')

    if notification_method == 'telegram':
        send_telegram_notification(business_name, response_preview)
    elif notification_method == 'email':
        send_email_notification(business_name, response_preview)


def send_telegram_notification(business_name, response_preview):
    """Send Telegram notification"""

    try:
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')

        if not bot_token or not chat_id:
            print("   ⚠️  Telegram credentials not set")
            return

        message = f"""🎉 NEW REPLY RECEIVED

Business: {business_name}

Response preview:
{response_preview[:200]}...

Check your Google Sheet for full details!"""

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message
        }

        requests.post(url, data=data)
        print("   ✅ Telegram notification sent")

    except Exception as error:
        print(f"   ⚠️  Could not send Telegram notification: {error}")


def send_email_notification(business_name, response_preview):
    """Send email notification"""
    # Implement email notification similar to send_emails.py
    print("   📧 Email notification (not yet implemented)")


def track_email_responses():
    """Main function to track responses"""

    print("\n🔍 Checking for email responses...")

    # Get Gmail service
    gmail_service = get_gmail_service()

    # Get sent businesses
    businesses = get_sent_businesses()

    if not businesses:
        print("❌ No sent emails found to track")
        return

    print(f"📊 Checking {len(businesses)} sent emails...\n")

    new_replies = 0

    for business in businesses:
        print(f"Checking: {business['name']} ({business['email']})")

        reply = check_for_reply(
            gmail_service,
            business['email'],
            business['date_sent']
        )

        if reply:
            print(f"   🎉 NEW REPLY FOUND!")
            print(f"   Preview: {reply[:100]}...")

            update_reply_status(business['row_number'], reply)
            send_notification(business['name'], reply)

            new_replies += 1
        else:
            print(f"   ⏳ No reply yet")

    # Summary
    print("\n" + "="*60)
    print("📊 TRACKING COMPLETE")
    print("="*60)
    print(f"🎉 New Replies: {new_replies}")
    print(f"📊 Total Checked: {len(businesses)}")

    if new_replies > 0:
        print("\n✅ Google Sheet updated with new responses")


if __name__ == "__main__":
    track_email_responses()
