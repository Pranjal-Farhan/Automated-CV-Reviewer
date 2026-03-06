from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from app.service.cv_service import CVService
from app.models.schemas import UploadResponse, ResultResponse, JobStatus

router = APIRouter(tags=["CV Reviewer"])

# Allowed file extensions
ALLOWED_EXTENSIONS = {".pdf", ".txt"}


@router.post("/cv/upload", response_model=UploadResponse)
async def upload_cv(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="CV/Resume file (PDF or TXT)")
):
    """
    Upload a CV file for parsing and analysis.
    
    Returns a job_id immediately. Use the job_id to poll for results.
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

    # Create job in DB (pending status)
    job_id = await CVService.create_job(file.filename)

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
async def get_result(job_id: str):
    """
    Check the status/result of a CV analysis job.
    
    - If processing is not done → returns status with "not ready" message.
    - If processing is done → returns the analysis text summary.
    - If processing failed → returns error details.
    """
    result = await CVService.get_result(job_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Job not found.")

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