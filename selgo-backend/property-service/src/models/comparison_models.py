# property-service/src/models/comparison_models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from .models import Base

class PropertyComparisonSession(Base):
    __tablename__ = "property_comparison_sessions"
    __table_args__ = {'extend_existing': True}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    session_id = Column(String(255), nullable=True)
    comparison_name = Column(String(255), nullable=True)
    is_saved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    comparison_items = relationship("PropertyComparisonItem", back_populates="session", cascade="all, delete-orphan")
    comparison_notes = relationship("PropertyComparisonNote", back_populates="session", cascade="all, delete-orphan")

class PropertyComparisonItem(Base):
    __tablename__ = "property_comparison_items"
    __table_args__ = {'extend_existing': True}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("property_comparison_sessions.id", ondelete="CASCADE"))
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"))
    sort_order = Column(Integer, default=0)
    is_favorite = Column(Boolean, default=False)
    user_rating = Column(Integer, nullable=True)  # 1-5 stars
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship("PropertyComparisonSession", back_populates="comparison_items")
    property = relationship("Property")

class PropertyComparisonNote(Base):
    __tablename__ = "property_comparison_notes"
    __table_args__ = {'extend_existing': True}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("property_comparison_sessions.id", ondelete="CASCADE"))
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"))
    note_text = Column(Text, nullable=False)
    note_category = Column(String(100), nullable=True)  # pros, cons, questions, general
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    session = relationship("PropertyComparisonSession", back_populates="comparison_notes")
    property = relationship("Property")

class PropertyComparisonCriteria(Base):
    __tablename__ = "property_comparison_criteria"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    criteria_name = Column(String(100), nullable=False)
    criteria_type = Column(String(50), nullable=False)  # numeric, boolean, text, rating
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)