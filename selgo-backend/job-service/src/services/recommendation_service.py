# File: job-service/src/services/recommendation_service.py

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, func, and_, or_
from typing import List, Dict, Any, Optional, Tuple
from ..models.job_models import Job, JobView, SavedJob
from ..models.profile_models import JobProfile, UserSkill, UserLanguage
from ..models.recommendation_models import JobRecommendation, UserJobPreferences, RecommendationAlgorithm
from ..repositories.job_repository import JobRepository
from ..utils.auth_utils import get_user_from_token
from datetime import datetime, timedelta
import logging
import math

logger = logging.getLogger(__name__)

class RecommendationService:
    def __init__(self):
        self.job_repo = JobRepository()
    
    def get_job_recommendations(self, db: Session, user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Get personalized job recommendations for user."""
        try:
            # Get user profile and preferences
            user_profile = self._get_user_profile(db, user_id)
            user_preferences = self._get_user_preferences(db, user_id)
            
            # Generate recommendations using different algorithms
            recommendations = []
            
            # 1. Content-based recommendations (40% weight)
            content_based = self._get_content_based_recommendations(db, user_id, user_profile, limit=limit//2)
            recommendations.extend(content_based)
            
            # 2. Collaborative filtering (30% weight)
            collaborative = self._get_collaborative_recommendations(db, user_id, limit=limit//3)
            recommendations.extend(collaborative)
            
            # 3. Location-based recommendations (20% weight)
            location_based = self._get_location_based_recommendations(db, user_id, user_profile, limit=limit//4)
            recommendations.extend(location_based)
            
            # 4. Recent/trending jobs (10% weight)
            trending = self._get_trending_recommendations(db, limit=limit//5)
            recommendations.extend(trending)
            
            # Remove duplicates and sort by score
            unique_recommendations = self._deduplicate_and_rank(recommendations)
            
            # Store recommendations in database
            self._store_recommendations(db, user_id, unique_recommendations[:limit])
            
            # Return formatted recommendations
            return self._format_recommendations(db, unique_recommendations[:limit])
            
        except Exception as e:
            logger.error(f"Error generating recommendations for user {user_id}: {str(e)}")
            # Fallback to recent jobs
            return self._get_fallback_recommendations(db, limit)
    
    def _get_user_profile(self, db: Session, user_id: int) -> Optional[JobProfile]:
        """Get user's job profile."""
        return db.query(JobProfile).options(
            joinedload(JobProfile.skills).joinedload(UserSkill.skill),
            joinedload(JobProfile.languages).joinedload(UserLanguage.language),
            joinedload(JobProfile.work_experiences)
        ).filter(JobProfile.user_id == user_id).first()
    
    def _get_user_preferences(self, db: Session, user_id: int) -> Optional[UserJobPreferences]:
        """Get user's job preferences."""
        return db.query(UserJobPreferences).filter(
            UserJobPreferences.user_id == user_id
        ).first()
    
    def _get_content_based_recommendations(self, db: Session, user_id: int, 
                                         user_profile: Optional[JobProfile], limit: int) -> List[Dict[str, Any]]:
        """Generate content-based recommendations based on user profile."""
        recommendations = []
        
        if not user_profile:
            return recommendations
        
        # Get jobs based on user's skills
        user_skills = [skill.skill.name for skill in user_profile.skills] if user_profile.skills else []
        
        # Get jobs based on desired job title
        desired_titles = [user_profile.desired_job_title] if user_profile.desired_job_title else []
        
        # Build query
        query = db.query(Job).filter(Job.status == "active")
        
        # Filter by skills (tags contain user skills)
        if user_skills:
            for skill in user_skills[:3]:  # Top 3 skills
                query = query.filter(Job.tags.contains([skill]))
        
        # Filter by desired job titles
        if desired_titles:
            title_filters = [Job.title.ilike(f"%{title}%") for title in desired_titles]
            query = query.filter(or_(*title_filters))
        
        # Filter by location preference
        if user_profile.location:
            query = query.filter(Job.location.ilike(f"%{user_profile.location}%"))
        
        # Filter by salary range
        if user_profile.desired_salary_min:
            query = query.filter(Job.salary_min >= user_profile.desired_salary_min)
        if user_profile.desired_salary_max:
            query = query.filter(Job.salary_max <= user_profile.desired_salary_max)
        
        # Exclude already viewed jobs
        viewed_job_ids = db.query(JobView.job_id).filter(JobView.user_id == user_id).subquery()
        query = query.filter(~Job.id.in_(viewed_job_ids))
        
        jobs = query.order_by(desc(Job.created_at)).limit(limit).all()
        
        for job in jobs:
            score = self._calculate_content_based_score(job, user_profile)
            recommendations.append({
                'job_id': job.id,
                'score': score,
                'algorithm': RecommendationAlgorithm.CONTENT_BASED,
                'reason': self._generate_content_based_reason(job, user_profile)
            })
        
        return recommendations
    
    def _get_collaborative_recommendations(self, db: Session, user_id: int, limit: int) -> List[Dict[str, Any]]:
        """Generate collaborative filtering recommendations."""
        recommendations = []
        
        # Find users with similar job viewing/saving patterns
        user_saved_jobs = db.query(SavedJob.job_id).filter(SavedJob.user_id == user_id).subquery()
        user_viewed_jobs = db.query(JobView.job_id).filter(JobView.user_id == user_id).subquery()
        
        # Find similar users who saved/viewed the same jobs
        similar_users = db.query(SavedJob.user_id).filter(
            SavedJob.job_id.in_(user_saved_jobs),
            SavedJob.user_id != user_id
        ).group_by(SavedJob.user_id).having(func.count(SavedJob.job_id) >= 2).all()
        
        if similar_users:
            similar_user_ids = [user[0] for user in similar_users]
            
            # Get jobs that similar users saved but current user hasn't seen
            recommended_jobs = db.query(Job).join(SavedJob).filter(
                SavedJob.user_id.in_(similar_user_ids),
                ~Job.id.in_(user_saved_jobs),
                ~Job.id.in_(user_viewed_jobs),
                Job.status == "active"
            ).order_by(desc(Job.created_at)).limit(limit).all()
            
            for job in recommended_jobs:
                score = 0.7  # Base collaborative score
                recommendations.append({
                    'job_id': job.id,
                    'score': score,
                    'algorithm': RecommendationAlgorithm.COLLABORATIVE,
                    'reason': 'Users with similar interests also saved this job'
                })
        
        return recommendations
    
    def _get_location_based_recommendations(self, db: Session, user_id: int, 
                                          user_profile: Optional[JobProfile], limit: int) -> List[Dict[str, Any]]:
        """Generate location-based recommendations."""
        recommendations = []
        
        if not user_profile or not user_profile.location:
            return recommendations
        
        # Get jobs in the same location or nearby
        location_query = db.query(Job).filter(
            Job.status == "active",
            or_(
                Job.location.ilike(f"%{user_profile.location}%"),
                Job.city.ilike(f"%{user_profile.location}%"),
                Job.is_remote == True
            )
        )
        
        # Exclude already viewed jobs
        viewed_job_ids = db.query(JobView.job_id).filter(JobView.user_id == user_id).subquery()
        location_query = location_query.filter(~Job.id.in_(viewed_job_ids))
        
        jobs = location_query.order_by(desc(Job.created_at)).limit(limit).all()
        
        for job in jobs:
            score = 0.6 if job.is_remote else 0.8  # Remote jobs get slightly lower score
            recommendations.append({
                'job_id': job.id,
                'score': score,
                'algorithm': RecommendationAlgorithm.LOCATION_BASED,
                'reason': f'Located in your preferred area: {user_profile.location}'
            })
        
        return recommendations
    
    def _get_trending_recommendations(self, db: Session, limit: int) -> List[Dict[str, Any]]:
        """Get trending/popular jobs."""
        recommendations = []
        
        # Get jobs with high view counts in the last 7 days
        cutoff_date = datetime.utcnow() - timedelta(days=7)
        trending_jobs = db.query(Job).filter(
            Job.status == "active",
            Job.created_at >= cutoff_date
        ).order_by(desc(Job.view_count)).limit(limit).all()
        
        for job in trending_jobs:
            score = min(0.5 + (job.view_count / 1000), 0.9)  # Score based on views
            recommendations.append({
                'job_id': job.id,
                'score': score,
                'algorithm': RecommendationAlgorithm.CONTENT_BASED,
                'reason': f'Trending job with {job.view_count} views'
            })
        
        return recommendations
    
    def _calculate_content_based_score(self, job: Job, user_profile: JobProfile) -> float:
        """Calculate content-based recommendation score."""
        score = 0.0
        
        # Skills match (40% of score)
        if user_profile.skills and job.tags:
            user_skills = set(skill.skill.name.lower() for skill in user_profile.skills)
            job_tags = set(tag.lower() for tag in job.tags)
            skills_match = len(user_skills.intersection(job_tags)) / len(user_skills)
            score += skills_match * 0.4
        
        # Title match (30% of score)
        if user_profile.desired_job_title and job.title:
            title_match = 1.0 if user_profile.desired_job_title.lower() in job.title.lower() else 0.0
            score += title_match * 0.3
        
        # Salary match (20% of score)
        if user_profile.desired_salary_min and job.salary_max:
            if job.salary_max >= user_profile.desired_salary_min:
                score += 0.2
        
        # Location match (10% of score)
        if user_profile.location and (job.location or job.is_remote):
            if job.is_remote or user_profile.location.lower() in (job.location or "").lower():
                score += 0.1
        
        return min(score, 1.0)
    
    def _generate_content_based_reason(self, job: Job, user_profile: JobProfile) -> str:
        """Generate reason for content-based recommendation."""
        reasons = []
        
        if user_profile.skills and job.tags:
            user_skills = set(skill.skill.name.lower() for skill in user_profile.skills)
            job_tags = set(tag.lower() for tag in job.tags)
            matching_skills = user_skills.intersection(job_tags)
            if matching_skills:
                reasons.append(f"Matches your skills: {', '.join(list(matching_skills)[:2])}")
        
        if user_profile.desired_job_title and job.title:
            if user_profile.desired_job_title.lower() in job.title.lower():
                reasons.append(f"Matches your desired role: {user_profile.desired_job_title}")
        
        if user_profile.location and job.location:
            if user_profile.location.lower() in job.location.lower():
                reasons.append(f"Located in {job.location}")
        
        return "; ".join(reasons) if reasons else "Recommended based on your profile"
    
    def _deduplicate_and_rank(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicates and rank by score."""
        seen_jobs = set()
        unique_recommendations = []
        
        # Sort by score first
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        for rec in recommendations:
            if rec['job_id'] not in seen_jobs:
                seen_jobs.add(rec['job_id'])
                unique_recommendations.append(rec)
        
        return unique_recommendations
    
    def _store_recommendations(self, db: Session, user_id: int, recommendations: List[Dict[str, Any]]) -> None:
        """Store recommendations in database."""
        try:
            # Delete old recommendations for this user
            db.query(JobRecommendation).filter(JobRecommendation.user_id == user_id).delete()
            
            # Store new recommendations
            for rec in recommendations:
                db_recommendation = JobRecommendation(
                    user_id=user_id,
                    job_id=rec['job_id'],
                    score=rec['score'],
                    algorithm_used=rec['algorithm'],
                    reason=rec['reason']
                )
                db.add(db_recommendation)
            
            db.commit()
            
        except Exception as e:
            logger.error(f"Error storing recommendations: {str(e)}")
            db.rollback()
    
    def _format_recommendations(self, db: Session, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format recommendations with job details."""
        formatted = []
        
        for rec in recommendations:
            job = db.query(Job).options(
                joinedload(Job.company)
            ).filter(Job.id == rec['job_id']).first()
            
            if job:
                formatted.append({
                    'job_id': job.id,
                    'title': job.title,
                    'company': job.company.name if job.company else None,
                    'location': job.location,
                    'salary_min': job.salary_min,
                    'salary_max': job.salary_max,
                    'score': rec['score'],
                    'reason': rec['reason'],
                    'created_at': job.created_at
                })
        
        return formatted
    
    def _get_fallback_recommendations(self, db: Session, limit: int) -> List[Dict[str, Any]]:
        """Fallback recommendations when personalization fails."""
        jobs = db.query(Job).options(
            joinedload(Job.company)
        ).filter(
            Job.status == "active"
        ).order_by(desc(Job.created_at)).limit(limit).all()
        
        return [{
            'job_id': job.id,
            'title': job.title,
            'company': job.company.name if job.company else None,
            'location': job.location,
            'salary_min': job.salary_min,
            'salary_max': job.salary_max,
            'score': 0.5,
            'reason': 'Recently posted job',
            'created_at': job.created_at
        } for job in jobs]
    
    def track_recommendation_interaction(self, db: Session, user_id: int, job_id: int, 
                                       interaction_type: str) -> None:
        """Track user interaction with recommendations."""
        try:
            recommendation = db.query(JobRecommendation).filter(
                JobRecommendation.user_id == user_id,
                JobRecommendation.job_id == job_id
            ).first()
            
            if recommendation:
                if interaction_type == "view":
                    recommendation.is_viewed = True
                    recommendation.viewed_at = datetime.utcnow()
                elif interaction_type == "click":
                    recommendation.is_clicked = True
                    recommendation.clicked_at = datetime.utcnow()
                elif interaction_type == "apply":
                    recommendation.is_applied = True
                    recommendation.applied_at = datetime.utcnow()
                elif interaction_type == "dismiss":
                    recommendation.is_dismissed = True
                    recommendation.dismissed_at = datetime.utcnow()
                
                db.commit()
                
        except Exception as e:
            logger.error(f"Error tracking recommendation interaction: {str(e)}")
            db.rollback()
    
    def update_user_preferences(self, db: Session, user_id: int, preferences: Dict[str, Any]) -> UserJobPreferences:
        """Update user job preferences."""
        user_prefs = db.query(UserJobPreferences).filter(
            UserJobPreferences.user_id == user_id
        ).first()
        
        if not user_prefs:
            user_prefs = UserJobPreferences(user_id=user_id)
            db.add(user_prefs)
        
        # Update preferences
        for key, value in preferences.items():
            if hasattr(user_prefs, key):
                setattr(user_prefs, key, value)
        
        user_prefs.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user_prefs)
        
        return user_prefs