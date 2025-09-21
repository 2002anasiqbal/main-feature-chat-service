from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from ..database.database import Base
import enum

class CommercialType(enum.Enum):
    FLIGHT = "flight"
    HOTEL = "hotel"
    CAR_RENTAL = "car_rental"
    PACKAGE_TOUR = "package_tour"
    CRUISE = "cruise"
    ACTIVITY = "activity"

class BookingStatus(enum.Enum):
    AVAILABLE = "available"
    BOOKED = "booked"
    CANCELLED = "cancelled"
    EXPIRED = "expired"

class CommercialListing(Base):
    __tablename__ = "commercial_listings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    commercial_type = Column(Enum(CommercialType), nullable=False, index=True)
    
    # Location information
    departure_location = Column(String(255))
    destination_location = Column(String(255), nullable=False)
    departure_coordinates = Column(Geometry('POINT'))
    destination_coordinates = Column(Geometry('POINT'))
    
    # Pricing
    price = Column(Float, nullable=False)
    currency = Column(String(3), default="NOK")
    price_per_person = Column(Boolean, default=True)
    
    # Dates
    departure_date = Column(DateTime)
    return_date = Column(DateTime)
    booking_deadline = Column(DateTime)
    
    # Capacity
    max_capacity = Column(Integer)
    available_spots = Column(Integer)
    
    # Provider information
    provider_name = Column(String(255))
    provider_contact = Column(String(255))
    
    # Status
    status = Column(Enum(BookingStatus), default=BookingStatus.AVAILABLE)
    is_active = Column(Boolean, default=True)
    
    # User information
    user_id = Column(Integer, nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    images = relationship("CommercialImage", back_populates="commercial_listing", cascade="all, delete-orphan")
    bookings = relationship("CommercialBooking", back_populates="commercial_listing")
    amenities = relationship("CommercialAmenity", back_populates="commercial_listing", cascade="all, delete-orphan")

class CommercialImage(Base):
    __tablename__ = "commercial_images"
    
    id = Column(Integer, primary_key=True, index=True)
    commercial_listing_id = Column(Integer, ForeignKey("commercial_listings.id"), nullable=False)
    image_url = Column(String(500), nullable=False)
    alt_text = Column(String(255))
    is_primary = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    commercial_listing = relationship("CommercialListing", back_populates="images")

class CommercialBooking(Base):
    __tablename__ = "commercial_bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    commercial_listing_id = Column(Integer, ForeignKey("commercial_listings.id"), nullable=False)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Booking details
    number_of_people = Column(Integer, default=1)
    total_price = Column(Float, nullable=False)
    booking_reference = Column(String(50), unique=True, index=True)
    
    # Contact information
    contact_name = Column(String(255), nullable=False)
    contact_email = Column(String(255), nullable=False)
    contact_phone = Column(String(50))
    
    # Special requests
    special_requests = Column(Text)
    
    # Status
    status = Column(Enum(BookingStatus), default=BookingStatus.BOOKED)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    commercial_listing = relationship("CommercialListing", back_populates="bookings")

class CommercialAmenity(Base):
    __tablename__ = "commercial_amenities"
    
    id = Column(Integer, primary_key=True, index=True)
    commercial_listing_id = Column(Integer, ForeignKey("commercial_listings.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    is_included = Column(Boolean, default=True)
    additional_cost = Column(Float, default=0.0)
    
    # Relationships
    commercial_listing = relationship("CommercialListing", back_populates="amenities")