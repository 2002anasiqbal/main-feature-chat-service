from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from ..database.database import get_db
from ..services.electronics_services import ElectronicsService
from ..models.electronics_schemas import (
    ElectronicsListingCreate, ElectronicsListingUpdate, ElectronicsListing, ElectronicsListResponse,
    ElectronicsSearchParams, ElectronicsCategory, ElectronicsCondition, ElectronicsStatsResponse,
    CategoryInfo
)
from ..utils.auth import get_current_user_id, get_current_user_data, get_optional_user_data
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/electronics", tags=["electronics"])

# Electronics Listings Endpoints
@router.post("/listings", response_model=ElectronicsListing, status_code=status.HTTP_201_CREATED)
async def create_electronics_listing(
    electronics_data: ElectronicsListingCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Create a new electronics listing."""
    service = ElectronicsService(db)
    return await service.create_electronics_listing(electronics_data, user_id)

@router.get("/listings", response_model=ElectronicsListResponse)
async def search_electronics_listings(
    category: Optional[ElectronicsCategory] = Query(None, description="Filter by category"),
    brand: Optional[str] = Query(None, description="Filter by brand"),
    condition: Optional[ElectronicsCondition] = Query(None, description="Filter by condition"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
    location: Optional[str] = Query(None, description="Filter by location"),
    year_from: Optional[int] = Query(None, ge=1900, description="Filter by year from"),
    year_to: Optional[int] = Query(None, le=2030, description="Filter by year to"),
    search_query: Optional[str] = Query(None, description="Search in title, description, brand, model"),
    has_warranty: Optional[bool] = Query(None, description="Filter by warranty availability"),
    includes_box: Optional[bool] = Query(None, description="Filter by original box inclusion"),
    shipping_available: Optional[bool] = Query(None, description="Filter by shipping availability"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    sort_by: Optional[str] = Query("created_at", regex="^(created_at|price|year|title)$", description="Sort field"),
    sort_order: Optional[str] = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """Search electronics listings with filters."""
    search_params = ElectronicsSearchParams(
        category=category,
        brand=brand,
        condition=condition,
        min_price=min_price,
        max_price=max_price,
        location=location,
        year_from=year_from,
        year_to=year_to,
        search_query=search_query,
        has_warranty=has_warranty,
        includes_box=includes_box,
        shipping_available=shipping_available,
        page=page,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
    service = ElectronicsService(db)
    return await service.search_electronics_listings(search_params)

@router.get("/listings/{electronics_id}", response_model=ElectronicsListing)
async def get_electronics_listing(
    electronics_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific electronics listing."""
    service = ElectronicsService(db)
    electronics_listing = await service.get_electronics_listing(electronics_id)
    
    if not electronics_listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Electronics listing not found"
        )
    
    return electronics_listing

@router.put("/listings/{electronics_id}", response_model=ElectronicsListing)
async def update_electronics_listing(
    electronics_id: int,
    electronics_data: ElectronicsListingUpdate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Update an electronics listing."""
    service = ElectronicsService(db)
    updated_listing = await service.update_electronics_listing(electronics_id, electronics_data, user_id)
    
    if not updated_listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Electronics listing not found or access denied"
        )
    
    return updated_listing

@router.delete("/listings/{electronics_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_electronics_listing(
    electronics_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Delete an electronics listing."""
    service = ElectronicsService(db)
    success = await service.delete_electronics_listing(electronics_id, user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Electronics listing not found or access denied"
        )

@router.put("/listings/{electronics_id}/mark-sold", status_code=status.HTTP_204_NO_CONTENT)
async def mark_electronics_as_sold(
    electronics_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Mark an electronics listing as sold."""
    service = ElectronicsService(db)
    success = await service.mark_as_sold(electronics_id, user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Electronics listing not found or access denied"
        )

# User's Electronics Listings
@router.get("/my-listings", response_model=ElectronicsListResponse)
async def get_my_electronics_listings(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get current user's electronics listings."""
    service = ElectronicsService(db)
    return await service.get_user_electronics_listings(user_id, page, limit)

# Image Upload Endpoints
@router.post("/listings/{electronics_id}/images")
async def upload_electronics_images(
    electronics_id: int,
    files: List[UploadFile] = File(...),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Upload images for an electronics listing."""
    if not files or all(not file.filename for file in files):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No files provided"
        )
    
    service = ElectronicsService(db)
    return await service.upload_electronics_images(electronics_id, user_id, files)

@router.delete("/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_electronics_image(
    image_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Remove an image from an electronics listing."""
    service = ElectronicsService(db)
    success = await service.remove_electronics_image(image_id, user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found or access denied"
        )

# Statistics Endpoint
@router.get("/statistics", response_model=ElectronicsStatsResponse)
async def get_electronics_statistics(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get electronics statistics for the current user."""
    service = ElectronicsService(db)
    return await service.get_electronics_statistics(user_id)

# Public Endpoints (no authentication required)
@router.get("/categories")
async def get_electronics_categories():
    """Get available electronics categories."""
    categories = [
        CategoryInfo(
            value="smartphones",
            label="Smartphones",
            subcategories=["iPhone", "Samsung", "Google Pixel", "OnePlus", "Xiaomi", "Other"]
        ),
        CategoryInfo(
            value="laptops",
            label="Laptops",
            subcategories=["MacBook", "ThinkPad", "Dell", "HP", "ASUS", "Gaming Laptops", "Ultrabooks"]
        ),
        CategoryInfo(
            value="tablets",
            label="Tablets",
            subcategories=["iPad", "Samsung Galaxy Tab", "Surface", "Android Tablets"]
        ),
        CategoryInfo(
            value="desktop_computers",
            label="Desktop Computers",
            subcategories=["Gaming PCs", "Workstations", "All-in-One", "Mini PCs"]
        ),
        CategoryInfo(
            value="gaming",
            label="Gaming",
            subcategories=["PlayStation", "Xbox", "Nintendo", "Gaming Accessories", "VR Headsets"]
        ),
        CategoryInfo(
            value="audio",
            label="Audio",
            subcategories=["Headphones", "Speakers", "Soundbars", "Turntables", "Amplifiers"]
        ),
        CategoryInfo(
            value="tv_video",
            label="TV & Video",
            subcategories=["Smart TVs", "Projectors", "Streaming Devices", "Blu-ray Players"]
        ),
        CategoryInfo(
            value="cameras",
            label="Cameras",
            subcategories=["DSLR", "Mirrorless", "Action Cameras", "Lenses", "Accessories"]
        ),
        CategoryInfo(
            value="smart_home",
            label="Smart Home",
            subcategories=["Smart Speakers", "Security Cameras", "Smart Lights", "Thermostats"]
        ),
        CategoryInfo(
            value="wearables",
            label="Wearables",
            subcategories=["Apple Watch", "Fitness Trackers", "Smart Glasses", "Other Wearables"]
        ),
        CategoryInfo(
            value="accessories",
            label="Accessories",
            subcategories=["Cases", "Chargers", "Cables", "Memory Cards", "Power Banks"]
        ),
        CategoryInfo(
            value="components",
            label="Components",
            subcategories=["CPUs", "GPUs", "RAM", "Storage", "Motherboards", "Power Supplies"]
        )
    ]
    
    return {"categories": categories}

@router.get("/conditions")
async def get_electronics_conditions():
    """Get available condition types."""
    return {
        "conditions": [
            {"value": "new", "label": "New"},
            {"value": "like_new", "label": "Like New"},
            {"value": "excellent", "label": "Excellent"},
            {"value": "good", "label": "Good"},
            {"value": "fair", "label": "Fair"},
            {"value": "poor", "label": "Poor"},
            {"value": "for_parts", "label": "For Parts/Not Working"}
        ]
    }

@router.get("/featured", response_model=List[ElectronicsListing])
async def get_featured_electronics_listings(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get featured electronics listings."""
    service = ElectronicsService(db)
    return await service.get_featured_listings(limit)