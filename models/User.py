from datetime import datetime,timezone
from typing import Optional
from pydantic import BaseModel
from enum import Enum

class RoleEnum(str, Enum):
    Organization = "Organization"
    Analyst = "Analyst"

class User(BaseModel):
    name: str
    email: str
    role: RoleEnum
    password: str
    date: Optional[datetime] = datetime.now(timezone.utc)