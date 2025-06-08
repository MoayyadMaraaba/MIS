
from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from models.Incident import location
from models.Incident import evidence

class CaseStatus(str, Enum):
    """
    Enum for case status.
    """
    NEW = "new"
    UNDER_INVESTIGATION = "under_investigation"
    RESOLVED = "resolved"
    ARCHIVED = "archived"

class Priority(str, Enum):
    """Enum for case priority.
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"   
class Perpetrator(BaseModel):
    name:str
    type:str

class Case(BaseModel):
    """
    Represents a case in the system.
    """
    case_id: str
    title: str
    description: str = ""  # Default description is an empty string
    violation_types: list[str]  # List of violation types
    status: CaseStatus  # Using the CaseStatus Enum
    priority: Priority  # Using the Priority Enum
    location: location
    victims: list[str]  # List of victim IDs
    evidence: list[evidence]
    perpetrators: list[Perpetrator]  # List of perpetrator IDs

    created_by: str  # ID of the user who created the case
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

