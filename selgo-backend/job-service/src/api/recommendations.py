# File: job-service/src/api/recommendations.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from ..database.database import get_db
from ..services.recommendation_service import RecommendationService
from ..services.analytics_service import JobAnalyticsService
from ..models.schemas import (
    JobResponse, MessageResponse, UserJobPreferencesCreate,
    UserJobPreferencesResponse, JobRecommendationResponse
)
from ..utils.auth_utils import get_current_user

router = APIRouter()
recommendation_service = RecommendationService()
analytics_service = JobAnalyticsService()

@router.get("/", response_model=List[JobRecommendationResponse])
async def get_job_recommendations(
    limit: int = Query(10, ge=1, le=50, description="Number of recommendations"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get personalized job recommendations for user."""
    user_id = current_user["user_id"]
    recommendations = recommendation_service.get_job_recommendations(db, user_id, limit)
    
    return [JobRecommendationResponse(**rec) for rec in recommendations]

@router.post("/preferences", response_model=UserJobPreferencesResponse)
async def update_job_preferences(
    preferences: UserJobPreferencesCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update user job preferences for better recommendations."""
    user_id = current_user["user_id"]
    updated_prefs = recommendation_service.update_user_preferences(
        db, user_id, preferences.dict()
    )
    return UserJobPreferencesResponse.model_validate(updated_prefs)

@router.get("/preferences", response_model=UserJobPreferencesResponse)
async def get_job_preferences(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get user's current job preferences."""
    user_id = current_user["user_id"]
    from ..models.recommendation_models import UserJobPreferences
    
    prefs = db.query(UserJobPreferences).filter(
        UserJobPreferences.user_id == user_id
    ).first()
    
    if not prefs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job preferences not found"
        )
    
    return UserJobPreferencesResponse.model_validate(prefs)

@router.post("/{job_id}/interaction", response_model=MessageResponse)
async def track_recommendation_interaction(
    job_id: int,
    interaction_type: str = Query(..., description="view, click, apply, dismiss"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Track user interaction with recommended job."""
    user_id = current_user["user_id"]
    
    # Track recommendation interaction
    recommendation_service.track_recommendation_interaction(
        db, user_id, job_id, interaction_type
    )
    
    # Also track general analytics
    analytics_service.track_job_interaction(
        db, job_id, interaction_type, user_id
    )
    
    return MessageResponse(message=f"Interaction '{interaction_type}' tracked successfully")