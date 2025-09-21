from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime
from .travel_models import TravelType, BookingStatus

# Base schemas
class TravelImageBase(BaseModel):
    image_url: str
    alt_text: Optional[str] = None
    is_primary: bool = False

class TravelImageCreate(TravelImageBase):
    pass

class TravelImage(TravelImageBase):
    id: int
    travel_listing_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class TravelAmenityBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_included: bool = True
    additional_cost: float = 0.0

class TravelAmenityCreate(TravelAmenityBase):
    pass

class TravelAmenity(TravelAmenityBase):
    id: int
    travel_listing_id: int
    
    class Config:
        orm_mode = True

class TravelBookingBase(BaseModel):
    number_of_people: int = 1
    contact_name: str
    contact_email: str
    contact_phone: Optional[str] = None
    special_requests: Optional[str] = None

class TravelBookingCreate(TravelBookingBase):
    travel_listing_id: int

class TravelBooking(TravelBookingBase):
    id: int
    travel_listing_id: int
    user_id: int
    total_price: float
    booking_reference: str
    status: BookingStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class TravelListingBase(BaseModel):
    title: str
    description: Optional[str] = None
    travel_type: TravelType
    departure_location: Optional[str] = None
    destination_location: str
    price: float
    currency: str = "NOK"
    price_per_person: bool = True
    departure_date: Optional[datetime] = None
    return_date: Optional[datetime] = None
    booking_deadline: Optional[datetime] = None
    max_capacity: Optional[int] = None
    available_spots: Optional[int] = None
    provider_name: Optional[str] = None
    provider_contact: Optional[str] = None

class TravelListingCreate(TravelListingBase):
    images: Optional[List[TravelImageCreate]] = []
    amenities: Optional[List[TravelAmenityCreate]] = []

class TravelListingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    travel_type: Optional[TravelType] = None
    departure_location: Optional[str] = None
    destination_location: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    price_per_person: Optional[bool] = None
    departure_date: Optional[datetime] = None
    return_date: Optional[datetime] = None
    booking_deadline: Optional[datetime] = None
    max_capacity: Optional[int] = None
    available_spots: Optional[int] = None
    provider_name: Optional[str] = None
    provider_contact: Optional[str] = None
    status: Optional[BookingStatus] = None
    is_active: Optional[bool] = None

class TravelListing(TravelListingBase):
    id: int
    user_id: int
    status: BookingStatus
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    images: List[TravelImage] = []
    amenities: List[TravelAmenity] = []
    
    class Config:
        orm_mode = True

class TravelListingWithBookings(TravelListing):
    bookings: List[TravelBooking] = []

# Search and filter schemas
class TravelSearchParams(BaseModel):
    travel_type: Optional[TravelType] = None
    destination: Optional[str] = None
    departure_location: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    departure_date_from: Optional[datetime] = None
    departure_date_to: Optional[datetime] = None
    max_capacity: Optional[int] = None
    page: int = 1
    limit: int = 20

class TravelListResponse(BaseModel):
    items: List[TravelListing]
    total: int
    page: int
    limit: int
    total_pages: int