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
            # Check for duplicate client
            duplicate = self.sheets_service.check_duplicate_client(data.name, data.email)
            if duplicate:
                return False, f"A client with this name or email already exists"
            
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
            
            # Generate welcome email
            try:
                welcome_email_html = self.ai_service.generate_welcome_email(client_data)
                
                # Send welcome email
                email_content = EmailContent(
                    recipient_email=form_data.email,
                    subject=f"Welcome to Your Coaching Program, {form_data.name}!",
                    body=f"Welcome {form_data.name}! We're excited to have you in our coaching program.",
                    html_body=welcome_email_html
                )
                
                email_sent = self.email_service.send_email(email_content)
                logger.info(f"Welcome email sent to {form_data.email}: {email_sent}")
            except Exception as e:
                logger.error(f"Error sending welcome email: {e}")
                # Don't fail the whole process if email fails
            
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
            
            # Update client end date if provided
            if form_data.new_end_date:
                self.sheets_service.update_client_end_date(
                    form_data.client_name,
                    form_data.new_end_date
                )
                logger.info(f"Updated end date for client: {form_data.client_name}")
            
            # Generate invoice email
            try:
                invoice_email_html = self.ai_service.generate_invoice_email(session_data)
                
                # Send invoice email
                email_content = EmailContent(
                    recipient_email=client.get("email", ""),
                    subject=f"Coaching Session Invoice - {form_data.session_date}",
                    body=f"Thank you for your coaching session on {form_data.session_date}.",
                    html_body=invoice_email_html
                )
                
                email_sent = self.email_service.send_email(email_content)
                logger.info(f"Invoice email sent to {client.get('email')}: {email_sent}")
            except Exception as e:
                logger.error(f"Error sending invoice email: {e}")
                # Don't fail the whole process if email fails
            
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
