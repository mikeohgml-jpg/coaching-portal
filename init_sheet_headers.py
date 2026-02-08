#!/usr/bin/env python
"""Initialize Google Sheets with proper headers."""

from services.google_sheets_service import GoogleSheetsService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("\n" + "="*70)
print("INITIALIZING GOOGLE SHEETS WITH NEW COLUMNS")
print("="*70 + "\n")

service = GoogleSheetsService()

# Define headers for Clients sheet (11 columns)
clients_headers = [
    "Name",
    "Email",
    "Package Type",
    "Start Date",
    "End Date",
    "Amount Paid",
    "Contract Number",
    "Invoice Number",
    "Client ID",
    "Created At",
    "Notes"
]

# Define headers for Sessions sheet (10 columns)
sessions_headers = [
    "Client Name",
    "Coaching Type",
    "Participant Count",
    "Coaching Hours",
    "Amount Collected",
    "Session Date",
    "Contract Number",
    "Invoice Number",
    "Created At",
    "Notes"
]

print("Adding headers to Clients sheet...")
print(f"Headers: {clients_headers}")

try:
    # Add headers to Clients sheet (row 1)
    service.service.spreadsheets().values().update(
        spreadsheetId=service.clients_sheet_id,
        range='A1:K1',
        valueInputOption='USER_ENTERED',
        body={'values': [clients_headers]}
    ).execute()
    print("✓ Clients sheet headers added successfully!")
except Exception as e:
    print(f"✗ Error adding Clients headers: {e}")

print("\nAdding headers to Sessions sheet...")
print(f"Headers: {sessions_headers}")

try:
    # Add headers to Sessions sheet (row 1)
    service.service.spreadsheets().values().update(
        spreadsheetId=service.sessions_sheet_id,
        range='A1:J1',
        valueInputOption='USER_ENTERED',
        body={'values': [sessions_headers]}
    ).execute()
    print("✓ Sessions sheet headers added successfully!")
except Exception as e:
    print(f"✗ Error adding Sessions headers: {e}")

print("\n" + "="*70)
print("SHEET INITIALIZATION COMPLETE")
print("="*70 + "\n")

# Verify current data
print("Current Clients in sheet:")
clients = service.get_all_clients()
for i, client in enumerate(clients, 1):
    print(f"  {i}. {client.get('name')} ({client.get('email')}) - Client ID: {client.get('client_id', 'N/A')}")

print(f"\nTotal clients: {len(clients)}")
print("\n" + "="*70 + "\n")
