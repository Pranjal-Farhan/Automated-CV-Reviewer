from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException, Depends
from app.service.cv_service import CVService
from app.models.schemas import UploadResponse, ResultResponse, JobStatus
from app.config.auth import get_current_user_id

router = APIRouter(tags=["CV Reviewer"])

# Allowed file extensions
ALLOWED_EXTENSIONS = {".pdf", ".txt"}


@router.post("/cv/upload", response_model=UploadResponse)
async def upload_cv(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="CV/Resume file (PDF or TXT)"),
    user_id: str = Depends(get_current_user_id),
):
    """
    Upload a CV file for parsing and analysis.
    Requires authentication. Returns a job_id immediately.
    """
    # Validate file extension
    filename = file.filename.lower()
    if not any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Read file content
    file_content = await file.read()

    if len(file_content) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # Create job in DB (pending status) — now includes user_id
    job_id = await CVService.create_job(file.filename, user_id)

    # Schedule background processing (async — returns immediately)
    background_tasks.add_task(
        CVService.process_cv, job_id, file_content, file.filename
    )

    return UploadResponse(
        job_id=job_id,
        status=JobStatus.PENDING,
        message="CV uploaded successfully. Processing has started.",
    )


@router.get("/cv/result/{job_id}", response_model=ResultResponse)
async def get_result(
    job_id: str,
    user_id: str = Depends(get_current_user_id),
):
    """
    Check the status/result of a CV analysis job.
    Requires authentication. Users can only access their own jobs.
    """
    result = await CVService.get_result(job_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Job not found.")

    # Ensure the user owns this job
    if result.get("user_id") and result["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied.")

    status = result["status"]

    # ⏳ Still processing
    if status in (JobStatus.PENDING, JobStatus.PROCESSING):
        return ResultResponse(
            job_id=job_id,
            status=status,
            filename=result["filename"],
            created_at=result.get("created_at"),
            message="The result is not ready yet. Please try again later.",
        )

    # ✅ Completed
    if status == JobStatus.COMPLETED:
        return ResultResponse(
            job_id=job_id,
            status=status,
            filename=result["filename"],
            analysis_result=result["analysis_result"],
            created_at=result.get("created_at"),
            completed_at=result.get("completed_at"),
            message="Analysis complete.",
        )

    # ❌ Failed
    return ResultResponse(
        job_id=job_id,
        status=status,
        filename=result["filename"],
        created_at=result.get("created_at"),
        completed_at=result.get("completed_at"),
        error=result.get("error"),
        message="Processing failed. See error field for details.",
    )


@router.get("/cv/history")
async def get_history(
    user_id: str = Depends(get_current_user_id),
):
    """
    Returns all CV analysis jobs for the authenticated user,
    sorted by most recent first.
    """
    from app.repository.cv_repository import CVRepository
    jobs = await CVRepository.get_jobs_by_user(user_id)
    return {
        "jobs": [
            {
                "job_id": j["job_id"],
                "status": j["status"],
                "filename": j.get("filename"),
                "created_at": j.get("created_at"),
                "completed_at": j.get("completed_at"),
                "has_result": j.get("analysis_result") is not None,
            }
            for j in jobs
        ]
    }