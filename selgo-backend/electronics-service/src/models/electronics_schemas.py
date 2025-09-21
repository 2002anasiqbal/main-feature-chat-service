from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from .electronics_models import ElectronicsCategory, ElectronicsCondition, ListingStatus
import json

# Base schemas
class ElectronicsImageBase(BaseModel):
    image_url: str
    alt_text: Optional[str] = None
    is_primary: bool = False
    display_order: int = 0

class ElectronicsImageCreate(ElectronicsImageBase):
    pass

class ElectronicsImage(ElectronicsImageBase):
    id: int
    electronics_listing_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class ElectronicsFeatureBase(BaseModel):
    feature_name: str
    feature_value: Optional[str] = None
    is_highlight: bool = False

class ElectronicsFeatureCreate(ElectronicsFeatureBase):
    pass

class ElectronicsFeature(ElectronicsFeatureBase):
    id: int
    electronics_listing_id: int
    
    class Config:
        orm_mode = True

# Main listing schemas
class ElectronicsListingBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=255)
    description: Optional[str] = None
    category: ElectronicsCategory
    subcategory: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = Field(None, ge=1900, le=2030)
    condition: ElectronicsCondition
    price: float = Field(..., gt=0)
    currency: str = "NOK"
    is_negotiable: bool = True
    original_price: Optional[float] = Field(None, gt=0)
    location: str = Field(..., min_length=2, max_length=255)
    postal_code: Optional[str] = None
    specifications: Optional[str] = None
    warranty_remaining: Optional[str] = None
    includes_original_box: bool = False
    includes_accessories: Optional[str] = None
    reason_for_selling: Optional[str] = None
    pickup_available: bool = True
    shipping_available: bool = False
    shipping_cost: Optional[float] = Field(None, ge=0)

    @validator('specifications')
    def validate_specifications(cls, v):
        if v:
            try:
                json.loads(v)
            except json.JSONDecodeError:
                raise ValueError('Specifications must be valid JSON')
        return v

class ElectronicsListingCreate(ElectronicsListingBase):
    images: Optional[List[ElectronicsImageCreate]] = []
    features: Optional[List[ElectronicsFeatureCreate]] = []

class ElectronicsListingUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=255)
    description: Optional[str] = None
    category: Optional[ElectronicsCategory] = None
    subcategory: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = Field(None, ge=1900, le=2030)
    condition: Optional[ElectronicsCondition] = None
    price: Optional[float] = Field(None, gt=0)
    is_negotiable: Optional[bool] = None
    original_price: Optional[float] = Field(None, gt=0)
    location: Optional[str] = Field(None, min_length=2, max_length=255)
    postal_code: Optional[str] = None
    specifications: Optional[str] = None
    warranty_remaining: Optional[str] = None
    includes_original_box: Optional[bool] = None
    includes_accessories: Optional[str] = None
    reason_for_selling: Optional[str] = None
    pickup_available: Optional[bool] = None
    shipping_available: Optional[bool] = None
    shipping_cost: Optional[float] = Field(None, ge=0)

    @validator('specifications')
    def validate_specifications(cls, v):
        if v:
            try:
                json.loads(v)
            except json.JSONDecodeError:
                raise ValueError('Specifications must be valid JSON')
        return v

class ElectronicsListing(ElectronicsListingBase):
    id: int
    user_id: int
    status: ListingStatus
    is_active: bool
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime] = None
    images: List[ElectronicsImage] = []
    features: List[ElectronicsFeature] = []
    
    class Config:
        orm_mode = True

# Search and filter schemas
class ElectronicsSearchParams(BaseModel):
    category: Optional[ElectronicsCategory] = None
    brand: Optional[str] = None
    condition: Optional[ElectronicsCondition] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    location: Optional[str] = None
    year_from: Optional[int] = Field(None, ge=1900)
    year_to: Optional[int] = Field(None, le=2030)
    search_query: Optional[str] = None
    has_warranty: Optional[bool] = None
    includes_box: Optional[bool] = None
    shipping_available: Optional[bool] = None
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=100)
    sort_by: Optional[str] = Field("created_at", regex="^(created_at|price|year|title)$")
    sort_order: Optional[str] = Field("desc", regex="^(asc|desc)$")

    @validator('max_price')
    def validate_price_range(cls, v, values):
        if v is not None and 'min_price' in values and values['min_price'] is not None:
            if v < values['min_price']:
                raise ValueError('max_price must be greater than or equal to min_price')
        return v

    @validator('year_to')
    def validate_year_range(cls, v, values):
        if v is not None and 'year_from' in values and values['year_from'] is not None:
            if v < values['year_from']:
                raise ValueError('year_to must be greater than or equal to year_from')
        return v

# Response schemas
class ElectronicsListResponse(BaseModel):
    items: List[ElectronicsListing]
    total: int
    page: int
    limit: int
    total_pages: int

class ElectronicsStatsResponse(BaseModel):
    total_listings: int
    active_listings: int
    sold_listings: int
    total_value: float
    average_price: float
    currency: str = "NOK"

# Category info schema
class CategoryInfo(BaseModel):
    value: str
    label: str
    subcategories: Optional[List[str]] = []