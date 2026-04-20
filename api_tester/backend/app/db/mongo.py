# app/db/mongo.py
from pymongo import MongoClient
from api_tester.backend.app.config import MONGODB_URI, MONGODB_DBNAME


client = MongoClient(MONGODB_URI)
db = client[MONGODB_DBNAME]
