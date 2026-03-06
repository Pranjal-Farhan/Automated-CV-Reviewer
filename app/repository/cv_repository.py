from datetime import datetime, timezone
from typing import Optional
from app.config.database import get_database
from app.models.schemas import JobStatus


class CVRepository:
    COLLECTION_NAME = "cv_jobs"

    @staticmethod
    def _get_collection():
        db = get_database()
        return db[CVRepository.COLLECTION_NAME]

    @staticmethod
    async def create_job(job_id: str, filename: str) -> dict:
        collection = CVRepository._get_collection()
        job_document = {
            "job_id": job_id,
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