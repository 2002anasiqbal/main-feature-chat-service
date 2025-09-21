from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum, Table, Text, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
import enum
from datetime import datetime

Base = declarative_base()

class ItemCondition(enum.Enum):
    NEW = "new"
    USED = "used"

class SellerType(enum.Enum):
    PRIVATE = "private"
    DEALER = "dealer"

class AdType(enum.Enum):
    FOR_SALE = "for_sale"
    WANTED = "wanted"
    GIVEAWAY = "giveaway"

class ItemCategory(Base):
    __tablename__ = 'item_categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    parent_id = Column(Integer, ForeignKey('item_categories.id', ondelete='CASCADE'), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    children = relationship("ItemCategory", backref=backref('parent', remote_side=[id]), cascade="all, delete-orphan")
    items = relationship("Item", back_populates="category")

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('item_categories.id'), nullable=False)
    condition = Column(Enum(ItemCondition), default=ItemCondition.USED)
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

    category = relationship("ItemCategory", back_populates="items")
    images = relationship("ItemImage", back_populates="item", cascade="all, delete-orphan")
    ratings = relationship("ItemRating", back_populates="item", cascade="all, delete-orphan")

class ItemImage(Base):
    __tablename__ = 'item_images'

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey('items.id', ondelete='CASCADE'), nullable=False)
    image_url = Column(String(255), nullable=False)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

    item = relationship("Item", back_populates="images")

class ItemRating(Base):
    __tablename__ = 'item_ratings'

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey('items.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, nullable=False)
    stars = Column(Integer, nullable=False)
    review = Column(Text)
    created_at = Column(DateTime, default=func.now())

    item = relationship("Item", back_populates="ratings")

class UserFavorite(Base):
    __tablename__ = 'user_favorites'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    item_id = Column(Integer, ForeignKey('items.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=func.now())

    item = relationship("Item", backref="favorited_by")

    __table_args__ = (
        Index('idx_user_item_unique', 'user_id', 'item_id', unique=True),
    )