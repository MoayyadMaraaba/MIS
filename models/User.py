from datetime import datetime

from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    role: str
    password: str
    date: datetime    