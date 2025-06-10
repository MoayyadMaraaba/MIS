from fastapi import APIRouter,status,Body,UploadFile,File,Form,Path,Query
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
from models.Incident import Incident
from models.Incident import ContactInfo
from models.Incident import location
from models.Incident import Incident_details

# DB
from config.db import createConnection

router = APIRouter()

UPLOAD_DIR = "uploads/evidence"
os.makedirs(UPLOAD_DIR, exist_ok=True)

from bson import ObjectId

def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
    return doc
    

@router.get("/")
def get(status: Optional[str], country: Optional[str], city: Optional[str], date: Optional[str]):
    db = createConnection()
    reports = db['incident_reports']
    search_query = {}
    
    if status:
        search_query['status'] = status
        
    if country:
        search_query['incident_details.location.country'] = country
    
    if city:
        search_query['incident_details.location.city'] = city
    
    if date:
        search_query['incident_details.date'] = date
    
    result = reports.find(search_query)
    incidents = [Incident.model_validate(serialize_doc(doc)) for doc in result]

    return {"incidents": incidents}

@router.get("/search")
def search(search_query: str):
    db = createConnection()
    reports = db['incident_reports']
    
    result = reports.find({"report_id": {"$regex": search_query, "$options": "i"}})
    incidents = [Incident.model_validate(serialize_doc(doc)) for doc in result]

    return {"incidents": incidents}

@router.get("/Count")
def get_count():
    db = createConnection()
    reports = db['incident_reports']
    reports_evidences = db['report_evidence']
    victims = db['victims']

    incidents_count = reports.count_documents({})
    evidences_count = reports_evidences.count_documents({})
    victims_count = victims.count_documents({})
    
    
    return {"Incidents": incidents_count, "Evidences": evidences_count, "Victims": victims_count}

@router.post("/")
def add(reporter_type: str = Form(...), 
       anonymous: bool = Form(...), 
       contact_info: Optional[str] = Form(...),
       incident_details: str = Form(...),
       Evidences: Optional[List[UploadFile]] = File(...), 
       Descriptions: Optional[List[str]] = Form(...)
       ):
    
    db = createConnection()
    reports = db['incident_reports']
    reports_evidences = db['report_evidence']
    
    contact = None
    if contact_info:
        # Contact Inforamtion
        parsed_contact = json.loads(contact_info)
        contact = ContactInfo(**parsed_contact)
    
    # Incident Details
    parsed_incident = json.loads(incident_details)
    incident = Incident_details(**parsed_incident)
    
    evidences = []
    names = []
    
    report_id = f"IR-{datetime.now().year}-{randint(1,10000)}"
    
    new_report = {
        "report_id": report_id,
        "reporter_type": reporter_type,
        "anonymous": anonymous,
        "incident_details": incident.model_dump(),
        "status": "New",
        "created_at": datetime.now(timezone.utc)
    }
    
    if contact is not None:
        new_report['contact_info'] = contact.model_dump()
        
    
    number = 0
    
    if Evidences is not None and Descriptions is not None:
        for ev in Evidences:
            if ev.content_type and ev.filename:
                filename = f"IR-Evidence-{number}-{randint(0,10000)}{os.path.splitext(ev.filename)[1]}"
                names.append(filename)  
                evidence = {"type": ev.content_type.split("/")[0], "url": f"/uploads/evidence/{filename}", "description": Descriptions[number] }
                evidences.append(evidence)
            number += 1
    
    new_report['evidence'] = evidences
    
    insertedID = reports.insert_one(new_report).inserted_id
    
    if Evidences is not None and Descriptions is not None:            
        number = 0
        for file in Evidences:
            file_path = os.path.join(UPLOAD_DIR, names[number]) # type: ignore
            
            e = evidences[number]
            e['report_id'] = insertedID
            reports_evidences.insert_one(e)
            number += 1
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            

    
    return {"result": str(insertedID)}

@router.patch("/{report_id}")
def update_status(report_id: str = Path(...), status: str = Body(...)):
    db = createConnection()
    reports = db['incident_reports']
    
    try:
        object_id = ObjectId(report_id)
    except Exception:
        return res({"error": "Invalid report_id"}, 400)

    result = reports.update_one({"_id": object_id}, {"$set": {"status": status}})
    
    if result.matched_count == 0:
        return res({"error": "Report not found"}, 404)

    return res({"message": "Status updated"}, 200)

@router.get("/analytics")
def get_analytics():
    db = createConnection()
    reports = db['incident_reports']
    
    pipeline = [
        {"$unwind": "$incident_details.violation_types"},
        {"$group": {
            "_id": "$incident_details.violation_types",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}}
    ]
    
    result = list(reports.aggregate(pipeline))
    
    return {"Violations": result}
    
