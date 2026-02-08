#!/usr/bin/env python
"""Check the actual sheet structure."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

from services.google_sheets_service import GoogleSheetsService

try:
    sheets = GoogleSheetsService()

    # Get rows from sheet
    result = sheets.service.spreadsheets().values().get(
        spreadsheetId=sheets.clients_sheet_id,
        range='1:6'
    ).execute()

    values = result.get('values', [])
    for i, row in enumerate(values):
        if i == 0:
            print("HEADERS:")
            for j, col in enumerate(row):
                col_letter = chr(65 + j)
                print(f"  {col_letter}: {col}")
        if i == 5 and len(row) > 0:
            print("\nROW 6 DATA:")
            for j, col in enumerate(row):
                col_letter = chr(65 + j)
                print(f"  {col_letter}: {col}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
