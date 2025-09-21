# File: job-service/src/models/analytics_models.py

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.database import Base
import enum

class JobAnalytics(Base):
    __tablename__ = 'job_analytics'
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    
    # Daily analytics
    date = Column(DateTime, nullable=False)
    views_count = Column(Integer, default=0)
    unique_views_count = Column(Integer, default=0)
    applications_count = Column(Integer, default=0)
    saves_count = Column(Integer, default=0)
    
    # User engagement
    avg_time_on_page = Column(Float, default=0.0)  # in seconds
    bounce_rate = Column(Float, default=0.0)  # percentage
    
    # Source tracking
    traffic_sources = Column(JSON, nullable=True)  # {source: count}
    
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    job = relationship("Job", back_populates="analytics")

class UserJobInteraction(Base):
    __tablename__ = 'user_job_interactions'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True, index=True)  # Nullable for anonymous users
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    
    # Interaction details
    interaction_type = Column(String(50), nullable=False)  # view, click, apply, save, share
    session_id = Column(String(255), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    referrer = Column(String(500), nullable=True)
    
    # Timing
    time_spent = Column(Integer, nullable=True)  # seconds spent on job page
    
    # Metadata
    additional_data = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    job = relationship("Job", back_populates="interactions")