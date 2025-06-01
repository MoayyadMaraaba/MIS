from fastapi import APIRouter

# Models
from models.User import User

# DB
from config.db import createConnection

router = APIRouter()

@router.post("/Register")
def createAccount():
    db = createConnection()
    
    return {"Collections": ""}