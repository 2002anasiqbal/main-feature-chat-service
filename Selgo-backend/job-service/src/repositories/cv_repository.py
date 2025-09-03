# File: job-service/src/repositories/cv_repository.py

from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from typing import Optional, List, Dict, Any
from ..models.cv_models import CV, UploadedCV, CVTemplate, CVStatus
from ..models.schemas import CVCreate, CVUpdate
from datetime import datetime
import logging
import os
import json

logger = logging.getLogger(__name__)

class CVRepository:
    
    def create_cv(self, db: Session, cv_data: CVCreate, user_id: int) -> CV:
        """Create a new CV."""
        try:
            # Handle template enum conversion - use UPPERCASE values for database
            if hasattr(cv_data.template, 'value'):
                template_value = cv_data.template.value.upper()
            else:
                template_value = str(cv_data.template).upper()
            
            # Ensure template value is valid (UPPERCASE for database)
            valid_templates = ['MODERN', 'CLASSIC', 'CREATIVE', 'MINIMAL']
            if template_value not in valid_templates:
                template_value = 'MODERN'
            
            # Convert cv_data to JSON string if it's a dict
            cv_data_json = cv_data.cv_data
            if isinstance(cv_data_json, dict):
                cv_data_json = json.dumps(cv_data_json)
            elif cv_data_json is None:
                cv_data_json = '{}'
            
            # Create the CV object
            db_cv = CV(
                user_id=user_id,
                title=cv_data.title,
                template=template_value,
                status='DRAFT',  # Use UPPERCASE for database enum
                cv_data=cv_data_json,
                is_public=cv_data.is_public,
                allow_downloads=cv_data.allow_downloads,
                view_count=0,
                download_count=0
            )
            
            db.add(db_cv)
            db.commit()
            db.refresh(db_cv)
            
            # IMPORTANT: Convert cv_data back to dict for response
            if db_cv.cv_data and isinstance(db_cv.cv_data, str):
                try:
                    db_cv.cv_data = json.loads(db_cv.cv_data)
                except json.JSONDecodeError:
                    db_cv.cv_data = {}
            
            logger.info(f"Created CV: {db_cv.id} for user: {user_id}")
            return db_cv
            
        except Exception as e:
            logger.error(f"Error creating CV: {str(e)}")
            db.rollback()
            raise
    
    def get_cv_by_id(self, db: Session, cv_id: int) -> Optional[CV]:
        """Get CV by ID."""
        cv = db.query(CV).filter(CV.id == cv_id).first()
        if cv and cv.cv_data and isinstance(cv.cv_data, str):
            try:
                cv.cv_data = json.loads(cv.cv_data)
            except json.JSONDecodeError:
                cv.cv_data = {}
        return cv
    
    def get_cvs_by_user(self, db: Session, user_id: int) -> List[CV]:
        """Get all CVs for a user."""
        cvs = db.query(CV).filter(
            CV.user_id == user_id
        ).order_by(desc(CV.updated_at)).all()
        
        # Parse JSON strings back to dicts
        for cv in cvs:
            if cv.cv_data and isinstance(cv.cv_data, str):
                try:
                    cv.cv_data = json.loads(cv.cv_data)
                except json.JSONDecodeError:
                    cv.cv_data = {}
        
        return cvs
    
    def update_cv(self, db: Session, cv_id: int, cv_data: CVUpdate) -> Optional[CV]:
        """Update CV."""
        db_cv = db.query(CV).filter(CV.id == cv_id).first()
        if not db_cv:
            return None
        
        update_data = cv_data.dict(exclude_unset=True)
        if update_data:
            # Handle template enum conversion if present
            if 'template' in update_data:
                template = update_data['template']
                if hasattr(template, 'value'):
                    update_data['template'] = template.value.upper()
                else:
                    update_data['template'] = str(template).upper()
            
            # Handle status enum conversion if present  
            if 'status' in update_data:
                status = update_data['status']
                if hasattr(status, 'value'):
                    update_data['status'] = status.value.upper()
                else:
                    update_data['status'] = str(status).upper()
            
            # Handle cv_data JSON conversion
            if 'cv_data' in update_data and isinstance(update_data['cv_data'], dict):
                update_data['cv_data'] = json.dumps(update_data['cv_data'])
            
            for field, value in update_data.items():
                setattr(db_cv, field, value)
            
            db_cv.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_cv)
            
            # Convert cv_data back to dict for response
            if db_cv.cv_data and isinstance(db_cv.cv_data, str):
                try:
                    db_cv.cv_data = json.loads(db_cv.cv_data)
                except json.JSONDecodeError:
                    db_cv.cv_data = {}
        
        return db_cv
    
    def update_cv_file_info(self, db: Session, cv_id: int, file_path: str, file_size: int) -> Optional[CV]:
        """Update CV file information after PDF generation."""
        db_cv = db.query(CV).filter(CV.id == cv_id).first()
        if not db_cv:
            return None
        
        db_cv.file_path = file_path
        db_cv.file_size = file_size
        db_cv.last_generated_at = datetime.utcnow()
        db_cv.status = 'COMPLETED'  # Use UPPERCASE for database enum
        
        db.commit()
        db.refresh(db_cv)
        
        # Convert cv_data back to dict for response
        if db_cv.cv_data and isinstance(db_cv.cv_data, str):
            try:
                db_cv.cv_data = json.loads(db_cv.cv_data)
            except json.JSONDecodeError:
                db_cv.cv_data = {}
        
        return db_cv
    
    def delete_cv(self, db: Session, cv_id: int) -> bool:
        """Delete CV."""
        db_cv = db.query(CV).filter(CV.id == cv_id).first()
        if db_cv:
            # Delete associated file if exists
            if db_cv.file_path and os.path.exists(db_cv.file_path):
                try:
                    os.remove(db_cv.file_path)
                except OSError:
                    logger.warning(f"Could not delete CV file: {db_cv.file_path}")
            
            db.delete(db_cv)
            db.commit()
            return True
        return False
    
    def increment_cv_view_count(self, db: Session, cv_id: int) -> None:
        """Increment CV view count."""
        db.query(CV).filter(CV.id == cv_id).update({
            CV.view_count: CV.view_count + 1
        })
        db.commit()
    
    def increment_cv_download_count(self, db: Session, cv_id: int) -> None:
        """Increment CV download count."""
        db.query(CV).filter(CV.id == cv_id).update({
            CV.download_count: CV.download_count + 1
        })
        db.commit()
    
    # Uploaded CV Methods
    def create_uploaded_cv(self, db: Session, user_id: int, file_info: Dict[str, Any]) -> UploadedCV:
        """Create uploaded CV record."""
        db_uploaded_cv = UploadedCV(
            user_id=user_id,
            **file_info
        )
        db.add(db_uploaded_cv)
        db.commit()
        db.refresh(db_uploaded_cv)
        
        logger.info(f"Uploaded CV: {db_uploaded_cv.id} for user: {user_id}")
        return db_uploaded_cv
    
    def get_uploaded_cv_by_id(self, db: Session, cv_id: int) -> Optional[UploadedCV]:
        """Get uploaded CV by ID."""
        return db.query(UploadedCV).filter(UploadedCV.id == cv_id).first()
    
    def get_uploaded_cvs_by_user(self, db: Session, user_id: int) -> List[UploadedCV]:
        """Get all uploaded CVs for a user."""
        return db.query(UploadedCV).filter(
            UploadedCV.user_id == user_id
        ).order_by(desc(UploadedCV.created_at)).all()
    
    def set_primary_cv(self, db: Session, user_id: int, cv_id: int) -> bool:
        """Set primary CV for user."""
        # First, unset all other CVs as primary
        db.query(UploadedCV).filter(
            UploadedCV.user_id == user_id
        ).update({UploadedCV.is_primary: False})
        
        # Set the specified CV as primary
        result = db.query(UploadedCV).filter(
            UploadedCV.id == cv_id,
            UploadedCV.user_id == user_id
        ).update({UploadedCV.is_primary: True})
        
        db.commit()
        return result > 0
    
    def delete_uploaded_cv(self, db: Session, cv_id: int, user_id: int) -> bool:
        """Delete uploaded CV."""
        db_cv = db.query(UploadedCV).filter(
            UploadedCV.id == cv_id,
            UploadedCV.user_id == user_id
        ).first()
        
        if db_cv:
            # Delete associated file
            if os.path.exists(db_cv.file_path):
                try:
                    os.remove(db_cv.file_path)
                except OSError:
                    logger.warning(f"Could not delete uploaded CV file: {db_cv.file_path}")
            
            db.delete(db_cv)
            db.commit()
            return True
        return False
    
    def increment_uploaded_cv_download_count(self, db: Session, cv_id: int) -> None:
        """Increment uploaded CV download count."""
        db.query(UploadedCV).filter(UploadedCV.id == cv_id).update({
            UploadedCV.download_count: UploadedCV.download_count + 1
        })
        db.commit()