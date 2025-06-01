from fastapi import APIRouter
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

@router.get("/")
def verifyToken():
    
    return {"IsValid":True}
