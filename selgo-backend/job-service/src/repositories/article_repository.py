# File: job-service/src/repositories/article_repository.py

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, and_, or_, func
from typing import Optional, List, Dict, Any, Tuple
from ..models.article_models import Article, ArticleCategory, PopularSearch
from ..models.schemas import ArticleCreate, ArticleUpdate, ArticleCategoryCreate
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class ArticleRepository:
    
    def create_article(self, db: Session, article_data: ArticleCreate, author_id: int) -> Article:
        """Create a new article."""
        db_article = Article(
            **article_data.dict(),
            author_id=author_id
        )
        db.add(db_article)
        db.commit()
        db.refresh(db_article)
        
        logger.info(f"Created article: {db_article.id} - {db_article.title}")
        return db_article
    
    def get_article_by_id(self, db: Session, article_id: int) -> Optional[Article]:
        """Get article by ID."""
        return db.query(Article).options(
            joinedload(Article.category)
        ).filter(Article.id == article_id).first()
    
    def get_article_by_slug(self, db: Session, slug: str) -> Optional[Article]:
        """Get article by slug."""
        return db.query(Article).options(
            joinedload(Article.category)
        ).filter(Article.slug == slug).first()
    
    def get_published_articles(self, db: Session, category_id: Optional[int] = None, 
                             limit: int = 20, offset: int = 0) -> Tuple[List[Article], int]:
        """Get published articles with pagination."""
        query = db.query(Article).options(
            joinedload(Article.category)
        ).filter(Article.status == "published")
        
        if category_id:
            query = query.filter(Article.category_id == category_id)
        
        total = query.count()
        articles = query.order_by(desc(Article.published_at)).offset(offset).limit(limit).all()
        
        return articles, total
    
    def get_featured_articles(self, db: Session, limit: int = 6) -> List[Article]:
        """Get featured articles for homepage."""
        return db.query(Article).options(
            joinedload(Article.category)
        ).filter(
            Article.status == "published",
            Article.featured_image.isnot(None)
        ).order_by(desc(Article.view_count)).limit(limit).all()
    
    def search_articles(self, db: Session, query_text: str, limit: int = 20, offset: int = 0) -> Tuple[List[Article], int]:
        """Search articles by title and content."""
        search_term = f"%{query_text}%"
        query = db.query(Article).options(
            joinedload(Article.category)
        ).filter(
            Article.status == "published",
            or_(
                Article.title.ilike(search_term),
                Article.content.ilike(search_term),
                Article.excerpt.ilike(search_term)
            )
        )
        
        total = query.count()
        articles = query.order_by(desc(Article.published_at)).offset(offset).limit(limit).all()
        
        return articles, total
    
    def update_article(self, db: Session, article_id: int, article_data: ArticleUpdate) -> Optional[Article]:
        """Update article."""
        db_article = db.query(Article).filter(Article.id == article_id).first()
        if not db_article:
            return None
        
        update_data = article_data.dict(exclude_unset=True)
        if update_data:
            for field, value in update_data.items():
                setattr(db_article, field, value)
            
            db_article.updated_at = datetime.utcnow()
            
            # Set published_at if status is being changed to published
            if update_data.get("status") == "published" and not db_article.published_at:
                db_article.published_at = datetime.utcnow()
            
            db.commit()
            db.refresh(db_article)
        
        return db_article
    
    def delete_article(self, db: Session, article_id: int) -> bool:
        """Delete article."""
        db_article = db.query(Article).filter(Article.id == article_id).first()
        if db_article:
            db.delete(db_article)
            db.commit()
            return True
        return False
    
    def increment_article_view_count(self, db: Session, article_id: int) -> None:
        """Increment article view count."""
        db.query(Article).filter(Article.id == article_id).update({
            Article.view_count: Article.view_count + 1
        })
        db.commit()
    
    # Category Methods
    def create_category(self, db: Session, category_data: ArticleCategoryCreate) -> ArticleCategory:
        """Create article category."""
        db_category = ArticleCategory(**category_data.dict())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    
    def get_categories(self, db: Session) -> List[ArticleCategory]:
        """Get all active article categories."""
        return db.query(ArticleCategory).filter(
            ArticleCategory.is_active == True
        ).order_by(ArticleCategory.display_order).all()
    
    def get_category_by_id(self, db: Session, category_id: int) -> Optional[ArticleCategory]:
        """Get category by ID."""
        return db.query(ArticleCategory).filter(ArticleCategory.id == category_id).first()
    
    def get_category_by_slug(self, db: Session, slug: str) -> Optional[ArticleCategory]:
        """Get category by slug."""
        return db.query(ArticleCategory).filter(ArticleCategory.slug == slug).first()
    
    # Popular Search Methods
    def record_search(self, db: Session, search_term: str, search_type: str) -> None:
        """Record or update search term."""
        existing = db.query(PopularSearch).filter(
            PopularSearch.search_term == search_term,
            PopularSearch.search_type == search_type
        ).first()
        
        if existing:
            existing.search_count += 1
            existing.last_searched = datetime.utcnow()
        else:
            new_search = PopularSearch(
                search_term=search_term,
                search_type=search_type,
                search_count=1
            )
            db.add(new_search)
        
        db.commit()
    
    def get_popular_searches_by_type(self, db: Session, search_type: str, limit: int = 5) -> List[str]:
        """Get popular searches by type."""
        searches = db.query(PopularSearch).filter(
            PopularSearch.search_type == search_type
        ).order_by(desc(PopularSearch.search_count)).limit(limit).all()
        
        return [search.search_term for search in searches]
    
    def get_popular_searches_grouped(self, db: Session) -> Dict[str, List[str]]:
        """Get popular searches grouped by type."""
        return {
            "positions": self.get_popular_searches_by_type(db, "position", 5),
            "locations": self.get_popular_searches_by_type(db, "location", 5),
            "articles": self.get_popular_searches_by_type(db, "article", 5)
        }
    
    def get_trending_articles(self, db: Session, days: int = 7, limit: int = 10) -> List[Article]:
        """Get trending articles based on recent views."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        return db.query(Article).options(
            joinedload(Article.category)
        ).filter(
            Article.status == "published",
            Article.updated_at >= cutoff_date
        ).order_by(desc(Article.view_count)).limit(limit).all()