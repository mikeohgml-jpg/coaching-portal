#!/usr/bin/env python
"""Fix the Clients sheet column structure - remove duplicate date/time columns."""

from services.google_sheets_service import GoogleSheetsService

print("\n" + "="*80)
print("FIXING CLIENTS SHEET STRUCTURE")
print("="*80 + "\n")

service = GoogleSheetsService()

# Get the current data
print("Reading current sheet structure...")
result = service.service.spreadsheets().values().get(
    spreadsheetId=service.clients_sheet_id,
    range='A:K'
).execute()

values = result.get('values', [])

print(f"Current columns: {len(values[0]) if values else 0}")
print(f"Headers: {values[0] if values else 'None'}\n")

# Define the correct column structure
correct_headers = [
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

print(f"Expected columns: {len(correct_headers)}")
print(f"Expected headers: {correct_headers}\n")

# Clear the entire sheet first
print("Clearing sheet...")
service.service.spreadsheets().batchUpdate(
    spreadsheetId=service.clients_sheet_id,
    body={
        'requests': [
            {
                'updateCells': {
                    'range': {
                        'sheetId': 0
                    },
                    'fields': 'userEnteredValue'
                }
            }
        ]
    }
).execute()

print("✓ Sheet cleared\n")

# Rewrite headers
print("Writing correct headers...")
service.service.spreadsheets().values().update(
    spreadsheetId=service.clients_sheet_id,
    range='A1:K1',
    valueInputOption='USER_ENTERED',
    body={'values': [correct_headers]}
).execute()

print("✓ Headers updated\n")

# Restore the data rows (rows 2 onwards from original)
if len(values) > 1:
    print(f"Restoring {len(values) - 1} data rows...")
    
    # Process each data row
    cleaned_rows = []
    for row_idx, row in enumerate(values[1:], 2):
        # Build a clean row with the correct structure
        # We need to map the old columns to the new ones
        
        if not row or not row[0]:  # Skip empty rows
            continue
        
        # Based on the current sheet structure from the screenshot:
        # A: Name, B: Email, C: Package Type, D: Start Date, E: End Date,
        # F: Amount Paid, G: Created At, H: Notes, I: Contract Number, J: (duplicate)
        
        # Map to new structure:
        clean_row = [
            row[0] if len(row) > 0 else "",  # Name -> A
            row[1] if len(row) > 1 else "",  # Email -> B
            row[2] if len(row) > 2 else "",  # Package Type -> C
            row[3] if len(row) > 3 else "",  # Start Date -> D
            row[4] if len(row) > 4 else "",  # End Date -> E
            row[5] if len(row) > 5 else "",  # Amount Paid -> F
            row[8] if len(row) > 8 else "",  # Contract Number (from column I) -> G
            "",  # Invoice Number (empty for now) -> H
            "",  # Client ID (empty for now) -> I
            row[6] if len(row) > 6 else "",  # Created At (from column G) -> J
            row[7] if len(row) > 7 else ""   # Notes (from column H) -> K
        ]
        
        cleaned_rows.append(clean_row)
    
    # Write the cleaned data back
    if cleaned_rows:
        service.service.spreadsheets().values().append(
            spreadsheetId=service.clients_sheet_id,
            range='A2:K',
            valueInputOption='USER_ENTERED',
            body={'values': cleaned_rows}
        ).execute()
        
        print(f"✓ Restored {len(cleaned_rows)} rows with correct structure\n")

# Clear the cache
service.client_cache = {}
service.cache_timestamp = None

print("="*80)
print("SHEET STRUCTURE FIXED")
print("="*80)
print("\nNew structure:")
print("A: Name")
print("B: Email")
print("C: Package Type")
print("D: Start Date")
print("E: End Date")
print("F: Amount Paid")
print("G: Contract Number")
print("H: Invoice Number")
print("I: Client ID")
print("J: Created At")
print("K: Notes")
print("\n" + "="*80 + "\n")

# Verify the result
print("Verifying updated sheet...")
clients = service.get_all_clients()
for i, client in enumerate(clients, 1):
    print(f"{i}. {client['name']} ({client['email']})")
    print(f"   Contract: {client.get('contract_number', '')}")
    print(f"   Client ID: {client.get('client_id', '')}")
    print()
