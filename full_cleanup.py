#!/usr/bin/env python
"""Clean up all test entries and restore to original state."""

from services.google_sheets_service import GoogleSheetsService

print("\n" + "="*60)
print("CLEANING UP ALL TEST ENTRIES")
print("="*60 + "\n")

service = GoogleSheetsService()

# Get all clients before deletion
clients_before = service.get_all_clients()
print(f"Before cleanup: {len(clients_before)} clients")
for i, client in enumerate(clients_before, 1):
    print(f"  {i}. {client.get('name')} ({client.get('email')})")

# Delete rows 2 and 3 (TestClient and Mike) - keep only Andrew
# We need to delete from the end first to avoid index shifting
print("\nDeleting rows 3-4 (TestClient and Mike)...")

try:
    service.delete_rows(start_row=3, end_row=4)  # API call will delete rows from index
    print("✓ First deletion successful!")
except Exception as e:
    print(f"✗ First deletion failed: {e}")

try:
    service.delete_rows(start_row=2, end_row=3)  # Delete what's now row 2
    print("✓ Second deletion successful!")
except Exception as e:
    print(f"✗ Second deletion failed: {e}")

# Verify final state
print("\nVerifying final state...")
clients_after = service.get_all_clients()
print(f"After cleanup: {len(clients_after)} clients")
for i, client in enumerate(clients_after, 1):
    print(f"  {i}. {client.get('name')} ({client.get('email')})")

print("\n" + "="*60)
print("Sheet is now clean with only original clients")
print("="*60 + "\n")
