from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime
from enum import Enum

class CommercialVehicleTypeEnum(str, Enum):
    TRUCK = "truck"
    VAN = "van"
    BUS = "bus"
    TRAILER = "trailer"
    CONSTRUCTION = "construction"
    AGRICULTURAL = "agricultural"
    INDUSTRIAL = "industrial"
    CRANE = "crane"
    EXCAVATOR = "excavator"
    FORKLIFT = "forklift"
    DUMP_TRUCK = "dump_truck"
    DELIVERY_TRUCK = "delivery_truck"

class VehicleConditionEnum(str, Enum):
    NEW = "new"
    LIKE_NEW = "like_new"
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    FOR_PARTS = "for_parts"

class FuelTypeEnum(str, Enum):
    DIESEL = "diesel"
    PETROL = "petrol"
    ELECTRIC = "electric"
    HYBRID = "hybrid"
    HYDROGEN = "hydrogen"
    CNG = "cng"
    LPG = "lpg"

class TransmissionTypeEnum(str, Enum):
    MANUAL = "manual"
    AUTOMATIC = "automatic"
    SEMI_AUTOMATIC = "semi_automatic"

class ListingStatusEnum(str, Enum):
    ACTIVE = "active"
    SOLD = "sold"
    RESERVED = "reserved"
    EXPIRED = "expired"
    REMOVED = "removed"

# Image schemas
class CommercialVehicleImageBase(BaseModel):
    image_url: str
    alt_text: Optional[str] = None
    is_primary: bool = False
    display_order: int = 0

class CommercialVehicleImageCreate(CommercialVehicleImageBase):
    pass

class CommercialVehicleImageResponse(CommercialVehicleImageBase):
    id: int
    vehicle_listing_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Feature schemas
class CommercialVehicleFeatureBase(BaseModel):
    feature_name: str
    feature_value: Optional[str] = None
    is_highlight: bool = False

class CommercialVehicleFeatureCreate(CommercialVehicleFeatureBase):
    pass

class CommercialVehicleFeatureResponse(CommercialVehicleFeatureBase):
    id: int
    vehicle_listing_id: int
    
    class Config:
        from_attributes = True

# Main listing schemas
class CommercialVehicleListingBase(BaseModel):
    title: str
    description: Optional[str] = None
    vehicle_type: CommercialVehicleTypeEnum
    make: str
    model: str
    year: int
    condition: VehicleConditionEnum
    engine_size: Optional[float] = None
    power_hp: Optional[int] = None
    power_kw: Optional[int] = None
    fuel_type: FuelTypeEnum
    transmission: Optional[TransmissionTypeEnum] = None
    mileage: Optional[int] = None
    payload_capacity: Optional[int] = None
    gross_weight: Optional[int] = None
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    axles: Optional[int] = None
    price: float
    currency: str = "NOK"
    is_negotiable: bool = True
    vat_included: bool = True
    location: str
    postal_code: Optional[str] = None
    registration_number: Optional[str] = None
    first_registration: Optional[datetime] = None
    next_inspection: Optional[datetime] = None
    has_valid_inspection: bool = True
    equipment_list: Optional[str] = None
    previous_owners: Optional[int] = None
    service_history_available: bool = False
    accident_history: Optional[str] = None
    pickup_available: bool = True
    delivery_available: bool = False
    delivery_cost: Optional[float] = None

    @validator('year')
    def validate_year(cls, v):
        current_year = datetime.now().year
        if v < 1900 or v > current_year + 1:
            raise ValueError(f'Year must be between 1900 and {current_year + 1}')
        return v

    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than 0')
        return v

class CommercialVehicleListingCreate(CommercialVehicleListingBase):
    images: Optional[List[CommercialVehicleImageCreate]] = []
    features: Optional[List[CommercialVehicleFeatureCreate]] = []

class CommercialVehicleListingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    vehicle_type: Optional[CommercialVehicleTypeEnum] = None
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    condition: Optional[VehicleConditionEnum] = None
    engine_size: Optional[float] = None
    power_hp: Optional[int] = None
    power_kw: Optional[int] = None
    fuel_type: Optional[FuelTypeEnum] = None
    transmission: Optional[TransmissionTypeEnum] = None
    mileage: Optional[int] = None
    payload_capacity: Optional[int] = None
    gross_weight: Optional[int] = None
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    axles: Optional[int] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    is_negotiable: Optional[bool] = None
    vat_included: Optional[bool] = None
    location: Optional[str] = None
    postal_code: Optional[str] = None
    registration_number: Optional[str] = None
    first_registration: Optional[datetime] = None
    next_inspection: Optional[datetime] = None
    has_valid_inspection: Optional[bool] = None
    equipment_list: Optional[str] = None
    previous_owners: Optional[int] = None
    service_history_available: Optional[bool] = None
    accident_history: Optional[str] = None
    pickup_available: Optional[bool] = None
    delivery_available: Optional[bool] = None
    delivery_cost: Optional[float] = None
    status: Optional[ListingStatusEnum] = None

class CommercialVehicleListingResponse(CommercialVehicleListingBase):
    id: int
    user_id: int
    status: ListingStatusEnum
    is_active: bool
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime] = None
    images: List[CommercialVehicleImageResponse] = []
    features: List[CommercialVehicleFeatureResponse] = []
    
    class Config:
        from_attributes = True

class CommercialVehicleListingListResponse(BaseModel):
    listings: List[CommercialVehicleListingResponse]
    total: int
    page: int
    per_page: int
    total_pages: int

# Search and filter schemas
class CommercialVehicleSearchFilters(BaseModel):
    vehicle_type: Optional[List[CommercialVehicleTypeEnum]] = None
    make: Optional[List[str]] = None
    model: Optional[List[str]] = None
    year_from: Optional[int] = None
    year_to: Optional[int] = None
    price_from: Optional[float] = None
    price_to: Optional[float] = None
    mileage_from: Optional[int] = None
    mileage_to: Optional[int] = None
    fuel_type: Optional[List[FuelTypeEnum]] = None
    transmission: Optional[List[TransmissionTypeEnum]] = None
    condition: Optional[List[VehicleConditionEnum]] = None
    location: Optional[str] = None
    payload_capacity_from: Optional[int] = None
    payload_capacity_to: Optional[int] = None
    has_valid_inspection: Optional[bool] = None
    delivery_available: Optional[bool] = None

class CommercialVehicleSearchRequest(BaseModel):
    query: Optional[str] = None
    filters: Optional[CommercialVehicleSearchFilters] = None
    sort_by: Optional[str] = "created_at"
    sort_order: Optional[str] = "desc"
    page: int = 1
    per_page: int = 20

# Statistics schemas
class CommercialVehicleStats(BaseModel):
    total_listings: int
    active_listings: int
    sold_listings: int
    average_price: float
    listings_by_type: dict
    listings_by_condition: dict
    listings_by_fuel_type: dict