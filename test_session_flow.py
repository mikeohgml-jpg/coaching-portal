#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test existing client session flow."""

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

from models import ExistingClientFormData
from services.google_sheets_service import GoogleSheetsService
from services.email_service import EmailService
from services.ai_service import AIService
from services.client_service import ClientService

def test_session():
    """Test adding a session for an existing client."""
    try:
        print("=" * 60)
        print("Testing Session Recording Flow")
        print("=" * 60)

        # Initialize services
        print("\n1. Initializing services...")
        sheets_service = GoogleSheetsService()
        email_service = EmailService()
        ai_service = AIService()
        client_service = ClientService(sheets_service, email_service, ai_service)
        print("   ✓ Services initialized")

        # Get existing clients
        print("\n2. Fetching existing clients...")
        clients = sheets_service.get_all_clients()
        if not clients:
            print("   ✗ No clients found! Please add a client first.")
            return False

        # Use the first client for testing
        test_client = clients[0]
        print(f"   ✓ Found {len(clients)} clients")
        print(f"   Testing with: {test_client.get('name')} ({test_client.get('email')})")

        # Create test session data
        print("\n3. Creating test session data...")
        test_session = ExistingClientFormData(
            client_name=test_client.get('name'),
            coaching_type="One-on-One Coaching",
            coaching_hours=2.0,
            amount_collected=400.00,
            session_date="2026-02-08",
            notes="Automated test session - safe to delete"
        )
        print(f"   ✓ Session: {test_session.coaching_hours} hours on {test_session.session_date}")

        # Add session
        print("\n4. Adding session to Google Sheets...")
        result = client_service.process_existing_client_session(test_session)
        print(f"   ✓ Session added successfully!")
        print(f"   Result: {result}")

        # Verify session was added
        print("\n5. Verifying session was added...")
        sessions = sheets_service.get_client_history(test_client.get('name'))
        if sessions:
            latest_session = sessions[-1]  # Get the latest session
            print(f"   ✓ Session verified in sheet!")
            print(f"   Total sessions for client: {len(sessions)}")
            print(f"   Latest session date: {latest_session.get('session_date')}")
            print(f"   Latest session invoice: {latest_session.get('invoice_number')}")
        else:
            print("   ⚠ No sessions found (this might be the first one)")

        print("\n" + "=" * 60)
        print("✓ SESSION RECORDING TEST PASSED")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n✗ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_session()
    sys.exit(0 if success else 1)
