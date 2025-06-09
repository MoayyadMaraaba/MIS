from fastapi import APIRouter,status,Body, Path
import bcrypt
from utils.helpers import res
from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv
import os
from bson import ObjectId
import json

load_dotenv()

# Models
from models.User import User

# DB
from config.db import createConnection

router = APIRouter()

def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
    return doc

@router.get("/Count")
def get_counts():
    db = createConnection()
    cases = db['cases']
    reports = db['incident_reports']
    reports_evidences = db['report_evidence']
    users = db['Users']
    victims = db['victims']
    
    cases_count = cases.count_documents({})
    incidents_count = reports.count_documents({})
    evidences_count = reports_evidences.count_documents({})
    orgs_count = users.count_documents({"Role": "Organization"})
    analysts_count = users.count_documents({"Role": "Analyst"})
    victims_count = victims.count_documents({})
    
    return {"Cases": cases_count, "Incidents": incidents_count, "Evidences": evidences_count, "Orgs": orgs_count, "Analysts": analysts_count, "Victims": victims_count}

@router.get("/Users")
def get_users():
    db = createConnection()
    users = db['Users']
    
    result = users.find({"$or":[ {"Role":"Organization"}, {"Role":"Analyst"}]})

    list_of_users = [User.model_validate(serialize_doc(doc)) for doc in result]

    return {"Users": list_of_users}

@router.patch("/User/Activate/{user_id}")
def activate_user(user_id: str = Path(...), Activation: str = Body(...)): 
    db = createConnection()
    users = db['Users']
    
    try:
        object_id = ObjectId(user_id)
    except Exception:
        return res({"error": "Invalid report_id"}, 400)

    value = False
    
    if json.loads(Activation) == "1":
        print("Its worked")
        value = True
    
    result = users.update_one({"_id": object_id}, {"$set": {"Activation": value}})

    return {"Message": "User updated successfully"}

@router.get("/Victims")
def get_victims():
    db = createConnection()
    victims = db['victims']
    
    listofPersons = list(victims.find({}, {"_id": 1, "contact_info": 1}))

    for person in listofPersons:
        person["_id"] = str(person["_id"])
    
    return {"Victims": listofPersons}
    

