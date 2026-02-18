"""Google Sheets API service for Coaching Portal."""

import logging
import json
import os
from typing import List, Dict, Optional, Any
from datetime import datetime
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import Config


logger = logging.getLogger(__name__)


class GoogleSheetsService:
    """Service for interacting with Google Sheets API."""
    
    def __init__(self):
        """Initialize Google Sheets service."""
        # Strip whitespace/newlines from sheet IDs
        self.clients_sheet_id = (Config.GOOGLE_CLIENTS_SHEET_ID or '').strip()
        self.sessions_sheet_id = (Config.GOOGLE_SESSIONS_SHEET_ID or '').strip()
        self.credentials = None
        self.service = None
        self.client_cache = {}
        self.cache_timestamp = None

        try:
            self._initialize_service()
            logger.info("Google Sheets service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Google Sheets service: {e}")
            raise
    
    def _initialize_service(self):
        """Initialize Google Sheets API client."""
        credentials_data = (Config.GOOGLE_CREDENTIALS_JSON or '').strip()

        if not credentials_data:
            raise ValueError("GOOGLE_CREDENTIALS_JSON not configured")

        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]

        # Resolve relative file paths against the project root (where config.py lives)
        if credentials_data and not os.path.isabs(credentials_data) and not credentials_data.startswith('{'):
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            resolved_path = os.path.join(project_root, credentials_data)
            if os.path.exists(resolved_path):
                credentials_data = resolved_path

        # Check if credentials_data is a file path or JSON string
        if os.path.exists(credentials_data):
            # Load from file (local development)
            logger.info("Loading credentials from file")
            self.credentials = service_account.Credentials.from_service_account_file(
                credentials_data,
                scopes=scopes
            )
        else:
            # Parse as JSON string (Vercel deployment)
            logger.info("Loading credentials from JSON string")
            try:
                import json
                credentials_info = json.loads(credentials_data)
                self.credentials = service_account.Credentials.from_service_account_info(
                    credentials_info,
                    scopes=scopes
                )
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid GOOGLE_CREDENTIALS_JSON format: {e}")

        # Build the Sheets API service
        self.service = build('sheets', 'v4', credentials=self.credentials)
    
    def _is_cache_valid(self) -> bool:
        """Check if client cache is still valid."""
        if not self.cache_timestamp:
            return False
        
        elapsed = (datetime.utcnow() - self.cache_timestamp).total_seconds()
        return elapsed < Config.CLIENT_CACHE_TTL
    
    def get_all_clients(self) -> List[Dict[str, Any]]:
        """Fetch all clients from the Clients sheet."""
        try:
            # Return cached data if valid
            if self._is_cache_valid() and self.client_cache:
                logger.info("Returning cached client list")
                return self.client_cache
            
            # Read from Clients sheet
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.clients_sheet_id,
                range='A:M'
            ).execute()
            
            values = result.get('values', [])
            
            if not values:
                logger.warning("No clients found in sheet")
                return []
            
            # Parse header and data rows
            header = values[0] if values else []
            clients = []
            
            for row in values[1:]:
                # Skip empty rows
                if not row or not row[0]:
                    continue
                
                # Parse columns based on actual sheet structure:
                # A:Client ID, B:Name, C:Address, D:Contact, E:Email, F:Package, G:Start, H:End, I:Amount, J:Payment Method, K:Contract, L:Invoice, M:Created At, N:Notes
                client = {
                    "client_id": row[0] if len(row) > 0 else "",
                    "name": row[1] if len(row) > 1 else "",
                    "address": row[2] if len(row) > 2 else "",
                    "contact": row[3] if len(row) > 3 else "",
                    "email": row[4] if len(row) > 4 else "",
                    "package_type": row[5] if len(row) > 5 else "",
                    "start_date": row[6] if len(row) > 6 else "",
                    "end_date": row[7] if len(row) > 7 else "",
                    "amount_paid": float(row[8]) if len(row) > 8 and row[8] else 0.0,
                    "payment_method": row[9] if len(row) > 9 else "upfront_deposit",
                    "contract_number": row[10] if len(row) > 10 else "",
                    "invoice_number": row[11] if len(row) > 11 else "",
                    "created_at": row[12] if len(row) > 12 else "",
                    "notes": row[13] if len(row) > 13 else ""
                }
                
                # Only add if client_id exists
                if client["client_id"]:
                    clients.append(client)
                    logger.debug(f"Added client: {client['name']}")
            
            # Update cache
            self.client_cache = clients
            self.cache_timestamp = datetime.utcnow()
            
            logger.info(f"Retrieved {len(clients)} clients from sheet")
            return clients
        
        except HttpError as e:
            logger.error(f"HTTP error fetching clients: {e}")
            raise
        except Exception as e:
            logger.error(f"Error fetching clients: {e}")
            raise
    
    def get_max_contract_number(self) -> str:
        """Find the highest contract number in Clients sheet and increment by 1."""
        try:
            from datetime import datetime
            current_year = datetime.utcnow().year
            max_contract_num = 0
            
            # Read from Clients sheet (Column K - Contract Number, updated from J)
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.clients_sheet_id,
                range='K:K'
            ).execute()
            
            values = result.get('values', [])
            # Skip header row and extract contract numbers for current year
            for row in values[1:]:
                if row and row[0]:
                    contract = row[0]
                    if contract and isinstance(contract, str):
                        # Extract numeric part from CT-YYYY-### format
                        parts = contract.split('-')
                        if len(parts) >= 3:
                            try:
                                year = int(parts[1])
                                num = int(parts[2])
                                # Only count contracts from current year
                                if year == current_year:
                                    max_contract_num = max(max_contract_num, num)
                            except ValueError:
                                pass
            
            # Increment by 1 and format
            next_num = max_contract_num + 1
            new_contract = f"CT-{current_year}-{str(next_num).zfill(3)}"
            logger.info(f"Generated next contract number: {new_contract} (max found was: {max_contract_num})")
            return new_contract
        
        except Exception as e:
            logger.error(f"Error getting max contract number: {e}")
            # Return a default if there's any error
            from datetime import datetime
            current_year = datetime.utcnow().year
            return f"CT-{current_year}-001"
    
    def add_new_client(self, client_data: Dict[str, Any]) -> str:
        """Add a new client to the Clients sheet."""
        try:
            # Generate Client ID (using current timestamp-based unique ID)
            import uuid
            client_id = f"CL-{uuid.uuid4().hex[:8].upper()}"
            
            # Auto-generate Contract Number
            contract_number = self.get_max_contract_number()
            
            # Auto-generate Invoice Number (take largest from both sheets)
            invoice_number = self.get_max_invoice_number()
            
            # Prepare row data in correct column order (matching actual sheet structure):
            # A:Client ID, B:Name, C:Address, D:Contact, E:Email, F:Package, G:Start, H:End, I:Amount, J:Payment Method, K:Contract, L:Invoice, M:Created At, N:Notes
            row = [
                client_id,                              # A: Client ID
                client_data.get("name", ""),           # B: Name
                client_data.get("address", ""),        # C: Address
                client_data.get("contact", ""),        # D: Contact
                client_data.get("email", ""),          # E: Email
                client_data.get("package_type", ""),   # F: Package Type
                client_data.get("start_date", ""),     # G: Start Date
                client_data.get("end_date", ""),       # H: End Date
                str(client_data.get("amount_paid", 0)), # I: Amount Paid
                client_data.get("payment_method", "upfront_deposit"), # J: Payment Method
                contract_number,                        # K: Contract Number (auto-generated)
                invoice_number,                         # L: Invoice Number (auto-generated from max across both sheets)
                datetime.utcnow().isoformat(),         # M: Created At
                client_data.get("notes", "")           # N: Notes
            ]
            
            # Append to Clients sheet
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.clients_sheet_id,
                range='A:N',
                valueInputOption='USER_ENTERED',
                body={'values': [row]}
            ).execute()
            
            # Invalidate cache
            self.client_cache = {}
            self.cache_timestamp = None
            
            updates = result.get('updates', {})
            logger.info(f"New client added: {client_data.get('name')}")
            
            return result.get('updates', {}).get('updatedRange', '')
        
        except HttpError as e:
            logger.error(f"HTTP error adding client: {e}")
            raise
        except Exception as e:
            logger.error(f"Error adding client: {e}")
            raise
    
    def get_max_invoice_number(self) -> str:
        """Find the highest INVOICE NUMBER in Clients sheet (INV-5XXX format) and increment by 1."""
        try:
            import re
            max_invoice_num = 0
            
            # Read from Clients sheet (Column L - Invoice Number) to find max for INV-5XXX format
            clients_result = self.service.spreadsheets().values().get(
                spreadsheetId=self.clients_sheet_id,
                range='L:L'
            ).execute()
            
            clients_values = clients_result.get('values', [])
            logger.info(f"Checking Clients sheet for INV-5XXX invoices...")
            
            for row in clients_values[1:]:  # Skip header
                if row and row[0]:
                    invoice = row[0].strip()
                    if invoice and isinstance(invoice, str):
                        # Extract numeric part from INV-5XXX format
                        match = re.search(r'INV-5(\d+)', invoice, re.IGNORECASE)
                        if match:
                            try:
                                num = int(match.group(1))
                                max_invoice_num = max(max_invoice_num, num)
                                logger.debug(f"Clients: {invoice} → {num}")
                            except ValueError:
                                pass
            
            # Increment by 1 and format as INV-5XXX
            next_num = max_invoice_num + 1
            new_invoice = f"INV-5{str(next_num).zfill(3)}"
            logger.info(f"Generated next CLIENT invoice number: {new_invoice} (max found: {max_invoice_num})")
            return new_invoice
        
        except Exception as e:
            logger.error(f"Error getting max invoice number: {e}")
            # Return a default if there's any error
            return "INV-5001"
    
    def get_max_session_invoice_number(self) -> str:
        """Find the highest invoice number in Sessions sheet (INV-001 format) and increment by 1."""
        try:
            import re
            max_invoice_num = 0
            
            # Read from Sessions sheet (Column K - Invoice Number) for INV-001 format
            sessions_result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sessions_sheet_id,
                range='K:K'
            ).execute()
            
            sessions_values = sessions_result.get('values', [])
            logger.info(f"Checking Sessions sheet for INV-001 invoices...")
            
            for row in sessions_values[1:]:  # Skip header
                if row and row[0]:
                    invoice = row[0].strip()
                    if invoice and isinstance(invoice, str):
                        # Extract numeric part from both INV-### and INV-5### formats for backward compatibility
                        match = re.search(r'INV-?(\d+)', invoice, re.IGNORECASE)
                        if match:
                            try:
                                num = int(match.group(1))
                                # If it's in INV-5 format, extract just the number part
                                if num > 999:
                                    num = num % 1000
                                max_invoice_num = max(max_invoice_num, num)
                                logger.debug(f"Sessions: {invoice} → {num}")
                            except ValueError:
                                pass
            
            # Increment by 1 and format as INV-001
            next_num = max_invoice_num + 1
            new_invoice = f"INV-{str(next_num).zfill(3)}"
            logger.info(f"Generated next SESSION invoice number: {new_invoice} (max found: {max_invoice_num})")
            return new_invoice
        
        except Exception as e:
            logger.error(f"Error getting max session invoice number: {e}")
            # Return a default if there's any error
            return "INV-001"
    
    def add_session(self, session_data: Dict[str, Any]) -> str:
        """Add a coaching session to the Sessions sheet."""
        try:
            # Get client ID and contract number from selected client
            client_name = session_data.get("client_name", "")
            client = self.get_client_by_name(client_name)
            client_id = client.get("client_id", "") if client else ""
            contract_number = client.get("contract_number", "") if client else ""
            
            # Get total package amount from client
            total_package_amount = float(client.get("amount_paid", 0)) if client else 0.0
            payment_method = client.get("payment_method", "upfront_deposit") if client else "upfront_deposit"
            
            # Auto-generate invoice number for session (INV-001 format)
            invoice_number = self.get_max_session_invoice_number()
            
            # Calculate running balance
            # Get all existing sessions for this client to sum up what's been collected so far
            existing_sessions = self.get_client_history(client_name)
            total_collected_so_far = sum(float(s.get("amount_collected", 0)) for s in existing_sessions)
            
            # Add this session's amount
            amount_collected = float(session_data.get("amount_collected", 0))
            new_total_collected = total_collected_so_far + amount_collected
            
            # Calculate remaining balance based on payment method
            if payment_method == "pay_per_session":
                # For pay-per-session clients, show total collected (not negative balance)
                remaining_balance = 0  # Or could be new_total_collected to show cumulative
            else:
                # For upfront deposit clients, show remaining balance
                remaining_balance = total_package_amount - new_total_collected
            
            # Prepare row data matching actual sheet columns:
            # A:Client ID, B:Client Name, C:Coaching Type, D:Coaching Hours,
            # E:Amount Paid ($), F:Amount Collected, G:Amount Balance,
            # H:Session Date, I:Payment Method, J:Contract Number, K:Invoice Number, L:Created At, M:Notes
            row = [
                client_id,                              # A: Client ID
                session_data.get("client_name", ""),   # B: Client Name
                session_data.get("coaching_type", ""), # C: Coaching Type
                str(session_data.get("coaching_hours", 0)), # D: Coaching Hours
                str(total_package_amount),              # E: Amount Paid ($) - client's total package
                str(amount_collected),                  # F: Amount Collected - this session
                str(remaining_balance),                 # G: Amount Balance - remaining after this session
                session_data.get("session_date", ""),  # H: Session Date
                payment_method,                         # I: Payment Method
                contract_number,                        # J: Contract Number
                invoice_number,                         # K: Invoice Number
                datetime.utcnow().isoformat(),         # L: Created At
                session_data.get("notes", "")          # M: Notes
            ]
            
            # Append to Sessions sheet
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.sessions_sheet_id,
                range='A:M',
                valueInputOption='USER_ENTERED',
                body={'values': [row]}
            ).execute()
            
            logger.info(f"Session added for client: {client_name} with invoice: {invoice_number}")
            return result.get('updates', {}).get('updatedRange', '')
        
        except HttpError as e:
            logger.error(f"HTTP error adding session: {e}")
            raise
        except Exception as e:
            logger.error(f"Error adding session: {e}")
            raise
    
    def check_duplicate_client(self, name: str, email: str) -> Optional[Dict[str, Any]]:
        """Check if a client already exists by email only (emails must be unique)."""
        max_retries = 2
        retry_count = 0
        
        while retry_count <= max_retries:
            try:
                clients = self.get_all_clients()
                
                # Only check email for duplicates since emails should be globally unique
                # But allow multiple people with the same name
                for client in clients:
                    if client.get("email", "").lower() == email.lower():
                        logger.info(f"Found duplicate email: {email} (client: {client.get('name')})")
                        return client
                
                return None
            
            except Exception as e:
                retry_count += 1
                if retry_count > max_retries:
                    logger.error(f"Error checking duplicate client after {max_retries} retries: {e}")
                    raise
                else:
                    logger.warning(f"Retry {retry_count}/{max_retries} for duplicate check due to: {e}")
                    import time
                    time.sleep(0.5 * retry_count)  # Brief backoff
    
    def get_client_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a specific client by name."""
        try:
            clients = self.get_all_clients()
            
            for client in clients:
                if client.get("name", "").lower() == name.lower():
                    return client
            
            return None
        
        except Exception as e:
            logger.error(f"Error getting client by name: {e}")
            raise
    
    def get_client_history(self, client_name: str) -> List[Dict[str, Any]]:
        """Fetch all sessions for a specific client."""
        try:
            # Read from Sessions sheet
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sessions_sheet_id,
                range='A:M'
            ).execute()
            
            values = result.get('values', [])
            
            if not values:
                logger.warning(f"No session history found for client: {client_name}")
                return []
            
            # Parse header and data rows
            # Actual columns: A:Client ID, B:Client Name, C:Coaching Type, D:Coaching Hours,
            # E:Amount Paid ($), F:Amount Collected, G:Amount Balance,
            # H:Session Date, I:Payment Method, J:Contract Number, K:Invoice Number, L:Created At, M:Notes
            sessions = []
            
            for row in values[1:]:
                # Match by client name (column B, index 1)
                if len(row) >= 6 and row[1].lower() == client_name.lower():
                    session = {
                        "client_id": row[0],
                        "client_name": row[1],
                        "coaching_type": row[2],
                        "coaching_hours": float(row[3]) if row[3] else 0.0,
                        "amount_collected": float(row[5]) if len(row) > 5 and row[5] else 0.0,
                        "session_date": row[7] if len(row) > 7 else "",
                        "payment_method": row[8] if len(row) > 8 else "upfront_deposit",
                        "contract_number": row[9] if len(row) > 9 else "",
                        "invoice_number": row[10] if len(row) > 10 else "",
                        "created_at": row[11] if len(row) > 11 else "",
                        "notes": row[12] if len(row) > 12 else ""
                    }
                    sessions.append(session)
            
            logger.info(f"Retrieved {len(sessions)} sessions for client: {client_name}")
            return sessions
        
        except HttpError as e:
            logger.error(f"HTTP error fetching client history: {e}")
            raise
        except Exception as e:
            logger.error(f"Error fetching client history: {e}")
            raise
    
    def update_client_end_date(self, client_name: str, new_end_date: str) -> bool:
        """Update a client's end date."""
        try:
            clients = self.get_all_clients()
            
            # Find the row number
            for idx, client in enumerate(clients, start=2):  # Start at 2 (skip header)
                if client.get("name", "").lower() == client_name.lower():
                    # Update the end date (Column F in new structure)
                    self.service.spreadsheets().values().update(
                        spreadsheetId=self.clients_sheet_id,
                        range=f'F{idx}',
                        valueInputOption='USER_ENTERED',
                        body={'values': [[new_end_date]]}
                    ).execute()
                    
                    # Invalidate cache
                    self.client_cache = {}
                    self.cache_timestamp = None
                    
                    logger.info(f"Updated end date for client: {client_name}")
                    return True
            
            logger.warning(f"Client not found for update: {client_name}")
            return False
        
        except HttpError as e:
            logger.error(f"HTTP error updating client: {e}")
            raise
        except Exception as e:
            logger.error(f"Error updating client: {e}")
            raise
    
    def delete_rows(self, start_row: int, end_row: int) -> bool:
        """Delete rows from the Clients sheet (1-indexed)."""
        try:
            # Convert to 0-indexed for API
            start_index = start_row - 1
            end_index = end_row
            
            request = self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.clients_sheet_id,
                body={
                    'requests': [
                        {
                            'deleteDimension': {
                                'range': {
                                    'sheetId': 0,  # Sheet1 (Clients sheet)
                                    'dimension': 'ROWS',
                                    'startIndex': start_index,
                                    'endIndex': end_index
                                }
                            }
                        }
                    ]
                }
            ).execute()
            
            # Invalidate cache
            self.client_cache = {}
            self.cache_timestamp = None
            
            logger.info(f"Deleted rows {start_row}-{end_row} from sheet")
            return True
        
        except HttpError as e:
            logger.error(f"HTTP error deleting rows: {e}")
            raise
        except Exception as e:
            logger.error(f"Error deleting rows: {e}")
            raise
