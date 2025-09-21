from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional, Dict, Any
from ..models.travel_models import TravelListing, TravelImage, TravelBooking, TravelAmenity, TravelType, BookingStatus
from ..models.travel_schemas import TravelListingCreate, TravelListingUpdate, TravelSearchParams
import logging
import uuid

logger = logging.getLogger(__name__)

class TravelRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_travel_listing(self, travel_data: TravelListingCreate, user_id: int) -> TravelListing:
        """Create a new travel listing."""
        try:
            # Create the main travel listing
            db_travel = TravelListing(
                **travel_data.dict(exclude={"images", "amenities"}),
                user_id=user_id
            )
            
            self.db.add(db_travel)
            self.db.flush()  # Get the ID without committing
            
            # Add images if provided
            if travel_data.images:
                for image_data in travel_data.images:
                    db_image = TravelImage(
                        **image_data.dict(),
                        travel_listing_id=db_travel.id
                    )
                    self.db.add(db_image)
            
            # Add amenities if provided
            if travel_data.amenities:
                for amenity_data in travel_data.amenities:
                    db_amenity = TravelAmenity(
                        **amenity_data.dict(),
                        travel_listing_id=db_travel.id
                    )
                    self.db.add(db_amenity)
            
            self.db.commit()
            self.db.refresh(db_travel)
            return db_travel
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating travel listing: {e}")
            raise

    def get_travel_listing(self, travel_id: int) -> Optional[TravelListing]:
        """Get a travel listing by ID."""
        return self.db.query(TravelListing).filter(
            TravelListing.id == travel_id,
            TravelListing.is_active == True
        ).first()

    def get_travel_listings(self, search_params: TravelSearchParams) -> tuple[List[TravelListing], int]:
        """Get travel listings with search and pagination."""
        query = self.db.query(TravelListing).filter(TravelListing.is_active == True)
        
        # Apply filters
        if search_params.travel_type:
            query = query.filter(TravelListing.travel_type == search_params.travel_type)
        
        if search_params.destination:
            query = query.filter(
                TravelListing.destination_location.ilike(f"%{search_params.destination}%")
            )
        
        if search_params.departure_location:
            query = query.filter(
                TravelListing.departure_location.ilike(f"%{search_params.departure_location}%")
            )
        
        if search_params.min_price:
            query = query.filter(TravelListing.price >= search_params.min_price)
        
        if search_params.max_price:
            query = query.filter(TravelListing.price <= search_params.max_price)
        
        if search_params.departure_date_from:
            query = query.filter(TravelListing.departure_date >= search_params.departure_date_from)
        
        if search_params.departure_date_to:
            query = query.filter(TravelListing.departure_date <= search_params.departure_date_to)
        
        if search_params.max_capacity:
            query = query.filter(TravelListing.max_capacity >= search_params.max_capacity)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (search_params.page - 1) * search_params.limit
        listings = query.offset(offset).limit(search_params.limit).all()
        
        return listings, total

    def get_user_travel_listings(self, user_id: int, page: int = 1, limit: int = 20) -> tuple[List[TravelListing], int]:
        """Get travel listings for a specific user."""
        query = self.db.query(TravelListing).filter(
            TravelListing.user_id == user_id,
            TravelListing.is_active == True
        )
        
        total = query.count()
        offset = (page - 1) * limit
        listings = query.offset(offset).limit(limit).all()
        
        return listings, total

    def update_travel_listing(self, travel_id: int, travel_data: TravelListingUpdate, user_id: int) -> Optional[TravelListing]:
        """Update a travel listing."""
        try:
            db_travel = self.db.query(TravelListing).filter(
                TravelListing.id == travel_id,
                TravelListing.user_id == user_id,
                TravelListing.is_active == True
            ).first()
            
            if not db_travel:
                return None
            
            # Update fields
            update_data = travel_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_travel, field, value)
            
            self.db.commit()
            self.db.refresh(db_travel)
            return db_travel
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating travel listing: {e}")
            raise

    def delete_travel_listing(self, travel_id: int, user_id: int) -> bool:
        """Soft delete a travel listing."""
        try:
            db_travel = self.db.query(TravelListing).filter(
                TravelListing.id == travel_id,
                TravelListing.user_id == user_id
            ).first()
            
            if not db_travel:
                return False
            
            db_travel.is_active = False
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting travel listing: {e}")
            raise

    def create_booking(self, travel_id: int, user_id: int, booking_data: dict) -> Optional[TravelBooking]:
        """Create a new booking for a travel listing."""
        try:
            # Check if travel listing exists and is available
            travel_listing = self.get_travel_listing(travel_id)
            if not travel_listing or travel_listing.status != BookingStatus.AVAILABLE:
                return None
            
            # Check availability
            if travel_listing.available_spots and travel_listing.available_spots < booking_data.get("number_of_people", 1):
                return None
            
            # Calculate total price
            total_price = travel_listing.price * booking_data.get("number_of_people", 1)
            
            # Generate booking reference
            booking_reference = f"TRV-{uuid.uuid4().hex[:8].upper()}"
            
            # Create booking
            db_booking = TravelBooking(
                travel_listing_id=travel_id,
                user_id=user_id,
                total_price=total_price,
                booking_reference=booking_reference,
                **booking_data
            )
            
            self.db.add(db_booking)
            
            # Update available spots
            if travel_listing.available_spots:
                travel_listing.available_spots -= booking_data.get("number_of_people", 1)
                if travel_listing.available_spots <= 0:
                    travel_listing.status = BookingStatus.BOOKED
            
            self.db.commit()
            self.db.refresh(db_booking)
            return db_booking
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating booking: {e}")
            raise

    def get_user_bookings(self, user_id: int, page: int = 1, limit: int = 20) -> tuple[List[TravelBooking], int]:
        """Get bookings for a specific user."""
        query = self.db.query(TravelBooking).filter(TravelBooking.user_id == user_id)
        
        total = query.count()
        offset = (page - 1) * limit
        bookings = query.offset(offset).limit(limit).all()
        
        return bookings, total

    def get_booking(self, booking_id: int, user_id: int) -> Optional[TravelBooking]:
        """Get a specific booking."""
        return self.db.query(TravelBooking).filter(
            TravelBooking.id == booking_id,
            TravelBooking.user_id == user_id
        ).first()

    def cancel_booking(self, booking_id: int, user_id: int) -> bool:
        """Cancel a booking."""
        try:
            booking = self.get_booking(booking_id, user_id)
            if not booking or booking.status == BookingStatus.CANCELLED:
                return False
            
            booking.status = BookingStatus.CANCELLED
            
            # Update travel listing availability
            travel_listing = booking.travel_listing
            if travel_listing.available_spots is not None:
                travel_listing.available_spots += booking.number_of_people
                if travel_listing.status == BookingStatus.BOOKED:
                    travel_listing.status = BookingStatus.AVAILABLE
            
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error cancelling booking: {e}")
            raise

    def add_images_to_listing(self, travel_id: int, user_id: int, image_urls: List[str]) -> bool:
        """Add images to a travel listing."""
        try:
            # Verify ownership
            travel_listing = self.db.query(TravelListing).filter(
                TravelListing.id == travel_id,
                TravelListing.user_id == user_id
            ).first()
            
            if not travel_listing:
                return False
            
            # Add images
            for url in image_urls:
                db_image = TravelImage(
                    travel_listing_id=travel_id,
                    image_url=url,
                    is_primary=False
                )
                self.db.add(db_image)
            
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error adding images: {e}")
            raise

    def remove_image(self, image_id: int, user_id: int) -> bool:
        """Remove an image from a travel listing."""
        try:
            image = self.db.query(TravelImage).join(TravelListing).filter(
                TravelImage.id == image_id,
                TravelListing.user_id == user_id
            ).first()
            
            if not image:
                return False
            
            self.db.delete(image)
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error removing image: {e}")
            raise