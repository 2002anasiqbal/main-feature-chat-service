from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional, Dict, Any
from ..models.commercial_models import CommercialListing, CommercialImage, CommercialBooking, CommercialAmenity, CommercialType, BookingStatus
from ..models.commercial_schemas import CommercialListingCreate, CommercialListingUpdate, CommercialSearchParams
import logging
import uuid

logger = logging.getLogger(__name__)

class CommercialRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_commercial_listing(self, commercial_data: CommercialListingCreate, user_id: int) -> CommercialListing:
        """Create a new commercial listing."""
        try:
            # Create the main commercial listing
            db_commercial = CommercialListing(
                **commercial_data.dict(exclude={"images", "amenities"}),
                user_id=user_id
            )
            
            self.db.add(db_commercial)
            self.db.flush()  # Get the ID without committing
            
            # Add images if provided
            if commercial_data.images:
                for image_data in commercial_data.images:
                    db_image = CommercialImage(
                        **image_data.dict(),
                        commercial_listing_id=db_commercial.id
                    )
                    self.db.add(db_image)
            
            # Add amenities if provided
            if commercial_data.amenities:
                for amenity_data in commercial_data.amenities:
                    db_amenity = CommercialAmenity(
                        **amenity_data.dict(),
                        commercial_listing_id=db_commercial.id
                    )
                    self.db.add(db_amenity)
            
            self.db.commit()
            self.db.refresh(db_commercial)
            return db_commercial
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating commercial listing: {e}")
            raise

    def get_commercial_listing(self, commercial_id: int) -> Optional[CommercialListing]:
        """Get a commercial listing by ID."""
        return self.db.query(CommercialListing).filter(
            CommercialListing.id == commercial_id,
            CommercialListing.is_active == True
        ).first()

    def get_commercial_listings(self, search_params: CommercialSearchParams) -> tuple[List[CommercialListing], int]:
        """Get commercial listings with search and pagination."""
        query = self.db.query(CommercialListing).filter(CommercialListing.is_active == True)
        
        # Apply filters
        if search_params.commercial_type:
            query = query.filter(CommercialListing.commercial_type == search_params.commercial_type)
        
        if search_params.destination:
            query = query.filter(
                CommercialListing.destination_location.ilike(f"%{search_params.destination}%")
            )
        
        if search_params.departure_location:
            query = query.filter(
                CommercialListing.departure_location.ilike(f"%{search_params.departure_location}%")
            )
        
        if search_params.min_price:
            query = query.filter(CommercialListing.price >= search_params.min_price)
        
        if search_params.max_price:
            query = query.filter(CommercialListing.price <= search_params.max_price)
        
        if search_params.departure_date_from:
            query = query.filter(CommercialListing.departure_date >= search_params.departure_date_from)
        
        if search_params.departure_date_to:
            query = query.filter(CommercialListing.departure_date <= search_params.departure_date_to)
        
        if search_params.max_capacity:
            query = query.filter(CommercialListing.max_capacity >= search_params.max_capacity)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (search_params.page - 1) * search_params.limit
        listings = query.offset(offset).limit(search_params.limit).all()
        
        return listings, total

    def get_user_commercial_listings(self, user_id: int, page: int = 1, limit: int = 20) -> tuple[List[CommercialListing], int]:
        """Get commercial listings for a specific user."""
        query = self.db.query(CommercialListing).filter(
            CommercialListing.user_id == user_id,
            CommercialListing.is_active == True
        )
        
        total = query.count()
        offset = (page - 1) * limit
        listings = query.offset(offset).limit(limit).all()
        
        return listings, total

    def update_commercial_listing(self, commercial_id: int, commercial_data: CommercialListingUpdate, user_id: int) -> Optional[CommercialListing]:
        """Update a commercial listing."""
        try:
            db_commercial = self.db.query(CommercialListing).filter(
                CommercialListing.id == commercial_id,
                CommercialListing.user_id == user_id,
                CommercialListing.is_active == True
            ).first()
            
            if not db_commercial:
                return None
            
            # Update fields
            update_data = commercial_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_commercial, field, value)
            
            self.db.commit()
            self.db.refresh(db_commercial)
            return db_commercial
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating commercial listing: {e}")
            raise

    def delete_commercial_listing(self, commercial_id: int, user_id: int) -> bool:
        """Soft delete a commercial listing."""
        try:
            db_commercial = self.db.query(CommercialListing).filter(
                CommercialListing.id == commercial_id,
                CommercialListing.user_id == user_id
            ).first()
            
            if not db_commercial:
                return False
            
            db_commercial.is_active = False
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting commercial listing: {e}")
            raise

    def create_booking(self, commercial_id: int, user_id: int, booking_data: dict) -> Optional[CommercialBooking]:
        """Create a new booking for a commercial listing."""
        try:
            # Check if commercial listing exists and is available
            commercial_listing = self.get_commercial_listing(commercial_id)
            if not commercial_listing or commercial_listing.status != BookingStatus.AVAILABLE:
                return None
            
            # Check availability
            if commercial_listing.available_spots and commercial_listing.available_spots < booking_data.get("number_of_people", 1):
                return None
            
            # Calculate total price
            total_price = commercial_listing.price * booking_data.get("number_of_people", 1)
            
            # Generate booking reference
            booking_reference = f"TRV-{uuid.uuid4().hex[:8].upper()}"
            
            # Create booking
            db_booking = CommercialBooking(
                commercial_listing_id=commercial_id,
                user_id=user_id,
                total_price=total_price,
                booking_reference=booking_reference,
                **booking_data
            )
            
            self.db.add(db_booking)
            
            # Update available spots
            if commercial_listing.available_spots:
                commercial_listing.available_spots -= booking_data.get("number_of_people", 1)
                if commercial_listing.available_spots <= 0:
                    commercial_listing.status = BookingStatus.BOOKED
            
            self.db.commit()
            self.db.refresh(db_booking)
            return db_booking
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating booking: {e}")
            raise

    def get_user_bookings(self, user_id: int, page: int = 1, limit: int = 20) -> tuple[List[CommercialBooking], int]:
        """Get bookings for a specific user."""
        query = self.db.query(CommercialBooking).filter(CommercialBooking.user_id == user_id)
        
        total = query.count()
        offset = (page - 1) * limit
        bookings = query.offset(offset).limit(limit).all()
        
        return bookings, total

    def get_booking(self, booking_id: int, user_id: int) -> Optional[CommercialBooking]:
        """Get a specific booking."""
        return self.db.query(CommercialBooking).filter(
            CommercialBooking.id == booking_id,
            CommercialBooking.user_id == user_id
        ).first()

    def cancel_booking(self, booking_id: int, user_id: int) -> bool:
        """Cancel a booking."""
        try:
            booking = self.get_booking(booking_id, user_id)
            if not booking or booking.status == BookingStatus.CANCELLED:
                return False
            
            booking.status = BookingStatus.CANCELLED
            
            # Update commercial listing availability
            commercial_listing = booking.commercial_listing
            if commercial_listing.available_spots is not None:
                commercial_listing.available_spots += booking.number_of_people
                if commercial_listing.status == BookingStatus.BOOKED:
                    commercial_listing.status = BookingStatus.AVAILABLE
            
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error cancelling booking: {e}")
            raise

    def add_images_to_listing(self, commercial_id: int, user_id: int, image_urls: List[str]) -> bool:
        """Add images to a commercial listing."""
        try:
            # Verify ownership
            commercial_listing = self.db.query(CommercialListing).filter(
                CommercialListing.id == commercial_id,
                CommercialListing.user_id == user_id
            ).first()
            
            if not commercial_listing:
                return False
            
            # Add images
            for url in image_urls:
                db_image = CommercialImage(
                    commercial_listing_id=commercial_id,
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
        """Remove an image from a commercial listing."""
        try:
            image = self.db.query(CommercialImage).join(CommercialListing).filter(
                CommercialImage.id == image_id,
                CommercialListing.user_id == user_id
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