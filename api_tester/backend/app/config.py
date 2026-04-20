# config.py
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DBNAME = os.getenv("MONGODB_DBNAME", "FlightBookDB")

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_TOKEN = os.getenv("API_TOKEN", None)
API_TIMEOUT = int(os.getenv("API_TIMEOUT", 10))

DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
