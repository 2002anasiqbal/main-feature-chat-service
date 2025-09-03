from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum, Table, Text, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
import enum
from datetime import datetime

Base = declarative_base()

# Association table for many-to-many relationship between cars and features
car_feature_association = Table(
    'car_feature_association',
    Base.metadata,
    Column('car_id', Integer, ForeignKey('cars.id'), primary_key=True),
    Column('feature_id', Integer, ForeignKey('car_features.id'), primary_key=True)
)

# Enum for car conditions
class CarCondition(enum.Enum):
    NEW = "new"
    USED = "used"

# Enum for seller types
class SellerType(enum.Enum):
    PRIVATE = "private"
    DEALER = "dealer"

# Enum for ad types
class AdType(enum.Enum):
    FOR_SALE = "for_sale"
    WANTED = "wanted"

class CarCategory(Base):
    __tablename__ = 'car_categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    parent_id = Column(Integer, ForeignKey('car_categories.id', ondelete='CASCADE'), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    children = relationship("CarCategory", backref=backref('parent', remote_side=[id]), cascade="all, delete-orphan")
    cars = relationship("Car", back_populates="category")

class CarFeature(Base):
    __tablename__ = 'car_features'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    cars = relationship("Car", secondary=car_feature_association, back_populates="features")

class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('car_categories.id'), nullable=False)
    condition = Column(Enum(CarCondition), default=CarCondition.USED)
    year = Column(Integer)
    make = Column(String(255))
    model = Column(String(255))
    mileage = Column(Integer)
    fuel_type = Column(String(100))
    transmission = Column(String(100))
    engine_size = Column(Float)
    color = Column(String(100))
    body_type = Column(String(100))
    seller_type = Column(Enum(SellerType), default=SellerType.PRIVATE)
    ad_type = Column(Enum(AdType), default=AdType.FOR_SALE)
    is_featured = Column(Boolean, default=False)
    status = Column(String(50), default="active")
    location = Column(Geometry('POINT', srid=4326))
    location_name = Column(String(255))
    user_id = Column(Integer, nullable=False)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    category = relationship("CarCategory", back_populates="cars")
    images = relationship("CarImage", back_populates="car", cascade="all, delete-orphan")
    features = relationship("CarFeature", secondary=car_feature_association, back_populates="cars")
    ratings = relationship("CarRating", back_populates="car", cascade="all, delete-orphan")

class CarImage(Base):
    __tablename__ = 'car_images'

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey('cars.id', ondelete='CASCADE'), nullable=False)
    image_url = Column(String(255), nullable=False)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

    car = relationship("Car", back_populates="images")

class CarRating(Base):
    __tablename__ = 'car_ratings'

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey('cars.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, nullable=False)
    stars = Column(Integer, nullable=False)  # 1-5 stars
    review = Column(Text)
    created_at = Column(DateTime, default=func.now())

    car = relationship("Car", back_populates="ratings")

class UserFavorite(Base):
    __tablename__ = 'user_favorites'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    car_id = Column(Integer, ForeignKey('cars.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=func.now())

    car = relationship("Car", backref="favorited_by")

    __table_args__ = (
        Index('idx_user_car_unique', 'user_id', 'car_id', unique=True),
    )