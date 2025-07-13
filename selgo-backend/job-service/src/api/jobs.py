# File: job-service/src/api/jobs.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database.database import get_db
from ..services.job_service import JobService
from sqlalchemy import func, desc
from ..models.schemas import (
    JobStatisticsResponse, FilterOptionsResponse, JobCategoryResponse,
    BulkJobAction, BulkJobResponse, JobFeedRequest, JobFeedResponse
)
from ..models.schemas import (
    JobCreate, JobUpdate, JobResponse, JobSearchRequest, JobSearchResponse,
    MessageResponse, JobTypeEnum, ExperienceLevelEnum
)
from ..utils.auth_utils import get_current_user, get_user_from_token
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
job_service = JobService()

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new job posting."""
    # Extract token from current_user or create a mock token
    mock_token = "mock_token"  # In production, extract from request
    return job_service.create_job(db, job_data, mock_token)

@router.get("/search", response_model=JobSearchResponse)
def search_jobs(
    q: Optional[str] = Query(None, description="Search query"),
    location: Optional[str] = Query(None, description="Location filter"),
    job_type: Optional[List[JobTypeEnum]] = Query(None, description="Job type filter"),
    experience_level: Optional[List[ExperienceLevelEnum]] = Query(None, description="Experience level filter"),
    salary_min: Optional[float] = Query(None, description="Minimum salary"),
    salary_max: Optional[float] = Query(None, description="Maximum salary"),
    is_remote: Optional[bool] = Query(None, description="Remote work filter"),
    company_id: Optional[int] = Query(None, description="Company filter"),
    category_id: Optional[int] = Query(None, description="Category filter"),
    tags: Optional[List[str]] = Query(None, description="Skills/tags filter"),
    posted_within_days: Optional[int] = Query(None, description="Posted within days"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    sort_by: Optional[str] = Query("created_at", description="Sort field"),
    sort_order: Optional[str] = Query("desc", description="Sort order"),
    db: Session = Depends(get_db)
):
    """Search jobs with filtering and pagination."""
    search_params = JobSearchRequest(
        q=q,
        location=location,
        job_type=job_type or [],
        experience_level=experience_level or [],
        salary_min=salary_min,
        salary_max=salary_max,
        is_remote=is_remote,
        company_id=company_id,
        category_id=category_id,
        tags=tags or [],
        posted_within_days=posted_within_days,
        page=page,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return job_service.search_jobs(db, search_params)

@router.get("/featured", response_model=List[JobResponse])
def get_featured_jobs(
    limit: int = Query(10, ge=1, le=50, description="Number of featured jobs"),
    db: Session = Depends(get_db)
):
    """Get featured jobs for homepage."""
    return job_service.get_featured_jobs(db, limit)

@router.get("/recent", response_model=List[JobResponse])
def get_recent_jobs(
    limit: int = Query(20, ge=1, le=100, description="Number of recent jobs"),
    db: Session = Depends(get_db)
):
    """Get recently posted jobs."""
    return job_service.get_recent_jobs(db, limit)

@router.get("/recommendations", response_model=List[JobResponse])
async def get_job_recommendations(
    limit: int = Query(10, ge=1, le=50, description="Number of recommendations"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get personalized job recommendations."""
    mock_token = "mock_token"  # In production, extract from request
    return job_service.get_job_recommendations(db, mock_token, limit)

@router.get("/saved", response_model=List[JobResponse])
async def get_saved_jobs(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get user's saved jobs."""
    mock_token = "mock_token"  # In production, extract from request
    return job_service.get_user_saved_jobs(db, mock_token)

@router.get("/viewed", response_model=List[JobResponse])
async def get_viewed_jobs(
    limit: int = Query(20, ge=1, le=100, description="Number of viewed jobs"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get user's recently viewed jobs (Last Viewed Jobs feature)."""
    mock_token = "mock_token"  # In production, extract from request
    return job_service.get_user_viewed_jobs(db, mock_token, limit)

@router.get("/company/{company_id}", response_model=List[JobResponse])
def get_jobs_by_company(
    company_id: int,
    limit: int = Query(10, ge=1, le=50, description="Number of jobs"),
    db: Session = Depends(get_db)
):
    """Get jobs by company."""
    return job_service.get_jobs_by_company(db, company_id, limit)

@router.get("/{job_id}", response_model=JobResponse)
def get_job_by_id(
    job_id: int,
    db: Session = Depends(get_db)
):
    """Get job by ID and increment view count."""
    # For anonymous access, pass None for user_token
    return job_service.get_job_by_id(db, job_id, None)

@router.get("/slug/{slug}", response_model=JobResponse)
def get_job_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    """Get job by slug and increment view count."""
    # For anonymous access, pass None for user_token
    return job_service.get_job_by_slug(db, slug, None)

@router.get("/{job_id}/similar", response_model=List[JobResponse])
def get_similar_jobs(
    job_id: int,
    limit: int = Query(5, ge=1, le=20, description="Number of similar jobs"),
    db: Session = Depends(get_db)
):
    """Get similar jobs to the given job."""
    return job_service.get_similar_jobs(db, job_id, limit)

@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: int,
    job_data: JobUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update job posting."""
    mock_token = "mock_token"  # In production, extract from request
    return job_service.update_job(db, job_id, job_data, mock_token)

@router.delete("/{job_id}", response_model=MessageResponse)
async def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete job posting."""
    mock_token = "mock_token"  # In production, extract from request
    return job_service.delete_job(db, job_id, mock_token)

@router.post("/{job_id}/save", response_model=MessageResponse)
async def save_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Save job for user."""
    mock_token = "mock_token"  # In production, extract from request
    return job_service.save_job(db, job_id, mock_token)

@router.delete("/{job_id}/save", response_model=MessageResponse)
async def unsave_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Remove saved job for user."""
    mock_token = "mock_token"  # In production, extract from request
    return job_service.unsave_job(db, job_id, mock_token)

@router.get("/statistics", response_model=JobStatisticsResponse)
def get_job_statistics(db: Session = Depends(get_db)):
    """Get job platform statistics."""
    return job_service.get_job_statistics(db)

@router.get("/filter-options", response_model=FilterOptionsResponse)
def get_filter_options(db: Session = Depends(get_db)):
    """Get available filter options for job search."""
    return job_service.get_filter_options(db)

@router.get("/categories", response_model=List[JobCategoryResponse])
def get_job_categories(db: Session = Depends(get_db)):
    """Get all job categories."""
    return job_service.get_job_categories(db)

@router.post("/bulk-action", response_model=BulkJobResponse)
async def bulk_job_action(
    bulk_action: BulkJobAction,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Perform bulk actions on jobs (admin only)."""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return job_service.bulk_job_action(db, bulk_action, current_user["user_id"])

@router.get("/feed", response_model=JobFeedResponse)
def get_job_feed(
    feed_request: JobFeedRequest = Depends(),
    db: Session = Depends(get_db)
):
    """Get personalized job feed for homepage."""
    return job_service.get_job_feed(db, feed_request)