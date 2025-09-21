# File: job-service/src/api/routes.py
# Update your existing routes.py to include all endpoints

from fastapi import APIRouter
from .jobs import router as jobs_router
from .profile import router as profile_router
from .cv import router as cv_router
from .salary import router as salary_router
from .articles import router as articles_router
from .companies import router as companies_router  # Add this
from .recommendations import router as recommendations_router
from .job_alerts import router as job_alerts_router
from .analytics import router as analytics_router

router = APIRouter()

# Include all sub-routers
router.include_router(jobs_router, prefix="/jobs", tags=["jobs"])
router.include_router(profile_router, prefix="/profile", tags=["profile"])
router.include_router(cv_router, prefix="/cv", tags=["cv"])
router.include_router(salary_router, prefix="/salary", tags=["salary"])
router.include_router(articles_router, prefix="/articles", tags=["articles"])
router.include_router(companies_router, prefix="/companies", tags=["companies"])
router.include_router(recommendations_router, prefix="/recommendations", tags=["recommendations"])
router.include_router(job_alerts_router, prefix="/job-alerts", tags=["job-alerts"])
router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])

@router.get("/")
def api_root():
    return {
        "message": "Job Service API",
        "version": "1.0.0",
        "endpoints": {
            "jobs": "/jobs",
            "profile": "/profile", 
            "cv": "/cv",
            "salary": "/salary",
            "articles": "/articles",
            "companies": "/companies",
            "recommendations": "/recommendations",
            "job_alerts": "/job-alerts",
            "analytics": "/analytics"
        }
    }