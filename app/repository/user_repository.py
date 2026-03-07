from datetime import datetime
from typing import Optional
from bson import ObjectId

from app.config.database import database


collection = database.get_collection("users")


async def create_indexes():
    await collection.create_index("email", unique=True)


async def find_by_email(email: str) -> Optional[dict]:
    return await collection.find_one({"email": email})


async def find_by_id(user_id: str) -> Optional[dict]:
    try:
        return await collection.find_one({"_id": ObjectId(user_id)})
    except Exception:
        return None


async def find_by_google_id(google_id: str) -> Optional[dict]:
    return await collection.find_one({"google_id": google_id})


async def create_user(user_data: dict) -> dict:
    user_data["created_at"] = datetime.utcnow()
    user_data["updated_at"] = datetime.utcnow()
    result = await collection.insert_one(user_data)
    user_data["_id"] = result.inserted_id
    return user_data


async def update_user(user_id: str, update_data: dict) -> Optional[dict]:
    update_data["updated_at"] = datetime.utcnow()
    await collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data},
    )
    return await find_by_id(user_id)