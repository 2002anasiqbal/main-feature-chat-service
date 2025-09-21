import os
import uuid
from typing import List, Optional
from fastapi import UploadFile, HTTPException
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class FileUtils:
    def __init__(self, upload_folder: str = "uploads", max_file_size: int = 10 * 1024 * 1024):
        self.upload_folder = upload_folder
        self.max_file_size = max_file_size
        self.allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".pdf"}
        
        # Create upload directory if it doesn't exist
        os.makedirs(upload_folder, exist_ok=True)
    
    def is_allowed_file(self, filename: str) -> bool:
        """Check if file extension is allowed."""
        return any(filename.lower().endswith(ext) for ext in self.allowed_extensions)
    
    def generate_unique_filename(self, original_filename: str) -> str:
        """Generate a unique filename while preserving the extension."""
        file_extension = os.path.splitext(original_filename)[1].lower()
        unique_id = str(uuid.uuid4())
        return f"{unique_id}{file_extension}"
    
    async def save_upload_file(self, upload_file: UploadFile, subfolder: str = "") -> str:
        """Save uploaded file and return the file path."""
        try:
            # Check file size
            content = await upload_file.read()
            if len(content) > self.max_file_size:
                raise HTTPException(
                    status_code=413,
                    detail=f"File too large. Maximum size is {self.max_file_size / (1024*1024):.1f}MB"
                )
            
            # Check file extension
            if not self.is_allowed_file(upload_file.filename):
                raise HTTPException(
                    status_code=400,
                    detail=f"File type not allowed. Allowed types: {', '.join(self.allowed_extensions)}"
                )
            
            # Create subfolder if specified
            save_folder = os.path.join(self.upload_folder, subfolder) if subfolder else self.upload_folder
            os.makedirs(save_folder, exist_ok=True)
            
            # Generate unique filename
            filename = self.generate_unique_filename(upload_file.filename)
            file_path = os.path.join(save_folder, filename)
            
            # Save file
            with open(file_path, "wb") as f:
                f.write(content)
            
            # Return relative path for URL generation
            return os.path.join(subfolder, filename) if subfolder else filename
            
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            raise HTTPException(status_code=500, detail="Error saving file")
    
    async def save_multiple_files(self, upload_files: List[UploadFile], subfolder: str = "") -> List[str]:
        """Save multiple uploaded files and return list of file paths."""
        file_paths = []
        for upload_file in upload_files:
            if upload_file.filename:  # Skip empty files
                file_path = await self.save_upload_file(upload_file, subfolder)
                file_paths.append(file_path)
        return file_paths
    
    def delete_file(self, file_path: str) -> bool:
        """Delete a file from the upload folder."""
        try:
            full_path = os.path.join(self.upload_folder, file_path)
            if os.path.exists(full_path):
                os.remove(full_path)
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
            return False
    
    def get_file_url(self, file_path: str, base_url: str = "") -> str:
        """Generate URL for accessing uploaded file."""
        if not file_path:
            return ""
        return f"{base_url}/uploads/{file_path}" if base_url else f"/uploads/{file_path}"

# Global file utils instance
file_utils = FileUtils()