from fastapi import Response,status, HTTPException
import json
import jwt
from dotenv import load_dotenv
import os

load_dotenv()

def res(content, status_code):
    return Response(content=json.dumps(content), status_code=status_code)

def get_secret_role(role:str):
    secret_key = ""
    
    if role == "Admin":
        secret_key = os.environ["admin_secret"]
    elif role == "Organization":
        secret_key = os.environ["organization_secret"]
    elif role == "Analyst":
        secret_key = os.environ['analyst_secret']
    
    return secret_key

def check_jwt(token: str, role: str):
    try:
        payload = jwt.decode(token, get_secret_role(role), algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
