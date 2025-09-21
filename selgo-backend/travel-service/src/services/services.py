from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from ..repositories.repositories import TravelRepository
from ..models.travel_schemas import (
    TravelListingCreate, TravelListingUpdate, TravelSearchParams,
    TravelListing, TravelBookingCreate, TravelBooking, TravelListResponse
)
from ..utils.file_utils import file_utils
from fastapi import UploadFile, HTTPException
import logging
import math

logger = logging.getLogger(__name__)

class TravelService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = TravelRepository(db)

    async def create_travel_listing(self, travel_data: TravelListingCreate, user_id: int) -> TravelListing:
        """Create a new travel listing."""
        try:
            db_travel = self.repository.create_travel_listing(travel_data, user_id)
            return TravelListing.from_orm(db_travel)
        except Exception as e:
            logger.error(f"Error in travel service create_travel_listing: {e}")
            raise HTTPException(status_code=500, detail="Error creating travel listing")

    async def get_travel_listing(self, travel_id: int) -> Optional[TravelListing]:
        """Get a travel listing by ID."""
        try:
            db_travel = self.repository.get_travel_listing(travel_id)
            return TravelListing.from_orm(db_travel) if db_travel else None
        except Exception as e:
            logger.error(f"Error in travel service get_travel_listing: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving travel listing")

    async def search_travel_listings(self, search_params: TravelSearchParams) -> TravelListResponse:
        """Search travel listings with filters and pagination."""
        try:
            listings, total = self.repository.get_travel_listings(search_params)
            
            travel_listings = [TravelListing.from_orm(listing) for listing in listings]
            total_pages = math.ceil(total / search_params.limit)
            
            return TravelListResponse(
                items=travel_listings,
                total=total,
                page=search_params.page,
                limit=search_params.limit,
                total_pages=total_pages
            )
        except Exception as e:
            logger.error(f"Error in travel service search_travel_listings: {e}")
            raise HTTPException(status_code=500, detail="Error searching travel listings")

    async def get_user_travel_listings(self, user_id: int, page: int = 1, limit: int = 20) -> TravelListResponse:
        """Get travel listings for a specific user."""
        try:
            listings, total = self.repository.get_user_travel_listings(user_id, page, limit)
            
            travel_listings = [TravelListing.from_orm(listing) for listing in listings]
            total_pages = math.ceil(total / limit)
            
            return TravelListResponse(
                items=travel_listings,
                total=total,
                page=page,
                limit=limit,
                total_pages=total_pages
            )
        except Exception as e:
            logger.error(f"Error in travel service get_user_travel_listings: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving user travel listings")

    async def update_travel_listing(self, travel_id: int, travel_data: TravelListingUpdate, user_id: int) -> Optional[TravelListing]:
        """Update a travel listing."""
        try:
            db_travel = self.repository.update_travel_listing(travel_id, travel_data, user_id)
            return TravelListing.from_orm(db_travel) if db_travel else None
        except Exception as e:
            logger.error(f"Error in travel service update_travel_listing: {e}")
            raise HTTPException(status_code=500, detail="Error updating travel listing")

    async def delete_travel_listing(self, travel_id: int, user_id: int) -> bool:
        """Delete a travel listing."""
        try:
            return self.repository.delete_travel_listing(travel_id, user_id)
        except Exception as e:
            logger.error(f"Error in travel service delete_travel_listing: {e}")
            raise HTTPException(status_code=500, detail="Error deleting travel listing")

    async def create_booking(self, travel_id: int, booking_data: TravelBookingCreate, user_id: int) -> Optional[TravelBooking]:
        """Create a new booking."""
        try:
            booking_dict = booking_data.dict(exclude={"travel_listing_id"})
            db_booking = self.repository.create_booking(travel_id, user_id, booking_dict)
            return TravelBooking.from_orm(db_booking) if db_booking else None
        except Exception as e:
            logger.error(f"Error in travel service create_booking: {e}")
            raise HTTPException(status_code=500, detail="Error creating booking")

    async def get_user_bookings(self, user_id: int, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        """Get bookings for a user."""
        try:
            bookings, total = self.repository.get_user_bookings(user_id, page, limit)
            
            booking_list = [TravelBooking.from_orm(booking) for booking in bookings]
            total_pages = math.ceil(total / limit)
            
            return {
                "items": booking_list,
                "total": total,
                "page": page,
                "limit": limit,
                "total_pages": total_pages
            }
        except Exception as e:
            logger.error(f"Error in travel service get_user_bookings: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving bookings")

    async def get_booking(self, booking_id: int, user_id: int) -> Optional[TravelBooking]:
        """Get a specific booking."""
        try:
            db_booking = self.repository.get_booking(booking_id, user_id)
            return TravelBooking.from_orm(db_booking) if db_booking else None
        except Exception as e:
            logger.error(f"Error in travel service get_booking: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving booking")

    async def cancel_booking(self, booking_id: int, user_id: int) -> bool:
        """Cancel a booking."""
        try:
            return self.repository.cancel_booking(booking_id, user_id)
        except Exception as e:
            logger.error(f"Error in travel service cancel_booking: {e}")
            raise HTTPException(status_code=500, detail="Error cancelling booking")

    async def upload_travel_images(self, travel_id: int, user_id: int, files: List[UploadFile]) -> Dict[str, Any]:
        """Upload images for a travel listing."""
        try:
            # Save files
            file_paths = await file_utils.save_multiple_files(files, f"travel/{travel_id}")
            
            # Generate URLs
            image_urls = [file_utils.get_file_url(path) for path in file_paths]
            
            # Add to database
            success = self.repository.add_images_to_listing(travel_id, user_id, image_urls)
            
            if success:
                return {
                    "message": "Images uploaded successfully",
                    "image_urls": image_urls,
                    "count": len(image_urls)
                }
            else:
                raise HTTPException(status_code=404, detail="Travel listing not found or access denied")
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in travel service upload_travel_images: {e}")
            raise HTTPException(status_code=500, detail="Error uploading images")

    async def remove_travel_image(self, image_id: int, user_id: int) -> bool:
        """Remove an image from a travel listing."""
        try:
            return self.repository.remove_image(image_id, user_id)
        except Exception as e:
            logger.error(f"Error in travel service remove_travel_image: {e}")
            raise HTTPException(status_code=500, detail="Error removing image")

    async def get_travel_statistics(self, user_id: int) -> Dict[str, Any]:
        """Get travel statistics for a user."""
        try:
            # Get user's listings
            listings, total_listings = self.repository.get_user_travel_listings(user_id, 1, 1000)
            
            # Get user's bookings
            bookings, total_bookings = self.repository.get_user_bookings(user_id, 1, 1000)
            
            # Calculate statistics
            active_listings = sum(1 for listing in listings if listing.is_active)
            total_revenue = sum(booking.total_price for booking in bookings if booking.status.value == "booked")
            
            return {
                "total_listings": total_listings,
                "active_listings": active_listings,
                "total_bookings": total_bookings,
                "total_revenue": total_revenue,
                "currency": "NOK"
            }
        except Exception as e:
            logger.error(f"Error in travel service get_travel_statistics: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving statistics")