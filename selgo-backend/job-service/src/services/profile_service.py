# File: job-service/src/services/profile_service.py

from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from ..repositories.profile_repository import ProfileRepository
from ..models.schemas import (
    JobProfileCreate, JobProfileUpdate, JobProfileResponse,
    WorkExperienceCreate, WorkExperienceResponse,
    EducationCreate, EducationResponse,
    UserSkillCreate, UserSkillResponse,
    UserLanguageCreate, UserLanguageResponse,
    SalaryEntryCreate, SalaryEntryResponse,
    MessageResponse
)
from ..utils.auth_utils import get_user_from_token
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

class ProfileService:
    def __init__(self):
        self.profile_repo = ProfileRepository()
    
    def create_or_get_profile(self, db: Session, user_token: str, profile_data: Optional[JobProfileCreate] = None) -> JobProfileResponse:
        """Create profile if it doesn't exist, or get existing profile."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            # Check if profile already exists
            existing_profile = self.profile_repo.get_profile_by_user_id(db, user_id)
            if existing_profile:
                return JobProfileResponse.model_validate(existing_profile)
            
            # Create new profile
            if not profile_data:
                profile_data = JobProfileCreate()
            
            profile = self.profile_repo.create_profile(db, profile_data, user_id)
            return JobProfileResponse.model_validate(profile)
            
        except Exception as e:
            logger.error(f"Error creating/getting profile: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create or get profile"
            )
    
    def get_profile(self, db: Session, user_token: str) -> JobProfileResponse:
        """Get user's job profile."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            profile = self.profile_repo.get_profile_by_user_id(db, user_id)
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profile not found"
                )
            
            return JobProfileResponse.model_validate(profile)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting profile: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get profile"
            )
    
    def update_profile(self, db: Session, user_token: str, profile_data: JobProfileUpdate) -> JobProfileResponse:
        """Update user's job profile."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            updated_profile = self.profile_repo.update_profile(db, user_id, profile_data)
            if not updated_profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profile not found"
                )
            
            return JobProfileResponse.model_validate(updated_profile)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating profile: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update profile"
            )
    
    def delete_profile(self, db: Session, user_token: str) -> MessageResponse:
        """Delete user's job profile."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            success = self.profile_repo.delete_profile(db, user_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profile not found"
                )
            
            return MessageResponse(message="Profile deleted successfully")
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting profile: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete profile"
            )
    
    # Work Experience Methods
    def add_work_experience(self, db: Session, user_token: str, experience_data: WorkExperienceCreate) -> WorkExperienceResponse:
        """Add work experience to profile."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            # Get profile
            profile = self.profile_repo.get_profile_by_user_id(db, user_id)
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profile not found"
                )
            
            experience = self.profile_repo.add_work_experience(db, profile.id, experience_data)
            return WorkExperienceResponse.model_validate(experience)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error adding work experience: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add work experience"
            )
    
    def update_work_experience(self, db: Session, user_token: str, experience_id: int, experience_data: Dict[str, Any]) -> WorkExperienceResponse:
        """Update work experience."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            # Verify ownership through profile
            profile = self.profile_repo.get_profile_by_user_id(db, user_id)
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profile not found"
                )
            
            updated_experience = self.profile_repo.update_work_experience(db, experience_id, experience_data)
            if not updated_experience:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Work experience not found"
                )
            
            return WorkExperienceResponse.model_validate(updated_experience)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating work experience: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update work experience"
            )
    
    def delete_work_experience(self, db: Session, user_token: str, experience_id: int) -> MessageResponse:
        """Delete work experience."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            # Verify ownership through profile
            profile = self.profile_repo.get_profile_by_user_id(db, user_id)
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profile not found"
                )
            
            success = self.profile_repo.delete_work_experience(db, experience_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Work experience not found"
                )
            
            return MessageResponse(message="Work experience deleted successfully")
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting work experience: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete work experience"
            )
    
    def get_work_experiences(self, db: Session, user_token: str) -> List[WorkExperienceResponse]:
        """Get user's work experiences."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            profile = self.profile_repo.get_profile_by_user_id(db, user_id)
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profile not found"
                )
            
            experiences = self.profile_repo.get_work_experiences_by_profile(db, profile.id)
            return [WorkExperienceResponse.model_validate(exp) for exp in experiences]
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting work experiences: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get work experiences"
            )
    
    # Education Methods
    def add_education(self, db: Session, user_token: str, education_data: EducationCreate) -> EducationResponse:
        """Add education to profile."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            profile = self.profile_repo.get_profile_by_user_id(db, user_id)
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profile not found"
                )
            
            education = self.profile_repo.add_education(db, profile.id, education_data)
            return EducationResponse.model_validate(education)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error adding education: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add education"
            )
    
    def update_education(self, db: Session, user_token: str, education_id: int, education_data: Dict[str, Any]) -> EducationResponse:
        """Update education."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            profile = self.profile_repo.get_profile_by_user_id(db, user_id)
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profile not found"
                )
            
            updated_education = self.profile_repo.update_education(db, education_id, education_data)
            if not updated_education:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Education not found"
                )
            
            return EducationResponse.model_validate(updated_education)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating education: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update education"
            )
    
    def delete_education(self, db: Session, user_token: str, education_id: int) -> MessageResponse:
        """Delete education."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            profile = self.profile_repo.get_profile_by_user_id(db, user_id)
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profile not found"
                )
            
            success = self.profile_repo.delete_education(db, education_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Education not found"
                )
            
            return MessageResponse(message="Education deleted successfully")
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting education: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete education"
            )
    
    # Skill Methods
    def add_skill(self, db: Session, user_token: str, skill_name: str, proficiency_level: str, years_of_experience: Optional[int] = None) -> UserSkillResponse:
        """Add skill to profile."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            profile = self.profile_repo.get_profile_by_user_id(db, user_id)
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profile not found"
                )
            
            # Get or create skill
            skill = self.profile_repo.get_or_create_skill(db, skill_name)
            
            # Create user skill
            skill_data = UserSkillCreate(
                skill_id=skill.id,
                proficiency_level=proficiency_level,
                years_of_experience=years_of_experience
            )
            
            user_skill = self.profile_repo.add_user_skill(db, profile.id, skill_data)
            return UserSkillResponse.model_validate(user_skill)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error adding skill: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add skill"
            )
    
    def search_skills(self, db: Session, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search available skills."""
        try:
            skills = self.profile_repo.search_skills(db, query, limit)
            return [{"id": skill.id, "name": skill.name, "category": skill.category} for skill in skills]
        except Exception as e:
            logger.error(f"Error searching skills: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to search skills"
            )
    
    # Language Methods
    def add_language(self, db: Session, user_token: str, language_name: str, proficiency_level: str) -> UserLanguageResponse:
        """Add language to profile."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            profile = self.profile_repo.get_profile_by_user_id(db, user_id)
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profile not found"
                )
            
            # Get or create language
            language = self.profile_repo.get_or_create_language(db, language_name)
            
            # Create user language
            language_data = UserLanguageCreate(
                language_id=language.id,
                proficiency_level=proficiency_level
            )
            
            user_language = self.profile_repo.add_user_language(db, profile.id, language_data)
            return UserLanguageResponse.model_validate(user_language)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error adding language: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add language"
            )
    
    def search_languages(self, db: Session, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search available languages."""
        try:
            languages = self.profile_repo.search_languages(db, query, limit)
            return [{"id": lang.id, "name": lang.name, "code": lang.code} for lang in languages]
        except Exception as e:
            logger.error(f"Error searching languages: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to search languages"
            )
    
    # Salary Methods
    def add_salary_entry(self, db: Session, user_token: str, salary_data: SalaryEntryCreate) -> SalaryEntryResponse:
        """Add salary entry to profile."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            profile = self.profile_repo.get_profile_by_user_id(db, user_id)
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profile not found"
                )
            
            salary_entry = self.profile_repo.add_salary_entry(db, profile.id, salary_data)
            return SalaryEntryResponse.model_validate(salary_entry)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error adding salary entry: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add salary entry"
            )
    
    def get_salary_entries(self, db: Session, user_token: str) -> List[SalaryEntryResponse]:
        """Get user's salary entries."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            profile = self.profile_repo.get_profile_by_user_id(db, user_id)
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profile not found"
                )
            
            entries = self.profile_repo.get_salary_entries_by_profile(db, profile.id)
            return [SalaryEntryResponse.model_validate(entry) for entry in entries]
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting salary entries: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get salary entries"
            )
            
  

    def get_profile_with_salary_comparison(self, db: Session, user_token: str) -> Dict[str, Any]:
        """Get profile with integrated salary comparison data."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            # Get profile
            profile = self.profile_repo.get_profile_by_user_id(db, user_id)
            if not profile:
                # Create default profile if doesn't exist
                from ..models.schemas import JobProfileCreate
                profile = self.profile_repo.create_profile(db, JobProfileCreate(), user_id)
            
            # Get basic profile data
            profile_data = JobProfileResponse.model_validate(profile)
            
            # Get salary comparison if work experience exists
            salary_comparison = None
            if profile.work_experiences:
                try:
                    current_experience = next(
                        (exp for exp in profile.work_experiences if exp.is_current), 
                        profile.work_experiences[0]
                    )
                    
                    if current_experience:
                        from datetime import datetime
                        start_date = current_experience.start_date
                        years_of_experience = (datetime.utcnow() - start_date).days // 365 if start_date else 0
                        
                        from ..models.schemas import SalaryComparisonRequest
                        from ..services.salary_service import SalaryService
                        
                        comparison_request = SalaryComparisonRequest(
                            job_title=current_experience.job_title,
                            location=profile.location or current_experience.location,
                            years_of_experience=years_of_experience
                        )
                        
                        salary_service = SalaryService()
                        salary_comparison = salary_service.compare_salary(db, comparison_request)
                except Exception as e:
                    logger.warning(f"Could not get salary comparison: {str(e)}")
            
            return {
                "profile": profile_data.dict(),
                "salary_comparison": salary_comparison,
                "has_sufficient_data": bool(profile.work_experiences),
                "next_steps": self._get_profile_next_steps(profile)
            }
            
        except Exception as e:
            logger.error(f"Error getting profile with salary comparison: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get profile data"
            )

    def _get_profile_next_steps(self, profile) -> List[str]:
        """Get recommended next steps for profile completion."""
        steps = []
        
        if not profile.work_experiences:
            steps.append("Add work experience to get salary comparisons")
        
        if not profile.professional_summary:
            steps.append("Add professional summary to improve recommendations")
        
        if not profile.skills:
            steps.append("Add skills to match with relevant jobs")
        
        if not profile.educations:
            steps.append("Add education information")
        
        if profile.profile_completion < 80:
            steps.append("Complete your profile to get better job matches")
        
        return steps