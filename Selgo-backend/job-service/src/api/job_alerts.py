# File: job-service/src/api/job_alerts.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database.database import get_db
from ..models.schemas import JobAlertCreate, JobAlertResponse, JobAlertUpdate, MessageResponse
from ..services.job_alert_service import JobAlertService
from ..utils.auth_utils import get_current_user

router = APIRouter()
job_alert_service = JobAlertService()

@router.post("/", response_model=JobAlertResponse, status_code=status.HTTP_201_CREATED)
async def create_job_alert(
    alert_data: JobAlertCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new job alert."""
    user_id = current_user["user_id"]
    return job_alert_service.create_job_alert(db, user_id, alert_data)

@router.get("/", response_model=List[JobAlertResponse])
async def get_user_job_alerts(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all job alerts for current user."""
    user_id = current_user["user_id"]
    return job_alert_service.get_user_job_alerts(db, user_id)

@router.put("/{alert_id}", response_model=JobAlertResponse)
async def update_job_alert(
    alert_id: int,
    alert_data: JobAlertUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update job alert."""
    user_id = current_user["user_id"]
    return job_alert_service.update_job_alert(db, user_id, alert_id, alert_data)

@router.delete("/{alert_id}", response_model=MessageResponse)
async def delete_job_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete job alert."""
    user_id = current_user["user_id"]
    return job_alert_service.delete_job_alert(db, user_id, alert_id)

@router.post("/{alert_id}/toggle", response_model=JobAlertResponse)
async def toggle_job_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Toggle job alert active status."""
    user_id = current_user["user_id"]
    return job_alert_service.toggle_job_alert(db, user_id, alert_id)