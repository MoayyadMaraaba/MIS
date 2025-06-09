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

@router.get("/violations")
def count_violations_by_type():
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

@router.get("/geodata")
def get_geodata():
    db = createConnection()
    reports = db['incident_reports']
    
    geodata = list(reports.find({}, {
        "_id": 0,
        "incident_details.location.city": 1,
        "incident_details.location.country": 1,
        "incident_details.location.coordinates": 1,
        "incident_details.violation_types": 1,
        "incident_details.date": 1
    }))
    
    return {"geodata": geodata}


@router.get("/timeline")
def get_cases_over_time(start: str = Query(None), end: str = Query(None)):
    db = createConnection()
    reports = db['incident_reports']
    
    match = {}

    if start or end:
        match["incident_details.date"] = {}
        if start:
            match["incident_details.date"]["$gte"] = datetime.fromisoformat(start)
        if end:
            match["incident_details.date"]["$lte"] = datetime.fromisoformat(end)
            
    pipeline = [
        { "$match": match },
        {
            "$addFields": {
                "incidentDate": { "$toDate": "$incident_details.date" }
            }
        },
        {
            "$group": {
                "_id": {
                    "date": {
                        "$dateToString": { "format": "%Y-%m-%d", "date": "$incidentDate" }
                    }
                },
                "count": { "$sum": 1 }
            }
        },
        { "$sort": { "_id.date": 1 } }
    ]
    
    timeline_data = list(reports.aggregate(pipeline))
    return {
        "timeline": [
            {"date": item["_id"]["date"], "count": item["count"]}
            for item in timeline_data
        ]
    }




