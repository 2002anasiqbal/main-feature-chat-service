# File: job-service/src/api/salary.py
# REPLACE your existing salary.py with this enhanced version

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database.database import get_db
from ..services.salary_service import SalaryService
from ..models.schemas import (
    SalaryComparisonRequest, SalaryComparisonResponse,
    SalaryEntryCreate, SalaryEntryResponse
)
from ..utils.auth_utils import get_current_user

router = APIRouter()
salary_service = SalaryService()

@router.post("/compare", response_model=dict)
def compare_salary_advanced(
    comparison_request: SalaryComparisonRequest,
    db: Session = Depends(get_db)
):
    """
    Get comprehensive salary comparison data with industry, experience, and location analysis.
    
    Returns structured comparison including:
    - Overall statistics (avg, median, percentiles)
    - Industry breakdown
    - Experience level analysis
    - Location comparison
    - Company size impact
    - Similar roles comparison
    - Percentile ranking
    """
    return salary_service.compare_salary(db, comparison_request)

@router.get("/compare/{job_title}")
def compare_salary_simple(
    job_title: str,
    location: Optional[str] = Query(None, description="Filter by location"),
    years_of_experience: Optional[int] = Query(None, description="Filter by years of experience"),
    industry: Optional[str] = Query(None, description="Filter by industry"),
    db: Session = Depends(get_db)
):
    """
    Simple salary comparison endpoint using query parameters.
    """
    comparison_request = SalaryComparisonRequest(
        job_title=job_title,
        location=location,
        years_of_experience=years_of_experience,
        industry=industry
    )
    return salary_service.compare_salary(db, comparison_request)

@router.post("/add", response_model=SalaryEntryResponse, status_code=status.HTTP_201_CREATED)
async def add_salary_data(
    salary_data: SalaryEntryCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Add salary data for comparison (contributes to anonymous statistics)."""
    mock_token = "mock_token"  # In production, extract from request
    return salary_service.add_salary_data(db, mock_token, salary_data)

@router.get("/insights/{job_title}")
def get_salary_insights(
    job_title: str,
    db: Session = Depends(get_db)
):
    """
    Get comprehensive salary insights and market analysis for a job title.
    
    Returns:
    - Market summary
    - Industry analysis
    - Experience level breakdown
    - Location comparison
    - Growth potential
    - Actionable recommendations
    """
    return salary_service.get_salary_insights(db, job_title)

@router.get("/market-overview")
def get_market_overview(
    industry: Optional[str] = Query(None, description="Filter by industry"),
    location: Optional[str] = Query(None, description="Filter by location"),
    limit: int = Query(20, description="Number of job titles to return"),
    db: Session = Depends(get_db)
):
    """
    Get market overview with top paying job titles and industry trends.
    """
    try:
        from ..models.profile_models import SalaryEntry
        from sqlalchemy import func, desc
        
        # Build base query
        query = db.query(
            SalaryEntry.job_title,
            func.count(SalaryEntry.id).label('count'),
            func.avg(SalaryEntry.annual_salary).label('avg_salary')
        ).filter(
            SalaryEntry.is_anonymous == True,
            SalaryEntry.annual_salary > 0
        )
        
        # Apply filters
        if industry:
            query = query.filter(SalaryEntry.industry.ilike(f"%{industry}%"))
        if location:
            query = query.filter(SalaryEntry.location.ilike(f"%{location}%"))
        
        # Group and filter
        results = query.group_by(
            SalaryEntry.job_title
        ).having(
            func.count(SalaryEntry.id) >= 3  # At least 3 entries
        ).order_by(
            desc('avg_salary')
        ).limit(limit).all()
        
        # Format results
        market_data = []
        for result in results:
            market_data.append({
                "job_title": result.job_title,
                "sample_size": result.count,
                "average_salary": round(result.avg_salary, 2)
            })
        
        return {
            "market_overview": market_data,
            "filters_applied": {
                "industry": industry,
                "location": location
            },
            "total_positions": len(market_data)
        }
        
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get market overview"
        )

@router.get("/benchmark/{job_title}")
def benchmark_salary(
    job_title: str,
    current_salary: float = Query(..., description="Your current salary to benchmark"),
    years_of_experience: Optional[int] = Query(None, description="Your years of experience"),
    industry: Optional[str] = Query(None, description="Your industry"),
    location: Optional[str] = Query(None, description="Your location"),
    db: Session = Depends(get_db)
):
    """
    Benchmark your current salary against market data.
    
    Returns:
    - Your percentile ranking
    - Salary gap analysis
    - Market position
    - Improvement recommendations
    """
    try:
        from ..models.profile_models import SalaryEntry
        from sqlalchemy import func
        
        # Build comparison query
        base_query = db.query(SalaryEntry).filter(
            SalaryEntry.job_title.ilike(f"%{job_title}%"),
            SalaryEntry.is_anonymous == True,
            SalaryEntry.annual_salary > 0
        )
        
        # Apply contextual filters
        if years_of_experience is not None:
            base_query = base_query.filter(
                SalaryEntry.years_of_experience.between(
                    max(0, years_of_experience - 2),
                    years_of_experience + 2
                )
            )
        
        if industry:
            base_query = base_query.filter(
                SalaryEntry.industry.ilike(f"%{industry}%")
            )
        
        if location:
            base_query = base_query.filter(
                SalaryEntry.location.ilike(f"%{location}%")
            )
        
        # Calculate percentile ranking
        total_count = base_query.count()
        
        if total_count < 5:
            return {
                "message": "Insufficient data for accurate benchmarking",
                "suggestion": "Try with broader criteria or similar job titles",
                "sample_size": total_count
            }
        
        # Count salaries below current salary
        below_count = base_query.filter(
            SalaryEntry.annual_salary <= current_salary
        ).count()
        
        percentile = (below_count / total_count) * 100
        
        # Get market statistics
        stats = base_query.with_entities(
            func.avg(SalaryEntry.annual_salary).label('avg_salary')
        ).first()
        
        # Determine market position
        if percentile >= 90:
            position = "Top Performer"
            position_description = "You're in the top 10% of earners for this role"
        elif percentile >= 75:
            position = "Above Average"
            position_description = "You're earning above the 75th percentile"
        elif percentile >= 50:
            position = "Market Average"
            position_description = "You're earning around the market median"
        elif percentile >= 25:
            position = "Below Average"
            position_description = "You're earning below the market median"
        else:
            position = "Entry Level"
            position_description = "You're in the bottom 25% of earners for this role"
        
        # Generate recommendations
        recommendations = []
        avg_gap = current_salary - stats.avg_salary
        
        if percentile < 50:
            recommendations.append("Consider negotiating a salary increase with your current employer")
            recommendations.append("Explore opportunities at companies known for competitive compensation")
            if avg_gap < -10000:
                recommendations.append(f"Market average is ${abs(avg_gap):,.0f} higher than your current salary")
        
        if percentile < 75:
            recommendations.append("Develop high-demand skills to increase your market value")
            recommendations.append("Consider pursuing relevant certifications or training")
        
        recommendations.extend([
            "Research total compensation packages, not just base salary",
            "Network within your industry to discover better opportunities",
            "Document your achievements for stronger salary negotiations"
        ])
        
        return {
            "benchmark_results": {
                "your_salary": current_salary,
                "percentile_ranking": round(percentile, 1),
                "market_position": position,
                "position_description": position_description,
                "sample_size": total_count
            },
            "market_comparison": {
                "market_average": round(stats.avg_salary, 2),
                "gap_to_average": round(avg_gap, 2)
            },
            "recommendations": recommendations,
            "context": {
                "job_title": job_title,
                "years_of_experience": years_of_experience,
                "industry": industry,
                "location": location
            }
        }
        
    except Exception as e:
        from fastapi import HTTPException
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error benchmarking salary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to benchmark salary"
        )