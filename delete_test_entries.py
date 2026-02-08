#!/usr/bin/env python
"""Delete test entries from Google Sheets."""

from services.google_sheets_service import GoogleSheetsService

print("\n" + "="*60)
print("CLEANING UP TEST ENTRIES FROM CLIENTS SHEET")
print("="*60 + "\n")

service = GoogleSheetsService()

# Get all clients before deletion
clients_before = service.get_all_clients()
print(f"Before cleanup: {len(clients_before)} clients")
for i, client in enumerate(clients_before, 1):
    print(f"  {i}. {client.get('name')} - {client.get('email')}")

# Delete rows 3 and 4 (Michael Oh and TestClient)
# These are represented as rows 3-5 in the delete API (since row 1 is header, and we delete 0-indexed)
print("\nDeleting rows 3-4 (Michael Oh and TestClient)...")

try:
    service.delete_rows(start_row=3, end_row=4)
    print("✓ Deletion successful!")
except Exception as e:
    print(f"✗ Deletion failed: {e}")

# Verify deletion
print("\nVerifying deletion...")
clients_after = service.get_all_clients()
print(f"After cleanup: {len(clients_after)} clients")
for i, client in enumerate(clients_after, 1):
    print(f"  {i}. {client.get('name')} - {client.get('email')}")

print("\n" + "="*60)
print("CLEANUP COMPLETE")
print("="*60 + "\n")
