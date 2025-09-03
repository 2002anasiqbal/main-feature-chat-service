# property-service/src/schemas.py
from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal
from uuid import UUID
import enum

class PropertyTypeEnum(str, enum.Enum):
    PURCHASE = "purchase"
    RENT = "rent"
    SELL = "sell"
    NUTRITION = "nutrition"

class PropertyCategoryEnum(str, enum.Enum):
    PLOTS = "plots"
    RESIDENCE_ABROAD = "residence_abroad"
    HOUSING_SALE = "housing_sale"
    NEW_HOMES = "new_homes"
    VACATION_HOMES = "vacation_homes"
    LEISURE_PLOTS = "leisure_plots"

class PropertyStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    SOLD = "sold"
    RENTED = "rented"
    PENDING = "pending"
    INACTIVE = "inactive"

# Base Schemas
class PropertyCategoryBase(BaseModel):
    label: str
    type: PropertyTypeEnum
    icon: Optional[str] = None
    route: Optional[str] = None
    description: Optional[str] = None

class PropertyCategoryCreate(PropertyCategoryBase):
    pass

class PropertyCategoryResponse(PropertyCategoryBase):
    id: int
    is_active: bool
    sort_order: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PropertyImageBase(BaseModel):
    image_url: str
    alt_text: Optional[str] = None
    is_primary: bool = False
    sort_order: int = 0

class PropertyImageCreate(PropertyImageBase):
    pass

class PropertyImageResponse(PropertyImageBase):
    id: UUID
    property_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

class FacilityBase(BaseModel):
    name: str
    icon: Optional[str] = None
    category: Optional[str] = None

class FacilityResponse(FacilityBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class PropertyFacilityBase(BaseModel):
    facility_id: int
    value: Optional[str] = None

class PropertyFacilityCreate(PropertyFacilityBase):
    pass

class PropertyFacilityResponse(PropertyFacilityBase):
    id: UUID
    property_id: UUID
    facility: Optional[FacilityResponse] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class PropertyBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: Decimal
    property_type: PropertyTypeEnum
    property_category: PropertyCategoryEnum
    
    # Property Details
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    rooms: Optional[int] = None
    use_area: Optional[float] = None
    plot_area: Optional[float] = None
    year_built: Optional[int] = None
    
    # Property Type and Features
    housing_type: Optional[str] = None
    ownership_form: Optional[str] = None
    condition: Optional[str] = None
    
    # Location
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: str = "Norway"
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Features
    is_furnished: bool = False
    has_balcony: bool = False
    has_terrace: bool = False
    has_fireplace: bool = False
    has_parking: bool = False
    parking_spaces: int = 0
    has_garden: bool = False
    has_basement: bool = False
    has_garage: bool = False
    
    # Energy and Utilities
    energy_rating: Optional[str] = None
    heating_type: Optional[str] = None
    
    # Financial
    monthly_costs: Optional[Decimal] = None
    deposit_amount: Optional[Decimal] = None
    shared_costs: Optional[Decimal] = None
    property_tax: Optional[Decimal] = None
    
    # Owner Information
    owner_name: Optional[str] = None
    owner_phone: Optional[str] = None
    owner_email: Optional[EmailStr] = None
    is_agent: bool = False
    agent_company: Optional[str] = None

class PropertyCreate(PropertyBase):
    owner_id: UUID
    category_id: Optional[int] = None
    images: Optional[List[PropertyImageCreate]] = []
    facilities: Optional[List[PropertyFacilityCreate]] = []

class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    status: Optional[PropertyStatusEnum] = None
    
    # Property Details
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    rooms: Optional[int] = None
    use_area: Optional[float] = None
    plot_area: Optional[float] = None
    year_built: Optional[int] = None
    
    # Features
    is_furnished: Optional[bool] = None
    has_balcony: Optional[bool] = None
    has_terrace: Optional[bool] = None
    has_fireplace: Optional[bool] = None
    has_parking: Optional[bool] = None
    parking_spaces: Optional[int] = None
    has_garden: Optional[bool] = None
    has_basement: Optional[bool] = None
    has_garage: Optional[bool] = None
    
    # Financial
    monthly_costs: Optional[Decimal] = None
    deposit_amount: Optional[Decimal] = None
    shared_costs: Optional[Decimal] = None
    property_tax: Optional[Decimal] = None

class PropertyResponse(PropertyBase):
    id: UUID
    status: PropertyStatusEnum
    slug: Optional[str] = None
    category_id: Optional[int] = None
    is_featured: bool
    is_premium: bool
    views_count: int
    favorites_count: int
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None
    
    # Relationships
    category: Optional[PropertyCategoryResponse] = None
    images: List[PropertyImageResponse] = []
    facilities: List[PropertyFacilityResponse] = []
    
    class Config:
        from_attributes = True

class PropertySummaryResponse(BaseModel):
    id: UUID
    title: str
    price: Decimal
    property_type: PropertyTypeEnum
    property_category: PropertyCategoryEnum
    city: Optional[str] = None
    bedrooms: Optional[int] = None
    use_area: Optional[float] = None
    primary_image: Optional[str] = None
    is_featured: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class PropertySearchParams(BaseModel):
    property_type: Optional[PropertyTypeEnum] = None
    property_category: Optional[PropertyCategoryEnum] = None
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
    city: Optional[str] = None
    bedrooms: Optional[int] = None
    min_area: Optional[float] = None
    max_area: Optional[float] = None
    keyword: Optional[str] = None
    page: int = 1
    size: int = 20
    sort_by: str = "created_at"
    sort_order: str = "desc"

class PropertyMessageBase(BaseModel):
    sender_name: str
    sender_email: EmailStr
    sender_phone: Optional[str] = None
    message: str

class PropertyMessageCreate(PropertyMessageBase):
    property_id: UUID

class PropertyMessageResponse(PropertyMessageBase):
    id: UUID
    property_id: UUID
    is_read: bool
    is_replied: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class PropertyComparisonCreate(BaseModel):
    property_ids: List[UUID]
    user_id: Optional[UUID] = None
    session_id: Optional[str] = None

class PropertyComparisonResponse(BaseModel):
    id: UUID
    properties: List[PropertyResponse]
    created_at: datetime
    
    class Config:
        from_attributes = True

class PropertyLoanEstimateRequest(BaseModel):
    property_id: UUID
    loan_amount: Decimal
    duration_months: int
    interest_rate: Optional[Decimal] = Decimal("3.5")  # Default interest rate
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class PropertyLoanEstimateResponse(BaseModel):
    property_id: UUID
    loan_amount: Decimal
    duration_months: int
    interest_rate: Decimal
    monthly_payment: Decimal
    total_payment: Decimal
    total_interest: Decimal
    
    class Config:
        from_attributes = True

class PopularCityResponse(BaseModel):
    id: int
    name: str
    state: Optional[str] = None
    country: str
    image_url: Optional[str] = None
    rental_count: int
    avg_price: Optional[Decimal] = None
    
    class Config:
        from_attributes = True

class RentalTipResponse(BaseModel):
    id: int
    title: str
    content: str
    tip_number: Optional[int] = None
    category: Optional[str] = None
    
    class Config:
        from_attributes = True

class FeedbackCreate(BaseModel):
    message: str
    page_url: Optional[str] = None
    email: Optional[EmailStr] = None
    rating: Optional[int] = None
    
    @validator('rating')
    def validate_rating(cls, v):
        if v is not None and (v < 1 or v > 5):
            raise ValueError('Rating must be between 1 and 5')
        return v

class FeedbackResponse(BaseModel):
    id: UUID
    message: str
    page_url: Optional[str] = None
    rating: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class PropertyPriceInsightResponse(BaseModel):
    city: str
    area: Optional[str] = None
    avg_price_per_sqm: Decimal
    currency: str
    period_description: str
    sample_size: int
    property_type: Optional[str] = None
    
    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int
    
# property-service/src/schemas/property_schemas.py (Additional schemas for points 6-10)
from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID

# Point 6: Property Map Location Schemas
class PropertyMapLocationBase(BaseModel):
    latitude: float
    longitude: float
    address_components: Optional[str] = None
    google_place_id: Optional[str] = None
    is_approximate: bool = False

class PropertyMapLocationCreate(PropertyMapLocationBase):
    property_id: UUID

class PropertyMapLocationResponse(PropertyMapLocationBase):
    id: UUID
    property_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

class PropertyMapSearchRequest(BaseModel):
    center_lat: float
    center_lng: float
    radius_km: float
    filters: Optional[Dict[str, Any]] = {}
    user_id: Optional[UUID] = None
    session_id: Optional[str] = None

class PropertyNearbyPlaceResponse(BaseModel):
    id: UUID
    place_name: str
    place_type: str
    distance_km: float
    
    class Config:
        from_attributes = True

# Point 7: Property Comparison Schemas
class PropertyComparisonSessionCreate(BaseModel):
    property_ids: List[UUID]
    comparison_name: Optional[str] = None
    user_id: Optional[UUID] = None
    session_id: Optional[str] = None

class PropertyComparisonItemResponse(BaseModel):
    id: UUID
    property_id: UUID
    sort_order: int
    is_favorite: bool
    user_rating: Optional[int] = None
    
    class Config:
        from_attributes = True

class PropertyComparisonNoteCreate(BaseModel):
    property_id: UUID
    note_text: str
    note_category: Optional[str] = None

class PropertyComparisonNoteResponse(BaseModel):
    id: UUID
    property_id: UUID
    note_text: str
    note_category: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class PropertyComparisonSessionResponse(BaseModel):
    id: UUID
    comparison_name: Optional[str] = None
    is_saved: bool
    created_at: datetime
    comparison_items: List[PropertyComparisonItemResponse] = []
    comparison_notes: List[PropertyComparisonNoteResponse] = []
    
    class Config:
        from_attributes = True

# Point 8: Property Loan Estimator Schemas
class PropertyLoanEstimateRequest(BaseModel):
    property_id: UUID
    property_price: Decimal
    down_payment: Decimal
    interest_rate: Decimal
    loan_term_years: int
    property_tax_monthly: Optional[Decimal] = None
    insurance_monthly: Optional[Decimal] = None
    hoa_fees_monthly: Optional[Decimal] = None
    user_id: Optional[UUID] = None
    session_id: Optional[str] = None

class PropertyLoanEstimateResponse(BaseModel):
    id: UUID
    property_id: UUID
    loan_amount: Decimal
    monthly_payment: Decimal
    total_payment: Decimal
    total_interest: Decimal
    total_monthly_cost: Optional[Decimal] = None
    calculation_date: datetime
    
    class Config:
        from_attributes = True

class LoanProviderResponse(BaseModel):
    id: int
    provider_name: str
    provider_type: str
    base_interest_rate: Decimal
    min_down_payment_percent: Decimal
    website_url: Optional[str] = None
    contact_phone: Optional[str] = None
    
    class Config:
        from_attributes = True

class PropertyLoanApplicationCreate(BaseModel):
    estimate_id: UUID
    provider_id: int
    applicant_name: str
    applicant_email: EmailStr
    applicant_phone: Optional[str] = None
    annual_income: Optional[Decimal] = None
    credit_score: Optional[int] = None
    employment_status: Optional[str] = None

class PropertyLoanApplicationResponse(BaseModel):
    id: UUID
    status: str
    application_date: datetime
    approved_amount: Optional[Decimal] = None
    approved_rate: Optional[Decimal] = None
    
    class Config:
        from_attributes = True

# Point 9: New Rental Ad Schemas
class RentalPropertyCreate(BaseModel):
    property_id: UUID
    monthly_rent: Decimal
    security_deposit: Decimal
    first_month_rent: Optional[Decimal] = None
    last_month_rent: Optional[Decimal] = None
    min_lease_duration_months: int = 12
    max_lease_duration_months: Optional[int] = None
    available_from: date
    lease_type: str = "fixed"
    pets_allowed: bool = False
    smoking_allowed: bool = False
    max_occupants: Optional[int] = None
    utilities_included: Optional[List[str]] = []
    parking_included: bool = False
    internet_included: bool = False
    minimum_income_multiple: Decimal = Decimal("3.0")
    credit_score_minimum: Optional[int] = None
    background_check_required: bool = True
    references_required: int = 2

class RentalPropertyResponse(BaseModel):
    id: UUID
    property_id: UUID
    monthly_rent: Decimal
    security_deposit: Decimal
    available_from: date
    lease_type: str
    pets_allowed: bool
    is_available: bool
    view_count: int
    inquiry_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class RentalApplicationCreate(BaseModel):
    rental_property_id: UUID
    desired_move_in_date: date
    lease_duration_months: int
    annual_income: Decimal
    employment_status: str
    employer_name: Optional[str] = None
    credit_score: Optional[int] = None
    previous_address: Optional[str] = None
    reason_for_moving: Optional[str] = None
    pets_description: Optional[str] = None
    special_requests: Optional[str] = None

class RentalApplicationResponse(BaseModel):
    id: UUID
    rental_property_id: UUID
    application_date: datetime
    desired_move_in_date: date
    status: str
    annual_income: Decimal
    employment_status: str
    
    class Config:
        from_attributes = True

# Point 10: Lease Contract Schemas
class LeaseContractCreate(BaseModel):
    rental_property_id: UUID
    application_id: Optional[UUID] = None
    tenant_id: UUID
    lease_start_date: date
    lease_end_date: date
    monthly_rent: Decimal
    security_deposit: Decimal
    lease_terms: str
    special_conditions: Optional[str] = None
    pets_clause: Optional[str] = None
    maintenance_responsibilities: Optional[str] = None

class LeaseContractTemplateResponse(BaseModel):
    id: int
    template_name: str
    template_type: str
    jurisdiction: str
    is_default: bool
    is_active: bool
    version: str
    approved_by_legal: bool
    
    class Config:
        from_attributes = True

class RentalSuggestionRequest(BaseModel):
    preferred_location: Optional[str] = None
    max_rent: Optional[Decimal] = None
    min_bedrooms: Optional[int] = None
    max_bedrooms: Optional[int] = None
    property_type: Optional[str] = None
    amenities_required: Optional[List[str]] = []
    user_id: Optional[UUID] = None
    session_id: Optional[str] = None

class RentalSuggestionResponse(BaseModel):
    id: UUID
    suggested_properties: List[UUID]
    suggestion_algorithm: Optional[str] = None
    suggestion_score: Optional[Decimal] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Authentication-related schemas
class AuthenticatedUser(BaseModel):
    user_id: UUID
    email: str
    is_verified: bool
    roles: List[str] = []

# Common response schemas
class SuccessResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    details: Optional[Dict[str, Any]] = None