#!/usr/bin/env python3
"""
Update Google Sheet with generated emails
"""

import os
from dotenv import load_dotenv
from .upload_to_sheets import get_sheets_service

load_dotenv()


def update_email(row_number, subject, body):
    """
    Update a specific row with generated email subject and body

    Args:
        row_number: Row number in the sheet (1-indexed, including header)
        subject: Email subject line
        body: Email body text
    """

    try:
        service = get_sheets_service()
        spreadsheet_id = os.getenv('GOOGLE_SPREADSHEET_ID')

        if not spreadsheet_id:
            print("❌ GOOGLE_SPREADSHEET_ID not set in .env")
            return

        # Update columns G (subject) and H (body)
        # Row number is already 1-indexed and includes header
        range_name = f'G{row_number}:H{row_number}'

        values = [[subject, body]]

        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body={'values': values}
        ).execute()

    except Exception as error:
        print(f"❌ Error updating row {row_number}: {error}")


def test_update_sheet_emails():
    """Test function"""
    # This will update row 2 (first business)
    update_email(
        row_number=2,
        subject="Test Subject Line",
        body="Test email body content..."
    )
    print("✅ Test update complete")


if __name__ == "__main__":
    test_update_sheet_emails()
