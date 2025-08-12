# File: job-service/src/models/job_models.py

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.database import Base
import enum
# Add missing imports for relationships
from .analytics_models import JobAnalytics, UserJobInteraction

class CompanyFollow(Base):
    __tablename__ = 'company_follows'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    followed_at = Column(DateTime, default=func.now())
    
    # Relationships
    company = relationship("Company", backref="followers")

class JobType(enum.Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time" 
    CONTRACT = "contract"
    TEMPORARY = "temporary"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"

class ExperienceLevel(enum.Enum):
    ENTRY = "entry"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    EXECUTIVE = "executive"

class JobStatus(enum.Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    DRAFT = "draft"
    PAUSED = "paused"

class Company(Base):
    __tablename__ = 'companies'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    website = Column(String(500), nullable=True)
    logo_url = Column(String(500), nullable=True)
    industry = Column(String(100), nullable=True)
    size = Column(String(50), nullable=True)  # "1-10", "11-50", etc.
    location = Column(String(255), nullable=True)
    founded_year = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    jobs = relationship("Job", back_populates="company")

class JobCategory(Base):
    __tablename__ = 'job_categories'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    parent_id = Column(Integer, ForeignKey('job_categories.id'), nullable=True)
    is_active = Column(Boolean, default=True)
    icon = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    parent = relationship("JobCategory", remote_side=[id], backref="children")
    jobs = relationship("Job", back_populates="category")

class Job(Base):
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    short_description = Column(Text, nullable=True)
    requirements = Column(Text, nullable=True)
    responsibilities = Column(Text, nullable=True)
    benefits = Column(Text, nullable=True)
    
    # Job details
    job_type = Column(Enum(JobType), nullable=False)
    experience_level = Column(Enum(ExperienceLevel), nullable=False)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    salary_currency = Column(String(3), default="USD")
    is_salary_negotiable = Column(Boolean, default=False)
    
    # Location
    location = Column(String(255), nullable=True)
    is_remote = Column(Boolean, default=False)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    
    # Application details
    application_deadline = Column(DateTime, nullable=True)
    application_email = Column(String(255), nullable=True)
    application_url = Column(String(500), nullable=True)
    contact_person = Column(String(255), nullable=True)
    contact_phone = Column(String(20), nullable=True)
    
    # Metadata
    status = Column(Enum(JobStatus), default=JobStatus.ACTIVE)
    featured = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    application_count = Column(Integer, default=0)
    tags = Column(JSON, nullable=True)  # Skills/tags as JSON array
    
    # Foreign keys
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('job_categories.id'), nullable=True)
    posted_by = Column(Integer, nullable=False)  # User ID from auth service
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    published_at = Column(DateTime, nullable=True)
    
    # Relationships
    company = relationship("Company", back_populates="jobs")
    category = relationship("JobCategory", back_populates="jobs")
    applications = relationship("JobApplication", back_populates="job")
    views = relationship("JobView", back_populates="job")
    analytics = relationship("JobAnalytics", back_populates="job")
    interactions = relationship("UserJobInteraction", back_populates="job")

class JobApplication(Base):
    __tablename__ = 'job_applications'
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    user_id = Column(Integer, nullable=False)  # User ID from auth service
    
    # Application data
    cover_letter = Column(Text, nullable=True)
    cv_file_path = Column(String(500), nullable=True)
    additional_info = Column(Text, nullable=True)
    
    # Status tracking
    status = Column(String(50), default="submitted")  # submitted, reviewed, interview, rejected, hired
    applied_at = Column(DateTime, default=func.now())
    reviewed_at = Column(DateTime, nullable=True)
    
    # Relationships
    job = relationship("Job", back_populates="applications")

class JobView(Base):
    __tablename__ = 'job_views'
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    user_id = Column(Integer, nullable=True)  # Nullable for anonymous views
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    viewed_at = Column(DateTime, default=func.now())
    
    # Relationships
    job = relationship("Job", back_populates="views")

class SavedJob(Base):
    __tablename__ = 'saved_jobs'
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    user_id = Column(Integer, nullable=False)  # User ID from auth service
    saved_at = Column(DateTime, default=func.now())
    
    # Add unique constraint in migration
    __table_args__ = {'sqlite_autoincrement': True}