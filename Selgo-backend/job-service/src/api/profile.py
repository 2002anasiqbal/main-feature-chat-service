# File: job-service/src/api/profile.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from ..database.database import get_db
from ..services.profile_service import ProfileService
from ..models.schemas import (
    JobProfileCreate, JobProfileUpdate, JobProfileResponse,
    WorkExperienceCreate, WorkExperienceResponse,
    EducationCreate, EducationResponse,
    MessageResponse, ProficiencyLevelEnum
)
from ..utils.auth_utils import get_current_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
profile_service = ProfileService()

@router.post("/", response_model=JobProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile_data: Optional[JobProfileCreate] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create or get job profile."""
    mock_token = "mock_token"  # In production, extract from request
    return profile_service.create_or_get_profile(db, mock_token, profile_data)

@router.get("/", response_model=JobProfileResponse)
async def get_profile(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get user's job profile."""
    mock_token = "mock_token"  # In production, extract from request
    return profile_service.get_profile(db, mock_token)

@router.put("/", response_model=JobProfileResponse)
async def update_profile(
    profile_data: JobProfileUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update user's job profile."""
    mock_token = "mock_token"  # In production, extract from request
    return profile_service.update_profile(db, mock_token, profile_data)

@router.delete("/", response_model=MessageResponse)
async def delete_profile(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete user's job profile."""
    mock_token = "mock_token"  # In production, extract from request
    return profile_service.delete_profile(db, mock_token)

# Work Experience endpoints
@router.post("/experience", response_model=WorkExperienceResponse)
async def add_work_experience(
    experience_data: WorkExperienceCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Add work experience to profile."""
    mock_token = "mock_token"  # In production, extract from request
    return profile_service.add_work_experience(db, mock_token, experience_data)

@router.get("/experience", response_model=List[WorkExperienceResponse])
async def get_work_experiences(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get user's work experiences."""
    mock_token = "mock_token"  # In production, extract from request
    return profile_service.get_work_experiences(db, mock_token)

@router.put("/experience/{experience_id}", response_model=WorkExperienceResponse)
async def update_work_experience(
    experience_id: int,
    experience_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update work experience."""
    mock_token = "mock_token"  # In production, extract from request
    return profile_service.update_work_experience(db, mock_token, experience_id, experience_data)

@router.delete("/experience/{experience_id}", response_model=MessageResponse)
async def delete_work_experience(
    experience_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete work experience."""
    mock_token = "mock_token"  # In production, extract from request
    return profile_service.delete_work_experience(db, mock_token, experience_id)

# Education endpoints
@router.post("/education", response_model=EducationResponse)
async def add_education(
    education_data: EducationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Add education to profile."""
    mock_token = "mock_token"  # In production, extract from request
    return profile_service.add_education(db, mock_token, education_data)

# Skills endpoints
@router.post("/skills")
async def add_skill(
    skill_name: str,
    proficiency_level: ProficiencyLevelEnum,
    years_of_experience: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Add skill to profile."""
    mock_token = "mock_token"  # In production, extract from request
    return profile_service.add_skill(db, mock_token, skill_name, proficiency_level, years_of_experience)

@router.get("/skills/search")
def search_skills(
    q: str = Query(..., description="Search query for skills"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Search available skills."""
    return profile_service.search_skills(db, q, limit)

# Languages endpoints
@router.post("/languages")
async def add_language(
    language_name: str,
    proficiency_level: ProficiencyLevelEnum,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Add language to profile."""
    mock_token = "mock_token"  # In production, extract from request
    return profile_service.add_language(db, mock_token, language_name, proficiency_level)

@router.get("/languages/search")
def search_languages(
    q: str = Query(..., description="Search query for languages"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Search available languages."""
    return profile_service.search_languages(db, q, limit)




@router.get("/dashboard", response_model=Dict[str, Any])
async def get_profile_dashboard(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get complete profile dashboard with salary comparison."""
    mock_token = "mock_token"
    return profile_service.get_profile_with_salary_comparison(db, mock_token)

@router.get("/salary-comparison", response_model=Dict[str, Any])
async def get_salary_comparison_for_profile(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get salary comparison based on user's current job profile."""
    mock_token = "mock_token"
    
    try:
        user_info = get_user_from_token(mock_token)
        user_id = user_info["user_id"]
        
        profile = profile_service.profile_repo.get_profile_by_user_id(db, user_id)
        if not profile or not profile.work_experiences:
            return {
                "error": "No work experience found",
                "message": "Please add work experience to your profile to get salary comparison",
                "redirect": "/routes/jobs/job-profile"
            }
        
        # Get current work experience
        current_exp = next(
            (exp for exp in profile.work_experiences if exp.is_current),
            profile.work_experiences[0]
        )
        
        from datetime import datetime
        years_exp = (datetime.utcnow() - current_exp.start_date).days // 365 if current_exp.start_date else 0
        
        from ..models.schemas import SalaryComparisonRequest
        from ..services.salary_service import SalaryService
        
        comparison_request = SalaryComparisonRequest(
            job_title=current_exp.job_title,
            location=profile.location or current_exp.location,
            years_of_experience=years_exp
        )
        
        salary_service = SalaryService()
        comparison_data = salary_service.compare_salary(db, comparison_request)
        
        # Add user context
        comparison_data["user_context"] = {
            "job_title": current_exp.job_title,
            "company": current_exp.company_name,
            "years_of_experience": years_exp,
            "location": profile.location or current_exp.location,
            "desired_salary_range": f"${profile.desired_salary_min or 0:,.0f} - ${profile.desired_salary_max or 0:,.0f}"
        }
        
        return comparison_data
        
    except Exception as e:
        logger.error(f"Error getting salary comparison: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get salary comparison"
        )