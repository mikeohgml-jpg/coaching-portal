#!/usr/bin/env python
"""Test script to check clients in Google Sheets."""

from services.google_sheets_service import GoogleSheetsService

service = GoogleSheetsService()
clients = service.get_all_clients()

print(f"\n{'='*60}")
print(f"Total clients in sheet: {len(clients)}")
print(f"{'='*60}\n")

for i, client in enumerate(clients, 1):
    print(f"{i}. Name: {client.get('name')}")
    print(f"   Email: {client.get('email')}")
    print(f"   Package: {client.get('package_type')}")
    print(f"   Start: {client.get('start_date')}")
    print(f"   End: {client.get('end_date')}")
    print()

print(f"{'='*60}\n")
