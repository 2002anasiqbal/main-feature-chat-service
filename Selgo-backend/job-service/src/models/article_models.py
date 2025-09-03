# File: job-service/src/models/article_models.py
from sqlalchemy import Float, Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.database import Base
import enum

class ArticleCategory(Base):
    __tablename__ = 'article_categories'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    articles = relationship("Article", back_populates="category")

class Article(Base):
    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Article content
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    excerpt = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    
    # Media
    featured_image = Column(String(500), nullable=True)
    image_alt = Column(String(255), nullable=True)
    
    # Categorization
    category_id = Column(Integer, ForeignKey('article_categories.id'), nullable=True)
    tags = Column(JSON, nullable=True)  # Array of tags
    
    # SEO
    meta_title = Column(String(255), nullable=True)
    meta_description = Column(Text, nullable=True)
    
    # Publishing
    status = Column(String(20), default="draft")  # draft, published, archived
    published_at = Column(DateTime, nullable=True)
    author_id = Column(Integer, nullable=False)  # User ID from auth service
    
    # Analytics
    view_count = Column(Integer, default=0)
    reading_time = Column(Integer, nullable=True)  # In minutes
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    category = relationship("ArticleCategory", back_populates="articles")

class PopularSearch(Base):
    __tablename__ = 'popular_searches'
    
    id = Column(Integer, primary_key=True, index=True)
    search_term = Column(String(255), nullable=False)
    search_type = Column(String(50), nullable=False)  # position, location, article
    search_count = Column(Integer, default=1)
    last_searched = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    
    # Display settings
    is_featured = Column(Boolean, default=False)
    display_order = Column(Integer, default=0)