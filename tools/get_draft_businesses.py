#!/usr/bin/env python3
"""
Get businesses with "Draft" status from Google Sheets
"""

import os
from dotenv import load_dotenv
from .upload_to_sheets import get_sheets_service

load_dotenv()


def get_draft_businesses():
    """
    Get all businesses with Status = "Draft" from Google Sheets

    Returns:
        list: List of business dictionaries with row numbers
    """

    try:
        service = get_sheets_service()
        spreadsheet_id = os.getenv('GOOGLE_SPREADSHEET_ID')

        if not spreadsheet_id:
            print("❌ GOOGLE_SPREADSHEET_ID not set in .env")
            return []

        # Get all rows
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='A2:N'  # Skip header row
        ).execute()

        rows = result.get('values', [])

        if not rows:
            print("❌ No data found in Google Sheet")
            return []

        # Filter for Draft status (column J, index 9)
        draft_businesses = []
        for i, row in enumerate(rows, start=2):  # Start at row 2 (skip header)
            # Ensure row has enough columns
            while len(row) < 14:
                row.append('')

            status = row[9] if len(row) > 9 else ''

            if status.lower() == 'draft':
                business = {
                    'row_number': i,
                    'name': row[0],
                    'location': row[1],
                    'email': row[2],
                    'phone': row[3],
                    'website': row[4],
                    'contact_person': row[5],
                    'generated_subject': row[6],
                    'generated_body': row[7],
                    'notes': row[8],
                    'status': row[9]
                }
                draft_businesses.append(business)

        return draft_businesses

    except Exception as error:
        print(f"❌ Error getting draft businesses: {error}")
        return []


def test_get_draft_businesses():
    """Test function"""
    businesses = get_draft_businesses()
    print(f"Found {len(businesses)} draft businesses:")
    for b in businesses:
        print(f"  Row {b['row_number']}: {b['name']}")


if __name__ == "__main__":
    test_get_draft_businesses()
