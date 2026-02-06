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
        self.sheets_id = Config.GOOGLE_SHEETS_ID
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
        credentials_path = Config.GOOGLE_CREDENTIALS_JSON
        
        if not credentials_path:
            raise ValueError("GOOGLE_CREDENTIALS_JSON not configured")
        
        if not os.path.exists(credentials_path):
            raise FileNotFoundError(f"Credentials file not found: {credentials_path}")
        
        # Load service account credentials
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=[
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
        )
        
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
                spreadsheetId=self.sheets_id,
                range='Clients!A:H'
            ).execute()
            
            values = result.get('values', [])
            
            if not values:
                logger.warning("No clients found in sheet")
                return []
            
            # Parse header and data rows
            header = values[0] if values else []
            clients = []
            
            for row in values[1:]:
                if len(row) >= 8:
                    client = {
                        "name": row[0],
                        "email": row[1],
                        "package_type": row[2],
                        "start_date": row[3],
                        "end_date": row[4],
                        "amount_paid": float(row[5]) if row[5] else 0.0,
                        "created_at": row[6],
                        "notes": row[7] if len(row) > 7 else ""
                    }
                    clients.append(client)
            
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
    
    def add_new_client(self, client_data: Dict[str, Any]) -> str:
        """Add a new client to the Clients sheet."""
        try:
            # Prepare row data
            row = [
                client_data.get("name", ""),
                client_data.get("email", ""),
                client_data.get("package_type", ""),
                client_data.get("start_date", ""),
                client_data.get("end_date", ""),
                str(client_data.get("amount_paid", 0)),
                datetime.utcnow().isoformat(),
                client_data.get("notes", "")
            ]
            
            # Append to Clients sheet
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.sheets_id,
                range='Clients!A:H',
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
    
    def add_session(self, session_data: Dict[str, Any]) -> str:
        """Add a coaching session to the Sessions sheet."""
        try:
            # Prepare row data
            row = [
                session_data.get("client_name", ""),
                session_data.get("coaching_type", ""),
                str(session_data.get("participant_count", 1)),
                str(session_data.get("coaching_hours", 0)),
                str(session_data.get("amount_collected", 0)),
                session_data.get("session_date", ""),
                datetime.utcnow().isoformat(),
                session_data.get("notes", "")
            ]
            
            # Append to Sessions sheet
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.sheets_id,
                range='Sessions!A:H',
                valueInputOption='USER_ENTERED',
                body={'values': [row]}
            ).execute()
            
            logger.info(f"Session added for client: {session_data.get('client_name')}")
            return result.get('updates', {}).get('updatedRange', '')
        
        except HttpError as e:
            logger.error(f"HTTP error adding session: {e}")
            raise
        except Exception as e:
            logger.error(f"Error adding session: {e}")
            raise
    
    def check_duplicate_client(self, name: str, email: str) -> Optional[Dict[str, Any]]:
        """Check if a client already exists by name or email."""
        try:
            clients = self.get_all_clients()
            
            for client in clients:
                if (client.get("name", "").lower() == name.lower() or 
                    client.get("email", "").lower() == email.lower()):
                    return client
            
            return None
        
        except Exception as e:
            logger.error(f"Error checking duplicate client: {e}")
            raise
    
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
                spreadsheetId=self.sheets_id,
                range='Sessions!A:H'
            ).execute()
            
            values = result.get('values', [])
            
            if not values:
                logger.warning(f"No session history found for client: {client_name}")
                return []
            
            # Parse header and data rows
            sessions = []
            
            for row in values[1:]:
                if len(row) >= 8 and row[0].lower() == client_name.lower():
                    session = {
                        "client_name": row[0],
                        "coaching_type": row[1],
                        "participant_count": int(row[2]) if row[2] else 1,
                        "coaching_hours": float(row[3]) if row[3] else 0.0,
                        "amount_collected": float(row[4]) if row[4] else 0.0,
                        "session_date": row[5],
                        "created_at": row[6],
                        "notes": row[7] if len(row) > 7 else ""
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
                    # Update the end date
                    self.service.spreadsheets().values().update(
                        spreadsheetId=self.sheets_id,
                        range=f'Clients!E{idx}',
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
