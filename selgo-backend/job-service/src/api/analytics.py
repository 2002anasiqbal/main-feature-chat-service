# File: job-service/src/api/analytics.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from ..database.database import get_db
from ..services.analytics_service import JobAnalyticsService
from ..utils.auth_utils import get_current_user

router = APIRouter()
analytics_service = JobAnalyticsService()

@router.get("/jobs/{job_id}", response_model=Dict[str, Any])
async def get_job_analytics(
    job_id: int,
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get analytics for a specific job (job owner only)."""
    # Verify job ownership
    from ..models.job_models import Job
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    if job.posted_by != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view analytics for this job"
        )
    
    return analytics_service.get_job_analytics(db, job_id, days)

@router.get("/employer", response_model=Dict[str, Any])
async def get_employer_analytics(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get analytics for all jobs posted by current user."""
    user_id = current_user["user_id"]
    return analytics_service.get_employer_analytics(db, user_id, days)

@router.get("/platform", response_model=Dict[str, Any])
async def get_platform_analytics(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get overall platform analytics (admin only)."""
    # Check if user is admin
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return analytics_service.get_platform_analytics(db, days)

@router.get("/user/activity", response_model=Dict[str, Any])
async def get_user_activity_analytics(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get analytics for current user's job search activity."""
    user_id = current_user["user_id"]
    return analytics_service.get_user_activity_analytics(db, user_id, days)

@router.post("/track", response_model=Dict[str, str])
async def track_job_interaction(
    job_id: int,
    interaction_type: str,
    session_id: Optional[str] = None,
    time_spent: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: Optional[dict] = Depends(get_current_user)
):
    """Track user interaction with job (can be anonymous)."""
    user_id = current_user["user_id"] if current_user else None
    
    analytics_service.track_job_interaction(
        db=db,
        job_id=job_id,
        interaction_type=interaction_type,
        user_id=user_id,
        session_id=session_id,
        time_spent=time_spent
    )
    
    return {"message": "Interaction tracked successfully"}