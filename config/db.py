from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def createConnection():
    client = MongoClient("mongodb://localhost:27017/")
    db = client[os.environ['database']]
    return db

