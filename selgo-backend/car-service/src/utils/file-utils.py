import os
import uuid
import shutil
from fastapi import UploadFile
from typing import List, Optional
import logging

from ..config.config import settings

logger = logging.getLogger(__name__)

def save_upload(
    upload_file: UploadFile,
    folder: str = None,
    valid_extensions: List[str] = None
) -> Optional[str]:
    """
    Save an uploaded file and return the path.

    Args:
        upload_file: The uploaded file
        folder: The subfolder to save the file in (relative to UPLOAD_FOLDER)
        valid_extensions: List of valid file extensions

    Returns:
        The relative path to the saved file, or None if there was an error
    """
    try:
        # Get the file extension
        _, ext = os.path.splitext(upload_file.filename)
        ext = ext.lower()

        # Validate file extension if specified
        if valid_extensions and ext not in valid_extensions:
            logger.warning(f"Invalid file extension: {ext}. Valid extensions: {valid_extensions}")
            return None

        # Generate a unique filename
        unique_filename = f"{uuid.uuid4()}{ext}"

        # Determine the upload path
        upload_folder = settings.UPLOAD_FOLDER
        if folder:
            upload_folder = os.path.join(upload_folder, folder)

        # Create the directory if it doesn't exist
        os.makedirs(upload_folder, exist_ok=True)

        # Set the file path
        file_path = os.path.join(upload_folder, unique_filename)

        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)

        # Return the relative path
        rel_path = os.path.join(folder, unique_filename) if folder else unique_filename
        return rel_path

    except Exception as e:
        logger.error(f"Error saving file: {e}")
        return None

def get_file_url(file_path: str) -> str:
    """
    Get the URL for a file.

    Args:
        file_path: The relative path to the file

    Returns:
        The URL for the file
    """
    return f"/uploads/{file_path}"

def delete_file(file_path: str) -> bool:
    """
    Delete a file.

    Args:
        file_path: The relative path to the file

    Returns:
        True if the file was deleted, False otherwise
    """
    try:
        # Get the absolute path
        abs_path = os.path.join(settings.UPLOAD_FOLDER, file_path)

        # Check if the file exists
        if not os.path.isfile(abs_path):
            logger.warning(f"File not found: {abs_path}")
            return False

        # Delete the file
        os.remove(abs_path)
        return True

    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        return False

def is_valid_image(file: UploadFile) -> bool:
    """
    Check if a file is a valid image.

    Args:
        file: The uploaded file

    Returns:
        True if the file is a valid image, False otherwise
    """
    valid_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
    valid_content_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]

    # Check extension
    _, ext = os.path.splitext(file.filename)
    if ext.lower() not in valid_extensions:
        return False

    # Check content type
    if file.content_type not in valid_content_types:
        return False

    return True

def get_file_size(file_path: str) -> int:
    """
    Get the size of a file in bytes.

    Args:
        file_path: The relative path to the file

    Returns:
        The size of the file in bytes, or 0 if the file doesn't exist
    """
    try:
        # Get the absolute path
        abs_path = os.path.join(settings.UPLOAD_FOLDER, file_path)

        # Check if the file exists
        if not os.path.isfile(abs_path):
            logger.warning(f"File not found: {abs_path}")
            return 0

        # Get the file size
        return os.path.getsize(abs_path)

    except Exception as e:
        logger.error(f"Error getting file size: {e}")
        return 0
