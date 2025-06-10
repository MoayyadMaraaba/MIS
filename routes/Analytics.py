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
import csv
import io
from fastapi.responses import StreamingResponse

load_dotenv()

# DB
from config.db import createConnection

router = APIRouter()

@router.get("/violations")
def count_violations_by_type(start: str = Query(None), end: str = Query(None)):
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
        {"$match": match},
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
def get_geodata(start: str = Query(None), end: str = Query(None)):
    db = createConnection()
    reports = db['incident_reports']
    
    match = {}

    if start or end:
        match["incident_details.date"] = {}
        if start:
            match["incident_details.date"]["$gte"] = datetime.fromisoformat(start)
        if end:
            match["incident_details.date"]["$lte"] = datetime.fromisoformat(end)
    
    geodata = list(reports.find(match, {
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
    
@router.get("/export")
def export_incidents_csv(start: str = Query(None), end: str = Query(None)):
    db = createConnection()
    reports = db['incident_reports']

    match = {}

    if start or end:
        match["incident_details.date"] = {}
        if start:
            match["incident_details.date"]["$gte"] = datetime.fromisoformat(start)
        if end:
            match["incident_details.date"]["$lte"] = datetime.fromisoformat(end)

    incidents = list(reports.find(match, {"_id": 0}))  # Exclude MongoDB _id

    def generate_csv():
        output = io.StringIO()
        if not incidents:
            return output.getvalue()
        
        writer = csv.DictWriter(output, fieldnames=['report_id', 'reporter_type', 'anonymous', 'date', 'country', 'city', 'email', 'phone', 'status', 'created_at'])
        writer.writeheader()
        for row in incidents:
                writer.writerow({
                    "report_id": row.get("report_id", ""),
                    "reporter_type": row.get("reporter_type", ""),
                    "anonymous": row.get("anonymous", ""),
                    "date": row.get("incident_details", {}).get("date", ""),
                    "country": row.get("incident_details", {}).get("location", {}).get("country", ""),
                    "city": row.get("incident_details", {}).get("location", {}).get("city", ""),
                    "email": row.get("contact_info", {}).get("email", ""),
                    "phone": row.get("contact_info", {}).get("phone", ""),
                    "status": row.get("status", ""),
                    "created_at": row.get("created_at", ""),
                })
        output.seek(0)
        return output.getvalue()

    csv_data = generate_csv()
    response = StreamingResponse(iter([csv_data]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=incidents.csv"
    return response


