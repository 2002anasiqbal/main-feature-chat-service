# property-service/src/models.py
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey, DECIMAL, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
import uuid
from datetime import datetime
import enum

Base = declarative_base()

class PropertyTypeEnum(str, enum.Enum):
    PURCHASE = "purchase"
    RENT = "rent"
    SELL = "sell"
    NUTRITION = "nutrition"

class PropertyCategoryEnum(str, enum.Enum):
    PLOTS = "plots"
    RESIDENCE_ABROAD = "residence_abroad"
    HOUSING_SALE = "housing_sale"
    NEW_HOMES = "new_homes"
    VACATION_HOMES = "vacation_homes"
    LEISURE_PLOTS = "leisure_plots"

class PropertyStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    SOLD = "sold"
    RENTED = "rented"
    PENDING = "pending"
    INACTIVE = "inactive"

class PropertyOwnershipEnum(str, enum.Enum):
    OWNED = "owned"
    LEASED = "leased"
    SHARED = "shared"

class PropertyConditionEnum(str, enum.Enum):
    NEW = "new"
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    NEEDS_RENOVATION = "needs_renovation"

class PropertyCategory(Base):
    __tablename__ = "property_categories"
    
    id = Column(Integer, primary_key=True)
    label = Column(String(100), nullable=False)
    type = Column(Enum(PropertyTypeEnum), nullable=False)
    icon = Column(String(255), nullable=True)
    route = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    properties = relationship("Property", back_populates="category")

class Property(Base):
    __tablename__ = "properties"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(DECIMAL(12, 2), nullable=False)
    
    # Category and Type
    category_id = Column(Integer, ForeignKey("property_categories.id"))
    property_type = Column(Enum(PropertyTypeEnum), nullable=False)
    property_category = Column(Enum(PropertyCategoryEnum), nullable=False)
    status = Column(Enum(PropertyStatusEnum), default=PropertyStatusEnum.ACTIVE)
    
    # Property Details
    bedrooms = Column(Integer, nullable=True)
    bathrooms = Column(Integer, nullable=True)
    rooms = Column(Integer, nullable=True)
    use_area = Column(Float, nullable=True)  # in square meters
    plot_area = Column(Float, nullable=True)  # in square meters
    year_built = Column(Integer, nullable=True)
    
    # Property Type and Condition
    housing_type = Column(String(100), nullable=True)  # Detached house, Apartment, etc.
    ownership_form = Column(Enum(PropertyOwnershipEnum), nullable=True)
    condition = Column(Enum(PropertyConditionEnum), nullable=True)
    
    # Location
    address = Column(String(500), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    country = Column(String(100), default="Norway")
    location = Column(Geometry('POINT'), nullable=True)  # PostGIS point for lat/lng
    
    # Features and Amenities
    is_furnished = Column(Boolean, default=False)
    has_balcony = Column(Boolean, default=False)
    has_terrace = Column(Boolean, default=False)
    has_fireplace = Column(Boolean, default=False)
    has_parking = Column(Boolean, default=False)
    parking_spaces = Column(Integer, default=0)
    has_garden = Column(Boolean, default=False)
    has_basement = Column(Boolean, default=False)
    has_garage = Column(Boolean, default=False)
    
    # Energy and Utilities
    energy_rating = Column(String(5), nullable=True)  # A, B, C, D, E, F, G
    heating_type = Column(String(100), nullable=True)
    
    # Financial
    monthly_costs = Column(DECIMAL(10, 2), nullable=True)  # For rentals
    deposit_amount = Column(DECIMAL(10, 2), nullable=True)  # For rentals
    shared_costs = Column(DECIMAL(10, 2), nullable=True)
    property_tax = Column(DECIMAL(10, 2), nullable=True)
    
    # Seller/Owner Information
    owner_id = Column(UUID(as_uuid=True), nullable=False)  # Reference to user service
    owner_name = Column(String(255), nullable=True)
    owner_phone = Column(String(20), nullable=True)
    owner_email = Column(String(255), nullable=True)
    is_agent = Column(Boolean, default=False)
    agent_company = Column(String(255), nullable=True)
    
    # Marketing
    is_featured = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    views_count = Column(Integer, default=0)
    favorites_count = Column(Integer, default=0)
    featured_until = Column(DateTime, nullable=True)
    
    # SEO and Meta
    meta_title = Column(String(255), nullable=True)
    meta_description = Column(String(500), nullable=True)
    slug = Column(String(255), nullable=True, unique=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime, nullable=True)
    sold_at = Column(DateTime, nullable=True)
    
    # Relationships
    category = relationship("PropertyCategory", back_populates="properties")
    images = relationship("PropertyImage", back_populates="property", cascade="all, delete-orphan")
    facilities = relationship("PropertyFacility", back_populates="property", cascade="all, delete-orphan")
    messages = relationship("PropertyMessage", back_populates="property", cascade="all, delete-orphan")
    comparisons = relationship("PropertyComparison", back_populates="property", cascade="all, delete-orphan")
    loan_requests = relationship("PropertyLoanRequest", back_populates="property", cascade="all, delete-orphan")

class PropertyImage(Base):
    __tablename__ = "property_images"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"))
    image_url = Column(String(500), nullable=False)
    alt_text = Column(String(255), nullable=True)
    is_primary = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    property = relationship("Property", back_populates="images")

class Facility(Base):
    __tablename__ = "facilities"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    icon = Column(String(255), nullable=True)
    category = Column(String(50), nullable=True)  # indoor, outdoor, utility, etc.
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class PropertyFacility(Base):
    __tablename__ = "property_facilities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"))
    facility_id = Column(Integer, ForeignKey("facilities.id"))
    value = Column(String(255), nullable=True)  # For facilities that have values
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    property = relationship("Property", back_populates="facilities")
    facility = relationship("Facility")

class PropertyMessage(Base):
    __tablename__ = "property_messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"))
    sender_name = Column(String(255), nullable=False)
    sender_email = Column(String(255), nullable=False)
    sender_phone = Column(String(20), nullable=True)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    is_replied = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    property = relationship("Property", back_populates="messages")

class PropertyComparison(Base):
    __tablename__ = "property_comparisons"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=True)  # Can be null for anonymous users
    session_id = Column(String(255), nullable=True)  # For anonymous tracking
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    property = relationship("Property", back_populates="comparisons")

class PropertyLoanRequest(Base):
    __tablename__ = "property_loan_requests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), nullable=True)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    loan_amount = Column(DECIMAL(12, 2), nullable=False)
    duration_months = Column(Integer, nullable=False)
    interest_rate = Column(DECIMAL(5, 2), nullable=True)
    monthly_payment = Column(DECIMAL(10, 2), nullable=True)
    total_payment = Column(DECIMAL(12, 2), nullable=True)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    property = relationship("Property", back_populates="loan_requests")

class PopularCity(Base):
    __tablename__ = "popular_cities"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    state = Column(String(100), nullable=True)
    country = Column(String(100), default="Norway")
    image_url = Column(String(500), nullable=True)
    rental_count = Column(Integer, default=0)
    avg_price = Column(DECIMAL(10, 2), nullable=True)
    is_featured = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class RentalTip(Base):
    __tablename__ = "rental_tips"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    tip_number = Column(Integer, nullable=True)
    category = Column(String(50), nullable=True)  # renter, landlord, general
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    page_url = Column(String(500), nullable=True)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    email = Column(String(255), nullable=True)
    message = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)  # 1-5 stars
    is_processed = Column(Boolean, default=False)
    admin_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class PropertyPriceInsight(Base):
    __tablename__ = "property_price_insights"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city = Column(String(100), nullable=False)
    area = Column(String(100), nullable=True)
    avg_price_per_sqm = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(3), default="NOK")
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    sample_size = Column(Integer, nullable=False)  # Number of properties in calculation
    property_type = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Future-ready tables for advanced features

class PropertyView(Base):
    __tablename__ = "property_views"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), nullable=True)
    session_id = Column(String(255), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    viewed_at = Column(DateTime, default=datetime.utcnow)

class PropertyFavorite(Base):
    __tablename__ = "property_favorites"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class LeaseContract(Base):
    __tablename__ = "lease_contracts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id"))
    landlord_id = Column(UUID(as_uuid=True), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), nullable=True)
    contract_url = Column(String(500), nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    monthly_rent = Column(DECIMAL(10, 2), nullable=False)
    deposit_amount = Column(DECIMAL(10, 2), nullable=True)
    status = Column(String(50), default="draft")  # draft, active, expired, terminated
    created_at = Column(DateTime, default=datetime.utcnow)