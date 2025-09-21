# File: job-service/src/services/job_alert_service.py

from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ..models.recommendation_models import JobAlert  # Changed from job_models to recommendation_models
from ..models.schemas import JobAlertCreate, JobAlertResponse, JobAlertUpdate, MessageResponse
from ..repositories.job_repository import JobRepository
from fastapi import HTTPException, status
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class JobAlertService:
    def __init__(self):
        self.job_repo = JobRepository()
    
    def create_job_alert(self, db: Session, user_id: int, alert_data: JobAlertCreate) -> JobAlertResponse:
        """Create a new job alert."""
        try:
            db_alert = JobAlert(
                user_id=user_id,
                **alert_data.dict()
            )
            
            db.add(db_alert)
            db.commit()
            db.refresh(db_alert)
            
            logger.info(f"Created job alert: {db_alert.id} for user: {user_id}")
            return JobAlertResponse.model_validate(db_alert)
            
        except Exception as e:
            logger.error(f"Error creating job alert: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create job alert"
            )
    
    def get_user_job_alerts(self, db: Session, user_id: int) -> List[JobAlertResponse]:
        """Get all job alerts for a user."""
        try:
            alerts = db.query(JobAlert).filter(
                JobAlert.user_id == user_id
            ).order_by(JobAlert.created_at.desc()).all()
            
            return [JobAlertResponse.model_validate(alert) for alert in alerts]
            
        except Exception as e:
            logger.error(f"Error getting user job alerts: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get job alerts"
            )
    
    def update_job_alert(self, db: Session, user_id: int, alert_id: int, alert_data: JobAlertUpdate) -> JobAlertResponse:
        """Update job alert."""
        try:
            db_alert = db.query(JobAlert).filter(
                JobAlert.id == alert_id,
                JobAlert.user_id == user_id
            ).first()
            
            if not db_alert:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Job alert not found"
                )
            
            update_data = alert_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_alert, field, value)
            
            db_alert.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_alert)
            
            return JobAlertResponse.model_validate(db_alert)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating job alert: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update job alert"
            )
    
    def delete_job_alert(self, db: Session, user_id: int, alert_id: int) -> MessageResponse:
        """Delete job alert."""
        try:
            db_alert = db.query(JobAlert).filter(
                JobAlert.id == alert_id,
                JobAlert.user_id == user_id
            ).first()
            
            if not db_alert:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Job alert not found"
                )
            
            db.delete(db_alert)
            db.commit()
            
            return MessageResponse(message="Job alert deleted successfully")
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting job alert: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete job alert"
            )
    
    def toggle_job_alert(self, db: Session, user_id: int, alert_id: int) -> JobAlertResponse:
        """Toggle job alert active status."""
        try:
            db_alert = db.query(JobAlert).filter(
                JobAlert.id == alert_id,
                JobAlert.user_id == user_id
            ).first()
            
            if not db_alert:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Job alert not found"
                )
            
            db_alert.is_active = not db_alert.is_active
            db_alert.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_alert)
            
            return JobAlertResponse.model_validate(db_alert)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error toggling job alert: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to toggle job alert"
            )
    
    def check_and_send_alerts(self, db: Session) -> Dict[str, int]:
        """Check all active alerts and send notifications for matching jobs."""
        try:
            # Get all active alerts
            active_alerts = db.query(JobAlert).filter(
                JobAlert.is_active == True
            ).all()
            
            alerts_processed = 0
            notifications_sent = 0
            
            for alert in active_alerts:
                # Check if it's time to send alert based on frequency
                if self._should_send_alert(alert):
                    matching_jobs = self._find_matching_jobs(db, alert)
                    
                    if matching_jobs:
                        # Send notification (implement email/push logic)
                        self._send_alert_notification(alert, matching_jobs)
                        
                        # Update alert statistics
                        alert.total_jobs_sent += len(matching_jobs)
                        alert.last_sent_at = datetime.utcnow()
                        notifications_sent += 1
                
                alerts_processed += 1
            
            db.commit()
            
            return {
                'alerts_processed': alerts_processed,
                'notifications_sent': notifications_sent
            }
            
        except Exception as e:
            logger.error(f"Error checking and sending alerts: {str(e)}")
            return {'alerts_processed': 0, 'notifications_sent': 0}
    
    def _should_send_alert(self, alert: JobAlert) -> bool:
        """Check if alert should be sent based on frequency."""
        if not alert.last_sent_at:
            return True
        
        now = datetime.utcnow()
        time_diff = now - alert.last_sent_at
        
        if alert.frequency == "daily":
            return time_diff.days >= 1
        elif alert.frequency == "weekly":
            return time_diff.days >= 7
        elif alert.frequency == "monthly":
            return time_diff.days >= 30
        
        return False
    
    def _find_matching_jobs(self, db: Session, alert: JobAlert) -> List[Dict[str, Any]]:
        """Find jobs matching the alert criteria."""
        try:
            # Convert alert criteria to search parameters
            from ..models.schemas import JobSearchRequest
            
            search_params = JobSearchRequest(**alert.search_criteria)
            
            # Only get jobs created since last alert or in last 24 hours
            if alert.last_sent_at:
                search_params.posted_within_days = (datetime.utcnow() - alert.last_sent_at).days
            else:
                search_params.posted_within_days = 1
            
            # Search for matching jobs
            jobs, total = self.job_repo.search_jobs(db, search_params)
            
            return [
                {
                    'id': job.id,
                    'title': job.title,
                    'company': job.company.name if job.company else None,
                    'location': job.location,
                    'salary_min': job.salary_min,
                    'salary_max': job.salary_max,
                    'created_at': job.created_at
                }
                for job in jobs
            ]
            
        except Exception as e:
            logger.error(f"Error finding matching jobs for alert {alert.id}: {str(e)}")
            return []
    
    def _send_alert_notification(self, alert: JobAlert, matching_jobs: List[Dict[str, Any]]) -> None:
        """Send notification for job alert."""
        try:
            # This would integrate with email/push notification service
            logger.info(f"Sending alert notification for alert {alert.id} with {len(matching_jobs)} jobs")
            
            # Example email implementation:
            # subject = f"New jobs matching your alert: {alert.alert_name}"
            # body = self._generate_alert_email_body(alert, matching_jobs)
            # send_email(user_email, subject, body)
            
            # Example push notification:
            # send_push_notification(alert.user_id, f"{len(matching_jobs)} new jobs match your alert")
            
        except Exception as e:
            logger.error(f"Error sending alert notification: {str(e)}")
    
    def _generate_alert_email_body(self, alert: JobAlert, matching_jobs: List[Dict[str, Any]]) -> str:
        """Generate email body for job alert."""
        body = f"Hello,\n\nWe found {len(matching_jobs)} new jobs matching your alert '{alert.alert_name}':\n\n"
        
        for job in matching_jobs[:5]:  # Show max 5 jobs in email
            body += f"• {job['title']} at {job['company'] or 'Company'}\n"
            body += f"  Location: {job['location'] or 'Not specified'}\n"
            if job['salary_min'] or job['salary_max']:
                salary = []
                if job['salary_min']:
                    salary.append(f"${job['salary_min']:,.0f}")
                if job['salary_max']:
                    salary.append(f"${job['salary_max']:,.0f}")
                body += f"  Salary: {' - '.join(salary)}\n"
            body += "\n"
        
        if len(matching_jobs) > 5:
            body += f"... and {len(matching_jobs) - 5} more jobs.\n\n"
        
        body += "Visit our job portal to view all matching jobs and apply.\n\n"
        body += "Best regards,\nThe Job Team"
        
        return body