from datetime import datetime,timezone
from typing import Optional,List
from pydantic import BaseModel,Field
from enum import Enum

class ContactInfo(BaseModel):
    email: str
    phone: str
    preferred_contact: str

class coor(BaseModel):
    type: str
    coordinates: List[float]

class location(BaseModel):
    country: str
    city: str
    coordinates: coor

class Incident_details(BaseModel):
    date: datetime
    location: location
    description: str
    violation_types: List[str]

class evidence(BaseModel):
    type: str
    url: str
    description: str
    date_captured: Optional[datetime] = datetime.now(timezone.utc)
    
    
class Incident(BaseModel):
    id: str = Field(alias="_id")
    report_id: str
    reporter_type: str
    anonymous: bool
    contact_info: Optional[ContactInfo]
    incident_details: Incident_details
    evidence: Optional[List[evidence]]
    status: str
    created_at: datetime = datetime.now(timezone.utc)