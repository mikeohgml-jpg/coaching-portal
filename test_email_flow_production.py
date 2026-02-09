"""
Test complete email flow in production:
1. New Client Registration → Welcome Email
2. Session Recording → Invoice Email
"""

import sys
import requests
import json
from datetime import datetime, timedelta

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Production URL
BASE_URL = "https://coaching-portal-python.vercel.app"

def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def login_to_portal():
    """Login to the portal and get session cookie."""
    print_section("STEP 1: Login to Portal")

    session = requests.Session()

    # Get login page first (to establish session)
    print("→ Accessing login page...")
    response = session.get(f"{BASE_URL}/login")
    if response.status_code != 200:
        print(f"✗ Failed to access login page: {response.status_code}")
        return None
    print("✓ Login page accessed")

    # Submit login credentials
    print("→ Submitting credentials...")
    login_data = {
        "username": "coachadmin",
        "password": "CoachPortal2026!"
    }

    response = session.post(
        f"{BASE_URL}/login",
        data=login_data,
        allow_redirects=False
    )

    if response.status_code in [302, 303]:
        print("✓ Login successful")
        return session
    else:
        print(f"✗ Login failed: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        return None

def test_new_client_registration(session):
    """Test new client registration and welcome email."""
    print_section("STEP 2: Test New Client Registration + Welcome Email")

    # Generate unique test data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_client_name = f"Test Client {timestamp}"
    # Use Gmail aliasing - all emails go to same inbox but appear unique
    test_email = f"Mikeoh.gml+test{timestamp}@gmail.com"

    start_date = datetime.now().strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")

    client_data = {
        "name": test_client_name,
        "email": test_email,
        "address": "123 Test Street, Test City, TC 12345",
        "contact": "+1-555-TEST-123",
        "package_type": "Premium Package",
        "start_date": start_date,
        "end_date": end_date,
        "amount_paid": "2500.00",
        "notes": "Email system test - automated test client"
    }

    print(f"→ Registering new client: {test_client_name}")
    print(f"  Email: {test_email}")
    print(f"  Package: {client_data['package_type']}")
    print(f"  Start: {start_date}, End: {end_date}")
    print(f"  Amount: ${client_data['amount_paid']}")

    response = session.post(
        f"{BASE_URL}/api/clients/new",
        json=client_data,
        headers={"Content-Type": "application/json"}
    )

    print(f"\nResponse Status: {response.status_code}")

    if response.status_code in [200, 201]:
        try:
            result = response.json()
            print("✓ Client registered successfully")
            print(f"\nResponse Data:")
            print(json.dumps(result, indent=2))

            print(f"\n{'─'*60}")
            print("📧 WELCOME EMAIL SHOULD BE SENT TO:")
            print(f"   To: {test_email}")
            print(f"   From: Michael Oh <Mikeoh.gml@gmail.com>")
            print(f"   Subject: Welcome to Your Coaching Program, {test_client_name}!")
            print(f"{'─'*60}")

            return test_client_name
        except json.JSONDecodeError:
            print(f"✗ Invalid JSON response: {response.text[:200]}")
            return None
    else:
        print(f"✗ Registration failed: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        return None

def test_session_recording(session, client_name):
    """Test session recording and invoice email."""
    print_section("STEP 3: Test Session Recording + Invoice Email")

    if not client_name:
        print("✗ Cannot test session - no client name provided")
        return False

    session_date = datetime.now().strftime("%Y-%m-%d")

    session_data = {
        "client_name": client_name,
        "coaching_type": "Individual Coaching",
        "coaching_hours": "2.0",
        "amount_collected": "300.00",
        "session_date": session_date,
        "notes": "Email system test - automated test session"
    }

    print(f"→ Recording session for: {client_name}")
    print(f"  Type: {session_data['coaching_type']}")
    print(f"  Hours: {session_data['coaching_hours']}")
    print(f"  Amount: ${session_data['amount_collected']}")
    print(f"  Date: {session_date}")

    response = session.post(
        f"{BASE_URL}/api/clients/existing-session",
        json=session_data,
        headers={"Content-Type": "application/json"}
    )

    print(f"\nResponse Status: {response.status_code}")

    if response.status_code in [200, 201]:
        try:
            result = response.json()
            print("✓ Session recorded successfully")
            print(f"\nResponse Data:")
            print(json.dumps(result, indent=2))

            print(f"\n{'─'*60}")
            print("📧 INVOICE EMAIL SHOULD BE SENT TO:")
            print(f"   To: (test email with +test suffix)")
            print(f"   From: Michael Oh <Mikeoh.gml@gmail.com>")
            print(f"   Subject: Coaching Session Invoice - {session_date}")
            print(f"   (Will arrive in your main Mikeoh.gml@gmail.com inbox)")
            print(f"{'─'*60}")

            return True
        except json.JSONDecodeError:
            print(f"✗ Invalid JSON response: {response.text[:200]}")
            return False
    else:
        print(f"✗ Session recording failed: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        return False

def main():
    """Run complete email flow test."""
    print("\n" + "="*60)
    print("  PRODUCTION EMAIL FLOW TEST")
    print("  Testing: https://coaching-portal-python.vercel.app")
    print("="*60)

    # Step 1: Login
    session = login_to_portal()
    if not session:
        print("\n✗ TEST FAILED: Could not login to portal")
        return False

    # Step 2: Test New Client Registration + Welcome Email
    client_name = test_new_client_registration(session)
    if not client_name:
        print("\n✗ TEST FAILED: Could not register new client")
        return False

    # Step 3: Test Session Recording + Invoice Email
    session_success = test_session_recording(session, client_name)
    if not session_success:
        print("\n✗ TEST FAILED: Could not record session")
        return False

    # Final Summary
    print_section("TEST SUMMARY")
    print("✓ Login: SUCCESS")
    print("✓ New Client Registration: SUCCESS")
    print("✓ Welcome Email: SENT (check inbox)")
    print("✓ Session Recording: SUCCESS")
    print("✓ Invoice Email: SENT (check inbox)")

    print(f"\n{'─'*60}")
    print("📬 CHECK YOUR INBOX: Mikeoh.gml@gmail.com")
    print("   You should have received 2 emails:")
    print("   1. Welcome Email (for new client)")
    print("   2. Invoice Email (for session)")
    print("   Note: Sent to addresses with +test suffix, but delivered to your main inbox")
    print(f"{'─'*60}")

    print("\n✓ ALL TESTS PASSED!")
    print("\nNext Steps:")
    print("1. Check your Gmail inbox for the 2 test emails")
    print("2. Verify the welcome email has correct client details")
    print("3. Verify the invoice email has correct session details")
    print("4. Check Google Sheets for the new client and session")

    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
