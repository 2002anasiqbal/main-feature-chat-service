# property-service/src/models/map_models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
import uuid
from datetime import datetime

from .models import Base

class PropertyMapLocation(Base):
    __tablename__ = "property_map_locations"
    __table_args__ = {'extend_existing': True}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location_point = Column(Geometry('POINT'), nullable=False)
    address_components = Column(Text, nullable=True)  # JSON string
    google_place_id = Column(String(255), nullable=True)
    is_approximate = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    property = relationship("Property", back_populates="map_location")

class PropertyMapSearch(Base):
    __tablename__ = "property_map_searches"
    __table_args__ = {'extend_existing': True}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    session_id = Column(String(255), nullable=True)
    center_lat = Column(Float, nullable=False)
    center_lng = Column(Float, nullable=False)
    radius_km = Column(Float, nullable=False)
    search_filters = Column(Text, nullable=True)  # JSON string
    results_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class PropertyMapBounds(Base):
    __tablename__ = "property_map_bounds"
    __table_args__ = {'extend_existing': True}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"))
    north_lat = Column(Float, nullable=False)
    south_lat = Column(Float, nullable=False)
    east_lng = Column(Float, nullable=False)
    west_lng = Column(Float, nullable=False)
    zoom_level = Column(Integer, default=10)
    created_at = Column(DateTime, default=datetime.utcnow)

class PropertyNearbyPlace(Base):
    __tablename__ = "property_nearby_places"
    __table_args__ = {'extend_existing': True}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"))
    place_name = Column(String(255), nullable=False)
    place_type = Column(String(100), nullable=False)  # school, hospital, shopping, transport
    distance_km = Column(Float, nullable=False)
    place_lat = Column(Float, nullable=True)
    place_lng = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    property = relationship("Property", back_populates="nearby_places")