# File: job-service/src/services/salary_service.py


from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, case, text
from typing import Dict, Any, Optional, List
from ..repositories.profile_repository import ProfileRepository
from ..models.schemas import (
    SalaryComparisonRequest, SalaryComparisonResponse,
    SalaryEntryCreate, SalaryEntryResponse
)
from ..models.profile_models import SalaryEntry
from ..models.job_models import Job, Company
from ..utils.auth_utils import get_user_from_token
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

class SalaryService:
    def __init__(self):
        self.profile_repo = ProfileRepository()
    
    def compare_salary(self, db: Session, comparison_request: SalaryComparisonRequest) -> Dict[str, Any]:
        """Get comprehensive salary comparison data with industry and experience analysis."""
        try:
            job_title = comparison_request.job_title
            location = comparison_request.location
            years_of_experience = comparison_request.years_of_experience
            industry = comparison_request.industry
            
            # Get overall statistics
            overall_stats = self._get_salary_statistics(db, job_title, location, years_of_experience, industry)
            
            # Get industry comparison
            industry_comparison = self._get_industry_comparison(db, job_title, industry)
            
            # Get experience level comparison
            experience_comparison = self._get_experience_comparison(db, job_title, years_of_experience)
            
            # Get location comparison
            location_comparison = self._get_location_comparison(db, job_title, location)
            
            # Get company size comparison
            company_size_comparison = self._get_company_size_comparison(db, job_title)
            
            # Get similar roles comparison
            similar_roles = self._get_similar_roles_comparison(db, job_title)
            
            # Calculate percentile ranking
            percentile_ranking = self._calculate_percentile_ranking(
                db, job_title, years_of_experience, industry, location
            )
            
            return {
                "job_title": job_title,
                "location": location,
                "years_of_experience": years_of_experience,
                "industry": industry,
                "overall_statistics": overall_stats,
                "industry_comparison": industry_comparison,
                "experience_comparison": experience_comparison,
                "location_comparison": location_comparison,
                "company_size_comparison": company_size_comparison,
                "similar_roles": similar_roles,
                "percentile_ranking": percentile_ranking,
                "recommendations": self._generate_salary_recommendations(
                    overall_stats, industry_comparison, experience_comparison
                )
            }
            
        except Exception as e:
            logger.error(f"Error comparing salary: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to compare salary"
            )
    
    def _get_salary_statistics(self, db: Session, job_title: str, location: str = None, 
                             years_of_experience: int = None, industry: str = None) -> Dict[str, Any]:
        """Get comprehensive salary statistics."""
        base_query = db.query(SalaryEntry).filter(
            SalaryEntry.job_title.ilike(f"%{job_title}%"),
            SalaryEntry.is_anonymous == True,
            SalaryEntry.annual_salary > 0
        )
        
        # Apply filters
        if location:
            base_query = base_query.filter(SalaryEntry.location.ilike(f"%{location}%"))
        if years_of_experience is not None:
            base_query = base_query.filter(
                SalaryEntry.years_of_experience.between(
                    max(0, years_of_experience - 2),
                    years_of_experience + 2
                )
            )
        if industry:
            base_query = base_query.filter(SalaryEntry.industry.ilike(f"%{industry}%"))
        
        # Get aggregated stats
        stats = base_query.with_entities(
            func.count(SalaryEntry.id).label('total_entries'),
            func.avg(SalaryEntry.annual_salary).label('avg_salary'),
            func.min(SalaryEntry.annual_salary).label('min_salary'),
            func.max(SalaryEntry.annual_salary).label('max_salary')
        ).first()
        
        if not stats or not stats.total_entries:
            return {
                "total_entries": 0,
                "average_salary": 0,
                "median_salary": 0,
                "min_salary": 0,
                "max_salary": 0,
                "percentile_25": 0,
                "percentile_75": 0,
                "currency": "USD"
            }
        
        # Get percentiles
        salaries = [entry.annual_salary for entry in base_query.all()]
        salaries.sort()
        n = len(salaries)
        
        percentile_25 = salaries[n // 4] if n >= 4 else salaries[0]
        median_salary = salaries[n // 2] if n % 2 == 1 else (salaries[n // 2 - 1] + salaries[n // 2]) / 2
        percentile_75 = salaries[3 * n // 4] if n >= 4 else salaries[-1]
        
        return {
            "total_entries": stats.total_entries,
            "average_salary": round(stats.avg_salary or 0, 2),
            "median_salary": round(median_salary, 2),
            "min_salary": round(stats.min_salary or 0, 2),
            "max_salary": round(stats.max_salary or 0, 2),
            "percentile_25": round(percentile_25, 2),
            "percentile_75": round(percentile_75, 2),
            "currency": "USD"
        }
    
    def _get_industry_comparison(self, db: Session, job_title: str, user_industry: str = None) -> List[Dict[str, Any]]:
        """Get salary comparison across different industries."""
        industry_stats = db.query(
            SalaryEntry.industry,
            func.count(SalaryEntry.id).label('count'),
            func.avg(SalaryEntry.annual_salary).label('avg_salary'),
            func.min(SalaryEntry.annual_salary).label('min_salary'),
            func.max(SalaryEntry.annual_salary).label('max_salary')
        ).filter(
            SalaryEntry.job_title.ilike(f"%{job_title}%"),
            SalaryEntry.is_anonymous == True,
            SalaryEntry.industry.isnot(None),
            SalaryEntry.annual_salary > 0
        ).group_by(
            SalaryEntry.industry
        ).having(
            func.count(SalaryEntry.id) >= 2
        ).order_by(
            func.avg(SalaryEntry.annual_salary).desc()
        ).all()
        
        result = []
        for stat in industry_stats:
            is_user_industry = user_industry and stat.industry.lower() == user_industry.lower()
            result.append({
                "industry": stat.industry,
                "count": stat.count,
                "average_salary": round(stat.avg_salary, 2),
                "min_salary": round(stat.min_salary, 2),
                "max_salary": round(stat.max_salary, 2),
                "is_user_industry": is_user_industry
            })
        
        return result
    
    def _get_experience_comparison(self, db: Session, job_title: str, user_experience: int = None) -> List[Dict[str, Any]]:
        """Get salary comparison across experience levels."""
        experience_brackets = [
            (0, 2, "0-2 years"),
            (3, 5, "3-5 years"), 
            (6, 10, "6-10 years"),
            (11, 15, "11-15 years"),
            (16, 100, "15+ years")
        ]
        
        result = []
        for min_exp, max_exp, label in experience_brackets:
            stats = db.query(
                func.count(SalaryEntry.id).label('count'),
                func.avg(SalaryEntry.annual_salary).label('avg_salary'),
                func.min(SalaryEntry.annual_salary).label('min_salary'),
                func.max(SalaryEntry.annual_salary).label('max_salary')
            ).filter(
                SalaryEntry.job_title.ilike(f"%{job_title}%"),
                SalaryEntry.is_anonymous == True,
                SalaryEntry.years_of_experience.between(min_exp, max_exp),
                SalaryEntry.annual_salary > 0
            ).first()
            
            if stats and stats.count and stats.count >= 2:
                is_user_bracket = (user_experience is not None and 
                                 min_exp <= user_experience <= max_exp)
                
                result.append({
                    "experience_range": label,
                    "min_years": min_exp,
                    "max_years": max_exp,
                    "count": stats.count,
                    "average_salary": round(stats.avg_salary, 2),
                    "min_salary": round(stats.min_salary, 2),
                    "max_salary": round(stats.max_salary, 2),
                    "is_user_bracket": is_user_bracket
                })
        
        return result
    
    def _get_location_comparison(self, db: Session, job_title: str, user_location: str = None) -> List[Dict[str, Any]]:
        """Get salary comparison across locations."""
        location_stats = db.query(
            SalaryEntry.location,
            func.count(SalaryEntry.id).label('count'),
            func.avg(SalaryEntry.annual_salary).label('avg_salary'),
            func.min(SalaryEntry.annual_salary).label('min_salary'),
            func.max(SalaryEntry.annual_salary).label('max_salary')
        ).filter(
            SalaryEntry.job_title.ilike(f"%{job_title}%"),
            SalaryEntry.is_anonymous == True,
            SalaryEntry.location.isnot(None),
            SalaryEntry.annual_salary > 0
        ).group_by(
            SalaryEntry.location
        ).having(
            func.count(SalaryEntry.id) >= 2
        ).order_by(
            func.avg(SalaryEntry.annual_salary).desc()
        ).limit(10).all()
        
        result = []
        for stat in location_stats:
            is_user_location = (user_location and 
                              user_location.lower() in stat.location.lower())
            
            result.append({
                "location": stat.location,
                "count": stat.count,
                "average_salary": round(stat.avg_salary, 2),
                "min_salary": round(stat.min_salary, 2),
                "max_salary": round(stat.max_salary, 2),
                "is_user_location": is_user_location
            })
        
        return result
    
    def _get_company_size_comparison(self, db: Session, job_title: str) -> List[Dict[str, Any]]:
        """Get salary comparison across company sizes."""
        size_stats = db.query(
            SalaryEntry.company_size,
            func.count(SalaryEntry.id).label('count'),
            func.avg(SalaryEntry.annual_salary).label('avg_salary')
        ).filter(
            SalaryEntry.job_title.ilike(f"%{job_title}%"),
            SalaryEntry.is_anonymous == True,
            SalaryEntry.company_size.isnot(None),
            SalaryEntry.annual_salary > 0
        ).group_by(
            SalaryEntry.company_size
        ).having(
            func.count(SalaryEntry.id) >= 2
        ).order_by(
            func.avg(SalaryEntry.annual_salary).desc()
        ).all()
        
        result = []
        for stat in size_stats:
            result.append({
                "company_size": stat.company_size,
                "count": stat.count,
                "average_salary": round(stat.avg_salary, 2)
            })
        
        return result
    
    def _get_similar_roles_comparison(self, db: Session, job_title: str) -> List[Dict[str, Any]]:
        """Get salary comparison for similar job roles."""
        # Find similar job titles
        similar_jobs = db.query(
            Job.title,
            func.count(Job.id).label('job_count')
        ).filter(
            or_(
                Job.title.ilike(f"%{job_title.split()[0]}%"),
                Job.tags.contains([job_title.lower()])
            ),
            Job.title != job_title
        ).group_by(Job.title).limit(5).all()
        
        result = []
        for job in similar_jobs:
            stats = db.query(
                func.count(SalaryEntry.id).label('count'),
                func.avg(SalaryEntry.annual_salary).label('avg_salary')
            ).filter(
                SalaryEntry.job_title.ilike(f"%{job.title}%"),
                SalaryEntry.is_anonymous == True,
                SalaryEntry.annual_salary > 0
            ).first()
            
            if stats and stats.count and stats.count >= 2:
                result.append({
                    "job_title": job.title,
                    "count": stats.count,
                    "average_salary": round(stats.avg_salary, 2),
                    "job_postings": job.job_count
                })
        
        return result
    
    def _calculate_percentile_ranking(self, db: Session, job_title: str, 
                                    years_of_experience: int = None, 
                                    industry: str = None, 
                                    location: str = None) -> Dict[str, Any]:
        """Calculate percentile ranking information."""
        base_query = db.query(SalaryEntry).filter(
            SalaryEntry.job_title.ilike(f"%{job_title}%"),
            SalaryEntry.is_anonymous == True,
            SalaryEntry.annual_salary > 0
        )
        
        # Apply context filters
        if years_of_experience is not None:
            base_query = base_query.filter(
                SalaryEntry.years_of_experience.between(
                    max(0, years_of_experience - 2),
                    years_of_experience + 2
                )
            )
        
        if industry:
            base_query = base_query.filter(SalaryEntry.industry.ilike(f"%{industry}%"))
        
        if location:
            base_query = base_query.filter(SalaryEntry.location.ilike(f"%{location}%"))
        
        salaries = [entry.annual_salary for entry in base_query.all()]
        
        if len(salaries) < 5:
            return {"message": "Insufficient data for percentile calculation"}
        
        salaries.sort()
        n = len(salaries)
        
        return {
            "total_sample_size": n,
            "percentiles": {
                "10th": round(salaries[n // 10] if n >= 10 else salaries[0], 2),
                "25th": round(salaries[n // 4] if n >= 4 else salaries[0], 2),
                "50th": round(salaries[n // 2] if n % 2 == 1 else (salaries[n // 2 - 1] + salaries[n // 2]) / 2, 2),
                "75th": round(salaries[3 * n // 4] if n >= 4 else salaries[-1], 2),
                "90th": round(salaries[9 * n // 10] if n >= 10 else salaries[-1], 2)
            }
        }
    
    def _generate_salary_recommendations(self, overall_stats: Dict, 
                                       industry_comparison: List, 
                                       experience_comparison: List) -> List[str]:
        """Generate personalized salary recommendations."""
        recommendations = []
        
        if overall_stats.get("total_entries", 0) > 0:
            avg_salary = overall_stats.get("average_salary", 0)
            recommendations.append(
                f"The average salary for this position is ${avg_salary:,.0f}"
            )
            
            if industry_comparison:
                top_industry = industry_comparison[0]
                recommendations.append(
                    f"Highest paying industry: {top_industry['industry']} "
                    f"(${top_industry['average_salary']:,.0f} average)"
                )
            
            if experience_comparison:
                senior_brackets = [exp for exp in experience_comparison 
                                 if exp['min_years'] >= 6]
                if senior_brackets:
                    senior_avg = senior_brackets[0]['average_salary']
                    recommendations.append(
                        f"Senior level positions (6+ years) average ${senior_avg:,.0f}"
                    )
        
        recommendations.extend([
            "Consider location impact - major tech hubs typically offer 20-30% higher salaries",
            "Company size matters - larger companies often provide better compensation packages",
            "Skills and certifications can increase earning potential by 15-25%",
            "Negotiate total compensation including benefits, not just base salary"
        ])
        
        return recommendations
    
    def add_salary_data(self, db: Session, user_token: str, salary_data: SalaryEntryCreate) -> SalaryEntryResponse:
        """Add salary data for comparison."""
        try:
            user_info = get_user_from_token(user_token)
            user_id = user_info["user_id"]
            
            profile = self.profile_repo.get_profile_by_user_id(db, user_id)
            if not profile:
                from ..models.schemas import JobProfileCreate
                profile = self.profile_repo.create_profile(db, JobProfileCreate(), user_id)
            
            salary_entry = self.profile_repo.add_salary_entry(db, profile.id, salary_data)
            return SalaryEntryResponse.model_validate(salary_entry)
            
        except Exception as e:
            logger.error(f"Error adding salary data: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add salary data"
            )
    
    def get_salary_insights(self, db: Session, job_title: str) -> Dict[str, Any]:
        """Get comprehensive salary insights for a job title."""
        try:
            comparison_request = SalaryComparisonRequest(job_title=job_title)
            full_comparison = self.compare_salary(db, comparison_request)
            
            overall_stats = full_comparison.get("overall_statistics", {})
            
            if overall_stats.get("total_entries", 0) == 0:
                return {
                    "job_title": job_title,
                    "message": "No salary data available for this position",
                    "suggestions": [
                        "Be the first to add salary data for this position",
                        "Try searching for similar job titles",
                        "Check industry salary reports",
                        "Consider broader job categories"
                    ]
                }
            
            insights = {
                "job_title": job_title,
                "summary": {
                    "average_salary": overall_stats.get("average_salary", 0),
                    "median_salary": overall_stats.get("median_salary", 0),
                    "salary_range": f"${overall_stats.get('min_salary', 0):,.0f} - ${overall_stats.get('max_salary', 0):,.0f}",
                    "sample_size": overall_stats.get("total_entries", 0)
                },
                "market_analysis": {
                    "top_paying_industries": full_comparison.get("industry_comparison", [])[:3],
                    "salary_by_experience": full_comparison.get("experience_comparison", []),
                    "top_locations": full_comparison.get("location_comparison", [])[:5],
                    "company_size_impact": full_comparison.get("company_size_comparison", [])
                },
                "growth_potential": {
                    "similar_roles": full_comparison.get("similar_roles", [])
                },
                "recommendations": full_comparison.get("recommendations", [])
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"Error getting salary insights: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get salary insights"
            )