from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from .item_models import ItemCondition, SellerType, AdType

class GeoPoint(BaseModel):
    latitude: float
    longitude: float

class ItemCategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class ItemCategoryCreate(ItemCategoryBase):
    pass

class ItemCategoryResponse(ItemCategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ItemCategoryNestedResponse(ItemCategoryResponse):
    children: List['ItemCategoryNestedResponse'] = []

    class Config:
        orm_mode = True

class ItemImageBase(BaseModel):
    image_url: str
    is_primary: bool = False

class ItemImageCreate(ItemImageBase):
    pass

class ItemImageResponse(ItemImageBase):
    id: int
    item_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ItemRatingBase(BaseModel):
    stars: int = Field(..., ge=1, le=5)
    review: Optional[str] = None

    @validator('stars')
    def validate_stars(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Rating must be between 1 and 5 stars')
        return v

class ItemRatingCreate(ItemRatingBase):
    item_id: int

class ItemRatingResponse(ItemRatingBase):
    id: int
    item_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category_id: int
    condition: Optional[ItemCondition] = None
    seller_type: Optional[SellerType] = None
    ad_type: Optional[AdType] = None
    is_featured: bool = False
    location_name: Optional[str] = None

class ItemCreate(ItemBase):
    location: Optional[GeoPoint] = None
    images: List[ItemImageCreate] = []

class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    condition: Optional[ItemCondition] = None
    seller_type: Optional[SellerType] = None
    ad_type: Optional[AdType] = None
    is_featured: Optional[bool] = None
    location: Optional[GeoPoint] = None
    location_name: Optional[str] = None

class ItemResponse(ItemBase):
    id: int
    status: str
    user_id: int
    view_count: int
    created_at: datetime
    updated_at: datetime
    location: Optional[GeoPoint] = None
    category: ItemCategoryResponse
    images: List[ItemImageResponse] = []

    class Config:
        orm_mode = True

class ItemListResponse(BaseModel):
    id: int
    title: str
    price: float
    location_name: Optional[str] = None
    created_at: datetime
    primary_image: Optional[str] = None

    class Config:
        orm_mode = True

class ItemDetailResponse(ItemResponse):
    ratings: List[ItemRatingResponse] = []
    avg_rating: Optional[float] = None

    class Config:
        orm_mode = True

class ItemFilterParams(BaseModel):
    category_id: Optional[int] = None
    condition: Optional[ItemCondition] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    location: Optional[GeoPoint] = None
    distance: Optional[float] = None
    seller_type: Optional[SellerType] = None
    ad_type: Optional[AdType] = None
    search_term: Optional[str] = None
    sort_by: Optional[str] = "created_at"
    sort_order: Optional[str] = "desc"
    limit: int = 10
    offset: int = 0

class PaginatedResponse(BaseModel):
    items: List[ItemListResponse]
    total: int
    limit: int
    offset: int

class UserFavoriteCreate(BaseModel):
    item_id: int

class UserFavoriteResponse(BaseModel):
    id: int
    user_id: int
    item_id: int
    created_at: datetime
    item: ItemListResponse

    class Config:
        orm_mode = True

class FavoriteToggleResponse(BaseModel):
    is_favorite: bool
    message: str

ItemCategoryNestedResponse.update_forward_refs()
