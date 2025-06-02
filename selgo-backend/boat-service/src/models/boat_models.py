from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
import enum
from datetime import datetime

Base = declarative_base()

# Association table for many-to-many relationship between boats and features
boat_feature_association = Table(
    'boat_feature_association',
    Base.metadata,
    Column('boat_id', Integer, ForeignKey('boats.id'), primary_key=True),
    Column('feature_id', Integer, ForeignKey('boat_features.id'), primary_key=True)
)

# Enum for boat conditions
class BoatCondition(enum.Enum):
    NEW = "new"
    LIKE_NEW = "like_new"
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    PROJECT_BOAT = "project_boat"

# Enum for seller types
class SellerType(enum.Enum):
    PRIVATE = "private"
    DEALER = "dealer"
    MANUFACTURER = "manufacturer"

# Enum for ad types
class AdType(enum.Enum):
    FOR_SALE = "for_sale"
    FOR_RENT = "for_rent"
    WANTED = "wanted"

# Enum for fix request status
class FixRequestStatus(enum.Enum):
    REQUESTED = "requested"
    APPROVED = "approved"
    DECLINED = "declined"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class BoatCategory(Base):
    __tablename__ = 'boat_categories'

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(255), nullable=False)
    icon = Column(String(255))
    parent_id = Column(Integer, ForeignKey('boat_categories.id', ondelete='CASCADE'), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    children = relationship("BoatCategory", 
                           backref=backref('parent', remote_side=[id]),
                           cascade="all")  # Remove delete-orphan, or add single_parent=True
    boats = relationship("Boat", back_populates="category")
    
class BoatFeature(Base):
    __tablename__ = 'boat_features'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    boats = relationship("Boat", secondary=boat_feature_association, back_populates="features")

class Boat(Base):
    __tablename__ = 'boats'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('boat_categories.id'), nullable=False)
    boat_type = Column(String(100)) 
    condition = Column(Enum(BoatCondition), default=BoatCondition.GOOD)
    year = Column(Integer)
    make = Column(String(255))
    model = Column(String(255))
    length = Column(Float)  # Length in feet
    beam = Column(Float)    # Width in feet
    draft = Column(Float)   # Depth below waterline in feet
    fuel_type = Column(String(100))
    hull_material = Column(String(100))
    engine_make = Column(String(255))
    engine_model = Column(String(255))
    engine_hours = Column(Integer)
    engine_power = Column(Integer)  # Power in HP
    seller_type = Column(Enum(SellerType), default=SellerType.PRIVATE)
    ad_type = Column(Enum(AdType), default=AdType.FOR_SALE)
    is_featured = Column(Boolean, default=False)
    status = Column(String(50), default="active")
    location = Column(Geometry('POINT', srid=4326))
    location_name = Column(String(255))  # Human-readable location
    user_id = Column(Integer, nullable=False)  # User who posted the ad
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    category = relationship("BoatCategory", back_populates="boats")
    images = relationship("BoatImage", back_populates="boat", cascade="all, delete-orphan")
    features = relationship("BoatFeature", secondary=boat_feature_association, back_populates="boats")
    fix_requests = relationship("BoatFixDoneRequest", back_populates="boat", cascade="all, delete-orphan")
    ratings = relationship("BoatRating", back_populates="boat", cascade="all, delete-orphan")

class BoatImage(Base):
    __tablename__ = 'boat_images'
    
    id = Column(Integer, primary_key=True, index=True)
    boat_id = Column(Integer, ForeignKey('boats.id', ondelete='CASCADE'), nullable=False)
    image_url = Column(String(255), nullable=False)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    boat = relationship("Boat", back_populates="images")

class BoatRating(Base):
    __tablename__ = 'boat_ratings'
    
    id = Column(Integer, primary_key=True, index=True)
    boat_id = Column(Integer, ForeignKey('boats.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, nullable=False)
    stars = Column(Integer, nullable=False)  # 1-5 stars
    review = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    boat = relationship("Boat", back_populates="ratings")

class BoatFixDoneRequest(Base):
    __tablename__ = 'boat_fix_done_requests'
    
    id = Column(Integer, primary_key=True, index=True)
    boat_id = Column(Integer, ForeignKey('boats.id', ondelete='CASCADE'), nullable=False)
    buyer_id = Column(Integer, nullable=False)
    seller_id = Column(Integer, nullable=False)
    status = Column(Enum(FixRequestStatus), default=FixRequestStatus.REQUESTED)
    price = Column(Float, nullable=False)  # The agreed price
    message = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    boat = relationship("Boat", back_populates="fix_requests")
