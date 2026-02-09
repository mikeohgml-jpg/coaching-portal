"""
Direct test of email sending to diagnose SMTP issues.
"""

import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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

print("="*60)
print("  DIRECT EMAIL TEST")
print("="*60)

# Get credentials
sender_email = os.getenv("GMAIL_SENDER_EMAIL", "").strip()
sender_password = os.getenv("GMAIL_APP_PASSWORD", "").strip()
sender_name = os.getenv("GMAIL_SENDER_NAME", "Michael Oh").strip()

print(f"\n📧 Email Configuration:")
print(f"   Sender Email: {sender_email}")
print(f"   Sender Name: {sender_name}")
print(f"   Password Set: {'Yes' if sender_password else 'No'} ({len(sender_password)} chars)")

if not sender_email or not sender_password:
    print("\n✗ ERROR: Email credentials not configured!")
    print("   Please check GMAIL_SENDER_EMAIL and GMAIL_APP_PASSWORD in .env")
    sys.exit(1)

# Test email
recipient = "mikeoh.gml@gmail.com"
subject = "🧪 Coaching Portal - Email Test"

# Create message
print(f"\n→ Creating test email...")
msg = MIMEMultipart('alternative')
msg['Subject'] = subject
msg['From'] = f"{sender_name} <{sender_email}>"
msg['To'] = recipient

# Plain text version
text_body = """
Hello!

This is a test email from your Coaching Portal email system.

If you're reading this, the email system is working correctly!

Best regards,
The Coaching Team
"""

# HTML version
html_body = """
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background-color: #007bff; color: white; padding: 20px; text-align: center; border-radius: 5px; }
        .content { padding: 20px 0; }
        .success { background-color: #d4edda; border: 1px solid #c3e6cb; padding: 15px; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 Email System Test</h1>
        </div>
        <div class="content">
            <p>Hello!</p>
            <p>This is a test email from your <strong>Coaching Portal</strong> email system.</p>
            <div class="success">
                <strong>✓ Success!</strong> If you're reading this, the email system is working correctly!
            </div>
            <p><strong>System Details:</strong></p>
            <ul>
                <li>Sender: Michael Oh</li>
                <li>Method: Gmail SMTP (Port 465, SSL)</li>
                <li>Status: Operational</li>
            </ul>
            <p>Your coaching portal will now automatically send:</p>
            <ul>
                <li>✉️ Welcome emails when new clients register</li>
                <li>✉️ Invoice emails when sessions are recorded</li>
            </ul>
            <p>Best regards,<br>The Coaching Team</p>
        </div>
    </div>
</body>
</html>
"""

part1 = MIMEText(text_body, 'plain')
part2 = MIMEText(html_body, 'html')

msg.attach(part1)
msg.attach(part2)

print("✓ Email message created")

# Send email
print(f"\n→ Connecting to Gmail SMTP server...")
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        print("✓ Connected to smtp.gmail.com:465 (SSL)")

        print(f"→ Authenticating as {sender_email}...")
        server.login(sender_email, sender_password)
        print("✓ Authentication successful")

        print(f"→ Sending email to {recipient}...")
        server.send_message(msg)
        print("✓ Email sent successfully!")

    print("\n" + "="*60)
    print("✓ EMAIL TEST SUCCESSFUL!")
    print("="*60)
    print(f"\n📬 CHECK YOUR INBOX: {recipient}")
    print("   Subject: 🧪 Coaching Portal - Email Test")
    print("   You should receive this email within 1-2 minutes.")
    print("\n   If you receive this email, your email system is working!")

except smtplib.SMTPAuthenticationError as e:
    print(f"\n✗ AUTHENTICATION FAILED!")
    print(f"   Error: {e}")
    print("\n   Possible causes:")
    print("   1. Gmail App Password is incorrect")
    print("   2. 2-Step Verification not enabled on Google Account")
    print("   3. App Password expired or revoked")
    print("\n   Solution:")
    print("   1. Go to: https://myaccount.google.com/apppasswords")
    print("   2. Generate a new App Password")
    print("   3. Update GMAIL_APP_PASSWORD in .env and Vercel")
    sys.exit(1)

except smtplib.SMTPException as e:
    print(f"\n✗ SMTP ERROR!")
    print(f"   Error: {e}")
    sys.exit(1)

except Exception as e:
    print(f"\n✗ UNEXPECTED ERROR!")
    print(f"   Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
