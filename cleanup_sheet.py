#!/usr/bin/env python
"""Cleanup test entries from Google Sheets."""

from services.google_sheets_service import GoogleSheetsService

service = GoogleSheetsService()

# Get all clients with row indices
clients = service.get_all_clients()

print(f"\nCurrent clients in sheet ({len(clients)} total):")
print("="*60)

rows_to_delete = []

for i, client in enumerate(clients, 1):
    name = client.get('name')
    email = client.get('email')
    print(f"{i}. {name} - {email}")
    
    # Mark test entries for deletion
    if name in ["Michael Oh", "TestClient"]:
        rows_to_delete.append(i + 1)  # +2 because row 1 is header, enumerate starts at 1
        print(f"   ^ MARKED FOR DELETION (test entry)")

print("="*60)

if rows_to_delete:
    print(f"\nFound {len(rows_to_delete)} test entries to delete: rows {rows_to_delete}")
    print("\nTo delete these rows manually:")
    print("1. Open the Google Sheet")
    print(f"2. Delete rows: {rows_to_delete}")
    print("3. Or use the API to delete them")
else:
    print("\nNo test entries found to delete!")

print()
