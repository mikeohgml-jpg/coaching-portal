#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test New Client registration flow."""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Load environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

from models import NewClientFormData
from services.google_sheets_service import GoogleSheetsService
from services.email_service import EmailService
from services.ai_service import AIService
from services.client_service import ClientService

def test_new_client():
    """Test adding a new client."""
    try:
        print("=" * 60)
        print("Testing New Client Registration Flow")
        print("=" * 60)

        # Initialize services
        print("\n1. Initializing services...")
        sheets_service = GoogleSheetsService()
        email_service = EmailService()
        ai_service = AIService()
        client_service = ClientService(sheets_service, email_service, ai_service)
        print("   ✓ Services initialized")

        # Create test client data
        print("\n2. Creating test client data...")
        test_data = NewClientFormData(
            name="Test Client AutoGen",
            email=f"test.autogen.{os.getpid()}@example.com",  # Unique email
            address="123 Test Street, Test City, TS 12345",
            contact="+1-555-TEST-01",
            package_type="Standard Package",
            start_date="2026-02-08",
            end_date="2026-05-08",
            amount_paid=2500.00,
            notes="Automated test client - safe to delete"
        )
        print(f"   ✓ Test client: {test_data.name} ({test_data.email})")

        # Check for duplicates
        print("\n3. Checking for duplicate clients...")
        duplicate = sheets_service.check_duplicate_client(test_data.name, test_data.email)
        if duplicate:
            print(f"   ⚠ Duplicate found: {duplicate.get('name')}")
            print("   Continuing anyway (this is expected if you ran this test before)...")
        else:
            print("   ✓ No duplicates found")

        # Add client
        print("\n4. Adding client to Google Sheets...")
        result = client_service.process_new_client_registration(test_data)
        print(f"   ✓ Client added successfully!")
        print(f"   Result: {result}")

        # Verify client was added
        print("\n5. Verifying client was added...")
        clients = sheets_service.get_all_clients()
        added_client = None
        for client in clients:
            if client.get('email') == test_data.email:
                added_client = client
                break

        if added_client:
            print(f"   ✓ Client verified in sheet!")
            print(f"   Client ID: {added_client.get('client_id')}")
            print(f"   Contract Number: {added_client.get('contract_number')}")
            print(f"   Invoice Number: {added_client.get('invoice_number')}")
        else:
            print("   ✗ Client not found in sheet!")
            return False

        print("\n" + "=" * 60)
        print("✓ NEW CLIENT REGISTRATION TEST PASSED")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n✗ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_new_client()
    sys.exit(0 if success else 1)
