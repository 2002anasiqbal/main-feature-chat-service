# property-service/src/services/holiday_rental_services.py
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc
from typing import List, Optional, Dict, Any, Tuple
from fastapi import HTTPException, status
from datetime import datetime, date, timedelta
from decimal import Decimal
import uuid
import logging

from ..models.holiday_rental_models import (
    HolidayRental, HolidayRentalBooking, HolidayRentalReview, HolidayRentalAvailability
)
from ..models.holiday_rental_schemas import (
    HolidayRentalCreate, HolidayRentalUpdate, HolidayRentalResponse,
    HolidayRentalBookingCreate, HolidayRentalBookingResponse,
    HolidayRentalReviewCreate, HolidayRentalReviewResponse,
    HolidayRentalAvailabilityCreate, HolidayRentalAvailabilityResponse,
    HolidayRentalSearchRequest, HolidayRentalListResponse,
    HolidayRentalStats, BookingStatusEnum
)

logger = logging.getLogger(__name__)

class HolidayRentalService:
    def __init__(self, db: Session):
        self.db = db

    async def create_holiday_rental(self, rental_data: HolidayRentalCreate, owner_id: str) -> HolidayRentalResponse:
        """Create a new holiday rental."""
        try:
            rental_dict = rental_data.dict()
            rental_dict['owner_id'] = owner_id
            
            rental = HolidayRental(**rental_dict)
            self.db.add(rental)
            self.db.commit()
            self.db.refresh(rental)
            
            return HolidayRentalResponse.from_orm(rental)
        except Exception as e:
            logger.error(f"Error creating holiday rental: {str(e)}")
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Failed to create holiday rental")

    async def get_holiday_rental_by_id(self, rental_id: str) -> Optional[HolidayRentalResponse]:
        """Get a holiday rental by ID."""
        rental = self.db.query(HolidayRental).filter(
            HolidayRental.id == rental_id
        ).first()
        
        if rental:
            return HolidayRentalResponse.from_orm(rental)
        return None

    async def update_holiday_rental(self, rental_id: str, rental_data: HolidayRentalUpdate, owner_id: str) -> Optional[HolidayRentalResponse]:
        """Update a holiday rental."""
        rental = self.db.query(HolidayRental).filter(
            and_(
                HolidayRental.id == rental_id,
                HolidayRental.owner_id == owner_id
            )
        ).first()
        
        if not rental:
            return None
        
        update_dict = rental_data.dict(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(rental, key, value)
        
        rental.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(rental)
        
        return HolidayRentalResponse.from_orm(rental)

    async def delete_holiday_rental(self, rental_id: str, owner_id: str) -> bool:
        """Delete a holiday rental."""
        rental = self.db.query(HolidayRental).filter(
            and_(
                HolidayRental.id == rental_id,
                HolidayRental.owner_id == owner_id
            )
        ).first()
        
        if not rental:
            return False
        
        self.db.delete(rental)
        self.db.commit()
        return True

    async def search_holiday_rentals(self, search_request: HolidayRentalSearchRequest) -> HolidayRentalListResponse:
        """Search holiday rentals with filters."""
        try:
            query = self.db.query(HolidayRental).filter(
                HolidayRental.is_active == True
            )
            
            # Apply filters
            if search_request.filters:
                filters = search_request.filters
                
                if filters.rental_type:
                    query = query.filter(HolidayRental.rental_type.in_(filters.rental_type))
                
                if filters.min_guests:
                    query = query.filter(HolidayRental.max_guests >= filters.min_guests)
                
                if filters.max_guests:
                    query = query.filter(HolidayRental.max_guests <= filters.max_guests)
                
                if filters.price_from:
                    query = query.filter(HolidayRental.price_per_night >= filters.price_from)
                
                if filters.price_to:
                    query = query.filter(HolidayRental.price_per_night <= filters.price_to)
                
                if filters.min_nights:
                    query = query.filter(HolidayRental.min_nights <= filters.min_nights)
                
                if filters.max_nights:
                    query = query.filter(
                        or_(
                            HolidayRental.max_nights >= filters.max_nights,
                            HolidayRental.max_nights.is_(None)
                        )
                    )
                
                # Amenity filters
                if filters.has_wifi:
                    query = query.filter(HolidayRental.has_wifi == filters.has_wifi)
                
                if filters.has_kitchen:
                    query = query.filter(HolidayRental.has_kitchen == filters.has_kitchen)
                
                if filters.has_hot_tub:
                    query = query.filter(HolidayRental.has_hot_tub == filters.has_hot_tub)
                
                if filters.has_sauna:
                    query = query.filter(HolidayRental.has_sauna == filters.has_sauna)
                
                if filters.has_boat_access:
                    query = query.filter(HolidayRental.has_boat_access == filters.has_boat_access)
                
                if filters.has_ski_access:
                    query = query.filter(HolidayRental.has_ski_access == filters.has_ski_access)
                
                if filters.has_beach_access:
                    query = query.filter(HolidayRental.has_beach_access == filters.has_beach_access)
                
                if filters.pets_allowed:
                    query = query.filter(HolidayRental.pets_allowed == filters.pets_allowed)
                
                if filters.instant_booking:
                    query = query.filter(HolidayRental.instant_booking == filters.instant_booking)
                
                if filters.min_rating:
                    query = query.filter(HolidayRental.average_rating >= filters.min_rating)
                
                # Date availability filter
                if filters.check_in_date and filters.check_out_date:
                    # Check if rental is available for the requested dates
                    unavailable_rentals = self.db.query(HolidayRentalBooking.holiday_rental_id).filter(
                        and_(
                            HolidayRentalBooking.status.in_(['confirmed', 'pending']),
                            or_(
                                and_(
                                    HolidayRentalBooking.check_in_date <= filters.check_in_date,
                                    HolidayRentalBooking.check_out_date > filters.check_in_date
                                ),
                                and_(
                                    HolidayRentalBooking.check_in_date < filters.check_out_date,
                                    HolidayRentalBooking.check_out_date >= filters.check_out_date
                                ),
                                and_(
                                    HolidayRentalBooking.check_in_date >= filters.check_in_date,
                                    HolidayRentalBooking.check_out_date <= filters.check_out_date
                                )
                            )
                        )
                    ).subquery()
                    
                    query = query.filter(~HolidayRental.id.in_(unavailable_rentals))
            
            # Apply text search
            if search_request.query:
                # Join with Property table for location search
                from ..models.models import Property
                query = query.join(Property, HolidayRental.property_id == Property.id)
                search_term = f"%{search_request.query}%"
                query = query.filter(
                    or_(
                        Property.title.ilike(search_term),
                        Property.description.ilike(search_term),
                        Property.city.ilike(search_term),
                        Property.address.ilike(search_term)
                    )
                )
            
            # Get total count
            total = query.count()
            
            # Apply sorting
            if search_request.sort_by:
                sort_column = getattr(HolidayRental, search_request.sort_by, None)
                if sort_column:
                    if search_request.sort_order == "desc":
                        query = query.order_by(desc(sort_column))
                    else:
                        query = query.order_by(asc(sort_column))
            
            # Apply pagination
            offset = (search_request.page - 1) * search_request.per_page
            rentals = query.offset(offset).limit(search_request.per_page).all()
            
            total_pages = (total + search_request.per_page - 1) // search_request.per_page
            
            return HolidayRentalListResponse(
                rentals=[HolidayRentalResponse.from_orm(rental) for rental in rentals],
                total=total,
                page=search_request.page,
                per_page=search_request.per_page,
                total_pages=total_pages
            )
        except Exception as e:
            logger.error(f"Error searching holiday rentals: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to search holiday rentals")

    async def create_booking(self, booking_data: HolidayRentalBookingCreate, guest_id: str) -> HolidayRentalBookingResponse:
        """Create a new holiday rental booking."""
        try:
            # Get the holiday rental
            rental = self.db.query(HolidayRental).filter(
                HolidayRental.id == booking_data.holiday_rental_id
            ).first()
            
            if not rental:
                raise HTTPException(status_code=404, detail="Holiday rental not found")
            
            # Check availability
            nights = (booking_data.check_out_date - booking_data.check_in_date).days
            if nights < rental.min_nights:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Minimum stay is {rental.min_nights} nights"
                )
            
            if rental.max_nights and nights > rental.max_nights:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Maximum stay is {rental.max_nights} nights"
                )
            
            if booking_data.guests > rental.max_guests:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Maximum guests allowed is {rental.max_guests}"
                )
            
            # Check for conflicting bookings
            conflicting_booking = self.db.query(HolidayRentalBooking).filter(
                and_(
                    HolidayRentalBooking.holiday_rental_id == booking_data.holiday_rental_id,
                    HolidayRentalBooking.status.in_(['confirmed', 'pending']),
                    or_(
                        and_(
                            HolidayRentalBooking.check_in_date <= booking_data.check_in_date,
                            HolidayRentalBooking.check_out_date > booking_data.check_in_date
                        ),
                        and_(
                            HolidayRentalBooking.check_in_date < booking_data.check_out_date,
                            HolidayRentalBooking.check_out_date >= booking_data.check_out_date
                        ),
                        and_(
                            HolidayRentalBooking.check_in_date >= booking_data.check_in_date,
                            HolidayRentalBooking.check_out_date <= booking_data.check_out_date
                        )
                    )
                )
            ).first()
            
            if conflicting_booking:
                raise HTTPException(status_code=400, detail="Dates are not available")
            
            # Calculate pricing
            base_price = rental.price_per_night * nights
            cleaning_fee = rental.cleaning_fee
            security_deposit = rental.security_deposit
            extra_fees = Decimal(0)
            
            if booking_data.pets > 0 and rental.pet_fee > 0:
                extra_fees += rental.pet_fee * booking_data.pets
            
            if booking_data.guests > 2 and rental.extra_guest_fee > 0:
                extra_fees += rental.extra_guest_fee * (booking_data.guests - 2)
            
            total_price = base_price + cleaning_fee + extra_fees
            
            # Create booking
            booking_dict = booking_data.dict()
            booking_dict.update({
                'guest_id': guest_id,
                'nights': nights,
                'base_price': base_price,
                'cleaning_fee': cleaning_fee,
                'security_deposit': security_deposit,
                'extra_fees': extra_fees,
                'total_price': total_price,
                'confirmation_code': str(uuid.uuid4())[:8].upper()
            })
            
            booking = HolidayRentalBooking(**booking_dict)
            self.db.add(booking)
            
            # Update rental statistics
            rental.total_bookings += 1
            
            self.db.commit()
            self.db.refresh(booking)
            
            return HolidayRentalBookingResponse.from_orm(booking)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating booking: {str(e)}")
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Failed to create booking")

    async def get_user_bookings(self, user_id: str, page: int = 1, per_page: int = 20) -> List[HolidayRentalBookingResponse]:
        """Get user's holiday rental bookings."""
        query = self.db.query(HolidayRentalBooking).filter(
            HolidayRentalBooking.guest_id == user_id
        )
        
        offset = (page - 1) * per_page
        bookings = query.order_by(desc(HolidayRentalBooking.created_at)).offset(offset).limit(per_page).all()
        
        return [HolidayRentalBookingResponse.from_orm(booking) for booking in bookings]

    async def get_owner_bookings(self, owner_id: str, page: int = 1, per_page: int = 20) -> List[HolidayRentalBookingResponse]:
        """Get owner's holiday rental bookings."""
        query = self.db.query(HolidayRentalBooking).join(
            HolidayRental, HolidayRentalBooking.holiday_rental_id == HolidayRental.id
        ).filter(
            HolidayRental.owner_id == owner_id
        )
        
        offset = (page - 1) * per_page
        bookings = query.order_by(desc(HolidayRentalBooking.created_at)).offset(offset).limit(per_page).all()
        
        return [HolidayRentalBookingResponse.from_orm(booking) for booking in bookings]

    async def update_booking_status(self, booking_id: str, status: BookingStatusEnum, user_id: str) -> Optional[HolidayRentalBookingResponse]:
        """Update booking status."""
        booking = self.db.query(HolidayRentalBooking).join(
            HolidayRental, HolidayRentalBooking.holiday_rental_id == HolidayRental.id
        ).filter(
            and_(
                HolidayRentalBooking.id == booking_id,
                or_(
                    HolidayRentalBooking.guest_id == user_id,
                    HolidayRental.owner_id == user_id
                )
            )
        ).first()
        
        if not booking:
            return None
        
        booking.status = status
        booking.updated_at = datetime.utcnow()
        
        if status == BookingStatusEnum.CONFIRMED:
            booking.confirmed_at = datetime.utcnow()
        elif status == BookingStatusEnum.CANCELLED:
            booking.cancelled_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(booking)
        
        return HolidayRentalBookingResponse.from_orm(booking)

    async def create_review(self, review_data: HolidayRentalReviewCreate, reviewer_id: str) -> HolidayRentalReviewResponse:
        """Create a review for a holiday rental."""
        try:
            # Verify the booking exists and belongs to the reviewer
            booking = self.db.query(HolidayRentalBooking).filter(
                and_(
                    HolidayRentalBooking.id == review_data.booking_id,
                    HolidayRentalBooking.guest_id == reviewer_id,
                    HolidayRentalBooking.status == BookingStatusEnum.COMPLETED
                )
            ).first()
            
            if not booking:
                raise HTTPException(status_code=404, detail="Booking not found or not eligible for review")
            
            # Check if review already exists
            existing_review = self.db.query(HolidayRentalReview).filter(
                HolidayRentalReview.booking_id == review_data.booking_id
            ).first()
            
            if existing_review:
                raise HTTPException(status_code=400, detail="Review already exists for this booking")
            
            # Create review
            review_dict = review_data.dict()
            review_dict.update({
                'holiday_rental_id': booking.holiday_rental_id,
                'reviewer_id': reviewer_id
            })
            
            review = HolidayRentalReview(**review_dict)
            self.db.add(review)
            
            # Update rental rating
            rental = self.db.query(HolidayRental).filter(
                HolidayRental.id == booking.holiday_rental_id
            ).first()
            
            if rental:
                # Calculate new average rating
                total_rating = self.db.query(func.sum(HolidayRentalReview.rating)).filter(
                    HolidayRentalReview.holiday_rental_id == rental.id
                ).scalar() or 0
                
                total_rating += review_data.rating
                rental.review_count += 1
                rental.average_rating = total_rating / rental.review_count
            
            self.db.commit()
            self.db.refresh(review)
            
            return HolidayRentalReviewResponse.from_orm(review)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating review: {str(e)}")
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Failed to create review")

    async def get_stats(self) -> HolidayRentalStats:
        """Get holiday rental statistics."""
        try:
            total_rentals = self.db.query(HolidayRental).count()
            active_rentals = self.db.query(HolidayRental).filter(
                HolidayRental.is_active == True
            ).count()
            
            total_bookings = self.db.query(HolidayRentalBooking).count()
            confirmed_bookings = self.db.query(HolidayRentalBooking).filter(
                HolidayRentalBooking.status == BookingStatusEnum.CONFIRMED
            ).count()
            
            # Average price
            avg_price_result = self.db.query(func.avg(HolidayRental.price_per_night)).filter(
                HolidayRental.is_active == True
            ).scalar()
            average_price = Decimal(str(avg_price_result)) if avg_price_result else Decimal(0)
            
            # Average rating
            avg_rating_result = self.db.query(func.avg(HolidayRental.average_rating)).filter(
                HolidayRental.is_active == True
            ).scalar()
            average_rating = Decimal(str(avg_rating_result)) if avg_rating_result else Decimal(0)
            
            # Popular locations (placeholder)
            popular_locations = []
            
            # Bookings by type
            type_stats = self.db.query(
                HolidayRental.rental_type,
                func.count(HolidayRentalBooking.id)
            ).join(
                HolidayRentalBooking, HolidayRental.id == HolidayRentalBooking.holiday_rental_id
            ).group_by(HolidayRental.rental_type).all()
            
            bookings_by_type = {str(rental_type): count for rental_type, count in type_stats}
            
            return HolidayRentalStats(
                total_rentals=total_rentals,
                active_rentals=active_rentals,
                total_bookings=total_bookings,
                confirmed_bookings=confirmed_bookings,
                average_price=average_price,
                average_rating=average_rating,
                popular_locations=popular_locations,
                bookings_by_type=bookings_by_type,
                seasonal_trends={}
            )
        except Exception as e:
            logger.error(f"Error getting holiday rental stats: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to get holiday rental statistics")