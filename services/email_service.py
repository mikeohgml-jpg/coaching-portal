"""Email service for Coaching Portal."""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional

from config import Config
from models import EmailContent


logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails via Gmail SMTP."""

    def __init__(self):
        """Initialize Gmail SMTP email service."""
        self.sender_email = (Config.GMAIL_SENDER_EMAIL or '').strip()
        self.sender_password = (Config.GMAIL_APP_PASSWORD or '').strip()
        self.sender_name = (Config.GMAIL_SENDER_NAME or 'Coaching Portal').strip()

        if self.sender_email and self.sender_password:
            logger.info(f"Email service initialized for: {self.sender_email}")
        else:
            logger.warning("Email service not configured (missing GMAIL_SENDER_EMAIL or GMAIL_APP_PASSWORD)")

    def send_email(self, email_content: EmailContent) -> bool:
        """Send an email via Gmail SMTP."""
        try:
            if not self.sender_email or not self.sender_password:
                logger.warning("Email credentials not configured, skipping email send")
                return False

            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = email_content.subject
            msg['From'] = f"{self.sender_name} <{self.sender_email}>"
            msg['To'] = email_content.recipient_email

            # Add plain text and HTML parts
            part1 = MIMEText(email_content.body, 'plain')
            part2 = MIMEText(email_content.html_body or email_content.body, 'html')

            msg.attach(part1)
            msg.attach(part2)

            # Send via Gmail SMTP
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            logger.info(f"✓ Email sent to {email_content.recipient_email}: {email_content.subject}")
            return True

        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP Authentication failed - check GMAIL_APP_PASSWORD: {e}")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error sending email: {e}")
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
