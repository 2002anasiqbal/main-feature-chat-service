from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database.database import get_db
from ..services.commercial_services import CommercialVehicleService
from ..models.commercial_schemas import (
    CommercialVehicleListingCreate, CommercialVehicleListingUpdate, CommercialVehicleListingResponse,
    CommercialVehicleListingListResponse, CommercialVehicleSearchRequest, CommercialVehicleStats,
    CommercialVehicleTypeEnum, VehicleConditionEnum, FuelTypeEnum
)
from ..utils.auth import get_current_user_id, get_current_user_data, get_optional_user_data
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/commercial-vehicles", tags=["commercial-vehicles"])

# Commercial Vehicle Listings Endpoints
@router.post("/listings", response_model=CommercialVehicleListingResponse, status_code=status.HTTP_201_CREATED)
async def create_commercial_vehicle_listing(
    vehicle_data: CommercialVehicleListingCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Create a new commercial vehicle listing."""
    service = CommercialVehicleService(db)
    return await service.create_listing(vehicle_data, user_id)

@router.get("/listings", response_model=CommercialVehicleListingListResponse)
async def search_commercial_vehicle_listings(
    vehicle_type: Optional[List[CommercialVehicleTypeEnum]] = Query(None, description="Filter by vehicle type"),
    make: Optional[List[str]] = Query(None, description="Filter by make"),
    model: Optional[List[str]] = Query(None, description="Filter by model"),
    year_from: Optional[int] = Query(None, description="Minimum year"),
    year_to: Optional[int] = Query(None, description="Maximum year"),
    price_from: Optional[float] = Query(None, description="Minimum price"),
    price_to: Optional[float] = Query(None, description="Maximum price"),
    mileage_from: Optional[int] = Query(None, description="Minimum mileage"),
    mileage_to: Optional[int] = Query(None, description="Maximum mileage"),
    fuel_type: Optional[List[FuelTypeEnum]] = Query(None, description="Filter by fuel type"),
    condition: Optional[List[VehicleConditionEnum]] = Query(None, description="Filter by condition"),
    location: Optional[str] = Query(None, description="Filter by location"),
    payload_capacity_from: Optional[int] = Query(None, description="Minimum payload capacity"),
    payload_capacity_to: Optional[int] = Query(None, description="Maximum payload capacity"),
    has_valid_inspection: Optional[bool] = Query(None, description="Filter by inspection status"),
    delivery_available: Optional[bool] = Query(None, description="Filter by delivery availability"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    sort_by: Optional[str] = Query("created_at", description="Sort field"),
    sort_order: Optional[str] = Query("desc", description="Sort order"),
    db: Session = Depends(get_db)
):
    """Search commercial vehicle listings with filters."""
    from ..models.commercial_schemas import CommercialVehicleSearchFilters
    
    filters = CommercialVehicleSearchFilters(
        vehicle_type=vehicle_type,
        make=make,
        model=model,
        year_from=year_from,
        year_to=year_to,
        price_from=price_from,
        price_to=price_to,
        mileage_from=mileage_from,
        mileage_to=mileage_to,
        fuel_type=fuel_type,
        condition=condition,
        location=location,
        payload_capacity_from=payload_capacity_from,
        payload_capacity_to=payload_capacity_to,
        has_valid_inspection=has_valid_inspection,
        delivery_available=delivery_available
    )
    
    search_request = CommercialVehicleSearchRequest(
        filters=filters,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        per_page=per_page
    )
    
    service = CommercialVehicleService(db)
    return await service.search_listings(search_request)

@router.get("/listings/{listing_id}", response_model=CommercialVehicleListingResponse)
async def get_commercial_vehicle_listing(
    listing_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific commercial vehicle listing by ID."""
    service = CommercialVehicleService(db)
    listing = await service.get_listing_by_id(listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Commercial vehicle listing not found")
    return listing

@router.put("/listings/{listing_id}", response_model=CommercialVehicleListingResponse)
async def update_commercial_vehicle_listing(
    listing_id: int,
    vehicle_data: CommercialVehicleListingUpdate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Update a commercial vehicle listing."""
    service = CommercialVehicleService(db)
    listing = await service.update_listing(listing_id, vehicle_data, user_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Commercial vehicle listing not found or not authorized")
    return listing

@router.delete("/listings/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_commercial_vehicle_listing(
    listing_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Delete a commercial vehicle listing."""
    service = CommercialVehicleService(db)
    success = await service.delete_listing(listing_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Commercial vehicle listing not found or not authorized")

@router.get("/my-listings", response_model=CommercialVehicleListingListResponse)
async def get_my_commercial_vehicle_listings(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get current user's commercial vehicle listings."""
    service = CommercialVehicleService(db)
    return await service.get_user_listings(user_id, page, per_page)

@router.post("/listings/{listing_id}/images")
async def upload_commercial_vehicle_images(
    listing_id: int,
    files: List[UploadFile] = File(...),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Upload images for a commercial vehicle listing."""
    service = CommercialVehicleService(db)
    return await service.upload_images(listing_id, files, user_id)

@router.delete("/listings/{listing_id}/images/{image_id}")
async def delete_commercial_vehicle_image(
    listing_id: int,
    image_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Delete an image from a commercial vehicle listing."""
    service = CommercialVehicleService(db)
    success = await service.delete_image(listing_id, image_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Image not found or not authorized")

@router.get("/stats", response_model=CommercialVehicleStats)
async def get_commercial_vehicle_stats(db: Session = Depends(get_db)):
    """Get commercial vehicle marketplace statistics."""
    service = CommercialVehicleService(db)
    return await service.get_stats()

@router.get("/makes")
async def get_commercial_vehicle_makes(
    vehicle_type: Optional[CommercialVehicleTypeEnum] = Query(None, description="Filter by vehicle type"),
    db: Session = Depends(get_db)
):
    """Get list of available commercial vehicle makes."""
    service = CommercialVehicleService(db)
    return await service.get_makes(vehicle_type)

@router.get("/models")
async def get_commercial_vehicle_models(
    make: str = Query(..., description="Vehicle make"),
    vehicle_type: Optional[CommercialVehicleTypeEnum] = Query(None, description="Filter by vehicle type"),
    db: Session = Depends(get_db)
):
    """Get list of available commercial vehicle models for a specific make."""
    service = CommercialVehicleService(db)
    return await service.get_models(make, vehicle_type)

@router.get("/featured", response_model=CommercialVehicleListingListResponse)
async def get_featured_commercial_vehicles(
    limit: int = Query(10, ge=1, le=50, description="Number of featured listings"),
    db: Session = Depends(get_db)
):
    """Get featured commercial vehicle listings."""
    service = CommercialVehicleService(db)
    return await service.get_featured_listings(limit)

@router.post("/listings/{listing_id}/mark-sold")
async def mark_commercial_vehicle_as_sold(
    listing_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Mark a commercial vehicle listing as sold."""
    service = CommercialVehicleService(db)
    success = await service.mark_as_sold(listing_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Commercial vehicle listing not found or not authorized")
    return {"message": "Commercial vehicle marked as sold"}

@router.post("/listings/{listing_id}/mark-available")
async def mark_commercial_vehicle_as_available(
    listing_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Mark a commercial vehicle listing as available."""
    service = CommercialVehicleService(db)
    success = await service.mark_as_available(listing_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Commercial vehicle listing not found or not authorized")
    return {"message": "Commercial vehicle marked as available"}