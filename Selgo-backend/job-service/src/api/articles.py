# File: job-service/src/api/articles.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from ..database.database import get_db
from ..services.article_service import ArticleService
from ..models.schemas import (
    ArticleResponse, ArticleCategoryResponse, PopularSearchesGrouped
)

router = APIRouter()
article_service = ArticleService()

@router.get("/", response_model=Dict[str, Any])
def get_articles(
    category_id: Optional[int] = Query(None, description="Filter by category"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Get published articles with pagination (Useful Articles feature)."""
    return article_service.get_articles(db, category_id, page, limit)

@router.get("/featured", response_model=List[ArticleResponse])
def get_featured_articles(
    limit: int = Query(6, ge=1, le=20, description="Number of featured articles"),
    db: Session = Depends(get_db)
):
    """Get featured articles for homepage."""
    return article_service.get_featured_articles(db, limit)

@router.get("/trending", response_model=List[ArticleResponse])
def get_trending_articles(
    days: int = Query(7, ge=1, le=30, description="Trending period in days"),
    limit: int = Query(10, ge=1, le=50, description="Number of trending articles"),
    db: Session = Depends(get_db)
):
    """Get trending articles."""
    return article_service.get_trending_articles(db, days, limit)

@router.get("/search", response_model=Dict[str, Any])
def search_articles(
    q: str = Query(..., description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Search articles."""
    return article_service.search_articles(db, q, page, limit)

@router.get("/categories", response_model=List[ArticleCategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """Get all article categories."""
    return article_service.get_categories(db)

@router.get("/popular-searches", response_model=PopularSearchesGrouped)
def get_popular_searches(db: Session = Depends(get_db)):
    """Get popular searches grouped by type (Popular Searches feature)."""
    return article_service.get_popular_searches(db)

@router.get("/{article_id}", response_model=ArticleResponse)
def get_article_by_id(
    article_id: int,
    db: Session = Depends(get_db)
):
    """Get article by ID and increment view count."""
    return article_service.get_article_by_id(db, article_id)

@router.get("/slug/{slug}", response_model=ArticleResponse)
def get_article_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    """Get article by slug and increment view count."""
    return article_service.get_article_by_slug(db, slug)