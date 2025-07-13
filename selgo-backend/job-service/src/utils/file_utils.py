# File: job-service/src/utils/file_utils.py

import os
import uuid
from typing import Tuple
from fastapi import UploadFile, HTTPException, status
from ..config.config import settings
import logging

logger = logging.getLogger(__name__)

def validate_file(file: UploadFile) -> None:
    """Validate uploaded file."""
    # Check file size
    if file.size and file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum allowed size of {settings.MAX_FILE_SIZE} bytes"
        )
    
    # Check file type
    if file.filename:
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in settings.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {file_extension} not allowed. Allowed types: {settings.ALLOWED_FILE_TYPES}"
            )

def save_uploaded_file(file: UploadFile, subfolder: str) -> Tuple[str, int]:
    """Save uploaded file and return path and size."""
    try:
        # Create directory if it doesn't exist
        upload_dir = os.path.join(settings.UPLOAD_DIR, subfolder)
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1] if file.filename else ""
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(upload_dir, unique_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = file.file.read()
            buffer.write(content)
        
        file_size = len(content)
        
        logger.info(f"File saved: {file_path} ({file_size} bytes)")
        return file_path, file_size
        
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save file"
        )

def delete_file(file_path: str) -> bool:
    """Delete file from filesystem."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"File deleted: {file_path}")
            return True
        return False
    except Exception as e:
        logger.error(f"Error deleting file {file_path}: {str(e)}")
        return False

def get_file_url(file_path: str) -> str:
    """Generate URL for file access."""
    # Convert absolute path to relative URL
    relative_path = file_path.replace(settings.UPLOAD_DIR, "").lstrip("/")
    return f"/uploads/{relative_path}"
