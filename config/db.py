import certifi
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def createConnection():
    # client = MongoClient(os.environ['mongo_uri'])
    client = MongoClient(os.environ['mongo_uri'], tlsCAFile=certifi.where()) # Use certifi to provide the CA certificates

    db = client[os.environ['database']]
    return db

