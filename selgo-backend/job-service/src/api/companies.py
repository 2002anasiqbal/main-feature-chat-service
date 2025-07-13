# File: job-service/src/api/companies.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database.database import get_db
from ..services.company_service import CompanyService
from ..models.schemas import (
    CompanyCreate, CompanyUpdate, CompanyResponse, CompanyResponseWithJobs,
    CompanyFollowResponse, MessageResponse
)
from ..utils.auth_utils import get_current_user

router = APIRouter()
company_service = CompanyService()

@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    company_data: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new company."""
    return company_service.create_company(db, company_data, current_user["user_id"])

@router.get("/{company_id}", response_model=CompanyResponseWithJobs)
def get_company(
    company_id: int,
    include_jobs: bool = Query(True, description="Include company jobs"),
    db: Session = Depends(get_db)
):
    """Get company by ID with optional jobs."""
    return company_service.get_company_with_jobs(db, company_id, include_jobs)

@router.get("/", response_model=List[CompanyResponse])
def get_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = Query(None, description="Search companies by name"),
    industry: Optional[str] = Query(None, description="Filter by industry"),
    db: Session = Depends(get_db)
):
    """Get companies with filters."""
    return company_service.search_companies(db, search, industry, skip, limit)

@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: int,
    company_data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update company (owner only)."""
    return company_service.update_company(db, company_id, company_data, current_user["user_id"])

@router.post("/{company_id}/follow", response_model=CompanyFollowResponse)
async def follow_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Follow a company."""
    return company_service.follow_company(db, company_id, current_user["user_id"])

@router.delete("/{company_id}/follow", response_model=MessageResponse)
async def unfollow_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Unfollow a company."""
    return company_service.unfollow_company(db, company_id, current_user["user_id"])

@router.get("/followed/list", response_model=List[CompanyFollowResponse])
async def get_followed_companies(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get companies followed by user."""
    return company_service.get_followed_companies(db, current_user["user_id"])