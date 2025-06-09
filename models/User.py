from datetime import datetime,timezone
from typing import Optional
from pydantic import BaseModel,Field
from enum import Enum

class RoleEnum(str, Enum):
    Organization = "Organization"
    Analyst = "Analyst"

class User(BaseModel):
    id: str = Field(alias="_id")
    Name: str
    Email: str
    Role: RoleEnum
    Password: str
    Activation: bool
    date: Optional[datetime] = datetime.now(timezone.utc)