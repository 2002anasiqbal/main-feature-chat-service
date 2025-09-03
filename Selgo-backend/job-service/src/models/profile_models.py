# File: job-service/src/models/profile_models.py

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.database import Base
import enum

class ProficiencyLevel(enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"  
    ADVANCED = "advanced"
    FLUENT = "fluent"
    NATIVE = "native"

class JobProfile(Base):
    __tablename__ = 'job_profiles'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, nullable=False, index=True)  # User ID from auth service
    
    # Contact Information
    phone = Column(String(20), nullable=True)
    location = Column(String(255), nullable=True)
    website = Column(String(500), nullable=True)
    linkedin_url = Column(String(500), nullable=True)
    github_url = Column(String(500), nullable=True)
    
    # Professional Summary
    professional_summary = Column(Text, nullable=True)
    
    # Job Preferences
    desired_job_title = Column(String(255), nullable=True)
    desired_salary_min = Column(Float, nullable=True)
    desired_salary_max = Column(Float, nullable=True)
    salary_currency = Column(String(3), default="USD")
    willing_to_relocate = Column(Boolean, default=False)
    available_from = Column(DateTime, nullable=True)
    
    # Profile Settings
    profile_visibility = Column(String(20), default="private")  # public, private, recruiter_only
    allow_contact = Column(Boolean, default=True)
    receive_job_alerts = Column(Boolean, default=True)
    profile_completion = Column(Integer, default=0)  # Percentage
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    work_experiences = relationship("WorkExperience", back_populates="profile")
    educations = relationship("Education", back_populates="profile")
    skills = relationship("UserSkill", back_populates="profile")
    languages = relationship("UserLanguage", back_populates="profile")
    salary_entries = relationship("SalaryEntry", back_populates="profile")

class WorkExperience(Base):
    __tablename__ = 'work_experiences'
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey('job_profiles.id'), nullable=False)
    
    # Job details
    job_title = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=False)
    company_website = Column(String(500), nullable=True)
    location = Column(String(255), nullable=True)
    
    # Duration
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)  # Null for current job
    is_current = Column(Boolean, default=False)
    
    # Description
    description = Column(Text, nullable=True)
    achievements = Column(Text, nullable=True)
    
    # Display order
    display_order = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    profile = relationship("JobProfile", back_populates="work_experiences")

class Education(Base):
    __tablename__ = 'educations'
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey('job_profiles.id'), nullable=False)
    
    # Education details
    degree = Column(String(255), nullable=False)
    field_of_study = Column(String(255), nullable=True)
    institution = Column(String(255), nullable=False)
    location = Column(String(255), nullable=True)
    
    # Duration
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    is_current = Column(Boolean, default=False)
    
    # Additional info
    gpa = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    
    # Display order
    display_order = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    profile = relationship("JobProfile", back_populates="educations")

class Skill(Base):
    __tablename__ = 'skills'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    category = Column(String(50), nullable=True)  # technical, soft, language, etc.
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user_skills = relationship("UserSkill", back_populates="skill")

class UserSkill(Base):
    __tablename__ = 'user_skills'
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey('job_profiles.id'), nullable=False)
    skill_id = Column(Integer, ForeignKey('skills.id'), nullable=False)
    proficiency_level = Column(Enum(ProficiencyLevel), nullable=False)
    years_of_experience = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    profile = relationship("JobProfile", back_populates="skills")
    skill = relationship("Skill", back_populates="user_skills")

class Language(Base):
    __tablename__ = 'languages'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    code = Column(String(5), nullable=True)  # ISO language code
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user_languages = relationship("UserLanguage", back_populates="language")

class UserLanguage(Base):
    __tablename__ = 'user_languages'
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey('job_profiles.id'), nullable=False)
    language_id = Column(Integer, ForeignKey('languages.id'), nullable=False)
    proficiency_level = Column(Enum(ProficiencyLevel), nullable=False)
    
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    profile = relationship("JobProfile", back_populates="languages")
    language = relationship("Language", back_populates="user_languages")

class SalaryEntry(Base):
    __tablename__ = 'salary_entries'
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey('job_profiles.id'), nullable=False)
    
    # Salary information
    job_title = Column(String(255), nullable=False)
    annual_salary = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    
    # Additional compensation
    bonus = Column(Float, nullable=True)
    stock_options = Column(Float, nullable=True)
    other_compensation = Column(Float, nullable=True)
    
    # Context
    company_name = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    years_of_experience = Column(Integer, nullable=True)
    company_size = Column(String(50), nullable=True)
    industry = Column(String(100), nullable=True)
    
    # Metadata
    is_current = Column(Boolean, default=True)
    is_anonymous = Column(Boolean, default=True)  # For salary comparison
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    profile = relationship("JobProfile", back_populates="salary_entries")