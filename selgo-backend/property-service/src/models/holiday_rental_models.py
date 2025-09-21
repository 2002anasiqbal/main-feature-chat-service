# property-service/src/models/holiday_rental_models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, DECIMAL, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import enum

# Import Base from your existing models
from .models import Base

class HolidayRentalTypeEnum(str, enum.Enum):
    CABIN = "cabin"
    COTTAGE = "cottage"
    CHALET = "chalet"
    VILLA = "villa"
    APARTMENT = "apartment"
    HOUSE = "house"
    BOAT = "boat"
    CAMPING = "camping"
    GLAMPING = "glamping"

class SeasonEnum(str, enum.Enum):
    SPRING = "spring"
    SUMMER = "summer"
    AUTUMN = "autumn"
    WINTER = "winter"
    ALL_YEAR = "all_year"

class BookingStatusEnum(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"

class HolidayRental(Base):
    __tablename__ = "holiday_rentals"
    __table_args__ = {'extend_existing': True}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"))
    owner_id = Column(UUID(as_uuid=True), nullable=False)  # User ID from auth service
    
    # Holiday Rental Specific Information
    rental_type = Column(String(50), nullable=False)  # HolidayRentalTypeEnum
    max_guests = Column(Integer, nullable=False)
    min_nights = Column(Integer, default=1)
    max_nights = Column(Integer, nullable=True)
    
    # Pricing
    price_per_night = Column(DECIMAL(10, 2), nullable=False)
    cleaning_fee = Column(DECIMAL(10, 2), default=0)
    security_deposit = Column(DECIMAL(10, 2), default=0)
    extra_guest_fee = Column(DECIMAL(10, 2), default=0)
    pet_fee = Column(DECIMAL(10, 2), default=0)
    
    # Seasonal Pricing
    summer_price_per_night = Column(DECIMAL(10, 2), nullable=True)
    winter_price_per_night = Column(DECIMAL(10, 2), nullable=True)
    weekend_surcharge = Column(DECIMAL(5, 2), default=0)  # Percentage
    holiday_surcharge = Column(DECIMAL(5, 2), default=0)  # Percentage
    
    # Availability
    available_seasons = Column(String(100), nullable=True)  # JSON array of seasons
    check_in_time = Column(String(10), default="15:00")
    check_out_time = Column(String(10), default="11:00")
    instant_booking = Column(Boolean, default=False)
    
    # Amenities and Features
    has_wifi = Column(Boolean, default=False)
    has_kitchen = Column(Boolean, default=False)
    has_washing_machine = Column(Boolean, default=False)
    has_dishwasher = Column(Boolean, default=False)
    has_tv = Column(Boolean, default=False)
    has_heating = Column(Boolean, default=False)
    has_air_conditioning = Column(Boolean, default=False)
    has_hot_tub = Column(Boolean, default=False)
    has_sauna = Column(Boolean, default=False)
    has_fireplace = Column(Boolean, default=False)
    has_bbq = Column(Boolean, default=False)
    has_boat_access = Column(Boolean, default=False)
    has_ski_access = Column(Boolean, default=False)
    has_beach_access = Column(Boolean, default=False)
    
    # Policies
    pets_allowed = Column(Boolean, default=False)
    smoking_allowed = Column(Boolean, default=False)
    parties_allowed = Column(Boolean, default=False)
    children_welcome = Column(Boolean, default=True)
    
    # Location Features
    distance_to_water = Column(Float, nullable=True)  # in meters
    distance_to_ski_lift = Column(Float, nullable=True)  # in meters
    distance_to_town_center = Column(Float, nullable=True)  # in meters
    distance_to_grocery_store = Column(Float, nullable=True)  # in meters
    
    # Booking Information
    cancellation_policy = Column(String(50), default="moderate")  # flexible, moderate, strict
    advance_booking_days = Column(Integer, default=1)  # How many days in advance can book
    
    # Status and Metrics
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    total_bookings = Column(Integer, default=0)
    average_rating = Column(DECIMAL(3, 2), default=0)
    review_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    property = relationship("Property", backref="holiday_rental")
    bookings = relationship("HolidayRentalBooking", back_populates="holiday_rental", cascade="all, delete-orphan")
    reviews = relationship("HolidayRentalReview", back_populates="holiday_rental", cascade="all, delete-orphan")
    availability = relationship("HolidayRentalAvailability", back_populates="holiday_rental", cascade="all, delete-orphan")

class HolidayRentalBooking(Base):
    __tablename__ = "holiday_rental_bookings"
    __table_args__ = {'extend_existing': True}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    holiday_rental_id = Column(UUID(as_uuid=True), ForeignKey("holiday_rentals.id", ondelete="CASCADE"))
    guest_id = Column(UUID(as_uuid=True), nullable=False)  # User ID from auth service
    
    # Booking Details
    check_in_date = Column(Date, nullable=False)
    check_out_date = Column(Date, nullable=False)
    nights = Column(Integer, nullable=False)
    guests = Column(Integer, nullable=False)
    adults = Column(Integer, nullable=False)
    children = Column(Integer, default=0)
    infants = Column(Integer, default=0)
    pets = Column(Integer, default=0)
    
    # Pricing
    base_price = Column(DECIMAL(10, 2), nullable=False)
    cleaning_fee = Column(DECIMAL(10, 2), default=0)
    security_deposit = Column(DECIMAL(10, 2), default=0)
    extra_fees = Column(DECIMAL(10, 2), default=0)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    
    # Guest Information
    guest_name = Column(String(255), nullable=False)
    guest_email = Column(String(255), nullable=False)
    guest_phone = Column(String(20), nullable=True)
    special_requests = Column(Text, nullable=True)
    
    # Status
    status = Column(String(20), default="pending")  # BookingStatusEnum
    payment_status = Column(String(20), default="pending")
    confirmation_code = Column(String(20), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    confirmed_at = Column(DateTime, nullable=True)
    cancelled_at = Column(DateTime, nullable=True)
    
    # Relationships
    holiday_rental = relationship("HolidayRental", back_populates="bookings")

class HolidayRentalReview(Base):
    __tablename__ = "holiday_rental_reviews"
    __table_args__ = {'extend_existing': True}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    holiday_rental_id = Column(UUID(as_uuid=True), ForeignKey("holiday_rentals.id", ondelete="CASCADE"))
    booking_id = Column(UUID(as_uuid=True), ForeignKey("holiday_rental_bookings.id", ondelete="CASCADE"))
    reviewer_id = Column(UUID(as_uuid=True), nullable=False)  # User ID from auth service
    
    # Review Content
    rating = Column(Integer, nullable=False)  # 1-5 stars
    title = Column(String(255), nullable=True)
    comment = Column(Text, nullable=True)
    
    # Detailed Ratings
    cleanliness_rating = Column(Integer, nullable=True)
    location_rating = Column(Integer, nullable=True)
    value_rating = Column(Integer, nullable=True)
    communication_rating = Column(Integer, nullable=True)
    check_in_rating = Column(Integer, nullable=True)
    accuracy_rating = Column(Integer, nullable=True)
    
    # Review Status
    is_approved = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    holiday_rental = relationship("HolidayRental", back_populates="reviews")

class HolidayRentalAvailability(Base):
    __tablename__ = "holiday_rental_availability"
    __table_args__ = {'extend_existing': True}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    holiday_rental_id = Column(UUID(as_uuid=True), ForeignKey("holiday_rentals.id", ondelete="CASCADE"))
    
    # Availability Period
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_available = Column(Boolean, default=True)
    
    # Pricing Override
    price_per_night = Column(DECIMAL(10, 2), nullable=True)  # Override default price
    min_nights = Column(Integer, nullable=True)  # Override default min nights
    
    # Reason for unavailability
    reason = Column(String(100), nullable=True)  # maintenance, booked, blocked, etc.
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    holiday_rental = relationship("HolidayRental", back_populates="availability")