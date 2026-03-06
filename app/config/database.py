import os
from motor.motor_asyncio import AsyncIOMotorClient

client: AsyncIOMotorClient = None
db = None


async def connect_db():
    global client, db
    mongo_url = os.getenv("MONGO_URL", "mongodb://mongodb:27017")
    db_name = os.getenv("MONGO_DB_NAME", "cv_reviewer")
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    await db["cv_jobs"].create_index("job_id", unique=True)


async def close_db():
    global client
    if client:
        client.close()


def get_database():
    return db
