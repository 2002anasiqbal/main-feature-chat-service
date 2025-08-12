# File: job-service/src/services/cv_service.py

from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from ..repositories.cv_repository import CVRepository
from ..repositories.profile_repository import ProfileRepository
from ..models.schemas import (
    CVCreate, CVUpdate, CVResponse, CVBuilderData,
    FileUploadResponse, MessageResponse, CVTemplateEnum
)
from ..models.cv_models import CVTemplate, CVStatus  # Import the actual enum classes
from ..utils.auth_utils import get_user_from_token
from ..utils.pdf_utils import generate_cv_pdf
from ..utils.file_utils import save_uploaded_file, validate_file
from fastapi import HTTPException, status, UploadFile
import logging
import os
import json
from datetime import datetime

logger = logging.getLogger(__name__)

def serialize_datetime(obj):
    """JSON serializer function that handles datetime objects"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

class CVService:
    def __init__(self):
        self.cv_repo = CVRepository()
        self.profile_repo = ProfileRepository()
    
    def create_cv(self, db: Session, user_token: str, cv_data: CVCreate) -> CVResponse:
        """Create a new CV."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            cv = self.cv_repo.create_cv(db, cv_data, user_id)
            return CVResponse.model_validate(cv)
            
        except Exception as e:
            logger.error(f"Error creating CV: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create CV"
            )
    
    def get_cv_by_id(self, db: Session, user_token: str, cv_id: int) -> CVResponse:
        """Get CV by ID."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            cv = self.cv_repo.get_cv_by_id(db, cv_id)
            if not cv:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="CV not found"
                )
            
            # Verify ownership
            if cv.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to access this CV"
                )
            
            return CVResponse.model_validate(cv)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting CV: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get CV"
            )
    
    def get_user_cvs(self, db: Session, user_token: str) -> List[CVResponse]:
        """Get all CVs for a user."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            cvs = self.cv_repo.get_cvs_by_user(db, user_id)
            return [CVResponse.model_validate(cv) for cv in cvs]
            
        except Exception as e:
            logger.error(f"Error getting user CVs: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get CVs"
            )
    
    def update_cv(self, db: Session, user_token: str, cv_id: int, cv_data: CVUpdate) -> CVResponse:
        """Update CV."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            # Get CV and verify ownership
            cv = self.cv_repo.get_cv_by_id(db, cv_id)
            if not cv:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="CV not found"
                )
            
            if cv.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to update this CV"
                )
            
            updated_cv = self.cv_repo.update_cv(db, cv_id, cv_data)
            return CVResponse.model_validate(updated_cv)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating CV: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update CV"
            )
    
    def delete_cv(self, db: Session, user_token: str, cv_id: int) -> MessageResponse:
        """Delete CV."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            # Get CV and verify ownership
            cv = self.cv_repo.get_cv_by_id(db, cv_id)
            if not cv:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="CV not found"
                )
            
            if cv.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to delete this CV"
                )
            
            success = self.cv_repo.delete_cv(db, cv_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to delete CV"
                )
            
            return MessageResponse(message="CV deleted successfully")
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting CV: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete CV"
            )
    
    def build_cv_from_profile(self, db: Session, user_token: str, cv_builder_data: CVBuilderData) -> CVResponse:
        """Build CV from CV builder data."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            # Serialize datetime objects in cv_builder_data
            cv_data_dict = self._serialize_cv_builder_data(cv_builder_data)
            
            # Create CV with builder data - FIX: Convert string to enum value
            cv_data = CVCreate(
                title=f"CV - {cv_builder_data.contact_info.email if cv_builder_data.contact_info else 'Generated'}",
                cv_data=cv_data_dict,
                template=CVTemplateEnum.MODERN  # This should match the string value
            )
            
            cv = self.cv_repo.create_cv(db, cv_data, user_id)
            
            # Generate PDF
            try:
                pdf_path, file_size = generate_cv_pdf(cv.id, cv_builder_data)
                self.cv_repo.update_cv_file_info(db, cv.id, pdf_path, file_size)
            except Exception as e:
                logger.warning(f"Failed to generate PDF for CV {cv.id}: {str(e)}")
            
            return CVResponse.model_validate(cv)
            
        except Exception as e:
            logger.error(f"Error building CV from profile: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to build CV"
            )
    
    def _serialize_cv_builder_data(self, cv_builder_data: CVBuilderData) -> Dict[str, Any]:
        """Convert CVBuilderData to a JSON-serializable dictionary."""
        try:
            # Convert to dict first
            data_dict = cv_builder_data.dict()
            
            # Recursively serialize datetime objects
            def serialize_nested(obj):
                if isinstance(obj, dict):
                    return {key: serialize_nested(value) for key, value in obj.items()}
                elif isinstance(obj, list):
                    return [serialize_nested(item) for item in obj]
                elif isinstance(obj, datetime):
                    return obj.isoformat()
                else:
                    return obj
            
            return serialize_nested(data_dict)
            
        except Exception as e:
            logger.error(f"Error serializing CV builder data: {str(e)}")
            # Return a simplified version if serialization fails
            return {
                "contact_info": {
                    "email": cv_builder_data.contact_info.email if cv_builder_data.contact_info else "",
                    "phone": cv_builder_data.contact_info.phone if cv_builder_data.contact_info else ""
                } if cv_builder_data.contact_info else None,
                "summary": {
                    "professional_summary": cv_builder_data.summary.professional_summary if cv_builder_data.summary else ""
                } if cv_builder_data.summary else None
            }
    
    def generate_cv_from_profile(self, db: Session, user_token: str) -> CVResponse:
        """Generate CV from user's job profile."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            # Get user's profile
            profile = self.profile_repo.get_profile_by_user_id(db, user_id)
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profile not found. Please create a profile first."
                )
            
            # Convert profile to CV builder data
            cv_builder_data = self._profile_to_cv_builder_data(profile)
            
            # Serialize the data
            cv_data_dict = self._serialize_cv_builder_data(cv_builder_data)
            
            # Create CV - FIX: Use the correct enum
            cv_data = CVCreate(
                title=f"CV - Generated from Profile",
                cv_data=cv_data_dict,
                template=CVTemplateEnum.MODERN
            )
            
            cv = self.cv_repo.create_cv(db, cv_data, user_id)
            
            # Generate PDF
            try:
                pdf_path, file_size = generate_cv_pdf(cv.id, cv_builder_data)
                self.cv_repo.update_cv_file_info(db, cv.id, pdf_path, file_size)
            except Exception as e:
                logger.warning(f"Failed to generate PDF for CV {cv.id}: {str(e)}")
            
            return CVResponse.model_validate(cv)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error generating CV from profile: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate CV from profile"
            )
    
    def upload_cv(self, db: Session, user_token: str, file: UploadFile, title: Optional[str] = None) -> FileUploadResponse:
        """Upload CV file."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            # Validate file
            validate_file(file)
            
            # Save file
            file_path, file_size = save_uploaded_file(file, "cvs")
            
            # Create uploaded CV record
            file_info = {
                "original_filename": file.filename,
                "file_path": file_path,
                "file_size": file_size,
                "file_type": file.filename.split('.')[-1].lower(),
                "title": title or file.filename
            }
            
            uploaded_cv = self.cv_repo.create_uploaded_cv(db, user_id, file_info)
            
            return FileUploadResponse(
                filename=uploaded_cv.original_filename,
                file_path=uploaded_cv.file_path,
                file_size=uploaded_cv.file_size,
                file_type=uploaded_cv.file_type
            )
            
        except Exception as e:
            logger.error(f"Error uploading CV: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload CV"
            )
    
    def download_cv(self, db: Session, user_token: str, cv_id: int) -> str:
        """Get CV download path and increment download count."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            cv = self.cv_repo.get_cv_by_id(db, cv_id)
            if not cv:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="CV not found"
                )
            
            # Verify ownership or public access
            if cv.user_id != user_id and not cv.is_public:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to download this CV"
                )
            
            if not cv.file_path or not os.path.exists(cv.file_path):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="CV file not found"
                )
            
            # Increment download count
            self.cv_repo.increment_cv_download_count(db, cv_id)
            
            return cv.file_path
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error downloading CV: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to download CV"
            )
    
    def _profile_to_cv_builder_data(self, profile) -> CVBuilderData:
        """Convert job profile to CV builder data format."""
        from ..models.schemas import (
            ContactInfoStep, WorkExperienceStep, EducationStep, 
            LanguageStep, SummaryStep
        )
        
        # Contact info
        contact_info = ContactInfoStep(
            email=str(profile.user_id),  # We'd need to get actual email from auth service
            phone=profile.phone,
            location=profile.location,
            website=profile.website,
            linkedin_url=profile.linkedin_url
        )
        
        # Work experience - serialize dates as strings
        work_experience = WorkExperienceStep(
            experiences=[
                {
                    "job_title": exp.job_title,
                    "company_name": exp.company_name,
                    "location": exp.location,
                    "start_date": exp.start_date.isoformat() if exp.start_date else None,
                    "end_date": exp.end_date.isoformat() if exp.end_date else None,
                    "is_current": exp.is_current,
                    "description": exp.description
                }
                for exp in profile.work_experiences
            ]
        )
        
        # Education - serialize dates as strings
        education = EducationStep(
            educations=[
                {
                    "degree": edu.degree,
                    "field_of_study": edu.field_of_study,
                    "institution": edu.institution,
                    "location": edu.location,
                    "start_date": edu.start_date.isoformat() if edu.start_date else None,
                    "end_date": edu.end_date.isoformat() if edu.end_date else None,
                    "is_current": edu.is_current,
                    "description": edu.description
                }
                for edu in profile.educations
            ]
        )
        
        # Languages
        languages = LanguageStep(
            languages=[
                {
                    "language_id": lang.language_id,
                    "proficiency_level": lang.proficiency_level
                }
                for lang in profile.languages
            ]
        )
        
        # Summary
        summary = SummaryStep(
            professional_summary=profile.professional_summary or ""
        )
        
        return CVBuilderData(
            contact_info=contact_info,
            work_experience=work_experience,
            education=education,
            languages=languages,
            summary=summary
        )