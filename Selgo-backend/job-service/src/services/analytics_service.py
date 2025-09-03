# File: job-service/src/services/analytics_service.py

from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from ..models.analytics_models import JobAnalytics, UserJobInteraction
from ..models.job_models import Job, JobView, SavedJob, JobApplication
import logging

logger = logging.getLogger(__name__)

class JobAnalyticsService:
    
    def track_job_interaction(self, db: Session, job_id: int, interaction_type: str,
                            user_id: Optional[int] = None, session_id: Optional[str] = None,
                            ip_address: Optional[str] = None, user_agent: Optional[str] = None,
                            referrer: Optional[str] = None, time_spent: Optional[int] = None) -> None:
        """Track user interaction with job."""
        try:
            interaction = UserJobInteraction(
                user_id=user_id,
                job_id=job_id,
                interaction_type=interaction_type,
                session_id=session_id,
                ip_address=ip_address,
                user_agent=user_agent,
                referrer=referrer,
                time_spent=time_spent
            )
            
            db.add(interaction)
            db.commit()
            
            # Update daily analytics
            self._update_daily_analytics(db, job_id, interaction_type)
            
        except Exception as e:
            logger.error(f"Error tracking job interaction: {str(e)}")
            db.rollback()
    
    def _update_daily_analytics(self, db: Session, job_id: int, interaction_type: str) -> None:
        """Update daily analytics for a job."""
        today = datetime.utcnow().date()
        
        # Get or create daily analytics record
        analytics = db.query(JobAnalytics).filter(
            JobAnalytics.job_id == job_id,
            func.date(JobAnalytics.date) == today
        ).first()
        
        if not analytics:
            analytics = JobAnalytics(job_id=job_id, date=datetime.utcnow())
            db.add(analytics)
        
        # Update counters based on interaction type
        if interaction_type == "view":
            analytics.views_count += 1
        elif interaction_type == "apply":
            analytics.applications_count += 1
        elif interaction_type == "save":
            analytics.saves_count += 1
        
        db.commit()
    
    def get_job_analytics(self, db: Session, job_id: int, days: int = 30) -> Dict[str, Any]:
        """Get analytics for a specific job."""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get daily analytics
        daily_analytics = db.query(JobAnalytics).filter(
            JobAnalytics.job_id == job_id,
            JobAnalytics.date >= start_date
        ).order_by(JobAnalytics.date).all()
        
        # Calculate summary statistics
        total_views = sum(a.views_count for a in daily_analytics)
        total_applications = sum(a.applications_count for a in daily_analytics)
        total_saves = sum(a.saves_count for a in daily_analytics)
        
        # Get conversion rates
        view_to_application_rate = (total_applications / total_views * 100) if total_views > 0 else 0
        view_to_save_rate = (total_saves / total_views * 100) if total_views > 0 else 0
        
        # Get geographic data
        geographic_data = self._get_geographic_analytics(db, job_id, start_date, end_date)
        
        # Get traffic sources
        traffic_sources = self._get_traffic_sources(db, job_id, start_date, end_date)
        
        return {
            'job_id': job_id,
            'period': {
                'start_date': start_date,
                'end_date': end_date,
                'days': days
            },
            'summary': {
                'total_views': total_views,
                'total_applications': total_applications,
                'total_saves': total_saves,
                'view_to_application_rate': round(view_to_application_rate, 2),
                'view_to_save_rate': round(view_to_save_rate, 2)
            },
            'daily_data': [
                {
                    'date': a.date.isoformat(),
                    'views': a.views_count,
                    'applications': a.applications_count,
                    'saves': a.saves_count
                }
                for a in daily_analytics
            ],
            'geographic_data': geographic_data,
            'traffic_sources': traffic_sources
        }
    
    def get_employer_analytics(self, db: Session, employer_id: int, days: int = 30) -> Dict[str, Any]:
        """Get analytics for all jobs posted by an employer."""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get all jobs by employer
        employer_jobs = db.query(Job).filter(Job.posted_by == employer_id).all()
        job_ids = [job.id for job in employer_jobs]
        
        if not job_ids:
            return {
                'employer_id': employer_id,
                'total_jobs': 0,
                'summary': {
                    'total_views': 0,
                    'total_applications': 0,
                    'total_saves': 0,
                    'avg_view_to_application_rate': 0,
                    'avg_view_to_save_rate': 0
                },
                'top_performing_jobs': [],
                'job_performance': []
            }
        
        # Get analytics for all jobs
        analytics_data = db.query(JobAnalytics).filter(
            JobAnalytics.job_id.in_(job_ids),
            JobAnalytics.date >= start_date
        ).all()
        
        # Aggregate data
        total_views = sum(a.views_count for a in analytics_data)
        total_applications = sum(a.applications_count for a in analytics_data)
        total_saves = sum(a.saves_count for a in analytics_data)
        
        # Calculate per-job performance
        job_performance = {}
        for job in employer_jobs:
            job_analytics = [a for a in analytics_data if a.job_id == job.id]
            job_views = sum(a.views_count for a in job_analytics)
            job_applications = sum(a.applications_count for a in job_analytics)
            job_saves = sum(a.saves_count for a in job_analytics)
            
            job_performance[job.id] = {
                'job_id': job.id,
                'title': job.title,
                'views': job_views,
                'applications': job_applications,
                'saves': job_saves,
                'application_rate': (job_applications / job_views * 100) if job_views > 0 else 0,
                'save_rate': (job_saves / job_views * 100) if job_views > 0 else 0,
                'created_at': job.created_at
            }
        
        # Get top performing jobs
        top_jobs = sorted(
            job_performance.values(),
            key=lambda x: x['views'],
            reverse=True
        )[:5]
        
        return {
            'employer_id': employer_id,
            'total_jobs': len(employer_jobs),
            'period': {
                'start_date': start_date,
                'end_date': end_date,
                'days': days
            },
            'summary': {
                'total_views': total_views,
                'total_applications': total_applications,
                'total_saves': total_saves,
                'avg_view_to_application_rate': round((total_applications / total_views * 100) if total_views > 0 else 0, 2),
                'avg_view_to_save_rate': round((total_saves / total_views * 100) if total_views > 0 else 0, 2)
            },
            'top_performing_jobs': top_jobs,
            'job_performance': list(job_performance.values())
        }
    
    def _get_geographic_analytics(self, db: Session, job_id: int, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get geographic distribution of job views."""
        # This would require IP geolocation - simplified for now
        interactions = db.query(UserJobInteraction).filter(
            UserJobInteraction.job_id == job_id,
            UserJobInteraction.interaction_type == "view",
            UserJobInteraction.created_at >= start_date,
            UserJobInteraction.created_at <= end_date,
            UserJobInteraction.ip_address.isnot(None)
        ).all()
        
        # Group by IP address (in real implementation, would geolocate)
        ip_counts = {}
        for interaction in interactions:
            ip = interaction.ip_address
            if ip:
                # Simplified: use first part of IP as "region"
                region = '.'.join(ip.split('.')[:2]) + '.x.x'
                ip_counts[region] = ip_counts.get(region, 0) + 1
        
        return [
            {'region': region, 'views': count}
            for region, count in sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)
        ]
    
    def _get_traffic_sources(self, db: Session, job_id: int, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get traffic sources for job views."""
        interactions = db.query(UserJobInteraction).filter(
            UserJobInteraction.job_id == job_id,
            UserJobInteraction.interaction_type == "view",
            UserJobInteraction.created_at >= start_date,
            UserJobInteraction.created_at <= end_date,
            UserJobInteraction.referrer.isnot(None)
        ).all()
        
        source_counts = {}
        for interaction in interactions:
            referrer = interaction.referrer
            if referrer:
                # Extract domain from referrer
                if 'google' in referrer:
                    source = 'Google Search'
                elif 'linkedin' in referrer:
                    source = 'LinkedIn'
                elif 'facebook' in referrer:
                    source = 'Facebook'
                elif 'indeed' in referrer:
                    source = 'Indeed'
                else:
                    source = 'Direct/Other'
            else:
                source = 'Direct'
            
            source_counts[source] = source_counts.get(source, 0) + 1
        
        return [
            {'source': source, 'views': count, 'percentage': round(count / len(interactions) * 100, 2)}
            for source, count in sorted(source_counts.items(), key=lambda x: x[1], reverse=True)
        ]
    
    def get_platform_analytics(self, db: Session, days: int = 30) -> Dict[str, Any]:
        """Get overall platform analytics."""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get total counts
        total_jobs = db.query(Job).filter(Job.created_at >= start_date).count()
        total_views = db.query(func.sum(JobAnalytics.views_count)).filter(
            JobAnalytics.date >= start_date
        ).scalar() or 0
        total_applications = db.query(func.sum(JobAnalytics.applications_count)).filter(
            JobAnalytics.date >= start_date
        ).scalar() or 0
        total_saves = db.query(func.sum(JobAnalytics.saves_count)).filter(
            JobAnalytics.date >= start_date
        ).scalar() or 0
        
        # Get daily trends
        daily_stats = db.query(
            func.date(JobAnalytics.date).label('date'),
            func.sum(JobAnalytics.views_count).label('views'),
            func.sum(JobAnalytics.applications_count).label('applications'),
            func.sum(JobAnalytics.saves_count).label('saves')
        ).filter(
            JobAnalytics.date >= start_date
        ).group_by(
            func.date(JobAnalytics.date)
        ).order_by('date').all()
        
        # Get top job categories
        top_categories = db.query(
            Job.category_id,
            func.count(Job.id).label('job_count'),
            func.sum(Job.view_count).label('total_views')
        ).filter(
            Job.created_at >= start_date
        ).group_by(
            Job.category_id
        ).order_by(
            desc('total_views')
        ).limit(10).all()
        
        return {
            'period': {
                'start_date': start_date,
                'end_date': end_date,
                'days': days
            },
            'summary': {
                'total_jobs_posted': total_jobs,
                'total_views': total_views,
                'total_applications': total_applications,
                'total_saves': total_saves,
                'avg_views_per_job': round(total_views / total_jobs, 2) if total_jobs > 0 else 0,
                'overall_application_rate': round(total_applications / total_views * 100, 2) if total_views > 0 else 0
            },
            'daily_trends': [
                {
                    'date': stat.date.isoformat(),
                    'views': stat.views or 0,
                    'applications': stat.applications or 0,
                    'saves': stat.saves or 0
                }
                for stat in daily_stats
            ],
            'top_categories': [
                {
                    'category_id': cat.category_id,
                    'job_count': cat.job_count,
                    'total_views': cat.total_views or 0
                }
                for cat in top_categories
            ]
        }
    
    def get_user_activity_analytics(self, db: Session, user_id: int, days: int = 30) -> Dict[str, Any]:
        """Get analytics for a specific user's job search activity."""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get user interactions
        interactions = db.query(UserJobInteraction).filter(
            UserJobInteraction.user_id == user_id,
            UserJobInteraction.created_at >= start_date
        ).all()
        
        # Group by interaction type
        interaction_counts = {}
        for interaction in interactions:
            interaction_type = interaction.interaction_type
            interaction_counts[interaction_type] = interaction_counts.get(interaction_type, 0) + 1
        
        # Get viewed jobs
        viewed_jobs = db.query(JobView).filter(
            JobView.user_id == user_id,
            JobView.viewed_at >= start_date
        ).count()
        
        # Get saved jobs
        saved_jobs = db.query(SavedJob).filter(
            SavedJob.user_id == user_id,
            SavedJob.saved_at >= start_date
        ).count()
        
        # Get applications
        applications = db.query(JobApplication).filter(
            JobApplication.user_id == user_id,
            JobApplication.applied_at >= start_date
        ).count()
        
        # Calculate activity score
        activity_score = (viewed_jobs * 1) + (saved_jobs * 2) + (applications * 5)
        
        return {
            'user_id': user_id,
            'period': {
                'start_date': start_date,
                'end_date': end_date,
                'days': days
            },
            'activity_summary': {
                'total_interactions': len(interactions),
                'jobs_viewed': viewed_jobs,
                'jobs_saved': saved_jobs,
                'applications_submitted': applications,
                'activity_score': activity_score
            },
            'interaction_breakdown': interaction_counts,
            'engagement_rate': {
                'save_rate': round(saved_jobs / viewed_jobs * 100, 2) if viewed_jobs > 0 else 0,
                'application_rate': round(applications / viewed_jobs * 100, 2) if viewed_jobs > 0 else 0
            }
        }