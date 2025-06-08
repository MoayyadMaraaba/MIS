from fastapi import APIRouter,Header,HTTPException
from dotenv import load_dotenv
import os
import jwt

from utils.helpers import check_jwt

load_dotenv()

router = APIRouter()

@router.get("/verify")
def verifyToken(role: str, authorization: str = Header(...)):
    token = authorization.split(" ")[1]
    
    return check_jwt(token, role)



