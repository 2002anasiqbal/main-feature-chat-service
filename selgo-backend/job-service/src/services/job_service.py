# File: job-service/src/services/job_service.py

from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any, Tuple
from ..repositories.job_repository import JobRepository
from ..models.schemas import (
    JobCreate, JobUpdate, JobSearchRequest, JobResponse, 
    JobSearchResponse, MessageResponse
)
from ..models.job_models import Job, Company, JobCategory, JobApplication, JobType, ExperienceLevel, JobStatus  # Added missing imports
from ..utils.auth_utils import get_user_from_token
from fastapi import HTTPException, status
import logging

    
from sqlalchemy import func, desc
from ..models.schemas import (
    JobStatisticsResponse, FilterOptionsResponse, JobCategoryResponse,
    BulkJobAction, BulkJobResponse, JobFeedRequest, JobFeedResponse
)


logger = logging.getLogger(__name__)

class JobService:
    def __init__(self):
        self.job_repo = JobRepository()
    
    def create_job(self, db: Session, job_data: JobCreate, user_token: str) -> JobResponse:
        """Create a new job posting."""
        try:
            # Validate user token and get user info
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            # Verify company exists
            company = db.query(Company).filter(Company.id == job_data.company_id).first()
            if not company:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Company not found"
                )
            
            # Create job
            job = self.job_repo.create_job(db, job_data, user_id)
            
            # Convert to response model
            return JobResponse.model_validate(job)
            
        except Exception as e:
            logger.error(f"Error creating job: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create job"
            )
    
    def get_job_by_id(self, db: Session, job_id: int, user_token: Optional[str] = None) -> JobResponse:
        """Get job by ID and increment view count."""
        job = self.job_repo.get_job_by_id(db, job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        # Track view if user is provided
        user_id = None
        if user_token:
            try:
                user_info = get_user_from_token(user_token)
                user_id = user_info["user_id"]
            except:
                pass  # Anonymous view
        
        # Increment view count
        self.job_repo.increment_view_count(db, job_id, user_id)
        
        return JobResponse.model_validate(job)
    
    def get_job_by_slug(self, db: Session, slug: str, user_token: Optional[str] = None) -> JobResponse:
        """Get job by slug and increment view count."""
        job = self.job_repo.get_job_by_slug(db, slug)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        # Track view if user is provided
        user_id = None
        if user_token:
            try:
                user_info = get_user_from_token(user_token)
                user_id = user_info["user_id"]
            except:
                pass  # Anonymous view
        
        # Increment view count
        self.job_repo.increment_view_count(db, job.id, user_id)
        
        return JobResponse.model_validate(job)
    
    def search_jobs(self, db: Session, search_params: JobSearchRequest) -> JobSearchResponse:
        """Search jobs with filtering and pagination."""
        try:
            jobs, total = self.job_repo.search_jobs(db, search_params)
            
            # Calculate total pages
            total_pages = (total + search_params.limit - 1) // search_params.limit
            
            # Convert jobs to response models
            job_responses = [JobResponse.model_validate(job) for job in jobs]
            
            return JobSearchResponse(
                jobs=job_responses,
                total=total,
                page=search_params.page,
                limit=search_params.limit,
                total_pages=total_pages
            )
            
        except Exception as e:
            logger.error(f"Error searching jobs: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to search jobs"
            )
    
    def get_featured_jobs(self, db: Session, limit: int = 10) -> List[JobResponse]:
        """Get featured jobs for homepage."""
        try:
            jobs = self.job_repo.get_featured_jobs(db, limit)
            return [JobResponse.model_validate(job) for job in jobs]
        except Exception as e:
            logger.error(f"Error getting featured jobs: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get featured jobs"
            )
    
    def get_recent_jobs(self, db: Session, limit: int = 20) -> List[JobResponse]:
        """Get recently posted jobs."""
        try:
            jobs = self.job_repo.get_recent_jobs(db, limit)
            return [JobResponse.model_validate(job) for job in jobs]
        except Exception as e:
            logger.error(f"Error getting recent jobs: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get recent jobs"
            )
    
    def get_job_recommendations(self, db: Session, user_token: str, limit: int = 10) -> List[JobResponse]:
        """Get job recommendations for user."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            # For now, return recent jobs
            # TODO: Implement proper recommendation algorithm
            jobs = self.job_repo.get_recent_jobs(db, limit)
            return [JobResponse.model_validate(job) for job in jobs]
            
        except Exception as e:
            logger.error(f"Error getting job recommendations: {str(e)}")
            # Return recent jobs as fallback
            jobs = self.job_repo.get_recent_jobs(db, limit)
            return [JobResponse.model_validate(job) for job in jobs]
    
    def get_similar_jobs(self, db: Session, job_id: int, limit: int = 5) -> List[JobResponse]:
        """Get similar jobs to the given job."""
        try:
            job = self.job_repo.get_job_by_id(db, job_id)
            if not job:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Job not found"
                )
            
            similar_jobs = self.job_repo.get_similar_jobs(db, job, limit)
            return [JobResponse.model_validate(job) for job in similar_jobs]
            
        except Exception as e:
            logger.error(f"Error getting similar jobs: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get similar jobs"
            )
    
    def update_job(self, db: Session, job_id: int, job_data: JobUpdate, user_token: str) -> JobResponse:
        """Update job posting."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            # Get job and verify ownership
            job = self.job_repo.get_job_by_id(db, job_id)
            if not job:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Job not found"
                )
            
            if job.posted_by != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to update this job"
                )
            
            # Update job
            updated_job = self.job_repo.update_job(db, job_id, job_data)
            if not updated_job:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update job"
                )
            
            return JobResponse.model_validate(updated_job)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating job: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update job"
            )
    
    def delete_job(self, db: Session, job_id: int, user_token: str) -> MessageResponse:
        """Delete job posting."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            # Get job and verify ownership
            job = self.job_repo.get_job_by_id(db, job_id)
            if not job:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Job not found"
                )
            
            if job.posted_by != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to delete this job"
                )
            
            # Delete job
            success = self.job_repo.delete_job(db, job_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to delete job"
                )
            
            return MessageResponse(message="Job deleted successfully")
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting job: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete job"
            )
    
    def save_job(self, db: Session, job_id: int, user_token: str) -> MessageResponse:
        """Save job for user."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            # Verify job exists
            job = self.job_repo.get_job_by_id(db, job_id)
            if not job:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Job not found"
                )
            
            # Save job
            success = self.job_repo.save_job(db, job_id, user_id)
            if success:
                return MessageResponse(message="Job saved successfully")
            else:
                return MessageResponse(message="Job already saved")
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error saving job: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save job"
            )
    
    def unsave_job(self, db: Session, job_id: int, user_token: str) -> MessageResponse:
        """Remove saved job for user."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            success = self.job_repo.unsave_job(db, job_id, user_id)
            if success:
                return MessageResponse(message="Job removed from saved")
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Saved job not found"
                )
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error unsaving job: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to remove saved job"
            )
    
    def get_user_saved_jobs(self, db: Session, user_token: str) -> List[JobResponse]:
        """Get saved jobs for user."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            jobs = self.job_repo.get_user_saved_jobs(db, user_id)
            return [JobResponse.model_validate(job) for job in jobs]
            
        except Exception as e:
            logger.error(f"Error getting saved jobs: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get saved jobs"
            )
    
    def get_user_viewed_jobs(self, db: Session, user_token: str, limit: int = 20) -> List[JobResponse]:
        """Get jobs viewed by user (Last Viewed Jobs feature)."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            jobs = self.job_repo.get_user_viewed_jobs(db, user_id, limit)
            return [JobResponse.model_validate(job) for job in jobs]
            
        except Exception as e:
            logger.error(f"Error getting viewed jobs: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get viewed jobs"
            )
    
    def get_jobs_by_company(self, db: Session, company_id: int, limit: int = 10) -> List[JobResponse]:
        """Get jobs by company."""
        try:
            jobs = self.job_repo.get_jobs_by_company(db, company_id, limit)
            return [JobResponse.model_validate(job) for job in jobs]
        except Exception as e:
            logger.error(f"Error getting jobs by company: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get jobs by company"
            )

    def get_job_statistics(self, db: Session) -> JobStatisticsResponse:
        """Get overall job platform statistics."""
        try:
            # Get basic counts
            total_jobs = db.query(Job).count()
            active_jobs = db.query(Job).filter(Job.status == "active").count()
            
            # Jobs this month
            from datetime import datetime, timedelta
            start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            jobs_this_month = db.query(Job).filter(Job.created_at >= start_of_month).count()
            
            # Total applications
            total_applications = db.query(JobApplication).count()
            
            # Average applications per job
            avg_applications = total_applications / total_jobs if total_jobs > 0 else 0
            
            # Top categories
            top_categories = db.query(
                JobCategory.name,
                func.count(Job.id).label('job_count')
            ).join(Job).group_by(JobCategory.name).order_by(desc('job_count')).limit(5).all()
            
            top_categories_data = [
                {"name": cat.name, "job_count": cat.job_count}
                for cat in top_categories
            ]
            
            # Top companies
            top_companies = db.query(
                Company.name,
                func.count(Job.id).label('job_count')
            ).join(Job).group_by(Company.name).order_by(desc('job_count')).limit(5).all()
            
            top_companies_data = [
                {"name": comp.name, "job_count": comp.job_count}
                for comp in top_companies
            ]
            
            # Salary insights
            salary_stats = db.query(
                func.avg(Job.salary_min).label('avg_min_salary'),
                func.avg(Job.salary_max).label('avg_max_salary'),
                func.min(Job.salary_min).label('min_salary'),
                func.max(Job.salary_max).label('max_salary')
            ).filter(
                Job.salary_min.isnot(None),
                Job.salary_max.isnot(None)
            ).first()
            
            salary_insights = {
                "average_min_salary": salary_stats.avg_min_salary or 0,
                "average_max_salary": salary_stats.avg_max_salary or 0,
                "lowest_salary": salary_stats.min_salary or 0,
                "highest_salary": salary_stats.max_salary or 0
            }
            
            return JobStatisticsResponse(
                total_jobs=total_jobs,
                active_jobs=active_jobs,
                jobs_this_month=jobs_this_month,
                total_applications=total_applications,
                avg_applications_per_job=round(avg_applications, 2),
                top_categories=top_categories_data,
                top_companies=top_companies_data,
                salary_insights=salary_insights
            )
            
        except Exception as e:
            logger.error(f"Error getting job statistics: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get job statistics"
            )

    def get_filter_options(self, db: Session) -> FilterOptionsResponse:
        """Get available filter options for job search."""
        try:
            # Job types
            job_types = [{"value": jt.value, "label": jt.value.replace("_", " ").title()} for jt in JobType]
            
            # Experience levels
            experience_levels = [{"value": el.value, "label": el.value.replace("_", " ").title()} for el in ExperienceLevel]
            
            # Industries (from companies)
            industries = db.query(Company.industry).filter(Company.industry.isnot(None)).distinct().all()
            industries_data = [{"name": ind[0], "job_count": 0} for ind in industries if ind[0]]
            
            # Company sizes
            company_sizes = [
                {"value": "1-10", "label": "1-10 employees"},
                {"value": "11-50", "label": "11-50 employees"},
                {"value": "51-200", "label": "51-200 employees"},
                {"value": "201-1000", "label": "201-1000 employees"},
                {"value": "1000+", "label": "1000+ employees"}
            ]
            
            # Locations (from jobs)
            locations = db.query(Job.city).filter(Job.city.isnot(None)).distinct().limit(50).all()
            locations_data = [{"city": loc[0], "job_count": 0} for loc in locations if loc[0]]
            
            # Salary ranges
            salary_ranges = [
                {"min": 0, "max": 50000, "label": "$0 - $50k"},
                {"min": 50000, "max": 100000, "label": "$50k - $100k"},
                {"min": 100000, "max": 150000, "label": "$100k - $150k"},
                {"min": 150000, "max": 200000, "label": "$150k - $200k"},
                {"min": 200000, "max": None, "label": "$200k+"}
            ]
            
            # Categories
            categories = db.query(JobCategory).filter(JobCategory.is_active == True).all()
            categories_data = [JobCategoryResponse.model_validate(cat) for cat in categories]
            
            return FilterOptionsResponse(
                job_types=job_types,
                experience_levels=experience_levels,
                industries=industries_data,
                company_sizes=company_sizes,
                locations=locations_data,
                salary_ranges=salary_ranges,
                categories=categories_data
            )
            
        except Exception as e:
            logger.error(f"Error getting filter options: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get filter options"
            )

    def get_job_categories(self, db: Session) -> List[JobCategoryResponse]:
        """Get all job categories."""
        try:
            categories = db.query(JobCategory).filter(JobCategory.is_active == True).all()
            
            # Add job count for each category
            result = []
            for category in categories:
                job_count = db.query(Job).filter(
                    Job.category_id == category.id,
                    Job.status == "active"
                ).count()
                
                category_dict = category.__dict__.copy()
                category_dict['job_count'] = job_count
                result.append(JobCategoryResponse.model_validate(category_dict))
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting job categories: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get job categories"
            )

    def bulk_job_action(self, db: Session, bulk_action: BulkJobAction, user_id: int) -> BulkJobResponse:
        """Perform bulk actions on jobs."""
        try:
            successful = []
            failed = []
            
            for job_id in bulk_action.job_ids:
                try:
                    job = db.query(Job).filter(Job.id == job_id).first()
                    if not job:
                        failed.append({"job_id": job_id, "error": "Job not found"})
                        continue
                    
                    # Check if user has permission (admin or job owner)
                    if user_id != job.posted_by:
                        failed.append({"job_id": job_id, "error": "Not authorized"})
                        continue
                    
                    # Perform action
                    if bulk_action.action == "activate":
                        job.status = JobStatus.ACTIVE
                    elif bulk_action.action == "deactivate":
                        job.status = JobStatus.PAUSED
                    elif bulk_action.action == "delete":
                        db.delete(job)
                    elif bulk_action.action == "feature":
                        job.featured = True
                    elif bulk_action.action == "unfeature":
                        job.featured = False
                    else:
                        failed.append({"job_id": job_id, "error": "Invalid action"})
                        continue
                    
                    successful.append(job_id)
                    
                except Exception as e:
                    failed.append({"job_id": job_id, "error": str(e)})
            
            db.commit()
            
            return BulkJobResponse(
                successful=successful,
                failed=failed,
                total_processed=len(bulk_action.job_ids)
            )
            
        except Exception as e:
            logger.error(f"Error performing bulk action: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to perform bulk action"
            )

    def get_job_feed(self, db: Session, feed_request: JobFeedRequest) -> JobFeedResponse:
        """Get personalized job feed for homepage."""
        try:
            jobs = []
            
            if feed_request.feed_type == "recent":
                jobs = self.job_repo.get_recent_jobs(db, feed_request.limit)
            elif feed_request.feed_type == "trending":
                # Get jobs with high view counts
                jobs = db.query(Job).filter(
                    Job.status == "active"
                ).order_by(desc(Job.view_count)).limit(feed_request.limit).all()
            elif feed_request.feed_type == "recommended":
                # Basic recommendation logic
                jobs = self.job_repo.get_featured_jobs(db, feed_request.limit)
            else:  # mixed
                # Get a mix of recent, featured, and trending
                recent = self.job_repo.get_recent_jobs(db, feed_request.limit // 3)
                featured = self.job_repo.get_featured_jobs(db, feed_request.limit // 3)
                trending = db.query(Job).filter(
                    Job.status == "active"
                ).order_by(desc(Job.view_count)).limit(feed_request.limit // 3).all()
                
                jobs = recent + featured + trending
                jobs = jobs[:feed_request.limit]  # Limit total
            
            # Convert to response format
            job_responses = []
            for job in jobs:
                job_dict = job.__dict__.copy()
                job_dict['analytics'] = {"views": job.view_count, "applications": job.application_count}
                job_dict['is_saved'] = False  # Would check user's saved jobs
                job_dict['is_applied'] = False  # Would check user's applications
                job_responses.append(job_dict)
            
            import uuid
            refresh_token = str(uuid.uuid4())
            
            return JobFeedResponse(
                jobs=job_responses,
                feed_type=feed_request.feed_type,
                personalized=bool(feed_request.user_skills or feed_request.user_location),
                refresh_token=refresh_token
            )
            
        except Exception as e:
            logger.error(f"Error getting job feed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get job feed"
            )