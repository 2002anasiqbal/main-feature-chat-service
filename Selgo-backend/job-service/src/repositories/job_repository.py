# File: job-service/src/repositories/job_repository.py

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, asc, func, and_, or_
from typing import Optional, List, Dict, Any, Tuple
from ..models.job_models import Job, Company, JobCategory, JobApplication, JobView, SavedJob
from ..models.schemas import JobCreate, JobUpdate, JobSearchRequest
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class JobRepository:
    
    def create_job(self, db: Session, job_data: JobCreate, user_id: int) -> Job:
        """Create a new job posting."""
        # Generate slug from title
        slug = self._generate_slug(db, job_data.title)
        
        db_job = Job(
            **job_data.dict(),
            slug=slug,
            posted_by=user_id,
            published_at=datetime.utcnow()
        )
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        
        logger.info(f"Created job: {db_job.id} - {db_job.title}")
        return db_job
    
    def get_job_by_id(self, db: Session, job_id: int) -> Optional[Job]:
        """Get job by ID with company information."""
        return db.query(Job).options(
            joinedload(Job.company),
            joinedload(Job.category)
        ).filter(Job.id == job_id).first()
    
    def get_job_by_slug(self, db: Session, slug: str) -> Optional[Job]:
        """Get job by slug with company information."""
        return db.query(Job).options(
            joinedload(Job.company),
            joinedload(Job.category)
        ).filter(Job.slug == slug).first()
    
    def search_jobs(self, db: Session, search_params: JobSearchRequest) -> Tuple[List[Job], int]:
        """Search jobs with filtering, sorting, and pagination."""
        query = db.query(Job).options(
            joinedload(Job.company),
            joinedload(Job.category)
        )
        
        # Apply filters
        query = self._apply_search_filters(query, search_params)
        
        # Get total count before pagination
        total = query.count()
        
        # Apply sorting
        query = self._apply_sorting(query, search_params.sort_by, search_params.sort_order)
        
        # Apply pagination
        offset = (search_params.page - 1) * search_params.limit
        jobs = query.offset(offset).limit(search_params.limit).all()
        
        return jobs, total
    
    def get_featured_jobs(self, db: Session, limit: int = 10) -> List[Job]:
        """Get featured jobs."""
        return db.query(Job).options(
            joinedload(Job.company)
        ).filter(
            Job.featured == True,
            Job.status == "active"
        ).order_by(desc(Job.created_at)).limit(limit).all()
    
    def get_recent_jobs(self, db: Session, limit: int = 20) -> List[Job]:
        """Get recently posted jobs."""
        return db.query(Job).options(
            joinedload(Job.company)
        ).filter(
            Job.status == "active"
        ).order_by(desc(Job.created_at)).limit(limit).all()
    
    def get_jobs_by_company(self, db: Session, company_id: int, limit: int = 10) -> List[Job]:
        """Get jobs by company."""
        return db.query(Job).options(
            joinedload(Job.company)
        ).filter(
            Job.company_id == company_id,
            Job.status == "active"
        ).order_by(desc(Job.created_at)).limit(limit).all()
    
    def get_similar_jobs(self, db: Session, job: Job, limit: int = 5) -> List[Job]:
        """Get similar jobs based on category, location, and title."""
        query = db.query(Job).options(
            joinedload(Job.company)
        ).filter(
            Job.id != job.id,
            Job.status == "active"
        )
        
        # Prioritize same category
        if job.category_id:
            query = query.filter(Job.category_id == job.category_id)
        
        # Same location preference
        if job.location:
            query = query.filter(Job.location.ilike(f"%{job.location}%"))
        
        return query.order_by(desc(Job.created_at)).limit(limit).all()
    
    def update_job(self, db: Session, job_id: int, job_data: JobUpdate) -> Optional[Job]:
        """Update job posting."""
        db_job = db.query(Job).filter(Job.id == job_id).first()
        if not db_job:
            return None
        
        update_data = job_data.dict(exclude_unset=True)
        if update_data:
            for field, value in update_data.items():
                setattr(db_job, field, value)
            
            db_job.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_job)
        
        return db_job
    
    def delete_job(self, db: Session, job_id: int) -> bool:
        """Delete job posting."""
        db_job = db.query(Job).filter(Job.id == job_id).first()
        if db_job:
            db.delete(db_job)
            db.commit()
            return True
        return False
    
    def increment_view_count(self, db: Session, job_id: int, user_id: Optional[int] = None, ip_address: Optional[str] = None) -> None:
        """Increment job view count and track view."""
        # Check if this user/IP already viewed this job recently (within 24 hours)
        recent_view = None
        if user_id:
            recent_view = db.query(JobView).filter(
                JobView.job_id == job_id,
                JobView.user_id == user_id,
                JobView.viewed_at > datetime.utcnow() - timedelta(hours=24)
            ).first()
        elif ip_address:
            recent_view = db.query(JobView).filter(
                JobView.job_id == job_id,
                JobView.ip_address == ip_address,
                JobView.viewed_at > datetime.utcnow() - timedelta(hours=24)
            ).first()
        
        if not recent_view:
            # Create new view record
            job_view = JobView(
                job_id=job_id,
                user_id=user_id,
                ip_address=ip_address
            )
            db.add(job_view)
            
            # Increment view count
            db.query(Job).filter(Job.id == job_id).update({
                Job.view_count: Job.view_count + 1
            })
            
            db.commit()
    
    def get_user_viewed_jobs(self, db: Session, user_id: int, limit: int = 20) -> List[Job]:
        """Get jobs viewed by user."""
        return db.query(Job).options(
            joinedload(Job.company)
        ).join(JobView).filter(
            JobView.user_id == user_id
        ).order_by(desc(JobView.viewed_at)).limit(limit).all()
    
    def save_job(self, db: Session, job_id: int, user_id: int) -> bool:
        """Save job for user."""
        existing = db.query(SavedJob).filter(
            SavedJob.job_id == job_id,
            SavedJob.user_id == user_id
        ).first()
        
        if not existing:
            saved_job = SavedJob(job_id=job_id, user_id=user_id)
            db.add(saved_job)
            db.commit()
            return True
        return False
    
    def unsave_job(self, db: Session, job_id: int, user_id: int) -> bool:
        """Remove saved job for user."""
        saved_job = db.query(SavedJob).filter(
            SavedJob.job_id == job_id,
            SavedJob.user_id == user_id
        ).first()
        
        if saved_job:
            db.delete(saved_job)
            db.commit()
            return True
        return False
    
    def get_user_saved_jobs(self, db: Session, user_id: int) -> List[Job]:
        """Get saved jobs for user."""
        return db.query(Job).options(
            joinedload(Job.company)
        ).join(SavedJob).filter(
            SavedJob.user_id == user_id
        ).order_by(desc(SavedJob.saved_at)).all()
    
    def _apply_search_filters(self, query, search_params: JobSearchRequest):
        """Apply search filters to query."""
        # Text search
        if search_params.q:
            search_term = f"%{search_params.q}%"
            query = query.filter(
                or_(
                    Job.title.ilike(search_term),
                    Job.description.ilike(search_term),
                    Job.short_description.ilike(search_term)
                )
            )
        
        # Location filter
        if search_params.location:
            location_term = f"%{search_params.location}%"
            query = query.filter(
                or_(
                    Job.location.ilike(location_term),
                    Job.city.ilike(location_term),
                    Job.state.ilike(location_term),
                    Job.country.ilike(location_term)
                )
            )
        
        # Job type filter
        if search_params.job_type:
            query = query.filter(Job.job_type.in_(search_params.job_type))
        
        # Experience level filter
        if search_params.experience_level:
            query = query.filter(Job.experience_level.in_(search_params.experience_level))
        
        # Salary range filter
        if search_params.salary_min:
            query = query.filter(
                or_(
                    Job.salary_min >= search_params.salary_min,
                    Job.salary_max >= search_params.salary_min
                )
            )
        
        if search_params.salary_max:
            query = query.filter(
                or_(
                    Job.salary_max <= search_params.salary_max,
                    Job.salary_min <= search_params.salary_max
                )
            )
        
        # Remote filter
        if search_params.is_remote is not None:
            query = query.filter(Job.is_remote == search_params.is_remote)
        
        # Company filter
        if search_params.company_id:
            query = query.filter(Job.company_id == search_params.company_id)
        
        # Category filter
        if search_params.category_id:
            query = query.filter(Job.category_id == search_params.category_id)
        
        # Tags filter
        if search_params.tags:
            for tag in search_params.tags:
                query = query.filter(Job.tags.contains([tag]))
        
        # Posted within days filter
        if search_params.posted_within_days:
            cutoff_date = datetime.utcnow() - timedelta(days=search_params.posted_within_days)
            query = query.filter(Job.created_at >= cutoff_date)
        
        # Only active jobs
        query = query.filter(Job.status == "active")
        
        return query
    
    def _apply_sorting(self, query, sort_by: str, sort_order: str):
        """Apply sorting to query."""
        if sort_order == "desc":
            order_func = desc
        else:
            order_func = asc
        
        if sort_by == "salary_max":
            query = query.order_by(order_func(Job.salary_max))
        elif sort_by == "view_count":
            query = query.order_by(order_func(Job.view_count))
        elif sort_by == "application_count":
            query = query.order_by(order_func(Job.application_count))
        elif sort_by == "title":
            query = query.order_by(order_func(Job.title))
        else:  # Default to created_at
            query = query.order_by(order_func(Job.created_at))
        
        return query
    
    def _generate_slug(self, db: Session, title: str) -> str:
        """Generate unique slug from title."""
        import re
        base_slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')
        
        # Check if slug exists
        existing = db.query(Job).filter(Job.slug == base_slug).first()
        if not existing:
            return base_slug
        
        # Generate unique slug with counter
        counter = 1
        while True:
            new_slug = f"{base_slug}-{counter}"
            existing = db.query(Job).filter(Job.slug == new_slug).first()
            if not existing:
                return new_slug
            counter += 1