
from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from models.Incident import location
from models.Incident import evidence


# Enum for case status.
class CaseStatus(str, Enum):
    """
    Enum for case status.
    """
    NEW = "new"
    UNDER_INVESTIGATION = "under_investigation"
    RESOLVED = "resolved"
    ARCHIVED = "archived"


# Enum for case priority.
class Priority(str, Enum):
    """Enum for case priority.
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"   

# A perpetrator in the system.
class Perpetrator(BaseModel):
    name:str
    type:str

class Case(BaseModel):
    """
    Represents a case in the system.
    """
    case_id: str # Unique identifier for the case
    title: str # Title of the case
    description: str = ""  # Default description is an empty string
    violation_types: list[str]  # List of violation types
    status: CaseStatus  # Using the CaseStatus Enum
    priority: Priority  # Using the Priority Enum
    location: location # Location of the incident
    date_occurred: datetime  # Date when the incident occurred
    date_reported: datetime # Date when the case was reported
    victims: list[str]  # List of victim IDs
    evidence: list[evidence] # List of evidence items
    perpetrators: list[Perpetrator]  # List of perpetrator IDs
    created_by: str  # ID of the user who created the case
    created_at: datetime = datetime.now() # Timestamp when the case was created
    updated_at: datetime = datetime.now() # Timestamp when the case was last updated

