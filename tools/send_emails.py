#!/usr/bin/env python3
"""
Send approved emails via Gmail with optimized SMTP connection reuse
"""

import os
import sys
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import RATE_LIMIT_DELAY, STATUS_APPROVED, STATUS_SENT, COL_STATUS
from tools.upload_to_sheets import get_sheets_service

load_dotenv()


def validate_gmail_credentials():
    """
    Validate that Gmail credentials exist

    Returns:
        tuple: (gmail_address, gmail_password)

    Raises:
        ValueError: If credentials are missing
    """
    gmail_address = os.getenv('GMAIL_ADDRESS')
    gmail_password = os.getenv('GMAIL_PASSWORD')

    if not gmail_address or not gmail_password:
        raise ValueError(
            "Gmail credentials not found in environment variables. "
            "Please set GMAIL_ADDRESS and GMAIL_PASSWORD in your .env file."
        )

    return gmail_address, gmail_password


def get_approved_businesses():
    """Get all businesses with Status = 'Approved'"""

    try:
        service = get_sheets_service()
        spreadsheet_id = os.getenv('GOOGLE_SPREADSHEET_ID')

        if not spreadsheet_id:
            raise ValueError("GOOGLE_SPREADSHEET_ID not set in .env")

        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='A2:N'
        ).execute()

        rows = result.get('values', [])

        approved_businesses = []
        for i, row in enumerate(rows, start=2):
            while len(row) < 14:
                row.append('')

            status = row[COL_STATUS] if len(row) > COL_STATUS else ''

            if status.lower() == STATUS_APPROVED.lower():
                business = {
                    'row_number': i,
                    'name': row[0],
                    'email': row[2],
                    'subject': row[6],
                    'body': row[7]
                }

                # Only include if email, subject, and body exist
                if business['email'] and business['subject'] and business['body']:
                    approved_businesses.append(business)

        return approved_businesses

    except Exception as error:
        print(f"❌ Error getting approved businesses: {error}")
        return []


class SMTPConnectionManager:
    """Context manager for SMTP connection with connection reuse"""

    def __init__(self, gmail_address, gmail_password):
        self.gmail_address = gmail_address
        self.gmail_password = gmail_password
        self.server = None

    def __enter__(self):
        """Establish SMTP connection"""
        try:
            self.server = smtplib.SMTP('smtp.gmail.com', 587)
            self.server.starttls()
            self.server.login(self.gmail_address, self.gmail_password)
            print("✅ Connected to Gmail SMTP server")
            return self
        except smtplib.SMTPAuthenticationError:
            raise ValueError(
                f"Authentication failed for {self.gmail_address}. "
                "Check your Gmail App Password in .env"
            )
        except smtplib.SMTPException as e:
            raise ConnectionError(f"Failed to connect to Gmail SMTP: {e}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close SMTP connection"""
        if self.server:
            try:
                self.server.quit()
                print("✅ Disconnected from Gmail SMTP server")
            except:
                pass  # Already disconnected

    def send_email(self, to_email, subject, body):
        """
        Send email using established SMTP connection

        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body

        Returns:
            bool: True if sent successfully, False otherwise
        """
        if not self.server:
            raise RuntimeError("SMTP connection not established")

        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.gmail_address
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            # Send using existing connection
            self.server.send_message(msg)
            return True

        except smtplib.SMTPRecipientsRefused:
            print(f"   ❌ Invalid email address: {to_email}")
            return False
        except smtplib.SMTPSenderRefused:
            print(f"   ❌ Sender refused by server")
            return False
        except smtplib.SMTPDataError as e:
            print(f"   ❌ SMTP data error: {e}")
            return False
        except Exception as error:
            print(f"   ❌ Error sending to {to_email}: {error}")
            return False


def update_sent_status(row_number, success=True):
    """Update sheet after sending email"""

    try:
        service = get_sheets_service()
        spreadsheet_id = os.getenv('GOOGLE_SPREADSHEET_ID')

        if success:
            # Update status to "Sent" and add date
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            range_name = f'J{row_number}:L{row_number}'
            values = [[STATUS_SENT, '', now]]  # Status, Date Approved (keep blank), Date Sent
        else:
            # Keep as Approved if failed
            range_name = f'I{row_number}'
            values = [['❌ Send failed - check email address']]

        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body={'values': values}
        ).execute()

    except Exception as error:
        print(f"   ⚠️  Could not update status: {error}")


def send_approved_emails():
    """
    Main function to send all approved emails with optimized SMTP connection

    Returns:
        int: Number of successfully sent emails
    """

    try:
        # Validate credentials first
        gmail_address, gmail_password = validate_gmail_credentials()
    except ValueError as e:
        print(f"❌ {e}")
        return 0

    print("\n🔍 Finding approved businesses...")
    businesses = get_approved_businesses()

    if not businesses:
        print("❌ No approved businesses found")
        print("   Make sure businesses have Status = 'Approved' in Google Sheet")
        return 0

    print(f"\n📊 Found {len(businesses)} approved businesses:")
    for b in businesses:
        print(f"  - {b['name']} ({b['email']})")

    # Confirm before sending
    print("\n⚠️  Ready to send emails!")
    confirm = input(f"Send {len(businesses)} emails? (yes/no): ").strip().lower()

    if confirm != 'yes':
        print("❌ Sending cancelled")
        return 0

    # Send emails using connection reuse
    print(f"\n📤 Sending {len(businesses)} emails...")
    sent_count = 0
    failed_count = 0

    try:
        # Establish ONE SMTP connection for all emails
        with SMTPConnectionManager(gmail_address, gmail_password) as smtp:
            for i, business in enumerate(businesses, 1):
                print(f"\n[{i}/{len(businesses)}] Sending to: {business['name']}")

                success = smtp.send_email(
                    to_email=business['email'],
                    subject=business['subject'],
                    body=business['body']
                )

                if success:
                    print(f"   ✅ Sent successfully")
                    update_sent_status(business['row_number'], success=True)
                    sent_count += 1
                else:
                    print(f"   ❌ Failed to send")
                    update_sent_status(business['row_number'], success=False)
                    failed_count += 1

                # Rate limiting - wait between sends
                if i < len(businesses):
                    print(f"   ⏳ Waiting {RATE_LIMIT_DELAY} seconds...")
                    time.sleep(RATE_LIMIT_DELAY)

    except (ValueError, ConnectionError) as e:
        print(f"\n❌ SMTP connection error: {e}")
        print("   Please check your Gmail credentials and try again")
        return sent_count

    # Summary
    print("\n" + "="*60)
    print("📊 SENDING COMPLETE")
    print("="*60)
    print(f"✅ Sent: {sent_count} emails")
    print(f"❌ Failed: {failed_count} emails")
    print(f"📊 Total: {len(businesses)} emails")

    return sent_count


if __name__ == "__main__":
    send_approved_emails()
