from fastapi import APIRouter,status,Body,UploadFile,File,Form,Path
import bcrypt
from utils.helpers import res
from datetime import datetime, timedelta, timezone
import jwt
from dotenv import load_dotenv
import os
from typing import List,Optional
from random import randint
import shutil
import json

load_dotenv()

# Models

# DB
from config.db import createConnection

router = APIRouter()


@router.get("/")
def get():
    return {"Hello": "World"}
    
