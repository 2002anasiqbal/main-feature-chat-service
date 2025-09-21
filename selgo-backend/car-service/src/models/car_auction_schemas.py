# car-service/src/models/car_auction_schemas.py
from pydantic import BaseModel, validator, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal
from uuid import UUID
import enum

class AuctionStatus(str, enum.Enum):
    UPCOMING = "upcoming"
    ACTIVE = "active"
    ENDED = "ended"
    CANCELLED = "cancelled"
    SOLD = "sold"

class BidStatus(str, enum.Enum):
    ACTIVE = "active"
    OUTBID = "outbid"
    WINNING = "winning"
    WON = "won"
    LOST = "lost"

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"

# Car Auction Schemas
class CarAuctionBase(BaseModel):
    title: str
    description: Optional[str] = None
    starting_price: Decimal
    reserve_price: Optional[Decimal] = None
    bid_increment: Decimal = 100
    buy_now_price: Optional[Decimal] = None
    start_time: datetime
    end_time: datetime
    auto_extend_minutes: int = 5
    inspection_period_hours: int = 48
    payment_due_days: int = 7
    pickup_location: Optional[str] = None
    shipping_available: bool = False
    shipping_cost: Optional[Decimal] = None
    buyers_premium_percent: Decimal = 0
    documentation_fee: Decimal = 0
    seller_name: Optional[str] = None
    seller_location: Optional[str] = None

    @validator('starting_price')
    def validate_starting_price(cls, v):
        if v <= 0:
            raise ValueError('Starting price must be greater than 0')
        return v

    @validator('end_time')
    def validate_end_time(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('End time must be after start time')
        return v

    @validator('reserve_price')
    def validate_reserve_price(cls, v, values):
        if v is not None and 'starting_price' in values and v < values['starting_price']:
            raise ValueError('Reserve price cannot be less than starting price')
        return v

class CarAuctionCreate(CarAuctionBase):
    car_id: int

class CarAuctionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    reserve_price: Optional[Decimal] = None
    buy_now_price: Optional[Decimal] = None
    end_time: Optional[datetime] = None
    auto_extend_minutes: Optional[int] = None
    inspection_period_hours: Optional[int] = None
    payment_due_days: Optional[int] = None
    pickup_location: Optional[str] = None
    shipping_available: Optional[bool] = None
    shipping_cost: Optional[Decimal] = None
    buyers_premium_percent: Optional[Decimal] = None
    documentation_fee: Optional[Decimal] = None
    is_featured: Optional[bool] = None

class CarAuctionResponse(CarAuctionBase):
    id: UUID
    car_id: int
    seller_id: UUID
    current_bid: Decimal
    status: AuctionStatus
    is_featured: bool
    is_reserve_met: bool
    total_bids: int
    unique_bidders: int
    view_count: int
    watch_count: int
    winning_bidder_id: Optional[UUID]
    winning_bid: Optional[Decimal]
    sold_at: Optional[datetime]
    seller_rating: Optional[Decimal]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CarAuctionListResponse(BaseModel):
    auctions: List[CarAuctionResponse]
    total: int
    page: int
    per_page: int
    total_pages: int

# Bid Schemas
class CarAuctionBidBase(BaseModel):
    bid_amount: Decimal
    max_bid: Optional[Decimal] = None  # For proxy bidding

    @validator('bid_amount')
    def validate_bid_amount(cls, v):
        if v <= 0:
            raise ValueError('Bid amount must be greater than 0')
        return v

    @validator('max_bid')
    def validate_max_bid(cls, v, values):
        if v is not None and 'bid_amount' in values and v < values['bid_amount']:
            raise ValueError('Max bid cannot be less than current bid amount')
        return v

class CarAuctionBidCreate(CarAuctionBidBase):
    auction_id: UUID

class CarAuctionBidResponse(CarAuctionBidBase):
    id: UUID
    auction_id: UUID
    bidder_id: UUID
    is_proxy_bid: bool
    is_auto_bid: bool
    status: BidStatus
    is_winning: bool
    bidder_name: Optional[str]
    bidder_location: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CarAuctionBidListResponse(BaseModel):
    bids: List[CarAuctionBidResponse]
    total: int
    current_page: int
    per_page: int
    total_pages: int

# Watcher Schemas
class CarAuctionWatcherBase(BaseModel):
    notify_on_bid: bool = True
    notify_on_outbid: bool = True
    notify_before_end: bool = True
    notify_minutes_before: int = 30

class CarAuctionWatcherCreate(CarAuctionWatcherBase):
    auction_id: UUID

class CarAuctionWatcherResponse(CarAuctionWatcherBase):
    id: UUID
    auction_id: UUID
    user_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

# Image Schemas
class CarAuctionImageBase(BaseModel):
    image_url: str
    thumbnail_url: Optional[str] = None
    alt_text: Optional[str] = None
    sort_order: int = 0
    is_primary: bool = False

class CarAuctionImageCreate(CarAuctionImageBase):
    auction_id: UUID

class CarAuctionImageResponse(CarAuctionImageBase):
    id: UUID
    auction_id: UUID
    file_size: Optional[int]
    width: Optional[int]
    height: Optional[int]
    format: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Report Schemas
class CarAuctionReportBase(BaseModel):
    exterior_condition: Optional[str] = None
    interior_condition: Optional[str] = None
    mechanical_condition: Optional[str] = None
    tire_condition: Optional[str] = None
    has_accidents: bool = False
    accident_description: Optional[str] = None
    has_rust: bool = False
    rust_description: Optional[str] = None
    has_scratches: bool = False
    scratch_description: Optional[str] = None
    has_dents: bool = False
    dent_description: Optional[str] = None
    last_service_date: Optional[datetime] = None
    last_service_mileage: Optional[int] = None
    service_history_available: bool = False
    service_notes: Optional[str] = None
    seller_notes: Optional[str] = None
    inspector_notes: Optional[str] = None

class CarAuctionReportCreate(CarAuctionReportBase):
    auction_id: UUID

class CarAuctionReportResponse(CarAuctionReportBase):
    id: UUID
    auction_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Transaction Schemas
class CarAuctionTransactionBase(BaseModel):
    final_bid: Decimal
    buyers_premium: Decimal = 0
    documentation_fee: Decimal = 0
    shipping_cost: Decimal = 0
    total_amount: Decimal
    payment_method: Optional[str] = None
    pickup_location: Optional[str] = None
    buyer_notes: Optional[str] = None
    seller_notes: Optional[str] = None

class CarAuctionTransactionCreate(CarAuctionTransactionBase):
    auction_id: UUID
    buyer_id: UUID
    seller_id: UUID

class CarAuctionTransactionResponse(CarAuctionTransactionBase):
    id: UUID
    auction_id: UUID
    buyer_id: UUID
    seller_id: UUID
    payment_status: PaymentStatus
    payment_reference: Optional[str]
    paid_at: Optional[datetime]
    pickup_scheduled: bool
    pickup_date: Optional[datetime]
    is_shipped: bool
    tracking_number: Optional[str]
    delivered_at: Optional[datetime]
    is_completed: bool
    completion_date: Optional[datetime]
    admin_notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Search and Filter Schemas
class CarAuctionSearchFilters(BaseModel):
    status: Optional[List[AuctionStatus]] = None
    make: Optional[str] = None
    model: Optional[str] = None
    year_from: Optional[int] = None
    year_to: Optional[int] = None
    price_from: Optional[Decimal] = None
    price_to: Optional[Decimal] = None
    mileage_from: Optional[int] = None
    mileage_to: Optional[int] = None
    location: Optional[str] = None
    has_reserve: Optional[bool] = None
    has_buy_now: Optional[bool] = None
    ending_soon: Optional[bool] = None  # Ending within 24 hours
    no_reserve: Optional[bool] = None
    featured_only: Optional[bool] = None
    seller_type: Optional[str] = None

class CarAuctionSearchRequest(BaseModel):
    query: Optional[str] = None
    filters: Optional[CarAuctionSearchFilters] = None
    sort_by: Optional[str] = "end_time"
    sort_order: Optional[str] = "asc"
    page: int = 1
    per_page: int = 20

# Statistics Schemas
class CarAuctionStats(BaseModel):
    total_auctions: int
    active_auctions: int
    completed_auctions: int
    total_bids: int
    average_final_price: Decimal
    highest_sale: Decimal
    total_sales_volume: Decimal
    popular_makes: List[Dict[str, Any]]
    auction_success_rate: Decimal
    average_bidders_per_auction: Decimal

# Notification Schemas
class AuctionNotification(BaseModel):
    type: str  # bid_placed, outbid, auction_ending, auction_won, etc.
    auction_id: UUID
    message: str
    data: Optional[Dict[str, Any]] = None
    created_at: datetime

# Dashboard Schemas
class SellerDashboard(BaseModel):
    active_auctions: int
    completed_auctions: int
    total_sales: Decimal
    pending_payments: int
    average_sale_price: Decimal
    success_rate: Decimal
    recent_auctions: List[CarAuctionResponse]

class BidderDashboard(BaseModel):
    active_bids: int
    won_auctions: int
    watched_auctions: int
    total_spent: Decimal
    pending_payments: int
    recent_bids: List[CarAuctionBidResponse]
    watched_ending_soon: List[CarAuctionResponse]