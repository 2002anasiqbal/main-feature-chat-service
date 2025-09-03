# File: job-service/src/services/article_service.py

from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any, Tuple
from ..repositories.article_repository import ArticleRepository
from ..models.schemas import (
    ArticleCreate, ArticleUpdate, ArticleResponse,
    ArticleCategoryResponse, PopularSearchesGrouped,
    MessageResponse
)
from ..utils.auth_utils import get_user_from_token
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

class ArticleService:
    def __init__(self):
        self.article_repo = ArticleRepository()
    
    def get_articles(self, db: Session, category_id: Optional[int] = None, 
                    page: int = 1, limit: int = 20) -> Dict[str, Any]:
        """Get published articles with pagination."""
        try:
            offset = (page - 1) * limit
            articles, total = self.article_repo.get_published_articles(
                db, category_id, limit, offset
            )
            
            total_pages = (total + limit - 1) // limit
            
            return {
                "articles": [ArticleResponse.model_validate(article) for article in articles],
                "total": total,
                "page": page,
                "limit": limit,
                "total_pages": total_pages
            }
            
        except Exception as e:
            logger.error(f"Error getting articles: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get articles"
            )
    
    def get_article_by_id(self, db: Session, article_id: int) -> ArticleResponse:
        """Get article by ID and increment view count."""
        try:
            article = self.article_repo.get_article_by_id(db, article_id)
            if not article:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Article not found"
                )
            
            # Increment view count
            self.article_repo.increment_article_view_count(db, article_id)
            
            return ArticleResponse.model_validate(article)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting article: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get article"
            )
    
    def get_article_by_slug(self, db: Session, slug: str) -> ArticleResponse:
        """Get article by slug and increment view count."""
        try:
            article = self.article_repo.get_article_by_slug(db, slug)
            if not article:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Article not found"
                )
            
            # Increment view count
            self.article_repo.increment_article_view_count(db, article.id)
            
            return ArticleResponse.model_validate(article)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting article: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get article"
            )
    
    def get_featured_articles(self, db: Session, limit: int = 6) -> List[ArticleResponse]:
        """Get featured articles for homepage."""
        try:
            articles = self.article_repo.get_featured_articles(db, limit)
            return [ArticleResponse.model_validate(article) for article in articles]
        except Exception as e:
            logger.error(f"Error getting featured articles: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get featured articles"
            )
    
    def search_articles(self, db: Session, query: str, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        """Search articles."""
        try:
            offset = (page - 1) * limit
            articles, total = self.article_repo.search_articles(db, query, limit, offset)
            
            # Record search
            self.article_repo.record_search(db, query, "article")
            
            total_pages = (total + limit - 1) // limit
            
            return {
                "articles": [ArticleResponse.model_validate(article) for article in articles],
                "total": total,
                "page": page,
                "limit": limit,
                "total_pages": total_pages,
                "query": query
            }
            
        except Exception as e:
            logger.error(f"Error searching articles: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to search articles"
            )
    
    def get_categories(self, db: Session) -> List[ArticleCategoryResponse]:
        """Get all article categories."""
        try:
            categories = self.article_repo.get_categories(db)
            return [ArticleCategoryResponse.model_validate(cat) for cat in categories]
        except Exception as e:
            logger.error(f"Error getting categories: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get categories"
            )
    
    def get_popular_searches(self, db: Session) -> PopularSearchesGrouped:
        """Get popular searches grouped by type."""
        try:
            searches = self.article_repo.get_popular_searches_grouped(db)
            return PopularSearchesGrouped(**searches)
        except Exception as e:
            logger.error(f"Error getting popular searches: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get popular searches"
            )
    
    def get_trending_articles(self, db: Session, days: int = 7, limit: int = 10) -> List[ArticleResponse]:
        """Get trending articles."""
        try:
            articles = self.article_repo.get_trending_articles(db, days, limit)
            return [ArticleResponse.model_validate(article) for article in articles]
        except Exception as e:
            logger.error(f"Error getting trending articles: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get trending articles"
            )