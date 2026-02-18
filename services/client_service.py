"""Client service for high-level client management."""

import logging
from typing import Dict, Any, Optional

from models import NewClientFormData, ExistingClientFormData, EmailContent
from services.google_sheets_service import GoogleSheetsService
from services.email_service import EmailService
from services.ai_service import AIService


logger = logging.getLogger(__name__)


class ClientService:
    """High-level service for client management and orchestration."""
    
    def __init__(self,
                 sheets_service: GoogleSheetsService,
                 email_service: EmailService,
                 ai_service: AIService):
        """Initialize client service with dependencies."""
        self.sheets_service = sheets_service
        self.email_service = email_service
        self.ai_service = ai_service
    
    def validate_new_client_data(self, data: NewClientFormData) -> tuple[bool, str]:
        """Validate new client data."""
        try:
            # Check for duplicate client (with timeout protection)
            try:
                duplicate = self.sheets_service.check_duplicate_client(data.name, data.email)
                if duplicate:
                    return False, f"A client with this name or email already exists"
            except Exception as check_error:
                # If duplicate check fails, log warning but allow registration to proceed
                logger.warning(f"Could not verify duplicate client (proceeding anyway): {check_error}")
            
            # All validation passed
            return True, "Validation successful"
        
        except Exception as e:
            logger.error(f"Error validating client data: {e}")
            return False, f"Validation error: {str(e)}"
    
    def validate_session_data(self, data: ExistingClientFormData) -> tuple[bool, str]:
        """Validate session data."""
        try:
            # Check if client exists
            client = self.sheets_service.get_client_by_name(data.client_name)
            if not client:
                return False, f"Client '{data.client_name}' not found"
            
            # All validation passed
            return True, "Validation successful"
        
        except Exception as e:
            logger.error(f"Error validating session data: {e}")
            return False, f"Validation error: {str(e)}"
    
    def process_new_client_registration(self, form_data: NewClientFormData) -> Dict[str, Any]:
        """Process a new client registration."""
        try:
            # Validate data
            is_valid, message = self.validate_new_client_data(form_data)
            if not is_valid:
                raise ValueError(message)
            
            # Prepare client data (Contract Number will be auto-generated)
            client_data = {
                "name": form_data.name,
                "email": form_data.email,
                "address": form_data.address or "",
                "contact": form_data.contact or "",
                "package_type": form_data.package_type,
                "start_date": form_data.start_date,
                "end_date": form_data.end_date,
                "amount_paid": form_data.amount_paid,
                "notes": form_data.notes or ""
            }
            
            # Add to Google Sheets
            sheets_result = self.sheets_service.add_new_client(client_data)
            logger.info(f"New client added to sheets: {form_data.name}")
            
            # Generate welcome email using template
            welcome_email_html = self.ai_service._get_welcome_email_template(client_data)
            logger.info(f"✓ Generated welcome email for {form_data.name}")

            # Log email content for verification (since Gmail API may not be configured)
            logger.info(f"Email would be sent to: {form_data.email}")
            logger.info(f"Subject: Welcome to Your Coaching Program, {form_data.name}!")

            # Try to send email (will fail gracefully if not configured)
            try:
                email_content = EmailContent(
                    recipient_email=form_data.email,
                    subject=f"Welcome to Your Coaching Program, {form_data.name}!",
                    body=f"Welcome {form_data.name}! We're excited to have you in our coaching program.",
                    html_body=welcome_email_html
                )

                email_sent = self.email_service.send_email(email_content)
                if email_sent:
                    logger.info(f"✓ Welcome email sent to {form_data.email}")
            except Exception as e:
                logger.warning(f"⚠ Email not sent (service not configured): {str(e)[:100]}")
            
            return {
                "status": "success",
                "client_name": form_data.name,
                "client_email": form_data.email,
                "message": "Client registered successfully",
                "sheets_result": sheets_result
            }
        
        except ValueError as e:
            logger.warning(f"Validation error in process_new_client_registration: {e}")
            raise
        except Exception as e:
            logger.error(f"Error processing new client registration: {e}")
            raise
    
    def _generate_invoice_email_html(self, session_data: Dict[str, Any]) -> str:
        """Generate hardcoded invoice email HTML template."""
        name = session_data.get('client_name', 'Valued Client')
        coaching_type = session_data.get('coaching_type', 'Coaching Session')
        session_date = session_data.get('session_date', '')
        hours = session_data.get('coaching_hours', 0)
        amount = session_data.get('amount_collected', 0)
        notes = session_data.get('notes', '')
        
        # Balance information (if provided)
        total_package = session_data.get('total_package', 0)
        total_collected = session_data.get('total_collected', 0)
        remaining_balance = session_data.get('remaining_balance', 0)
        
        return f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #28a745; color: white; padding: 20px; text-align: center; border-radius: 5px; }}
                .content {{ padding: 20px 0; }}
                .invoice-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                .invoice-table th, .invoice-table td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
                .invoice-table th {{ background-color: #f5f5f5; }}
                .total-row {{ font-weight: bold; background-color: #f5f5f5; }}
                .balance-row {{ font-weight: bold; background-color: #e8f5e9; }}
                .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 30px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Session Invoice</h1>
                </div>
                <div class="content">
                    <p>Hello {name},</p>
                    <p>Thank you for completing your coaching session. Here's the summary:</p>
                    <table class="invoice-table">
                        <tr>
                            <th>Description</th>
                            <th>Details</th>
                        </tr>
                        <tr>
                            <td>Coaching Type</td>
                            <td>{coaching_type}</td>
                        </tr>
                        <tr>
                            <td>Session Date</td>
                            <td>{session_date}</td>
                        </tr>
                        <tr>
                            <td>Hours</td>
                            <td>{hours}</td>
                        </tr>
                        <tr class="total-row">
                            <td>Amount Collected</td>
                            <td>${amount:.2f}</td>
                        </tr>
                        <tr>
                            <td>Package Total</td>
                            <td>${total_package:.2f}</td>
                        </tr>
                        <tr>
                            <td>Total Collected to Date</td>
                            <td>${total_collected:.2f}</td>
                        </tr>
                        <tr class="balance-row">
                            <td>Remaining Balance</td>
                            <td>${remaining_balance:.2f}</td>
                        </tr>
                    </table>
                    {f'<p><strong>Notes:</strong> {notes}</p>' if notes else ''}
                    <p>Thank you for your investment in your growth and development!</p>
                    <p>Best regards,<br>The Coaching Team</p>
                </div>
                <div class="footer">
                    <p>This email was sent in response to your coaching session.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def process_existing_client_session(self, form_data: ExistingClientFormData) -> Dict[str, Any]:
        """Process an existing client coaching session."""
        try:
            # Validate data
            is_valid, message = self.validate_session_data(form_data)
            if not is_valid:
                raise ValueError(message)
            
            # Get client info
            client = self.sheets_service.get_client_by_name(form_data.client_name)
            
            # Prepare session data
            session_data = {
                "client_name": form_data.client_name,
                "coaching_type": form_data.coaching_type,
                "coaching_hours": form_data.coaching_hours,
                "amount_collected": form_data.amount_collected,
                "session_date": form_data.session_date,
                "notes": form_data.notes or ""
            }
            
            # Add session to Google Sheets
            sheets_result = self.sheets_service.add_session(session_data)
            logger.info(f"Session added for client: {form_data.client_name}")
            
            # Calculate balance information for invoice email
            total_package = float(client.get('amount_paid', 0))
            sessions = self.sheets_service.get_client_history(form_data.client_name)
            total_collected = sum(float(s.get('amount_collected', 0)) for s in sessions)
            remaining_balance = total_package - total_collected
            
            # Add balance info to session data for email
            session_data['total_package'] = total_package
            session_data['total_collected'] = total_collected
            session_data['remaining_balance'] = remaining_balance
            
            # Update client end date if provided
            if form_data.new_end_date:
                self.sheets_service.update_client_end_date(
                    form_data.client_name,
                    form_data.new_end_date
                )
                logger.info(f"Updated end date for client: {form_data.client_name}")
            
            # Generate invoice email using hardcoded template
            invoice_email_html = self._generate_invoice_email_html(session_data)
            logger.info(f"✓ Generated invoice email for {form_data.client_name}")

            # Log email content for verification
            logger.info(f"Email would be sent to: {client.get('email')}")
            logger.info(f"Subject: Coaching Session Invoice - {form_data.session_date}")

            # Try to send email (will fail gracefully if not configured)
            try:
                email_content = EmailContent(
                    recipient_email=client.get("email", ""),
                    subject=f"Coaching Session Invoice - {form_data.session_date}",
                    body=f"Thank you for your coaching session on {form_data.session_date}.",
                    html_body=invoice_email_html
                )

                email_sent = self.email_service.send_email(email_content)
                if email_sent:
                    logger.info(f"✓ Invoice email sent to {client.get('email')}")
            except Exception as e:
                logger.warning(f"⚠ Email not sent (service not configured): {str(e)[:100]}")
            
            return {
                "status": "success",
                "client_name": form_data.client_name,
                "session_date": form_data.session_date,
                "amount_collected": form_data.amount_collected,
                "message": "Session recorded successfully",
                "sheets_result": sheets_result
            }
        
        except ValueError as e:
            logger.warning(f"Validation error in process_existing_client_session: {e}")
            raise
        except Exception as e:
            logger.error(f"Error processing existing client session: {e}")
            raise
