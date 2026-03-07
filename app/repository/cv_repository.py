from datetime import datetime, timezone
from typing import Optional, List
from app.config.database import get_database
from app.models.schemas import JobStatus


class CVRepository:
    COLLECTION_NAME = "cv_jobs"

    @staticmethod
    def _get_collection():
        db = get_database()
        return db[CVRepository.COLLECTION_NAME]

    @staticmethod
    async def create_job(job_id: str, filename: str, user_id: str = None) -> dict:
        collection = CVRepository._get_collection()
        job_document = {
            "job_id": job_id,
            "user_id": user_id,
            "filename": filename,
            "status": JobStatus.PENDING,
            "raw_text": None,
            "analysis_result": None,
            "created_at": datetime.now(timezone.utc),
            "completed_at": None,
            "error": None,
        }
        await collection.insert_one(job_document)
        return job_document

    @staticmethod
    async def get_job_by_id(job_id: str) -> Optional[dict]:
        collection = CVRepository._get_collection()
        return await collection.find_one(
            {"job_id": job_id}, {"_id": 0}
        )

    @staticmethod
    async def update_status(job_id: str, status: JobStatus, **kwargs):
        collection = CVRepository._get_collection()
        update_fields = {"status": status}
        update_fields.update(kwargs)
        if status in (JobStatus.COMPLETED, JobStatus.FAILED):
            update_fields["completed_at"] = datetime.now(timezone.utc)
        await collection.update_one(
            {"job_id": job_id}, {"$set": update_fields}
        )

    @staticmethod
    async def save_result(job_id: str, raw_text: str, analysis_result: str):
        await CVRepository.update_status(
            job_id, JobStatus.COMPLETED,
            raw_text=raw_text, analysis_result=analysis_result,
        )

    @staticmethod
    async def save_error(job_id: str, error_message: str):
        await CVRepository.update_status(
            job_id, JobStatus.FAILED, error=error_message,
        )

    @staticmethod
    async def get_jobs_by_user(user_id: str, limit: int = 50) -> List[dict]:
        """Return all jobs belonging to a user, most recent first."""
        collection = CVRepository._get_collection()
        cursor = collection.find(
            {"user_id": user_id},
            {"_id": 0, "raw_text": 0},  # Exclude heavy fields from listing
        ).sort("created_at", -1).limit(limit)
        return await cursor.to_list(length=limit)

    @staticmethod
    async def create_indexes():
        """Create database indexes for performance."""
        collection = CVRepository._get_collection()
        await collection.create_index("job_id", unique=True)
        await collection.create_index("user_id")
        await collection.create_index("created_at")