from datetime import datetime, timezone
from typing import Optional
from bson import ObjectId
from app.config.database import get_database


COLLECTION_NAME = "users"


def _get_collection():
    """Get the users collection lazily — only after DB is connected."""
    db = get_database()
    return db[COLLECTION_NAME]


async def create_indexes():
    collection = _get_collection()
    await collection.create_index("email", unique=True)
    await collection.create_index("google_id", sparse=True)


async def find_by_email(email: str) -> Optional[dict]:
    collection = _get_collection()
    return await collection.find_one({"email": email})


async def find_by_id(user_id: str) -> Optional[dict]:
    collection = _get_collection()
    try:
        return await collection.find_one({"_id": ObjectId(user_id)})
    except Exception:
        return None


async def find_by_google_id(google_id: str) -> Optional[dict]:
    collection = _get_collection()
    return await collection.find_one({"google_id": google_id})


async def create_user(user_data: dict) -> dict:
    collection = _get_collection()
    user_data["created_at"] = datetime.now(timezone.utc)
    user_data["updated_at"] = datetime.now(timezone.utc)
    result = await collection.insert_one(user_data)
    user_data["_id"] = result.inserted_id
    return user_data


async def update_user(user_id: str, update_data: dict) -> Optional[dict]:
    collection = _get_collection()
    update_data["updated_at"] = datetime.now(timezone.utc)
    await collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data},
    )
    return await find_by_id(user_id)