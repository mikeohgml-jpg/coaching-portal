"""AI service for generating email content using Claude."""

import logging
import json
from typing import Dict, Any, Optional
import requests

from config import Config


logger = logging.getLogger(__name__)


class AIService:
    """Service for generating content using Claude via OpenRouter."""
    
    def __init__(self):
        """Initialize AI service."""
        self.api_key = Config.OPENROUTER_API_KEY or Config.ANTHROPIC_API_KEY
        self.base_url = "https://openrouter.io/api/v1"
        self.model = "anthropic/claude-3-5-sonnet"
        
        if not self.api_key:
            logger.warning("No API key configured for AI service")
    
    def generate_welcome_email(self, client_data: Dict[str, Any]) -> str:
        """Generate a personalized welcome email for a new client."""
        try:
            if not self.api_key:
                logger.warning("AI service not configured, returning template")
                return self._get_welcome_email_template(client_data)
            
            prompt = f"""
            Generate a professional and warm welcome email for a new coaching client.
            
            Client Information:
            - Name: {client_data.get('name')}
            - Email: {client_data.get('email')}
            - Package Type: {client_data.get('package_type')}
            - Start Date: {client_data.get('start_date')}
            - End Date: {client_data.get('end_date')}
            - Amount Paid: ${client_data.get('amount_paid')}
            
            Create an HTML email that:
            1. Welcomes them warmly
            2. Acknowledges their coaching investment
            3. Sets expectations for the program
            4. Provides next steps
            5. Is professional yet personable
            
            Return only the HTML body, wrapped in <html> tags.
            """
            
            response = self._call_claude_api(prompt)
            return response
        
        except Exception as e:
            logger.error(f"Error generating welcome email: {e}")
            return self._get_welcome_email_template(client_data)
    
    def generate_invoice_email(self, session_data: Dict[str, Any]) -> str:
        """Generate an invoice email for a coaching session."""
        try:
            if not self.api_key:
                logger.warning("AI service not configured, returning template")
                return self._get_invoice_email_template(session_data)
            
            prompt = f"""
            Generate a professional invoice confirmation email for a coaching session.
            
            Session Information:
            - Client Name: {session_data.get('client_name')}
            - Coaching Type: {session_data.get('coaching_type')}
            - Session Date: {session_data.get('session_date')}
            - Hours: {session_data.get('coaching_hours')}
            - Participants: {session_data.get('participant_count')}
            - Amount: ${session_data.get('amount_collected')}
            
            Create an HTML email that:
            1. Thanks them for the session
            2. Provides a clear summary of services rendered
            3. Shows the amount due/paid
            4. Is professional and clear
            
            Return only the HTML body, wrapped in <html> tags.
            """
            
            response = self._call_claude_api(prompt)
            return response
        
        except Exception as e:
            logger.error(f"Error generating invoice email: {e}")
            return self._get_invoice_email_template(session_data)
    
    def _call_claude_api(self, prompt: str) -> str:
        """Call Claude API via OpenRouter."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 2000,
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract the generated text
            if result.get('choices') and len(result['choices']) > 0:
                return result['choices'][0]['message']['content'].strip()
            
            logger.warning("No content in API response")
            return ""
        
        except requests.exceptions.RequestException as e:
            logger.error(f"API request error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error calling Claude API: {e}")
            raise
    
    def _get_welcome_email_template(self, client_data: Dict[str, Any]) -> str:
        """Get a fallback welcome email template."""
        name = client_data.get('name', 'Valued Client')
        package = client_data.get('package_type', 'Coaching Program')
        start_date = client_data.get('start_date', '')
        end_date = client_data.get('end_date', '')
        amount = client_data.get('amount_paid', 0)
        
        return f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; border-radius: 5px; }}
                .content {{ padding: 20px 0; }}
                .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 30px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to Your Coaching Program!</h1>
                </div>
                <div class="content">
                    <p>Hello {name},</p>
                    <p>We're excited to have you join our coaching program!</p>
                    <p><strong>Your Program Details:</strong></p>
                    <ul>
                        <li><strong>Package:</strong> {package}</li>
                        <li><strong>Start Date:</strong> {start_date}</li>
                        <li><strong>End Date:</strong> {end_date}</li>
                        <li><strong>Investment:</strong> ${amount:.2f}</li>
                    </ul>
                    <p>Your coach will be reaching out shortly to schedule your first session. 
                    If you have any questions in the meantime, please don't hesitate to reach out.</p>
                    <p>We look forward to supporting your personal and professional growth!</p>
                    <p>Best regards,<br>The Coaching Team</p>
                </div>
                <div class="footer">
                    <p>This email was sent in response to your coaching program registration.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _get_invoice_email_template(self, session_data: Dict[str, Any]) -> str:
        """Get a fallback invoice email template."""
        name = session_data.get('client_name', 'Valued Client')
        coaching_type = session_data.get('coaching_type', 'Coaching Session')
        session_date = session_data.get('session_date', '')
        hours = session_data.get('coaching_hours', 0)
        participants = session_data.get('participant_count', 1)
        amount = session_data.get('amount_collected', 0)
        
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
                        <tr>
                            <td>Participants</td>
                            <td>{participants}</td>
                        </tr>
                        <tr class="total-row">
                            <td>Amount Due</td>
                            <td>${amount:.2f}</td>
                        </tr>
                    </table>
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
