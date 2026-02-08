#!/usr/bin/env python
"""Restore the sheet with correct client data."""

from services.google_sheets_service import GoogleSheetsService
import time

service = GoogleSheetsService()

# The clients that should be in the sheet
clients_to_restore = [
    {
        "name": "Andrew",
        "email": "mikeoh.gml@gmail.com",
        "package_type": "Starter",
        "start_date": "2026-02-07",
        "end_date": "2026-04-02",
        "amount_paid": 1200.00,
        "notes": ""
    },
    {
        "name": "Sarah Johnson",
        "email": "sarah@example.com", 
        "package_type": "Premium Package",
        "start_date": "2026-02-10",
        "end_date": "2026-05-10",
        "amount_paid": 2500.00,
        "notes": "New client test"
    }
]

print("\n" + "="*60)
print("RESTORING CLIENTS TO SHEET")
print("="*60 + "\n")

for client_data in clients_to_restore:
    try:
        service.add_new_client(client_data)
        print(f"✓ Added: {client_data['name']} ({client_data['email']})")
        time.sleep(0.5)  # Small delay between requests
    except Exception as e:
        print(f"✗ Failed to add {client_data['name']}: {e}")

# Verify restoration
print("\nVerifying restoration...")
time.sleep(1)
clients = service.get_all_clients()
print(f"\nFinal state: {len(clients)} clients")
for i, client in enumerate(clients, 1):
    print(f"  {i}. {client['name']} ({client['email']})")

print("\n" + "="*60)
print("RESTORATION COMPLETE")
print("="*60 + "\n")
