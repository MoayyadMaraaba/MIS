from fastapi import APIRouter,status,Body
import bcrypt
from utils.helpers import res
from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv
import os

load_dotenv()

# Models
from models.User import User

# DB
from config.db import createConnection

router = APIRouter()

@router.post("/Register")
async def createAccount(user: User):
    db = createConnection()
    users = db['Users']
    
    # Check for existing email
    if users.find_one({"Email": user.email}):
        return res({"Error": "Email already exists"}, status.HTTP_400_BAD_REQUEST)
    
    # hashing the password
    hashed = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
    
    # Create a document for mongo database
    new_user = {
        "Name": user.name,
        "Email": user.email,
        "Role": user.role,
        "Password": hashed,
        "Activation": False,
        "Date": user.date
    }
    
    # insert to database
    users.insert_one(new_user)
    
    return res({"Message": "User created successfully"}, status.HTTP_201_CREATED)

def create_jwt(data:dict, expires_in_minutes,role):
    payload = data.copy()

    # Add expiration time
    expire = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
    payload.update({"exp": expire})
    
    # select a secret key based on role
    secret_key = ""
    if role == "Admin":
        secret_key = os.environ['admin_secret']
    elif role == "Organization":
        secret_key = os.environ['organization_secret']
    elif role == "Analyst":
        secret_key = os.environ['analyst_secret']

    # generate the jwt
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token

@router.post("/Login")
async def login(email:str = Body(...), password:str = Body(...)):
    db = createConnection()
    users = db['Users']
    
    # find the user using email
    user = users.find_one({"Email": email})
    
    # if the user is none that means the user is not registered
    if user is None:
        return res({"Error": "User Not Found"}, status.HTTP_400_BAD_REQUEST)

    # if the user is found then compare the password with hashed password
    if bcrypt.checkpw(password.encode(), user['Password'].encode()) and user['Activation'] == True:
        payload = {"userId": str(user['_id']),"role": user['Role']}
        token = create_jwt(payload, 120, user['Role'])
                
        return res({"Message": "User LoggedIn", "Token": token, "Role": user['Role']}, status.HTTP_200_OK)
    
    # the password is wrong
    return res({"Error": "Wrong credentials"}, status.HTTP_400_BAD_REQUEST)
