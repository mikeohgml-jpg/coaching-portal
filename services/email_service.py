"""Email service for Coaching Portal."""

import logging
import base64
from email.mime.text import MIMEText
from typing import Dict, Any, Optional
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import Config
from models import EmailContent


logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails via Gmail API."""
    
    def __init__(self):
        """Initialize Gmail email service."""
        self.credentials = None
        self.service = None
        self.sender_email = Config.GMAIL_SENDER_EMAIL
        
        try:
            self._initialize_service()
            logger.info("Email service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing email service: {e}")
            # Continue without email service - it may not be configured
    
    def _initialize_service(self):
        """Initialize Gmail API client."""
        if not Config.GOOGLE_CREDENTIALS_JSON:
            logger.warning("GOOGLE_CREDENTIALS_JSON not configured, email service disabled")
            return
        
        try:
            # Load service account credentials
            self.credentials = service_account.Credentials.from_service_account_file(
                Config.GOOGLE_CREDENTIALS_JSON,
                scopes=['https://www.googleapis.com/auth/gmail.send']
            )
            
            # Build the Gmail API service
            self.service = build('gmail', 'v1', credentials=self.credentials)
        except Exception as e:
            logger.error(f"Could not initialize Gmail service: {e}")
    
    def send_email(self, email_content: EmailContent) -> bool:
        """Send an email via Gmail API."""
        try:
            if not self.service:
                logger.warning("Email service not available, skipping email send")
                return False
            
            if not self.sender_email:
                logger.warning("Sender email not configured, skipping email send")
                return False
            
            # Create message
            message = MIMEText(email_content.html_body or email_content.body, 'html')
            message['to'] = email_content.recipient_email
            message['from'] = self.sender_email
            message['subject'] = email_content.subject
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            # Send message
            send_message = {'raw': raw_message}
            self.service.users().messages().send(
                userId='me',
                body=send_message
            ).execute()
            
            logger.info(f"Email sent to {email_content.recipient_email}: {email_content.subject}")
            return True
        
        except HttpError as e:
            logger.error(f"HTTP error sending email: {e}")
            return False
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    def format_email(self, 
                    template: str,
                    context: Dict[str, Any]) -> str:
        """Format an email using a template and context."""
        try:
            # Simple template formatting
            html_body = template
            
            for key, value in context.items():
                placeholder = f"{{{{{key}}}}}"
                html_body = html_body.replace(placeholder, str(value))
            
            return html_body
        
        except Exception as e:
            logger.error(f"Error formatting email: {e}")
            raise
    
    def get_welcome_email_template(self) -> str:
        """Get the welcome email HTML template."""
        return """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background-color: #007bff; color: white; padding: 20px; text-align: center; border-radius: 5px; }
                .content { padding: 20px 0; }
                .footer { text-align: center; color: #999; font-size: 12px; margin-top: 30px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to Your Coaching Program!</h1>
                </div>
                <div class="content">
                    <p>Hello {{client_name}},</p>
                    <p>We're excited to have you join our coaching program!</p>
                    <p><strong>Program Details:</strong></p>
                    <ul>
                        <li><strong>Package:</strong> {{package_type}}</li>
                        <li><strong>Start Date:</strong> {{start_date}}</li>
                        <li><strong>End Date:</strong> {{end_date}}</li>
                        <li><strong>Investment:</strong> ${{amount_paid}}</li>
                    </ul>
                    <p>Your coach will be reaching out shortly to schedule your first session. 
                    If you have any questions in the meantime, please don't hesitate to reach out.</p>
                    <p>Looking forward to supporting your growth!</p>
                    <p>Best regards,<br>The Coaching Team</p>
                </div>
                <div class="footer">
                    <p>This email was sent to {{client_email}}</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def get_invoice_email_template(self) -> str:
        """Get the invoice email HTML template."""
        return """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background-color: #28a745; color: white; padding: 20px; text-align: center; border-radius: 5px; }
                .content { padding: 20px 0; }
                .invoice-table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                .invoice-table th, .invoice-table td { border: 1px solid #ddd; padding: 10px; text-align: left; }
                .invoice-table th { background-color: #f5f5f5; }
                .total-row { font-weight: bold; background-color: #f5f5f5; }
                .footer { text-align: center; color: #999; font-size: 12px; margin-top: 30px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Session Invoice</h1>
                </div>
                <div class="content">
                    <p>Hello {{client_name}},</p>
                    <p>Thank you for completing your coaching session. Here's the summary:</p>
                    <table class="invoice-table">
                        <tr>
                            <th>Description</th>
                            <th>Details</th>
                        </tr>
                        <tr>
                            <td>Coaching Type</td>
                            <td>{{coaching_type}}</td>
                        </tr>
                        <tr>
                            <td>Session Date</td>
                            <td>{{session_date}}</td>
                        </tr>
                        <tr>
                            <td>Hours</td>
                            <td>{{coaching_hours}}</td>
                        </tr>
                        <tr>
                            <td>Participants</td>
                            <td>{{participant_count}}</td>
                        </tr>
                        <tr class="total-row">
                            <td>Amount Due</td>
                            <td>${{amount_collected}}</td>
                        </tr>
                    </table>
                    <p>Payment received on {{session_date}}. Thank you for your investment in your growth!</p>
                    <p>Best regards,<br>The Coaching Team</p>
                </div>
                <div class="footer">
                    <p>This email was sent to {{client_email}}</p>
                </div>
            </div>
        </body>
        </html>
        """
