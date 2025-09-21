from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from ..database.database import get_db
from ..services.services import TravelService
from ..models.travel_schemas import (
    TravelListingCreate, TravelListingUpdate, TravelListing, TravelListResponse,
    TravelBookingCreate, TravelBooking, TravelSearchParams, TravelType, BookingStatus
)
from ..utils.auth import get_current_user_id, get_current_user_data, get_optional_user_data
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/travel", tags=["travel"])

# Travel Listings Endpoints
@router.post("/listings", response_model=TravelListing, status_code=status.HTTP_201_CREATED)
async def create_travel_listing(
    travel_data: TravelListingCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Create a new travel listing."""
    service = TravelService(db)
    return await service.create_travel_listing(travel_data, user_id)

@router.get("/listings", response_model=TravelListResponse)
async def search_travel_listings(
    travel_type: Optional[TravelType] = Query(None, description="Filter by travel type"),
    destination: Optional[str] = Query(None, description="Filter by destination"),
    departure_location: Optional[str] = Query(None, description="Filter by departure location"),
    min_price: Optional[float] = Query(None, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, description="Maximum price filter"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Search travel listings with filters."""
    search_params = TravelSearchParams(
        travel_type=travel_type,
        destination=destination,
        departure_location=departure_location,
        min_price=min_price,
        max_price=max_price,
        page=page,
        limit=limit
    )
    
    service = TravelService(db)
    return await service.search_travel_listings(search_params)

@router.get("/listings/{travel_id}", response_model=TravelListing)
async def get_travel_listing(
    travel_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific travel listing."""
    service = TravelService(db)
    travel_listing = await service.get_travel_listing(travel_id)
    
    if not travel_listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Travel listing not found"
        )
    
    return travel_listing

@router.put("/listings/{travel_id}", response_model=TravelListing)
async def update_travel_listing(
    travel_id: int,
    travel_data: TravelListingUpdate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Update a travel listing."""
    service = TravelService(db)
    updated_listing = await service.update_travel_listing(travel_id, travel_data, user_id)
    
    if not updated_listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Travel listing not found or access denied"
        )
    
    return updated_listing

@router.delete("/listings/{travel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_travel_listing(
    travel_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Delete a travel listing."""
    service = TravelService(db)
    success = await service.delete_travel_listing(travel_id, user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Travel listing not found or access denied"
        )

# User's Travel Listings
@router.get("/my-listings", response_model=TravelListResponse)
async def get_my_travel_listings(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get current user's travel listings."""
    service = TravelService(db)
    return await service.get_user_travel_listings(user_id, page, limit)

# Image Upload Endpoints
@router.post("/listings/{travel_id}/images")
async def upload_travel_images(
    travel_id: int,
    files: List[UploadFile] = File(...),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Upload images for a travel listing."""
    if not files or all(not file.filename for file in files):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No files provided"
        )
    
    service = TravelService(db)
    return await service.upload_travel_images(travel_id, user_id, files)

@router.delete("/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_travel_image(
    image_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Remove an image from a travel listing."""
    service = TravelService(db)
    success = await service.remove_travel_image(image_id, user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found or access denied"
        )

# Booking Endpoints
@router.post("/listings/{travel_id}/bookings", response_model=TravelBooking, status_code=status.HTTP_201_CREATED)
async def create_booking(
    travel_id: int,
    booking_data: TravelBookingCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Create a new booking for a travel listing."""
    # Set the travel_listing_id from the URL parameter
    booking_data.travel_listing_id = travel_id
    
    service = TravelService(db)
    booking = await service.create_booking(travel_id, booking_data, user_id)
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to create booking. Travel may not be available or insufficient capacity."
        )
    
    return booking

@router.get("/bookings", response_model=Dict[str, Any])
async def get_my_bookings(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get current user's bookings."""
    service = TravelService(db)
    return await service.get_user_bookings(user_id, page, limit)

@router.get("/bookings/{booking_id}", response_model=TravelBooking)
async def get_booking(
    booking_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get a specific booking."""
    service = TravelService(db)
    booking = await service.get_booking(booking_id, user_id)
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    return booking

@router.put("/bookings/{booking_id}/cancel", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_booking(
    booking_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Cancel a booking."""
    service = TravelService(db)
    success = await service.cancel_booking(booking_id, user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found or already cancelled"
        )

# Statistics Endpoint
@router.get("/statistics")
async def get_travel_statistics(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get travel statistics for the current user."""
    service = TravelService(db)
    return await service.get_travel_statistics(user_id)

# Public Endpoints (no authentication required)
@router.get("/types")
async def get_travel_types():
    """Get available travel types."""
    return {
        "travel_types": [
            {"value": "flight", "label": "Flights"},
            {"value": "hotel", "label": "Hotels"},
            {"value": "car_rental", "label": "Car Rentals"},
            {"value": "package_tour", "label": "Package Tours"},
            {"value": "cruise", "label": "Cruises"},
            {"value": "activity", "label": "Activities & Tours"}
        ]
    }

@router.get("/featured", response_model=TravelListResponse)
async def get_featured_travel_listings(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get featured travel listings."""
    # For now, just return recent listings
    search_params = TravelSearchParams(page=1, limit=limit)
    service = TravelService(db)
    return await service.search_travel_listings(search_params)