from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


# --- Request/Response Models ---

class UploadResponse(BaseModel):
    """Returned immediately after file upload."""
    job_id: str
    status: str
    message: str


class ResultResponse(BaseModel):
    """Returned when user queries for result."""
    job_id: str
    status: str
    filename: Optional[str] = None
    analysis_result: Optional[str] = None
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    message: Optional[str] = None


# --- Internal DB Document Model ---

class CVJobDocument(BaseModel):
    """Shape of the document stored in MongoDB."""
    job_id: str
    filename: str
    status: JobStatus = JobStatus.PENDING
    raw_text: Optional[str] = None
    analysis_result: Optional[str] = None
    created_at: datetime = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None




