# File: job-service/src/services/company_service.py
from sqlalchemy import func, desc, or_
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from ..models.job_models import Company, Job, CompanyFollow
from ..models.schemas import (
    CompanyCreate, CompanyUpdate, CompanyResponse, CompanyResponseWithJobs,
    CompanyFollowResponse, MessageResponse
)
from fastapi import HTTPException, status
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class CompanyService:
    
    def create_company(self, db: Session, company_data: CompanyCreate, user_id: int) -> CompanyResponse:
        """Create a new company."""
        try:
            db_company = Company(
                **company_data.dict(),
                # Add owner_id or similar field if needed
            )
            db.add(db_company)
            db.commit()
            db.refresh(db_company)
            
            logger.info(f"Created company: {db_company.id} - {db_company.name}")
            return CompanyResponse.model_validate(db_company)
            
        except Exception as e:
            logger.error(f"Error creating company: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create company"
            )
    
    def get_company_with_jobs(self, db: Session, company_id: int, include_jobs: bool = True) -> CompanyResponseWithJobs:
        """Get company with optional jobs."""
        try:
            query = db.query(Company)
            if include_jobs:
                query = query.options(joinedload(Company.jobs))
            
            company = query.filter(Company.id == company_id).first()
            if not company:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Company not found"
                )
            
            # Calculate job count and average salary
            job_count = db.query(Job).filter(Job.company_id == company_id, Job.status == "active").count()
            
            avg_salary_result = db.query(
                func.avg((Job.salary_min + Job.salary_max) / 2).label('avg_salary')
            ).filter(
                Job.company_id == company_id,
                Job.salary_min.isnot(None),
                Job.salary_max.isnot(None)
            ).first()
            
            avg_salary = avg_salary_result.avg_salary if avg_salary_result.avg_salary else None
            
            company_dict = company.__dict__.copy()
            company_dict['job_count'] = job_count
            company_dict['avg_salary'] = avg_salary
            
            if include_jobs:
                company_dict['jobs'] = [job for job in company.jobs if job.status == "active"]
            
            return CompanyResponseWithJobs.model_validate(company_dict)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting company: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get company"
            )
    
    def search_companies(self, db: Session, search: Optional[str], industry: Optional[str], 
                        skip: int, limit: int) -> List[CompanyResponse]:
        """Search companies with filters."""
        try:
            query = db.query(Company)
            
            if search:
                search_term = f"%{search}%"
                query = query.filter(
                    or_(
                        Company.name.ilike(search_term),
                        Company.description.ilike(search_term)
                    )
                )
            
            if industry:
                query = query.filter(Company.industry.ilike(f"%{industry}%"))
            
            companies = query.offset(skip).limit(limit).all()
            return [CompanyResponse.model_validate(company) for company in companies]
            
        except Exception as e:
            logger.error(f"Error searching companies: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to search companies"
            )
    
    def update_company(self, db: Session, company_id: int, company_data: CompanyUpdate, user_id: int) -> CompanyResponse:
        """Update company."""
        try:
            company = db.query(Company).filter(Company.id == company_id).first()
            if not company:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Company not found"
                )
            
            # Add ownership check if needed
            # if company.owner_id != user_id:
            #     raise HTTPException(status_code=403, detail="Not authorized")
            
            update_data = company_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(company, field, value)
            
            company.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(company)
            
            return CompanyResponse.model_validate(company)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating company: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update company"
            )
    
    def follow_company(self, db: Session, company_id: int, user_id: int) -> CompanyFollowResponse:
        """Follow a company."""
        try:
            # Check if company exists
            company = db.query(Company).filter(Company.id == company_id).first()
            if not company:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Company not found"
                )
            
            # Check if already following
            existing_follow = db.query(CompanyFollow).filter(
                CompanyFollow.company_id == company_id,
                CompanyFollow.user_id == user_id
            ).first()
            
            if existing_follow:
                return CompanyFollowResponse.model_validate(existing_follow)
            
            # Create new follow
            follow = CompanyFollow(
                company_id=company_id,
                user_id=user_id
            )
            db.add(follow)
            db.commit()
            db.refresh(follow)
            
            return CompanyFollowResponse.model_validate(follow)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error following company: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to follow company"
            )
    
    def unfollow_company(self, db: Session, company_id: int, user_id: int) -> MessageResponse:
        """Unfollow a company."""
        try:
            follow = db.query(CompanyFollow).filter(
                CompanyFollow.company_id == company_id,
                CompanyFollow.user_id == user_id
            ).first()
            
            if not follow:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Company follow not found"
                )
            
            db.delete(follow)
            db.commit()
            
            return MessageResponse(message="Company unfollowed successfully")
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error unfollowing company: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to unfollow company"
            )
    
    def get_followed_companies(self, db: Session, user_id: int) -> List[CompanyFollowResponse]:
        """Get companies followed by user."""
        try:
            follows = db.query(CompanyFollow).options(
                joinedload(CompanyFollow.company)
            ).filter(CompanyFollow.user_id == user_id).all()
            
            return [CompanyFollowResponse.model_validate(follow) for follow in follows]
            
        except Exception as e:
            logger.error(f"Error getting followed companies: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get followed companies"
            )