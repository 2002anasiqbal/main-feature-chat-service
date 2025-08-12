# File: job-service/src/models/cv_models.py

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.database import Base
import enum

class CVTemplate(enum.Enum):
    MODERN = "modern"
    CLASSIC = "classic"
    CREATIVE = "creative"
    MINIMAL = "minimal"

class CVStatus(enum.Enum):
    DRAFT = "draft"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class CV(Base):
    __tablename__ = 'cvs'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)  # User ID from auth service
    
    # CV Metadata
    title = Column(String(255), nullable=False)
    template = Column(Enum(CVTemplate), default=CVTemplate.MODERN)
    status = Column(Enum(CVStatus), default=CVStatus.DRAFT)
    
    # File information
    file_path = Column(String(500), nullable=True)  # Generated PDF path
    file_size = Column(Integer, nullable=True)
    
    # CV Data (JSON structure for flexibility)
    cv_data = Column(JSON, nullable=True)
    
    # Settings
    is_public = Column(Boolean, default=False)
    allow_downloads = Column(Boolean, default=True)
    
    # Analytics
    view_count = Column(Integer, default=0)
    download_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_generated_at = Column(DateTime, nullable=True)

class UploadedCV(Base):
    __tablename__ = 'uploaded_cvs'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)  # User ID from auth service
    
    # File information
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String(10), nullable=False)  # pdf, doc, docx
    
    # Metadata
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    is_primary = Column(Boolean, default=False)  # Primary CV for applications
    
    # Analytics
    download_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())