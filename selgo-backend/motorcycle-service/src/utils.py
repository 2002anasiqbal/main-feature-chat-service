# selgo-backend/motorcycle-service/src/utils.py
import os
import uuid
from typing import Optional
from fastapi import UploadFile, HTTPException
from PIL import Image
import aiofiles
from .config import settings

async def save_uploaded_image(file: UploadFile, motorcycle_id: int) -> str:
    """
    Save uploaded image file and return the file path
    """
    # Validate file type
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in settings.ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Allowed types: {', '.join(settings.ALLOWED_IMAGE_EXTENSIONS)}"
        )
    
    # Generate unique filename
    unique_filename = f"{motorcycle_id}_{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    # Ensure upload directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        
        # Validate file size
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE / (1024*1024):.1f}MB"
            )
        
        await f.write(content)
    
    # Optimize image (optional)
    try:
        optimize_image(file_path)
    except Exception as e:
        print(f"Warning: Could not optimize image {file_path}: {e}")
    
    return f"/uploads/motorcycles/{unique_filename}"

def optimize_image(file_path: str, max_width: int = 1200, quality: int = 85):
    """
    Optimize image by resizing and compressing
    """
    try:
        with Image.open(file_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Resize if too large
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            # Save with optimization
            img.save(file_path, optimize=True, quality=quality)
    except Exception as e:
        print(f"Error optimizing image {file_path}: {e}")

def generate_slug(text: str) -> str:
    """
    Generate URL-friendly slug from text
    """
    import re
    # Convert to lowercase and replace spaces/special chars with hyphens
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def format_price(price: float) -> str:
    """
    Format price for display
    """
    return f"${price:,.2f}"

def calculate_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two points using Haversine formula
    """
    import math
    
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Earth's radius in kilometers
    r = 6371
    
    return c * r

def validate_year(year: int) -> bool:
    """
    Validate motorcycle year
    """
    import datetime
    current_year = datetime.datetime.now().year
    return 1900 <= year <= current_year + 1

def validate_engine_size(engine_size: int) -> bool:
    """
    Validate engine size (CC)
    """
    return 50 <= engine_size <= 2500

def validate_mileage(mileage: int) -> bool:
    """
    Validate mileage
    """
    return 0 <= mileage <= 500000

class EmailService:
    """
    Simple email service for notifications
    """
    
    @staticmethod
    async def send_contact_notification(
        seller_email: str,
        motorcycle_title: str,
        sender_name: str,
        sender_email: str,
        sender_phone: str,
        message: str
    ):
        """
        Send email notification to seller when contacted
        """
        # This is a placeholder - implement with your preferred email service
        # (SendGrid, AWS SES, SMTP, etc.)
        
        email_subject = f"New inquiry about your motorcycle: {motorcycle_title}"
        email_body = f"""
        You have received a new inquiry about your motorcycle listing.
        
        Motorcycle: {motorcycle_title}
        
        From: {sender_name}
        Email: {sender_email}
        Phone: {sender_phone}
        
        Message:
        {message}
        
        You can reply directly to this email to contact the buyer.
        """
        
        # TODO: Implement actual email sending
        print(f"Email notification sent to {seller_email}")
        print(f"Subject: {email_subject}")
        print(f"Body: {email_body}")

def create_thumbnail(image_path: str, size: tuple = (300, 200)) -> str:
    """
    Create thumbnail from image
    """
    try:
        base_path, ext = os.path.splitext(image_path)
        thumbnail_path = f"{base_path}_thumb{ext}"
        
        with Image.open(image_path) as img:
            img.thumbnail(size, Image.Resampling.LANCZOS)
            img.save(thumbnail_path, optimize=True, quality=80)
        
        return thumbnail_path
    except Exception as e:
        print(f"Error creating thumbnail for {image_path}: {e}")
        return image_path  # Return original if thumbnail creation fails 
