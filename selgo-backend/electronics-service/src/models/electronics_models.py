from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class ElectronicsCategory(enum.Enum):
    SMARTPHONES = "smartphones"
    LAPTOPS = "laptops"
    TABLETS = "tablets"
    DESKTOP_COMPUTERS = "desktop_computers"
    GAMING = "gaming"
    AUDIO = "audio"
    TV_VIDEO = "tv_video"
    CAMERAS = "cameras"
    SMART_HOME = "smart_home"
    WEARABLES = "wearables"
    ACCESSORIES = "accessories"
    COMPONENTS = "components"

class ElectronicsCondition(enum.Enum):
    NEW = "new"
    LIKE_NEW = "like_new"
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    FOR_PARTS = "for_parts"

class ListingStatus(enum.Enum):
    ACTIVE = "active"
    SOLD = "sold"
    RESERVED = "reserved"
    EXPIRED = "expired"
    REMOVED = "removed"

class ElectronicsListing(Base):
    __tablename__ = "electronics_listings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Basic information
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    category = Column(Enum(ElectronicsCategory), nullable=False, index=True)
    subcategory = Column(String(100), index=True)
    
    # Product details
    brand = Column(String(100), index=True)
    model = Column(String(100), index=True)
    year = Column(Integer, index=True)
    condition = Column(Enum(ElectronicsCondition), nullable=False, index=True)
    
    # Pricing
    price = Column(Float, nullable=False, index=True)
    currency = Column(String(3), default="NOK")
    is_negotiable = Column(Boolean, default=True)
    original_price = Column(Float)
    
    # Location
    location = Column(String(255), nullable=False, index=True)
    postal_code = Column(String(20), index=True)
    
    # Technical specifications (JSON-like text field)
    specifications = Column(Text)  # Store as JSON string
    
    # Status and metadata
    status = Column(Enum(ListingStatus), default=ListingStatus.ACTIVE, index=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    expires_at = Column(DateTime)
    
    # Additional details
    warranty_remaining = Column(String(100))
    includes_original_box = Column(Boolean, default=False)
    includes_accessories = Column(Text)
    reason_for_selling = Column(Text)
    
    # Delivery options
    pickup_available = Column(Boolean, default=True)
    shipping_available = Column(Boolean, default=False)
    shipping_cost = Column(Float)
    
    # Relationships
    images = relationship("ElectronicsImage", back_populates="electronics_listing", cascade="all, delete-orphan")
    features = relationship("ElectronicsFeature", back_populates="electronics_listing", cascade="all, delete-orphan")

class ElectronicsImage(Base):
    __tablename__ = "electronics_images"
    
    id = Column(Integer, primary_key=True, index=True)
    electronics_listing_id = Column(Integer, ForeignKey("electronics_listings.id"), nullable=False)
    image_url = Column(String(500), nullable=False)
    alt_text = Column(String(255))
    is_primary = Column(Boolean, default=False)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    electronics_listing = relationship("ElectronicsListing", back_populates="images")

class ElectronicsFeature(Base):
    __tablename__ = "electronics_features"
    
    id = Column(Integer, primary_key=True, index=True)
    electronics_listing_id = Column(Integer, ForeignKey("electronics_listings.id"), nullable=False)
    feature_name = Column(String(100), nullable=False)
    feature_value = Column(String(255))
    is_highlight = Column(Boolean, default=False)
    
    # Relationships
    electronics_listing = relationship("ElectronicsListing", back_populates="features")