from fastapi import APIRouter, Query,status,Body,UploadFile,File,Form,Path,Header
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
import utils.helpers as helpers
from bson import ObjectId

load_dotenv()

# Models
from models.Case import Case, CaseStatus

# DB
from config.db import createConnection

router = APIRouter()
db = createConnection()

def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
    return doc

def serialize_doc1(doc):
    def fix_value(v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, datetime):
            return v.isoformat()
        return v

    return {k: fix_value(v) for k, v in doc.items()}

# Key API Endpoints:
# • GET /cases/ – List all cases - search/filter functionality (by date, location, violation type). ✅
# • POST /cases/ – Create a new case ✅
# • GET /cases/{case_id} – Retrieve a specific case ✅
# • PATCH /cases/{case_id} – Update case status + save to case_status_history ✅ 
# • DELETE /cases/{case_id} – Archive a case + Save to Cases_Archive ✅

# List all cases - search/filter functionality (by date, location (city), violation type).
@router.get("/")
def list_cases(
    caseStatus: Optional[str] = Query(default=None),
    priority: Optional[str] = Query(default=None),
    country: Optional[str] = Query(default=None),
    violation_type: Optional[str] = Query(default=None)
):
    query = {}
    if caseStatus:
        query["status"] = caseStatus
    if priority:
        query["priority"] = priority
    if country:
        query["location.country"] = country
    if violation_type:
        query["violation_types"] = violation_type
    
    cases = list(db.cases.find(query, {"_id":0}))
    if not cases:
        return res(status_code=status.HTTP_404_NOT_FOUND, content="No cases found.")

    ca = [Case.model_validate(serialize_doc(doc)) for doc in cases]
    return {"Cases": ca}

# Retrieve a specific case 
@router.get("/{case_id}")
def get_case(case_id: str):
    case = db.cases.find_one({"case_id": case_id})

    if not case:
        return res(status_code=status.HTTP_404_NOT_FOUND, content="Case not found.")

    return res(status_code=status.HTTP_200_OK, content=str(case))

@router.get("/history/{case_id}")
def get_history(case_id: str = Path(...)):
    records = list(
        db.case_status_history
        .find({"case_id": case_id})
        .sort("updated_at", -1)
    )

    # Serialize records before returning
    history_records = [serialize_doc1(doc) for doc in records]
    return {"History": history_records}    
     

# Create a new case
@router.post("/")
def create_case(case: Case = Body(...)):

    # Insert the case into the database
    result = db.cases.insert_one(case.model_dump())
    
    for victim in case.victims:
        db.victims.update_one({"_id": ObjectId(victim)}, {"$push": {"cases_involved": str(result.inserted_id)}})
        
    return res(status_code=status.HTTP_201_CREATED, content="Case created successfully, with id: " + str(result.inserted_id))

# Update case status
@router.patch("/{case_id}")
def update_case_status(case_id: str = Path(...), caseStatus: CaseStatus = Body(...), authorization: str = Header(...)):
    
    # Validate the case ID
    if not db.cases.find_one({"case_id": case_id}):
        return res(status_code=status.HTTP_404_NOT_FOUND, content="Case not found.")
    
    # Update the case status
    result = db.cases.update_one({"case_id": case_id}, {"$set": {"status": caseStatus}})
    
    # Get the token from the authorization header
    token = authorization.split(" ")[1]
    # Get the payload from the JWT token 
    # Admin is the only role that can update case status
    payload = helpers.check_jwt(token, "Admin")
    
    # Add status update to case_status_history
    result_history = db.case_status_history.insert_one({
        "case_id": case_id,
        "status": caseStatus,
        "updated_at": datetime.now(timezone.utc),
        "updated_by": ObjectId(payload["userId"])
    })
    
    if result.modified_count == 0:
        return res(status_code=status.HTTP_400_BAD_REQUEST, content="Failed to update case status.")
    if result_history.inserted_id is None:
        return res(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Failed to save case status history.")
        
    return res(status_code=status.HTTP_200_OK, content="Case status updated successfully.")

# Archive a case 
# Delete case
@router.delete("/{case_id}")
def delete_case(case_id: str = Path(...), authorization: str = Header(...)):

    # Validate the case ID
    case = db.cases.find_one({"case_id": case_id})
    if not case:
        return res(status_code=status.HTTP_404_NOT_FOUND, content="Case not found.")
    
    token = authorization.split(" ")[1]
    payload = helpers.check_jwt(token, "Admin")
    
    # Archive the case
    db.case_archive.insert_one({
        "case_id": case["case_id"],
        "title": case["title"],
        "description": case["description"],
        "violation_types": case["violation_types"],
        "status": case["status"],
        "priority": case["priority"],
        "location": case["location"],
        "date_occurred": case["date_occurred"],
        "date_reported": case["date_reported"],
        "victims": case["victims"],
        "evidence": case["evidence"],
        "perpetrators": case["perpetrators"],
        "created_by": case["created_by"],
        "created_at": case["created_at"],
        "updated_at": case["updated_at"],
        "archived_at": datetime.now(timezone.utc),
        # Get userId from the JWT token
        "archived_by":ObjectId(payload["userId"])})
    
    # Delete the case
    result = db.cases.delete_one({"case_id": case_id})

    if result.deleted_count == 0:
        return res(status_code=status.HTTP_400_BAD_REQUEST, content="Failed to delete case.")

    return res(status_code=status.HTTP_200_OK, content="Case deleted successfully.")
