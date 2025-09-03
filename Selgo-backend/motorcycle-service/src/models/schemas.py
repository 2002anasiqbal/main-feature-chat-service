# selgo-backend/motorcycle-service/src/models/schemas.py

from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum

class MotorcycleType(str, Enum):
    ADVENTURE = "adventure"
    NAKNE = "nakne"
    TOURING = "touring"
    SPORTS = "sports"
    CRUISER = "cruiser"
    SCOOTER = "scooter"

class ConditionEnum(str, Enum):
    NEW = "new"
    LIKE_NEW = "like_new"
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    PROJECT_BIKE = "project_bike"

class SellerTypeEnum(str, Enum):
    PRIVATE = "private"
    DEALER = "dealer"

# Add SellerInfo schema for external user data
class SellerInfo(BaseModel):
    id: int
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Base schemas
class MotorcycleCategoryBase(BaseModel):
    name: str
    slug: str
    icon: Optional[str] = None
    description: Optional[str] = None

class MotorcycleCategoryCreate(MotorcycleCategoryBase):
    pass

class MotorcycleCategory(MotorcycleCategoryBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class MotorcycleImageBase(BaseModel):
    image_url: str
    is_primary: bool = False
    alt_text: Optional[str] = None

class MotorcycleImageCreate(MotorcycleImageBase):
    pass

class MotorcycleImage(MotorcycleImageBase):
    id: int
    motorcycle_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class MotorcycleBase(BaseModel):
    title: str
    description: Optional[str] = None
    brand: str
    model: str
    year: int
    engine_size: Optional[int] = None
    mileage: Optional[int] = None
    price: Decimal
    condition: ConditionEnum
    motorcycle_type: MotorcycleType
    seller_type: SellerTypeEnum = SellerTypeEnum.PRIVATE
    city: Optional[str] = None
    address: Optional[str] = None
    netbill: bool = False

class MotorcycleCreate(MotorcycleBase):
    category_id: int
    seller_id: int
    images: Optional[List[MotorcycleImageCreate]] = []

class MotorcycleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    engine_size: Optional[int] = None
    mileage: Optional[int] = None
    price: Optional[Decimal] = None
    condition: Optional[ConditionEnum] = None
    motorcycle_type: Optional[MotorcycleType] = None
    seller_type: Optional[SellerTypeEnum] = None
    city: Optional[str] = None
    address: Optional[str] = None
    netbill: Optional[bool] = None
    is_featured: Optional[bool] = None

class Motorcycle(MotorcycleBase):
    id: int
    category_id: int
    seller_id: int
    is_active: bool
    is_featured: bool
    views_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    category: Optional[MotorcycleCategory] = None
    seller: Optional[SellerInfo] = None
    images: List[MotorcycleImage] = []
    
    class Config:
        from_attributes = True

class MotorcycleListResponse(BaseModel):
    id: int
    title: str
    brand: str
    model: str
    year: int
    price: Decimal
    condition: ConditionEnum
    motorcycle_type: MotorcycleType
    city: Optional[str] = None
    is_featured: bool
    views_count: int
    created_at: datetime
    primary_image: Optional[str] = None
    
    class Config:
        from_attributes = True

class MotorcycleSearchFilters(BaseModel):
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    motorcycle_type: Optional[MotorcycleType] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    city: Optional[str] = None
    condition: Optional[ConditionEnum] = None
    seller_type: Optional[SellerTypeEnum] = None
    price_min: Optional[Decimal] = None
    price_max: Optional[Decimal] = None
    year_min: Optional[int] = None
    year_max: Optional[int] = None
    mileage_min: Optional[int] = None
    mileage_max: Optional[int] = None
    engine_size_min: Optional[int] = None
    engine_size_max: Optional[int] = None
    search_term: Optional[str] = None

class MapFilterRequest(BaseModel):
    latitude: float
    longitude: float
    radius_km: int = 50
    filters: Optional[MotorcycleSearchFilters] = None

class LoanCalculationRequest(BaseModel):
    price: Decimal
    term_months: int = 36
    interest_rate: Optional[Decimal] = None

class LoanCalculationResponse(BaseModel):
    price: Decimal
    term_months: int
    interest_rate: Decimal
    monthly_payment: Decimal
    total_amount: Decimal
    total_interest: Decimal

class PaginatedResponse(BaseModel):
    items: List[MotorcycleListResponse]
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool
    
class UserFavoriteMotorcycleCreate(BaseModel):
    motorcycle_id: int

class FavoriteMotorcycleInfo(BaseModel):
    id: int
    title: str
    brand: str
    model: str
    year: int
    price: Decimal
    city: Optional[str] = None
    motorcycle_type: MotorcycleType
    condition: ConditionEnum
    created_at: str  # Use string for JSON compatibility
    primary_image: Optional[str] = None

class UserFavoriteMotorcycleResponse(BaseModel):
    id: int
    user_id: int
    motorcycle_id: int
    created_at: str  # Use string for JSON compatibility
    motorcycle: FavoriteMotorcycleInfo

class FavoriteToggleResponse(BaseModel):
    is_favorite: bool
    message: str