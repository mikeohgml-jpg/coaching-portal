#!/usr/bin/env python
"""Display all clients with new fields."""

from services.google_sheets_service import GoogleSheetsService

service = GoogleSheetsService()
clients = service.get_all_clients()

print('\n' + '='*80)
print('CLIENTS IN SHEET WITH NEW FIELDS')
print('='*80 + '\n')

for i, client in enumerate(clients, 1):
    print(f'{i}. {client["name"]} ({client["email"]})')
    print(f'   Package: {client.get("package_type", "N/A")}')
    print(f'   Amount: ${client.get("amount_paid", 0):.2f}')
    print(f'   Contract #: {client.get("contract_number", "")}')
    print(f'   Invoice #: {client.get("invoice_number", "")}')
    print(f'   Client ID: {client.get("client_id", "")}')
    print()

print('='*80 + '\n')
