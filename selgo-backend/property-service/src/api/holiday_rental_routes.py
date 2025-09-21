# property-service/src/api/holiday_rental_routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from decimal import Decimal

from ..database.database import get_db
from ..services.holiday_rental_services import HolidayRentalService
from ..models.holiday_rental_schemas import (
    HolidayRentalCreate, HolidayRentalUpdate, HolidayRentalResponse,
    HolidayRentalBookingCreate, HolidayRentalBookingResponse,
    HolidayRentalReviewCreate, HolidayRentalReviewResponse,
    HolidayRentalAvailabilityCreate, HolidayRentalAvailabilityResponse,
    HolidayRentalSearchRequest, HolidayRentalListResponse,
    HolidayRentalStats, HolidayRentalTypeEnum, BookingStatusEnum,
    HolidayRentalSearchFilters
)
from ..utils.auth import get_current_user_id, get_current_user_data
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/holiday-rentals", tags=["holiday-rentals"])

# Holiday Rental Management
@router.post("/", response_model=HolidayRentalResponse, status_code=status.HTTP_201_CREATED)
async def create_holiday_rental(
    rental_data: HolidayRentalCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Create a new holiday rental."""
    service = HolidayRentalService(db)
    return await service.create_holiday_rental(rental_data, user_id)

@router.get("/search", response_model=HolidayRentalListResponse)
async def search_holiday_rentals(
    query: Optional[str] = Query(None, description="Search query"),
    rental_type: Optional[List[HolidayRentalTypeEnum]] = Query(None, description="Filter by rental type"),
    min_guests: Optional[int] = Query(None, description="Minimum number of guests"),
    max_guests: Optional[int] = Query(None, description="Maximum number of guests"),
    price_from: Optional[Decimal] = Query(None, description="Minimum price per night"),
    price_to: Optional[Decimal] = Query(None, description="Maximum price per night"),
    check_in_date: Optional[date] = Query(None, description="Check-in date"),
    check_out_date: Optional[date] = Query(None, description="Check-out date"),
    min_nights: Optional[int] = Query(None, description="Minimum nights"),
    max_nights: Optional[int] = Query(None, description="Maximum nights"),
    location: Optional[str] = Query(None, description="Location filter"),
    has_wifi: Optional[bool] = Query(None, description="Has WiFi"),
    has_kitchen: Optional[bool] = Query(None, description="Has kitchen"),
    has_hot_tub: Optional[bool] = Query(None, description="Has hot tub"),
    has_sauna: Optional[bool] = Query(None, description="Has sauna"),
    has_boat_access: Optional[bool] = Query(None, description="Has boat access"),
    has_ski_access: Optional[bool] = Query(None, description="Has ski access"),
    has_beach_access: Optional[bool] = Query(None, description="Has beach access"),
    pets_allowed: Optional[bool] = Query(None, description="Pets allowed"),
    instant_booking: Optional[bool] = Query(None, description="Instant booking available"),
    min_rating: Optional[Decimal] = Query(None, description="Minimum rating"),
    sort_by: Optional[str] = Query("created_at", description="Sort field"),
    sort_order: Optional[str] = Query("desc", description="Sort order"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Search holiday rentals with filters."""
    filters = HolidayRentalSearchFilters(
        rental_type=rental_type,
        min_guests=min_guests,
        max_guests=max_guests,
        price_from=price_from,
        price_to=price_to,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        min_nights=min_nights,
        max_nights=max_nights,
        location=location,
        has_wifi=has_wifi,
        has_kitchen=has_kitchen,
        has_hot_tub=has_hot_tub,
        has_sauna=has_sauna,
        has_boat_access=has_boat_access,
        has_ski_access=has_ski_access,
        has_beach_access=has_beach_access,
        pets_allowed=pets_allowed,
        instant_booking=instant_booking,
        min_rating=min_rating
    )
    
    search_request = HolidayRentalSearchRequest(
        query=query,
        filters=filters,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        per_page=per_page
    )
    
    service = HolidayRentalService(db)
    return await service.search_holiday_rentals(search_request)

@router.get("/{rental_id}", response_model=HolidayRentalResponse)
async def get_holiday_rental(
    rental_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific holiday rental by ID."""
    service = HolidayRentalService(db)
    rental = await service.get_holiday_rental_by_id(rental_id)
    if not rental:
        raise HTTPException(status_code=404, detail="Holiday rental not found")
    return rental

@router.put("/{rental_id}", response_model=HolidayRentalResponse)
async def update_holiday_rental(
    rental_id: str,
    rental_data: HolidayRentalUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Update a holiday rental."""
    service = HolidayRentalService(db)
    rental = await service.update_holiday_rental(rental_id, rental_data, user_id)
    if not rental:
        raise HTTPException(status_code=404, detail="Holiday rental not found or not authorized")
    return rental

@router.delete("/{rental_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_holiday_rental(
    rental_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Delete a holiday rental."""
    service = HolidayRentalService(db)
    success = await service.delete_holiday_rental(rental_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Holiday rental not found or not authorized")

# Booking Management
@router.post("/bookings", response_model=HolidayRentalBookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: HolidayRentalBookingCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Create a new holiday rental booking."""
    service = HolidayRentalService(db)
    return await service.create_booking(booking_data, user_id)

@router.get("/bookings/my-bookings", response_model=List[HolidayRentalBookingResponse])
async def get_my_bookings(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get current user's holiday rental bookings."""
    service = HolidayRentalService(db)
    return await service.get_user_bookings(user_id, page, per_page)

@router.get("/bookings/my-property-bookings", response_model=List[HolidayRentalBookingResponse])
async def get_my_property_bookings(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get bookings for current user's holiday rental properties."""
    service = HolidayRentalService(db)
    return await service.get_owner_bookings(user_id, page, per_page)

@router.patch("/bookings/{booking_id}/status", response_model=HolidayRentalBookingResponse)
async def update_booking_status(
    booking_id: str,
    status: BookingStatusEnum,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Update booking status."""
    service = HolidayRentalService(db)
    booking = await service.update_booking_status(booking_id, status, user_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found or not authorized")
    return booking

# Review Management
@router.post("/reviews", response_model=HolidayRentalReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    review_data: HolidayRentalReviewCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Create a review for a holiday rental."""
    service = HolidayRentalService(db)
    return await service.create_review(review_data, user_id)

# Statistics
@router.get("/stats/overview", response_model=HolidayRentalStats)
async def get_holiday_rental_stats(db: Session = Depends(get_db)):
    """Get holiday rental marketplace statistics."""
    service = HolidayRentalService(db)
    return await service.get_stats()

# Featured and Popular
@router.get("/featured/list", response_model=HolidayRentalListResponse)
async def get_featured_holiday_rentals(
    limit: int = Query(10, ge=1, le=50, description="Number of featured rentals"),
    db: Session = Depends(get_db)
):
    """Get featured holiday rentals."""
    filters = HolidayRentalSearchFilters()
    search_request = HolidayRentalSearchRequest(
        filters=filters,
        sort_by="average_rating",
        sort_order="desc",
        page=1,
        per_page=limit
    )
    
    service = HolidayRentalService(db)
    return await service.search_holiday_rentals(search_request)

@router.get("/popular/destinations")
async def get_popular_destinations(db: Session = Depends(get_db)):
    """Get popular holiday rental destinations."""
    # This would typically query the database for popular locations
    # For now, return a placeholder response
    return {
        "destinations": [
            {"name": "Oslo", "count": 45, "average_price": 1200},
            {"name": "Bergen", "count": 32, "average_price": 1100},
            {"name": "Trondheim", "count": 28, "average_price": 950},
            {"name": "Stavanger", "count": 22, "average_price": 1050},
            {"name": "Tromsø", "count": 18, "average_price": 1300}
        ]
    }

@router.get("/types/available")
async def get_available_rental_types(db: Session = Depends(get_db)):
    """Get available holiday rental types with counts."""
    # This would typically query the database for rental type statistics
    # For now, return a placeholder response
    return {
        "types": [
            {"type": "cabin", "count": 85, "average_price": 1150},
            {"type": "cottage", "count": 62, "average_price": 1050},
            {"type": "apartment", "count": 45, "average_price": 900},
            {"type": "house", "count": 38, "average_price": 1400},
            {"type": "chalet", "count": 25, "average_price": 1600},
            {"type": "villa", "count": 15, "average_price": 2200}
        ]
    }