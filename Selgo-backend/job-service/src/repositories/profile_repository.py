# File: job-service/src/repositories/profile_repository.py

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, and_, func
from typing import Optional, List, Dict, Any
from ..models.profile_models import (
    JobProfile, WorkExperience, Education, Skill, UserSkill, 
    Language, UserLanguage, SalaryEntry
)
from ..models.schemas import (
    JobProfileCreate, JobProfileUpdate, WorkExperienceCreate, 
    EducationCreate, UserSkillCreate, UserLanguageCreate, SalaryEntryCreate
)
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ProfileRepository:
    
    def create_profile(self, db: Session, profile_data: JobProfileCreate, user_id: int) -> JobProfile:
        """Create a new job profile."""
        db_profile = JobProfile(
            **profile_data.dict(),
            user_id=user_id
        )
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        
        # Calculate initial profile completion
        self._update_profile_completion(db, db_profile.id)
        
        logger.info(f"Created job profile for user: {user_id}")
        return db_profile
    
    def get_profile_by_user_id(self, db: Session, user_id: int) -> Optional[JobProfile]:
        """Get job profile by user ID with all related data."""
        return db.query(JobProfile).options(
            joinedload(JobProfile.work_experiences),
            joinedload(JobProfile.educations),
            joinedload(JobProfile.skills).joinedload(UserSkill.skill),
            joinedload(JobProfile.languages).joinedload(UserLanguage.language),
            joinedload(JobProfile.salary_entries)
        ).filter(JobProfile.user_id == user_id).first()
    
    def get_profile_by_id(self, db: Session, profile_id: int) -> Optional[JobProfile]:
        """Get job profile by ID."""
        return db.query(JobProfile).options(
            joinedload(JobProfile.work_experiences),
            joinedload(JobProfile.educations),
            joinedload(JobProfile.skills).joinedload(UserSkill.skill),
            joinedload(JobProfile.languages).joinedload(UserLanguage.language)
        ).filter(JobProfile.id == profile_id).first()
    
    def update_profile(self, db: Session, user_id: int, profile_data: JobProfileUpdate) -> Optional[JobProfile]:
        """Update job profile."""
        db_profile = db.query(JobProfile).filter(JobProfile.user_id == user_id).first()
        if not db_profile:
            return None
        
        update_data = profile_data.dict(exclude_unset=True)
        if update_data:
            for field, value in update_data.items():
                setattr(db_profile, field, value)
            
            db_profile.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_profile)
            
            # Update profile completion
            self._update_profile_completion(db, db_profile.id)
        
        return db_profile
    
    def delete_profile(self, db: Session, user_id: int) -> bool:
        """Delete job profile."""
        db_profile = db.query(JobProfile).filter(JobProfile.user_id == user_id).first()
        if db_profile:
            db.delete(db_profile)
            db.commit()
            return True
        return False
    
    # Work Experience Methods
    def add_work_experience(self, db: Session, profile_id: int, experience_data: WorkExperienceCreate) -> WorkExperience:
        """Add work experience to profile."""
        db_experience = WorkExperience(
            **experience_data.dict(),
            profile_id=profile_id
        )
        db.add(db_experience)
        db.commit()
        db.refresh(db_experience)
        
        # Update profile completion
        self._update_profile_completion(db, profile_id)
        
        return db_experience
    
    def update_work_experience(self, db: Session, experience_id: int, experience_data: Dict[str, Any]) -> Optional[WorkExperience]:
        """Update work experience."""
        db_experience = db.query(WorkExperience).filter(WorkExperience.id == experience_id).first()
        if not db_experience:
            return None
        
        for field, value in experience_data.items():
            setattr(db_experience, field, value)
        
        db.commit()
        db.refresh(db_experience)
        
        # Update profile completion
        self._update_profile_completion(db, db_experience.profile_id)
        
        return db_experience
    
    def delete_work_experience(self, db: Session, experience_id: int) -> bool:
        """Delete work experience."""
        db_experience = db.query(WorkExperience).filter(WorkExperience.id == experience_id).first()
        if db_experience:
            profile_id = db_experience.profile_id
            db.delete(db_experience)
            db.commit()
            
            # Update profile completion
            self._update_profile_completion(db, profile_id)
            return True
        return False
    
    def get_work_experiences_by_profile(self, db: Session, profile_id: int) -> List[WorkExperience]:
        """Get work experiences for profile."""
        return db.query(WorkExperience).filter(
            WorkExperience.profile_id == profile_id
        ).order_by(desc(WorkExperience.start_date)).all()
    
    # Education Methods
    def add_education(self, db: Session, profile_id: int, education_data: EducationCreate) -> Education:
        """Add education to profile."""
        db_education = Education(
            **education_data.dict(),
            profile_id=profile_id
        )
        db.add(db_education)
        db.commit()
        db.refresh(db_education)
        
        # Update profile completion
        self._update_profile_completion(db, profile_id)
        
        return db_education
    
    def update_education(self, db: Session, education_id: int, education_data: Dict[str, Any]) -> Optional[Education]:
        """Update education."""
        db_education = db.query(Education).filter(Education.id == education_id).first()
        if not db_education:
            return None
        
        for field, value in education_data.items():
            setattr(db_education, field, value)
        
        db.commit()
        db.refresh(db_education)
        
        # Update profile completion
        self._update_profile_completion(db, db_education.profile_id)
        
        return db_education
    
    def delete_education(self, db: Session, education_id: int) -> bool:
        """Delete education."""
        db_education = db.query(Education).filter(Education.id == education_id).first()
        if db_education:
            profile_id = db_education.profile_id
            db.delete(db_education)
            db.commit()
            
            # Update profile completion
            self._update_profile_completion(db, profile_id)
            return True
        return False
    
    def get_educations_by_profile(self, db: Session, profile_id: int) -> List[Education]:
        """Get educations for profile."""
        return db.query(Education).filter(
            Education.profile_id == profile_id
        ).order_by(desc(Education.start_date)).all()
    
    # Skill Methods
    def get_or_create_skill(self, db: Session, skill_name: str, category: str = None) -> Skill:
        """Get existing skill or create new one."""
        skill = db.query(Skill).filter(Skill.name.ilike(skill_name)).first()
        if not skill:
            skill = Skill(name=skill_name, category=category)
            db.add(skill)
            db.commit()
            db.refresh(skill)
        return skill
    
    def add_user_skill(self, db: Session, profile_id: int, skill_data: UserSkillCreate) -> UserSkill:
        """Add skill to user profile."""
        # Check if skill already exists for this user
        existing = db.query(UserSkill).filter(
            UserSkill.profile_id == profile_id,
            UserSkill.skill_id == skill_data.skill_id
        ).first()
        
        if existing:
            # Update existing skill
            existing.proficiency_level = skill_data.proficiency_level
            existing.years_of_experience = skill_data.years_of_experience
            db.commit()
            db.refresh(existing)
            return existing
        
        db_user_skill = UserSkill(
            **skill_data.dict(),
            profile_id=profile_id
        )
        db.add(db_user_skill)
        db.commit()
        db.refresh(db_user_skill)
        
        # Update profile completion
        self._update_profile_completion(db, profile_id)
        
        return db_user_skill
    
    def update_user_skill(self, db: Session, user_skill_id: int, skill_data: Dict[str, Any]) -> Optional[UserSkill]:
        """Update user skill."""
        db_user_skill = db.query(UserSkill).filter(UserSkill.id == user_skill_id).first()
        if not db_user_skill:
            return None
        
        for field, value in skill_data.items():
            setattr(db_user_skill, field, value)
        
        db.commit()
        db.refresh(db_user_skill)
        return db_user_skill
    
    def delete_user_skill(self, db: Session, user_skill_id: int) -> bool:
        """Delete user skill."""
        db_user_skill = db.query(UserSkill).filter(UserSkill.id == user_skill_id).first()
        if db_user_skill:
            profile_id = db_user_skill.profile_id
            db.delete(db_user_skill)
            db.commit()
            
            # Update profile completion
            self._update_profile_completion(db, profile_id)
            return True
        return False
    
    def get_user_skills_by_profile(self, db: Session, profile_id: int) -> List[UserSkill]:
        """Get user skills for profile."""
        return db.query(UserSkill).options(
            joinedload(UserSkill.skill)
        ).filter(UserSkill.profile_id == profile_id).all()
    
    def search_skills(self, db: Session, query: str, limit: int = 10) -> List[Skill]:
        """Search skills by name."""
        return db.query(Skill).filter(
            Skill.name.ilike(f"%{query}%"),
            Skill.is_active == True
        ).limit(limit).all()
    
    # Language Methods
    def get_or_create_language(self, db: Session, language_name: str, code: str = None) -> Language:
        """Get existing language or create new one."""
        language = db.query(Language).filter(Language.name.ilike(language_name)).first()
        if not language:
            language = Language(name=language_name, code=code)
            db.add(language)
            db.commit()
            db.refresh(language)
        return language
    
    def add_user_language(self, db: Session, profile_id: int, language_data: UserLanguageCreate) -> UserLanguage:
        """Add language to user profile."""
        # Check if language already exists for this user
        existing = db.query(UserLanguage).filter(
            UserLanguage.profile_id == profile_id,
            UserLanguage.language_id == language_data.language_id
        ).first()
        
        if existing:
            # Update existing language
            existing.proficiency_level = language_data.proficiency_level
            db.commit()
            db.refresh(existing)
            return existing
        
        db_user_language = UserLanguage(
            **language_data.dict(),
            profile_id=profile_id
        )
        db.add(db_user_language)
        db.commit()
        db.refresh(db_user_language)
        
        # Update profile completion
        self._update_profile_completion(db, profile_id)
        
        return db_user_language
    
    def delete_user_language(self, db: Session, user_language_id: int) -> bool:
        """Delete user language."""
        db_user_language = db.query(UserLanguage).filter(UserLanguage.id == user_language_id).first()
        if db_user_language:
            profile_id = db_user_language.profile_id
            db.delete(db_user_language)
            db.commit()
            
            # Update profile completion
            self._update_profile_completion(db, profile_id)
            return True
        return False
    
    def get_user_languages_by_profile(self, db: Session, profile_id: int) -> List[UserLanguage]:
        """Get user languages for profile."""
        return db.query(UserLanguage).options(
            joinedload(UserLanguage.language)
        ).filter(UserLanguage.profile_id == profile_id).all()
    
    def search_languages(self, db: Session, query: str, limit: int = 10) -> List[Language]:
        """Search languages by name."""
        return db.query(Language).filter(
            Language.name.ilike(f"%{query}%"),
            Language.is_active == True
        ).limit(limit).all()
    
    # Salary Methods
    def add_salary_entry(self, db: Session, profile_id: int, salary_data: SalaryEntryCreate) -> SalaryEntry:
        """Add salary entry to profile."""
        db_salary = SalaryEntry(
            **salary_data.dict(),
            profile_id=profile_id
        )
        db.add(db_salary)
        db.commit()
        db.refresh(db_salary)
        return db_salary
    
    def update_salary_entry(self, db: Session, salary_id: int, salary_data: Dict[str, Any]) -> Optional[SalaryEntry]:
        """Update salary entry."""
        db_salary = db.query(SalaryEntry).filter(SalaryEntry.id == salary_id).first()
        if not db_salary:
            return None
        
        for field, value in salary_data.items():
            setattr(db_salary, field, value)
        
        db_salary.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_salary)
        return db_salary
    
    def delete_salary_entry(self, db: Session, salary_id: int) -> bool:
        """Delete salary entry."""
        db_salary = db.query(SalaryEntry).filter(SalaryEntry.id == salary_id).first()
        if db_salary:
            db.delete(db_salary)
            db.commit()
            return True
        return False
    
    def get_salary_entries_by_profile(self, db: Session, profile_id: int) -> List[SalaryEntry]:
        """Get salary entries for profile."""
        return db.query(SalaryEntry).filter(
            SalaryEntry.profile_id == profile_id
        ).order_by(desc(SalaryEntry.created_at)).all()
    
    def get_salary_comparison_data(self, db: Session, job_title: str, location: str = None, 
                                 years_of_experience: int = None, industry: str = None) -> Dict[str, Any]:
        """Get salary comparison data for analysis."""
        query = db.query(SalaryEntry).filter(
            SalaryEntry.job_title.ilike(f"%{job_title}%"),
            SalaryEntry.is_anonymous == True
        )
        
        if location:
            query = query.filter(SalaryEntry.location.ilike(f"%{location}%"))
        
        if years_of_experience is not None:
            # Allow ±2 years range
            query = query.filter(
                SalaryEntry.years_of_experience.between(
                    max(0, years_of_experience - 2),
                    years_of_experience + 2
                )
            )
        
        if industry:
            query = query.filter(SalaryEntry.industry.ilike(f"%{industry}%"))
        
        salaries = [entry.annual_salary for entry in query.all()]
        
        if not salaries:
            return {
                "total_entries": 0,
                "average_salary": 0,
                "median_salary": 0,
                "min_salary": 0,
                "max_salary": 0,
                "percentile_25": 0,
                "percentile_75": 0
            }
        
        salaries.sort()
        n = len(salaries)
        
        return {
            "total_entries": n,
            "average_salary": sum(salaries) / n,
            "median_salary": salaries[n // 2] if n % 2 == 1 else (salaries[n // 2 - 1] + salaries[n // 2]) / 2,
            "min_salary": min(salaries),
            "max_salary": max(salaries),
            "percentile_25": salaries[n // 4] if n >= 4 else salaries[0],
            "percentile_75": salaries[3 * n // 4] if n >= 4 else salaries[-1]
        }
    
    def _update_profile_completion(self, db: Session, profile_id: int) -> None:
        """Calculate and update profile completion percentage."""
        profile = db.query(JobProfile).filter(JobProfile.id == profile_id).first()
        if not profile:
            return
        
        completion_score = 0
        max_score = 100
        
        # Basic profile info (30 points)
        if profile.phone:
            completion_score += 5
        if profile.location:
            completion_score += 5
        if profile.professional_summary:
            completion_score += 10
        if profile.desired_job_title:
            completion_score += 5
        if profile.desired_salary_min or profile.desired_salary_max:
            completion_score += 5
        
        # Work experience (25 points)
        work_experiences = db.query(WorkExperience).filter(
            WorkExperience.profile_id == profile_id
        ).count()
        if work_experiences > 0:
            completion_score += min(25, work_experiences * 12)  # Up to 25 points
        
        # Education (20 points)
        educations = db.query(Education).filter(
            Education.profile_id == profile_id
        ).count()
        if educations > 0:
            completion_score += min(20, educations * 10)  # Up to 20 points
        
        # Skills (15 points)
        skills = db.query(UserSkill).filter(
            UserSkill.profile_id == profile_id
        ).count()
        if skills > 0:
            completion_score += min(15, skills * 3)  # Up to 15 points
        
        # Languages (10 points)
        languages = db.query(UserLanguage).filter(
            UserLanguage.profile_id == profile_id
        ).count()
        if languages > 0:
            completion_score += min(10, languages * 5)  # Up to 10 points
        
        # Ensure completion doesn't exceed 100%
        completion_percentage = min(100, completion_score)
        
        # Update profile
        profile.profile_completion = completion_percentage
        db.commit()