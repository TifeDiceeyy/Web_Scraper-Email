#!/usr/bin/env python3
"""
Upload businesses to Google Sheets
"""

import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import pickle
from pathlib import Path

load_dotenv()

# Google Sheets API scopes
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def get_sheets_service():
    """Get authenticated Google Sheets service"""

    creds = None
    token_path = Path(__file__).parent.parent / "token.pickle"
    creds_file = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')

    # Load existing credentials
    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for next time
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return build('sheets', 'v4', credentials=creds)


def upload_businesses(businesses):
    """
    Upload businesses to Google Sheets

    Args:
        businesses: List of business dictionaries
    """

    try:
        service = get_sheets_service()
        spreadsheet_id = os.getenv('GOOGLE_SPREADSHEET_ID')

        if not spreadsheet_id:
            print("❌ GOOGLE_SPREADSHEET_ID not set in .env")
            return

        # Check if sheet exists and has headers
        try:
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range='A1:N1'
            ).execute()

            headers_exist = len(result.get('values', [])) > 0

        except HttpError:
            headers_exist = False

        # Create headers if they don't exist
        if not headers_exist:
            headers = [[
                'Business Name',
                'Location',
                'Email',
                'Phone',
                'Website',
                'Contact Person',
                'Generated Subject',
                'Generated Body',
                'Your Notes',
                'Status',
                'Date Approved',
                'Date Sent',
                'Last Response',
                'Response Details'
            ]]

            service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range='A1:N1',
                valueInputOption='RAW',
                body={'values': headers}
            ).execute()

            print("   ✅ Created sheet headers")

        # Prepare business data
        rows = []
        for business in businesses:
            rows.append([
                business.get('name', ''),
                business.get('location', ''),
                business.get('email', ''),
                business.get('phone', ''),
                business.get('website', ''),
                business.get('contact_person', ''),
                '',  # Generated Subject (empty)
                '',  # Generated Body (empty)
                '',  # Your Notes (empty)
                'Draft',  # Status
                '',  # Date Approved
                '',  # Date Sent
                '',  # Last Response
                ''   # Response Details
            ])

        # Append to sheet
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range='A2:N',
            valueInputOption='RAW',
            body={'values': rows}
        ).execute()

        print(f"   ✅ Uploaded {len(businesses)} businesses to Google Sheets")

    except HttpError as error:
        print(f"❌ Google Sheets API error: {error}")
    except Exception as error:
        print(f"❌ Error uploading to sheets: {error}")


def test_upload_to_sheets():
    """Test function"""
    test_businesses = [
        {
            'name': 'Test Dental',
            'location': 'San Francisco, CA',
            'email': 'contact@testdental.com',
            'phone': '(555) 123-4567',
            'website': 'https://testdental.com'
        }
    ]

    upload_businesses(test_businesses)


if __name__ == "__main__":
    test_upload_to_sheets()
