from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from .car_models import CarCondition, SellerType, AdType

# Pydantic models (schemas) for request and response validation

# Category schemas
class CarCategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class CarCategoryCreate(CarCategoryBase):
    pass

class CarCategoryResponse(CarCategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CarCategoryNestedResponse(CarCategoryResponse):
    children: List['CarCategoryNestedResponse'] = []

    class Config:
        orm_mode = True

# Feature schemas
class CarFeatureBase(BaseModel):
    name: str

class CarFeatureCreate(CarFeatureBase):
    pass

class CarFeatureResponse(CarFeatureBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Image schemas
class CarImageBase(BaseModel):
    image_url: str
    is_primary: bool = False

class CarImageCreate(CarImageBase):
    pass

class CarImageResponse(CarImageBase):
    id: int
    car_id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Rating schemas
class CarRatingBase(BaseModel):
    stars: int = Field(..., ge=1, le=5)
    review: Optional[str] = None

    @validator('stars')
    def validate_stars(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Rating must be between 1 and 5 stars')
        return v

class CarRatingCreate(CarRatingBase):
    car_id: int

class CarRatingResponse(CarRatingBase):
    id: int
    car_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Car schemas
class GeoPoint(BaseModel):
    latitude: float
    longitude: float

class CarBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category_id: int
    condition: Optional[CarCondition] = None
    year: Optional[int] = None
    make: Optional[str] = None
    model: Optional[str] = None
    mileage: Optional[int] = None
    fuel_type: Optional[str] = None
    transmission: Optional[str] = None
    engine_size: Optional[float] = None
    color: Optional[str] = None
    body_type: Optional[str] = None
    seller_type: Optional[SellerType] = None
    ad_type: Optional[AdType] = None
    is_featured: bool = False
    location_name: Optional[str] = None

class CarCreate(CarBase):
    location: Optional[GeoPoint] = None
    features: List[int] = []  # List of feature IDs
    images: List[CarImageCreate] = []

class CarUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    condition: Optional[CarCondition] = None
    year: Optional[int] = None
    make: Optional[str] = None
    model: Optional[str] = None
    mileage: Optional[int] = None
    fuel_type: Optional[str] = None
    transmission: Optional[str] = None
    engine_size: Optional[float] = None
    color: Optional[str] = None
    body_type: Optional[str] = None
    seller_type: Optional[SellerType] = None
    ad_type: Optional[AdType] = None
    is_featured: Optional[bool] = None
    location: Optional[GeoPoint] = None
    location_name: Optional[str] = None
    features: Optional[List[int]] = None  # List of feature IDs

class CarResponse(CarBase):
    id: int
    status: str
    user_id: int
    view_count: int
    created_at: datetime
    updated_at: datetime
    location: Optional[GeoPoint] = None
    category: CarCategoryResponse
    images: List[CarImageResponse] = []
    features: List[CarFeatureResponse] = []

    class Config:
        orm_mode = True

class CarListResponse(BaseModel):
    id: int
    title: str
    price: float
    location_name: Optional[str] = None
    year: Optional[int] = None
    make: Optional[str] = None
    model: Optional[str] = None
    mileage: Optional[int] = None
    created_at: datetime
    primary_image: Optional[str] = None

    class Config:
        orm_mode = True

class CarDetailResponse(CarResponse):
    ratings: List[CarRatingResponse] = []
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
class CarFilterParams(BaseModel):
    category_id: Optional[int] = None
    condition: Optional[CarCondition] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    year_min: Optional[int] = None
    year_max: Optional[int] = None
    mileage_min: Optional[int] = None
    mileage_max: Optional[int] = None
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
    car_id: int

class UserFavoriteResponse(BaseModel):
    id: int
    user_id: int
    car_id: int
    created_at: datetime
    car: CarListResponse

    class Config:
        orm_mode = True

class FavoriteToggleResponse(BaseModel):
    is_favorite: bool
    message: str

# Update the forward references
CarCategoryNestedResponse.update_forward_refs()
