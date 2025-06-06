from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def createConnection():
    client = MongoClient(os.environ['mongo_uri'])
    db = client[os.environ['database']]
    return db

