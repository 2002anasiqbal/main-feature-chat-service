# selgo-backend/motorcycle-service/src/models.py
from sqlalchemy import Column, Integer, String, Text, DECIMAL, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
import enum

Base = declarative_base()

# Define Python enums
class MotorcycleType(enum.Enum):
    ADVENTURE = "adventure"
    NAKNE = "nakne"
    TOURING = "touring"
    SPORTS = "sports"
    CRUISER = "cruiser"
    SCOOTER = "scooter"

class ConditionEnum(enum.Enum):
    NEW = "new"
    LIKE_NEW = "like_new"
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    PROJECT_BIKE = "project_bike"

class SellerTypeEnum(enum.Enum):
    PRIVATE = "private"
    DEALER = "dealer"

class MotorcycleCategory(Base):
    __tablename__ = "motorcycle_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    icon = Column(String(255))
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    motorcycles = relationship("Motorcycle", back_populates="category")


class Motorcycle(Base):
    __tablename__ = "motorcycles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    engine_size = Column(Integer)  # CC
    mileage = Column(Integer)  # KM
    price = Column(DECIMAL(10, 2), nullable=False)
    
    # Use String instead of ENUM for now to avoid enum issues
    condition = Column(String(50), nullable=False)
    motorcycle_type = Column(String(50), nullable=False) 
    seller_type = Column(String(50), default='private')
    
    # Location
    city = Column(String(100))
    address = Column(String(255))
    location = Column(Geometry('POINT'))
    
    # Additional fields
    netbill = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    views_count = Column(Integer, default=0)
    
    # Relationships
    category_id = Column(Integer, ForeignKey("motorcycle_categories.id"))
    seller_id = Column(Integer)  # References user in auth service - NO foreign key
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    category = relationship("MotorcycleCategory", back_populates="motorcycles")
    images = relationship("MotorcycleImage", back_populates="motorcycle", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="motorcycle")
    
    # NO seller relationship - will be fetched from auth service

class MotorcycleImage(Base):
    __tablename__ = "motorcycle_images"
    
    id = Column(Integer, primary_key=True, index=True)
    motorcycle_id = Column(Integer, ForeignKey("motorcycles.id"))
    image_url = Column(String(500), nullable=False)
    is_primary = Column(Boolean, default=False)
    alt_text = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    motorcycle = relationship("Motorcycle", back_populates="images")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer)  # References user in auth service
    receiver_id = Column(Integer)  # References user in auth service
    motorcycle_id = Column(Integer, ForeignKey("motorcycles.id"))
    
    subject = Column(String(200))
    content = Column(Text, nullable=False)
    phone = Column(String(20))
    email = Column(String(255))
    
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    motorcycle = relationship("Motorcycle", back_populates="messages")

class LoanOffer(Base):
    __tablename__ = "loan_offers"
    
    id = Column(Integer, primary_key=True, index=True)
    motorcycle_id = Column(Integer, ForeignKey("motorcycles.id"))
    price = Column(DECIMAL(10, 2), nullable=False)
    term_months = Column(Integer, nullable=False)
    interest_rate = Column(DECIMAL(5, 2), nullable=False)
    monthly_payment = Column(DECIMAL(10, 2), nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())