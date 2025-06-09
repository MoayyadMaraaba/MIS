from bson import ObjectId
from fastapi import APIRouter, HTTPException,status,Body,UploadFile,File,Form,Path
import bcrypt
from pydantic import BaseModel, Field
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


class Demographics(BaseModel):
    gender: str
    age: int
    ethnicity: str
    occupation: str
    
    
class Contact_info(BaseModel):
    email: str
    phone: str
    secure_messaging: str

    
class Risk_assessment(BaseModel):
    level: str
    threats: List[str] 
    protection_needed: bool


class Support_service(BaseModel):
    type: str
    provider: str
    status: str


@router.post("/")
def add(type: str = Body(...), 
       anonymous: bool = Body(False), 
       demographics: Demographics = Body(...),
       contact_info: Optional[Contact_info] = Body(None),
       cases_involved: List[str] = Body(...),
       risk_assessment: Risk_assessment = Body(...),
       support_services: List[Support_service] = Body(...),
       ):
        

    
    new_person = {
        "type": type,
        "anonymous": anonymous,
        "demographics": demographics.model_dump(),
        "contact_info": contact_info.model_dump() if contact_info else None,
        "cases_involved": cases_involved,
        "risk_assessment": risk_assessment.model_dump(),
        "support_services": [service.model_dump() for service in support_services], 
        "created_at": datetime.now(timezone.utc),
        "updated_at":  datetime.now(timezone.utc)
    }
    
    db = createConnection()
    persons = db['victims']
    
    inserted_id = persons.insert_one(new_person).inserted_id

    return {"result": str(inserted_id)}

   
@router.get("/{victim_id}")
def getPerson(victim_id: str = Path(...)):

        db = createConnection()
        persons = db['victims']
        
        try:
            object_id = ObjectId(victim_id)
        except Exception:
            return res({"error": "Invalid victim_id"}, 400)
       
        result = persons.find_one({"_id": object_id})
             
        if result == None:
            return res({"error": "person not found"}, 404)
        
        result['_id'] = str(result['_id'])
   
        return {"person": result}   


class Risk_level_update(BaseModel):
    level: str

@router.patch("/{victim_id}")
def update_risk_level(victim_id: str = Path(...),  risk_level_update: Risk_level_update = Body(...)):
    
    db = createConnection()
    persons = db['victims']
    
    try:
        object_id = ObjectId(victim_id)
    except Exception:
        return res({"error": "Invalid victim_id"}, 400)
    
    result = persons.update_one({"_id": object_id}, {"$set": {"risk_assessment.level": risk_level_update.level}})
    
    if result.matched_count == 0 :
         return res({"error": "person not exist"}, 404)
       
    return res({"message": "risk level updated"}, 200)

@router.get("/case/{case_id}")
def get_cases(case_id: str = Path(...)):
    
    db = createConnection()
    persons = db['victims']

    listofPersons = list(persons.find({"cases_involved":case_id}))

    for person in listofPersons:
        person["_id"] = str(person["_id"])
    
    if len(listofPersons) == 0:
            return res({"error": "there is no victims for this case"}, 404)
            
    return {"List victims": listofPersons}


@router.get("/")
def get_Victims():
    
    db = createConnection()
    persons = db['victims']

    Victims = list(persons.find({}))

    for person in Victims:
        person["_id"] = str(person["_id"])
    
    if len(Victims) == 0:
            return res({"error": "there is no victims for this case"}, 404)
            
    return {"List victims": Victims}