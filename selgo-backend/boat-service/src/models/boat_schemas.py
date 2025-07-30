from pydantic import BaseModel, Field, validator, root_validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum
from .boat_models import BoatCondition, SellerType, AdType, FixRequestStatus

# Pydantic models (schemas) for request and response validation

# Category schemas
class BoatCategoryBase(BaseModel):
    label: str
    icon: Optional[str] = None
    parent_id: Optional[int] = None

class BoatCategoryCreate(BoatCategoryBase):
    pass

class BoatCategoryResponse(BoatCategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class BoatCategoryWithCountResponse(BoatCategoryResponse):
    count: int = 0

class BoatCategoryNestedResponse(BoatCategoryResponse):
    children: List['BoatCategoryNestedResponse'] = []
    
    class Config:
        orm_mode = True

# Feature schemas
class BoatFeatureBase(BaseModel):
    name: str

class BoatFeatureCreate(BoatFeatureBase):
    pass

class BoatFeatureResponse(BoatFeatureBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

# Image schemas
class BoatImageBase(BaseModel):
    image_url: str
    is_primary: bool = False

class BoatImageCreate(BoatImageBase):
    pass

class BoatImageResponse(BoatImageBase):
    id: int
    boat_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

# Rating schemas
class BoatRatingBase(BaseModel):
    stars: int = Field(..., ge=1, le=5)
    review: Optional[str] = None
    
    @validator('stars')
    def validate_stars(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Rating must be between 1 and 5 stars')
        return v

class BoatRatingCreate(BoatRatingBase):
    boat_id: int

class BoatRatingResponse(BoatRatingBase):
    id: int
    boat_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

# Fix Done Request schemas
class BoatFixDoneRequestBase(BaseModel):
    price: float
    message: Optional[str] = None

class BoatFixDoneRequestCreate(BoatFixDoneRequestBase):
    boat_id: int

class BoatFixDoneRequestResponse(BoatFixDoneRequestBase):
    id: int
    boat_id: int
    buyer_id: int
    seller_id: int
    status: FixRequestStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class BoatFixDoneRequestStatusUpdate(BaseModel):
    status: FixRequestStatus

# Boat schemas
class GeoPoint(BaseModel):
    latitude: float
    longitude: float

class BoatBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category_id: int
    boat_type: Optional[str] = None
    condition: Optional[BoatCondition] = None
    year: Optional[int] = None
    make: Optional[str] = None
    model: Optional[str] = None
    length: Optional[float] = None
    beam: Optional[float] = None
    draft: Optional[float] = None
    fuel_type: Optional[str] = None
    hull_material: Optional[str] = None
    engine_make: Optional[str] = None
    engine_model: Optional[str] = None
    engine_hours: Optional[int] = None
    engine_power: Optional[int] = None
    seller_type: Optional[SellerType] = None
    ad_type: Optional[AdType] = None
    is_featured: bool = False
    location_name: Optional[str] = None

class BoatCreate(BoatBase):
    location: Optional[GeoPoint] = None
    features: List[int] = []  # List of feature IDs
    images: List[BoatImageCreate] = []

class BoatUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    condition: Optional[BoatCondition] = None
    year: Optional[int] = None
    make: Optional[str] = None
    model: Optional[str] = None
    length: Optional[float] = None
    beam: Optional[float] = None
    draft: Optional[float] = None
    fuel_type: Optional[str] = None
    hull_material: Optional[str] = None
    engine_make: Optional[str] = None
    engine_model: Optional[str] = None
    engine_hours: Optional[int] = None
    engine_power: Optional[int] = None
    seller_type: Optional[SellerType] = None
    ad_type: Optional[AdType] = None
    is_featured: Optional[bool] = None
    location: Optional[GeoPoint] = None
    location_name: Optional[str] = None
    features: Optional[List[int]] = None  # List of feature IDs

class BoatResponse(BoatBase):
    id: int
    status: str
    user_id: int
    view_count: int
    created_at: datetime
    updated_at: datetime
    location: Optional[GeoPoint] = None
    category: BoatCategoryResponse
    images: List[BoatImageResponse] = []
    features: List[BoatFeatureResponse] = []
    
    class Config:
        orm_mode = True

class BoatListResponse(BaseModel):
    id: int
    title: str
    price: float
    location_name: Optional[str] = None
    year: Optional[int] = None
    make: Optional[str] = None
    model: Optional[str] = None
    length: Optional[float] = None
    created_at: datetime
    primary_image: Optional[str] = None
    
    class Config:
        orm_mode = True

class BoatDetailResponse(BoatResponse):
    fix_requests: List[BoatFixDoneRequestResponse] = []
    ratings: List[BoatRatingResponse] = []
    avg_rating: Optional[float] = None
    
    class Config:
        orm_mode = True

# Loan Estimation schemas
class LoanEstimateRequest(BaseModel):
    price: float
    duration: int = Field(..., description="Loan term in months")
    interest_rate: Optional[float] = None  # Annual interest rate, e.g., 5.5% = 5.5

class LoanEstimateResponse(BaseModel):
    monthly_payment: float
    total_interest: float
    total_payable: float
    breakdown: Dict[str, Any]  # Monthly breakdown

# Filter schemas
class BoatFilterParams(BaseModel):
    category_id: Optional[int] = None
    boat_type: Optional[str] = None  
    boat_types: Optional[List[str]] = None  # ✅ ADDED: Support for multiple boat types
    condition: Optional[BoatCondition] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    year_min: Optional[int] = None
    year_max: Optional[int] = None
    length_min: Optional[float] = None
    length_max: Optional[float] = None
    location: Optional[GeoPoint] = None
    distance: Optional[float] = None
    seller_type: Optional[SellerType] = None
    ad_type: Optional[AdType] = None
    features: Optional[List[int]] = None
    search_term: Optional[str] = None
    sort_by: Optional[str] = "created_at"
    sort_order: Optional[str] = "desc"
    limit: int = 10
    offset: int = 0

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    limit: int
    offset: int

# Favorite schemas
class UserFavoriteCreate(BaseModel):
    boat_id: int
    
class FavoriteBoatInfo(BaseModel):
    id: int
    title: str
    price: float
    location_name: Optional[str] = None
    year: Optional[int] = None
    make: Optional[str] = None
    model: Optional[str] = None
    length: Optional[float] = None
    created_at: str  # Use string instead of datetime for JSON compatibility
    primary_image: Optional[str] = None
    
class UserFavoriteSimple(BaseModel):
    id: int
    user_id: int
    boat_id: int
    created_at: str  # Use string instead of datetime for JSON compatibility
    boat: FavoriteBoatInfo

class UserFavoriteResponse(BaseModel):
    id: int
    user_id: int
    boat_id: int
    created_at: datetime
    boat: BoatListResponse
    
    class Config:
        orm_mode = True

class FavoriteToggleResponse(BaseModel):
    is_favorite: bool
    message: str

# Update the forward references
BoatCategoryNestedResponse.update_forward_refs()
