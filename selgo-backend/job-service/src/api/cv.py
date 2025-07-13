# File: job-service/src/api/cv.py

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database.database import get_db
from ..services.cv_service import CVService
from ..models.schemas import (
    CVCreate, CVUpdate, CVResponse, CVBuilderData,
    FileUploadResponse, MessageResponse
)
from ..utils.auth_utils import get_current_user

router = APIRouter()
cv_service = CVService()

@router.post("/", response_model=CVResponse, status_code=status.HTTP_201_CREATED)
async def create_cv(
    cv_data: CVCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new CV."""
    mock_token = "mock_token"  # In production, extract from request
    return cv_service.create_cv(db, mock_token, cv_data)

@router.get("/", response_model=List[CVResponse])
async def get_user_cvs(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all CVs for the current user."""
    mock_token = "mock_token"  # In production, extract from request
    return cv_service.get_user_cvs(db, mock_token)

@router.post("/build", response_model=CVResponse)
async def build_cv(
    cv_builder_data: CVBuilderData,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Build CV from CV builder data (Complete Resume Builder feature)."""
    mock_token = "mock_token"  # In production, extract from request
    return cv_service.build_cv_from_profile(db, mock_token, cv_builder_data)

@router.post("/generate-from-profile", response_model=CVResponse)
async def generate_cv_from_profile(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Generate CV from user's job profile."""
    mock_token = "mock_token"  # In production, extract from request
    return cv_service.generate_cv_from_profile(db, mock_token)

@router.post("/upload", response_model=FileUploadResponse)
async def upload_cv(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Upload CV file (Add a CV feature)."""
    mock_token = "mock_token"  # In production, extract from request
    return cv_service.upload_cv(db, mock_token, file, title)

@router.get("/{cv_id}", response_model=CVResponse)
async def get_cv(
    cv_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get CV by ID."""
    mock_token = "mock_token"  # In production, extract from request
    return cv_service.get_cv_by_id(db, mock_token, cv_id)

@router.put("/{cv_id}", response_model=CVResponse)
async def update_cv(
    cv_id: int,
    cv_data: CVUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update CV."""
    mock_token = "mock_token"  # In production, extract from request
    return cv_service.update_cv(db, mock_token, cv_id, cv_data)

@router.delete("/{cv_id}", response_model=MessageResponse)
async def delete_cv(
    cv_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete CV."""
    mock_token = "mock_token"  # In production, extract from request
    return cv_service.delete_cv(db, mock_token, cv_id)

@router.get("/{cv_id}/download")
async def download_cv(
    cv_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Download CV as PDF (Download Profile as CV feature)."""
    mock_token = "mock_token"  # In production, extract from request
    file_path = cv_service.download_cv(db, mock_token, cv_id)
    return FileResponse(file_path, media_type='application/pdf', filename=f"cv_{cv_id}.pdf")