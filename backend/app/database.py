from pathlib import Path
import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import PyMongoError


BACKEND_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BACKEND_DIR / ".env")
load_dotenv(BACKEND_DIR.parent / ".env")

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "student_analytics")

client: MongoClient | None = MongoClient(MONGODB_URI) if MONGODB_URI else None
database: Database | None = client[MONGODB_DATABASE] if client else None


def check_mongodb_connection() -> bool:
    if client is None:
        return False

    try:
        client.admin.command("ping")
    except PyMongoError:
        return False

    return True