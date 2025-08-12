# File: job-service/src/models/recommendation_models.py

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.database import Base
import enum

class RecommendationAlgorithm(enum.Enum):
    CONTENT_BASED = "content_based"
    COLLABORATIVE = "collaborative"
    HYBRID = "hybrid"
    LOCATION_BASED = "location_based"

class JobRecommendation(Base):
    __tablename__ = 'job_recommendations'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    
    # Recommendation scoring
    score = Column(Float, nullable=False)
    algorithm_used = Column(Enum(RecommendationAlgorithm), nullable=False)
    reason = Column(String(500), nullable=True)
    
    # User interaction tracking
    is_viewed = Column(Boolean, default=False)
    is_clicked = Column(Boolean, default=False)
    is_applied = Column(Boolean, default=False)
    is_dismissed = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    viewed_at = Column(DateTime, nullable=True)
    clicked_at = Column(DateTime, nullable=True)
    applied_at = Column(DateTime, nullable=True)
    dismissed_at = Column(DateTime, nullable=True)
    
    # Relationships
    job = relationship("Job")

class UserJobPreferences(Base):
    __tablename__ = 'user_job_preferences'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, nullable=False, index=True)
    
    # Preferred job criteria
    preferred_job_titles = Column(JSON, nullable=True)  # Array of job titles
    preferred_locations = Column(JSON, nullable=True)   # Array of locations
    preferred_job_types = Column(JSON, nullable=True)   # Array of job types
    preferred_experience_levels = Column(JSON, nullable=True)
    
    # Salary preferences
    min_salary = Column(Float, nullable=True)
    max_salary = Column(Float, nullable=True)
    salary_currency = Column(String(3), default="USD")
    
    # Work preferences
    remote_preference = Column(String(20), default="no_preference")  # remote_only, hybrid, office_only, no_preference
    preferred_company_sizes = Column(JSON, nullable=True)
    preferred_industries = Column(JSON, nullable=True)
    
    # Notification preferences
    email_notifications = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=True)
    notification_frequency = Column(String(20), default="daily")  # daily, weekly, monthly
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class JobAlert(Base):
    __tablename__ = 'job_alerts'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Alert criteria
    alert_name = Column(String(255), nullable=False)
    search_criteria = Column(JSON, nullable=False)  # Store search parameters
    
    # Alert settings
    is_active = Column(Boolean, default=True)
    notification_method = Column(String(20), default="email")  # email, push, both
    frequency = Column(String(20), default="daily")  # daily, weekly, monthly
    
    # Statistics
    total_jobs_sent = Column(Integer, default=0)
    last_sent_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())