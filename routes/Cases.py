from fastapi import APIRouter, Query,status,Body,UploadFile,File,Form,Path
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
from models.Case import Case, CaseStatus

load_dotenv()

# Models

# DB
from config.db import createConnection

router = APIRouter()
db = createConnection()



# Key API Endpoints:
# • GET /cases/ – List all cases - search/filter functionality (by date, location, violation type). ✅
# • POST /cases/ – Create a new case ✅
# • GET /cases/{case_id} – Retrieve a specific case ✅
# • PATCH /cases/{case_id} – Update case status ✅ TODO save to case_status_history
# • DELETE /cases/{case_id} – Archive a case 

# List all cases - search/filter functionality (by date, location (city), violation type).
@router.get("/")
def list_cases(
    caseStatus: Optional[CaseStatus] = Query(default=None),
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
    cases = list(db.cases.find(query))
    if not cases:
        return res(status_code=status.HTTP_404_NOT_FOUND, content="No cases found.")

    return res(status_code=status.HTTP_200_OK, content=json.dumps(cases, default=str)) 

# Retrieve a specific case 
@router.get("/{case_id}")
def get_case(case_id: str):
    case = db.cases.find_one({"case_id": case_id})

    if not case:
        return res(status_code=status.HTTP_404_NOT_FOUND, content="Case not found.")

    return res(status_code=status.HTTP_200_OK, content=str(case))


# Create a new case
@router.post("/")
def create_case(case: Case):
    # Validate the request body
    if not case.title or not case.description:
        return res(status_code=status.HTTP_400_BAD_REQUEST,content={"error": "Title and description are required."})

    # Insert the case into the database
    result = db.cases.insert_one(case.model_dump())

    return res(status_code=status.HTTP_201_CREATED, content="Case created successfully, with id: " + str(result.inserted_id))

# TODO save to case_status_history
# Update case status
@router.patch("/{case_id}")
def update_case_status(case_id: str, caseStatus: CaseStatus):
    # Validate the case ID
    if not db.cases.find_one({"case_id": case_id}):
        return res(status_code=status.HTTP_404_NOT_FOUND, content="Case not found.")

    # Update the case status
    result = db.cases.update_one({"case_id": case_id}, {"$set": {"status": caseStatus}})

    if result.modified_count == 0:
        return res(status_code=status.HTTP_400_BAD_REQUEST, content="Failed to update case status.")

    return res(status_code=status.HTTP_200_OK, content="Case status updated successfully.")

# TODO Save to Cases_Archive
# Archive a case 
# Delete case
@router.delete("/{case_id}")
def delete_case(case_id: str):
    # Validate the case ID
    if not db.cases.find_one({"case_id": case_id}):
        return res(status_code=status.HTTP_404_NOT_FOUND, content="Case not found.")

    # Delete the case
    result = db.cases.delete_one({"case_id": case_id})

    if result.deleted_count == 0:
        return res(status_code=status.HTTP_400_BAD_REQUEST, content="Failed to delete case.")

    return res(status_code=status.HTTP_200_OK, content="Case deleted successfully.")
