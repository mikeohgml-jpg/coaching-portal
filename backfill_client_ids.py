"""Backfill Client IDs for existing clients."""

import uuid
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
from config import Config

# Initialize service
creds = service_account.Credentials.from_service_account_file(
    Config.GOOGLE_CREDENTIALS_JSON,
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
service = build('sheets', 'v4', credentials=creds)

# Read all client data
result = service.spreadsheets().values().get(
    spreadsheetId=Config.GOOGLE_CLIENTS_SHEET_ID,
    range='A:K'
).execute()
values = result.get('values', [])

# Generate Client IDs for rows without them
updates = []
for idx, row in enumerate(values[1:], start=2):  # Skip header
    if row and not row[0]:  # Client ID is empty
        # Generate a unique Client ID
        client_id = 'CL-{}'.format(uuid.uuid4().hex[:8].upper())
        # Queue update for column A
        updates.append({'range': 'A{}'.format(idx), 'values': [[client_id]]})
        client_name = row[1] if len(row) > 1 else 'Unknown'
        print('Row {}: Generated {} for {}'.format(idx, client_id, client_name))

# Batch update all Client IDs
if updates:
    batch_body = {'data': updates, 'valueInputOption': 'USER_ENTERED'}
    service.spreadsheets().values().batchUpdate(
        spreadsheetId=Config.GOOGLE_CLIENTS_SHEET_ID,
        body=batch_body
    ).execute()
    print()
    print('Successfully updated {} clients with Client IDs'.format(len(updates)))
else:
    print('No clients needed Client ID assignments')
