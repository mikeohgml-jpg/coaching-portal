"""Pydantic data models for Coaching Portal."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, validator


class NewClientFormData(BaseModel):
    """Data model for new client registration form."""
    
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    package_type: str = Field(..., description="Type of coaching package")
    start_date: str = Field(..., description="YYYY-MM-DD format")
    end_date: str = Field(..., description="YYYY-MM-DD format")
    amount_paid: float = Field(..., gt=0)
    notes: Optional[str] = None
    
    @validator("start_date", "end_date")
    def validate_date_format(cls, v):
        """Validate date format is YYYY-MM-DD."""
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
    
    @validator("end_date")
    def end_date_after_start(cls, v, values):
        """Validate end date is after start date."""
        if "start_date" in values:
            start = datetime.strptime(values["start_date"], "%Y-%m-%d")
            end = datetime.strptime(v, "%Y-%m-%d")
            if end <= start:
                raise ValueError("End date must be after start date")
        return v
    
    model_config = {"json_schema_extra": {
        "example": {
            "name": "John Doe",
            "email": "john@example.com",
            "package_type": "Standard",
            "start_date": "2024-01-01",
            "end_date": "2024-03-31",
            "amount_paid": 1500.00,
            "notes": "Interested in leadership coaching"
        }
    }}


class ExistingClientFormData(BaseModel):
    """Data model for existing client session form."""
    
    client_name: str = Field(..., min_length=1, max_length=255)
    coaching_type: str = Field(..., description="Type of coaching session")
    participant_count: int = Field(..., gt=0)
    coaching_hours: float = Field(..., gt=0)
    amount_collected: float = Field(..., ge=0)
    session_date: str = Field(..., description="YYYY-MM-DD format")
    notes: Optional[str] = None
    new_end_date: Optional[str] = None
    
    @validator("session_date", "new_end_date")
    def validate_date_format(cls, v):
        """Validate date format is YYYY-MM-DD if provided."""
        if v is not None:
            try:
                datetime.strptime(v, "%Y-%m-%d")
                return v
            except ValueError:
                raise ValueError("Date must be in YYYY-MM-DD format")
        return v
    
    model_config = {"json_schema_extra": {
        "example": {
            "client_name": "Jane Smith",
            "coaching_type": "One-on-One",
            "participant_count": 1,
            "coaching_hours": 2.0,
            "amount_collected": 300.00,
            "session_date": "2024-02-06",
            "notes": "Focused on strategic planning",
            "new_end_date": None
        }
    }}


class ClientRecord(BaseModel):
    """Data model representing a client record from sheets."""
    
    id: Optional[str] = None
    name: str
    email: EmailStr
    package_type: str
    start_date: str
    end_date: str
    amount_paid: float
    created_at: str
    notes: Optional[str] = None
    
    model_config = {"json_schema_extra": {
        "example": {
            "id": "row_123",
            "name": "John Doe",
            "email": "john@example.com",
            "package_type": "Standard",
            "start_date": "2024-01-01",
            "end_date": "2024-03-31",
            "amount_paid": 1500.00,
            "created_at": "2024-01-01T10:00:00Z",
            "notes": "Leadership coaching"
        }
    }}


class SessionRecord(BaseModel):
    """Data model representing a coaching session record."""
    
    id: Optional[str] = None
    client_id: str
    client_name: str
    coaching_type: str
    participant_count: int
    coaching_hours: float
    amount_collected: float
    session_date: str
    created_at: str
    notes: Optional[str] = None
    
    model_config = {"json_schema_extra": {
        "example": {
            "id": "row_456",
            "client_id": "row_123",
            "client_name": "John Doe",
            "coaching_type": "One-on-One",
            "participant_count": 1,
            "coaching_hours": 2.0,
            "amount_collected": 300.00,
            "session_date": "2024-02-06",
            "created_at": "2024-02-06T10:00:00Z",
            "notes": "Strategic planning session"
        }
    }}


class EmailContent(BaseModel):
    """Data model for email content."""
    
    recipient_email: EmailStr
    subject: str
    body: str
    html_body: Optional[str] = None
    
    model_config = {"json_schema_extra": {
        "example": {
            "recipient_email": "client@example.com",
            "subject": "Welcome to Coaching Program",
            "body": "Welcome to your coaching program...",
            "html_body": "<html><body>Welcome to your coaching program...</body></html>"
        }
    }}


class ClientListItem(BaseModel):
    """Simplified client for dropdown lists."""
    
    name: str
    email: str
    package_type: str
    active: bool = True
    
    model_config = {"json_schema_extra": {
        "example": {
            "name": "John Doe",
            "email": "john@example.com",
            "package_type": "Standard",
            "active": True
        }
    }}
