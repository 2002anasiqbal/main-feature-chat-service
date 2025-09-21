# car-service/src/models/car_auction_models.py
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum, Text, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import enum
import uuid
from datetime import datetime

# Import Base from existing models
from .car_models import Base

class AuctionStatus(enum.Enum):
    UPCOMING = "upcoming"
    ACTIVE = "active"
    ENDED = "ended"
    CANCELLED = "cancelled"
    SOLD = "sold"

class BidStatus(enum.Enum):
    ACTIVE = "active"
    OUTBID = "outbid"
    WINNING = "winning"
    WON = "won"
    LOST = "lost"

class PaymentStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"

class CarAuction(Base):
    __tablename__ = 'car_auctions'
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    car_id = Column(Integer, ForeignKey('cars.id', ondelete='CASCADE'), nullable=False)
    seller_id = Column(UUID(as_uuid=True), nullable=False)  # User ID from auth service
    
    # Auction Details
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Pricing
    starting_price = Column(DECIMAL(12, 2), nullable=False)
    reserve_price = Column(DECIMAL(12, 2), nullable=True)  # Minimum price to sell
    current_bid = Column(DECIMAL(12, 2), default=0)
    bid_increment = Column(DECIMAL(8, 2), default=100)  # Minimum bid increment
    buy_now_price = Column(DECIMAL(12, 2), nullable=True)  # Optional buy-it-now price
    
    # Timing
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    auto_extend_minutes = Column(Integer, default=5)  # Auto-extend if bid in last X minutes
    
    # Status
    status = Column(Enum(AuctionStatus), default=AuctionStatus.UPCOMING)
    is_featured = Column(Boolean, default=False)
    is_reserve_met = Column(Boolean, default=False)
    
    # Statistics
    total_bids = Column(Integer, default=0)
    unique_bidders = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    watch_count = Column(Integer, default=0)
    
    # Winner Information
    winning_bidder_id = Column(UUID(as_uuid=True), nullable=True)
    winning_bid = Column(DECIMAL(12, 2), nullable=True)
    sold_at = Column(DateTime, nullable=True)
    
    # Seller Information
    seller_name = Column(String(255), nullable=True)
    seller_location = Column(String(255), nullable=True)
    seller_rating = Column(DECIMAL(3, 2), nullable=True)
    
    # Auction Terms
    inspection_period_hours = Column(Integer, default=48)  # Hours for inspection after winning
    payment_due_days = Column(Integer, default=7)  # Days to complete payment
    pickup_location = Column(String(500), nullable=True)
    shipping_available = Column(Boolean, default=False)
    shipping_cost = Column(DECIMAL(8, 2), nullable=True)
    
    # Additional Fees
    buyers_premium_percent = Column(DECIMAL(5, 2), default=0)  # Percentage fee for buyer
    documentation_fee = Column(DECIMAL(8, 2), default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    car = relationship("Car", backref="auctions")
    bids = relationship("CarAuctionBid", back_populates="auction", cascade="all, delete-orphan")
    watchers = relationship("CarAuctionWatcher", back_populates="auction", cascade="all, delete-orphan")

class CarAuctionBid(Base):
    __tablename__ = 'car_auction_bids'
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    auction_id = Column(UUID(as_uuid=True), ForeignKey('car_auctions.id', ondelete='CASCADE'), nullable=False)
    bidder_id = Column(UUID(as_uuid=True), nullable=False)  # User ID from auth service
    
    # Bid Details
    bid_amount = Column(DECIMAL(12, 2), nullable=False)
    max_bid = Column(DECIMAL(12, 2), nullable=True)  # For proxy bidding
    is_proxy_bid = Column(Boolean, default=False)
    is_auto_bid = Column(Boolean, default=False)  # System generated proxy bid
    
    # Status
    status = Column(Enum(BidStatus), default=BidStatus.ACTIVE)
    is_winning = Column(Boolean, default=False)
    
    # Bidder Information
    bidder_name = Column(String(255), nullable=True)
    bidder_location = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    auction = relationship("CarAuction", back_populates="bids")

class CarAuctionWatcher(Base):
    __tablename__ = 'car_auction_watchers'
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    auction_id = Column(UUID(as_uuid=True), ForeignKey('car_auctions.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)  # User ID from auth service
    
    # Notification Preferences
    notify_on_bid = Column(Boolean, default=True)
    notify_on_outbid = Column(Boolean, default=True)
    notify_before_end = Column(Boolean, default=True)
    notify_minutes_before = Column(Integer, default=30)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    auction = relationship("CarAuction", back_populates="watchers")

class CarAuctionImage(Base):
    __tablename__ = 'car_auction_images'
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    auction_id = Column(UUID(as_uuid=True), ForeignKey('car_auctions.id', ondelete='CASCADE'), nullable=False)
    
    # Image Details
    image_url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500), nullable=True)
    alt_text = Column(String(255), nullable=True)
    sort_order = Column(Integer, default=0)
    is_primary = Column(Boolean, default=False)
    
    # Image Metadata
    file_size = Column(Integer, nullable=True)  # in bytes
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    format = Column(String(10), nullable=True)  # jpg, png, etc.
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    auction = relationship("CarAuction", backref="images")

class CarAuctionReport(Base):
    __tablename__ = 'car_auction_reports'
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    auction_id = Column(UUID(as_uuid=True), ForeignKey('car_auctions.id', ondelete='CASCADE'), nullable=False)
    
    # Vehicle Condition Report
    exterior_condition = Column(String(20), nullable=True)  # excellent, good, fair, poor
    interior_condition = Column(String(20), nullable=True)
    mechanical_condition = Column(String(20), nullable=True)
    tire_condition = Column(String(20), nullable=True)
    
    # Damage Report
    has_accidents = Column(Boolean, default=False)
    accident_description = Column(Text, nullable=True)
    has_rust = Column(Boolean, default=False)
    rust_description = Column(Text, nullable=True)
    has_scratches = Column(Boolean, default=False)
    scratch_description = Column(Text, nullable=True)
    has_dents = Column(Boolean, default=False)
    dent_description = Column(Text, nullable=True)
    
    # Service History
    last_service_date = Column(DateTime, nullable=True)
    last_service_mileage = Column(Integer, nullable=True)
    service_history_available = Column(Boolean, default=False)
    service_notes = Column(Text, nullable=True)
    
    # Additional Notes
    seller_notes = Column(Text, nullable=True)
    inspector_notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    auction = relationship("CarAuction", backref="condition_report")

class CarAuctionTransaction(Base):
    __tablename__ = 'car_auction_transactions'
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    auction_id = Column(UUID(as_uuid=True), ForeignKey('car_auctions.id', ondelete='CASCADE'), nullable=False)
    buyer_id = Column(UUID(as_uuid=True), nullable=False)  # User ID from auth service
    seller_id = Column(UUID(as_uuid=True), nullable=False)  # User ID from auth service
    
    # Transaction Details
    final_bid = Column(DECIMAL(12, 2), nullable=False)
    buyers_premium = Column(DECIMAL(10, 2), default=0)
    documentation_fee = Column(DECIMAL(8, 2), default=0)
    shipping_cost = Column(DECIMAL(8, 2), default=0)
    total_amount = Column(DECIMAL(12, 2), nullable=False)
    
    # Payment Information
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    payment_method = Column(String(50), nullable=True)
    payment_reference = Column(String(100), nullable=True)
    paid_at = Column(DateTime, nullable=True)
    
    # Delivery Information
    pickup_scheduled = Column(Boolean, default=False)
    pickup_date = Column(DateTime, nullable=True)
    pickup_location = Column(String(500), nullable=True)
    is_shipped = Column(Boolean, default=False)
    tracking_number = Column(String(100), nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    
    # Transaction Status
    is_completed = Column(Boolean, default=False)
    completion_date = Column(DateTime, nullable=True)
    
    # Notes
    buyer_notes = Column(Text, nullable=True)
    seller_notes = Column(Text, nullable=True)
    admin_notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    auction = relationship("CarAuction", backref="transaction")