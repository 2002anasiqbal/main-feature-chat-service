# property-service/src/models/rental_models.py (Fixed - prevents table conflicts)
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, DECIMAL, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

# Import Base from your existing models
from .models import Base

class RentalProperty(Base):
    __tablename__ = "rental_properties"
    __table_args__ = {'extend_existing': True}  # Fix for table conflicts
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"))
    landlord_id = Column(UUID(as_uuid=True), nullable=False)  # User ID from auth service
    
    # Rental Specific Information
    monthly_rent = Column(DECIMAL(10, 2), nullable=False)
    security_deposit = Column(DECIMAL(10, 2), nullable=False)
    first_month_rent = Column(DECIMAL(10, 2), nullable=True)
    last_month_rent = Column(DECIMAL(10, 2), nullable=True)
    
    # Lease Terms
    min_lease_duration_months = Column(Integer, default=12)
    max_lease_duration_months = Column(Integer, nullable=True)
    available_from = Column(Date, nullable=False)
    lease_type = Column(String(50), default="fixed")  # fixed, month_to_month, flexible
    
    # Rental Policies
    pets_allowed = Column(Boolean, default=False)
    smoking_allowed = Column(Boolean, default=False)
    max_occupants = Column(Integer, nullable=True)
    utilities_included = Column(Text, nullable=True)  # JSON array
    parking_included = Column(Boolean, default=False)
    internet_included = Column(Boolean, default=False)
    
    # Requirements
    minimum_income_multiple = Column(DECIMAL(3, 1), default=3.0)  # 3x rent
    credit_score_minimum = Column(Integer, nullable=True)
    background_check_required = Column(Boolean, default=True)
    references_required = Column(Integer, default=2)
    
    # Status
    is_available = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    inquiry_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    rental_applications = relationship("RentalApplication", back_populates="rental_property")
    lease_contracts = relationship("LeaseContract", back_populates="rental_property")

class RentalApplication(Base):
    __tablename__ = "rental_applications"
    __table_args__ = {'extend_existing': True}  # Fix for table conflicts
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rental_property_id = Column(UUID(as_uuid=True), ForeignKey("rental_properties.id", ondelete="CASCADE"))
    applicant_id = Column(UUID(as_uuid=True), nullable=False)  # User ID from auth service
    
    # Application Information
    application_date = Column(DateTime, default=datetime.utcnow)
    desired_move_in_date = Column(Date, nullable=False)
    lease_duration_months = Column(Integer, nullable=False)
    
    # Applicant Details
    annual_income = Column(DECIMAL(12, 2), nullable=False)
    employment_status = Column(String(100), nullable=False)
    employer_name = Column(String(255), nullable=True)
    credit_score = Column(Integer, nullable=True)
    previous_address = Column(Text, nullable=True)
    reason_for_moving = Column(Text, nullable=True)
    
    # References
    personal_references = Column(Text, nullable=True)  # JSON array
    professional_references = Column(Text, nullable=True)  # JSON array
    
    # Additional Information
    pets_description = Column(Text, nullable=True)
    special_requests = Column(Text, nullable=True)
    emergency_contact = Column(Text, nullable=True)  # JSON object
    
    # Application Status
    status = Column(String(50), default="pending")  # pending, approved, rejected, withdrawn
    reviewed_date = Column(DateTime, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    landlord_notes = Column(Text, nullable=True)
    
    # Relationships
    rental_property = relationship("RentalProperty", back_populates="rental_applications")

class LeaseContract(Base):
    __tablename__ = "lease_contracts"
    __table_args__ = {'extend_existing': True}  # Fix for table conflicts
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rental_property_id = Column(UUID(as_uuid=True), ForeignKey("rental_properties.id", ondelete="CASCADE"))
    application_id = Column(UUID(as_uuid=True), ForeignKey("rental_applications.id"))
    landlord_id = Column(UUID(as_uuid=True), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    
    # Contract Details
    contract_number = Column(String(100), unique=True, nullable=False)
    lease_start_date = Column(Date, nullable=False)
    lease_end_date = Column(Date, nullable=False)
    monthly_rent = Column(DECIMAL(10, 2), nullable=False)
    security_deposit = Column(DECIMAL(10, 2), nullable=False)
    
    # Contract Terms
    lease_terms = Column(Text, nullable=False)  # Full contract text or JSON
    special_conditions = Column(Text, nullable=True)
    pets_clause = Column(Text, nullable=True)
    maintenance_responsibilities = Column(Text, nullable=True)
    
    # Status and Signatures
    status = Column(String(50), default="draft")  # draft, pending, signed, active, terminated, expired
    landlord_signed = Column(Boolean, default=False)
    tenant_signed = Column(Boolean, default=False)
    landlord_signature_date = Column(DateTime, nullable=True)
    tenant_signature_date = Column(DateTime, nullable=True)
    contract_file_url = Column(String(500), nullable=True)
    
    # Termination
    termination_date = Column(Date, nullable=True)
    termination_reason = Column(String(255), nullable=True)
    termination_notice_date = Column(Date, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    rental_property = relationship("RentalProperty", back_populates="lease_contracts")
    application = relationship("RentalApplication")

class LeaseContractTemplate(Base):
    __tablename__ = "lease_contract_templates"
    __table_args__ = {'extend_existing': True}  # Fix for table conflicts
    
    id = Column(Integer, primary_key=True)
    template_name = Column(String(255), nullable=False)
    template_type = Column(String(100), nullable=False)  # standard, furnished, commercial
    jurisdiction = Column(String(100), default="Norway")
    template_content = Column(Text, nullable=False)  # HTML or markdown template
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    version = Column(String(20), default="1.0")
    created_by = Column(UUID(as_uuid=True), nullable=True)
    approved_by_legal = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RentalSuggestion(Base):
    __tablename__ = "rental_suggestions"
    __table_args__ = {'extend_existing': True}  # Fix for table conflicts
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    session_id = Column(String(255), nullable=True)
    
    # Search Criteria
    preferred_location = Column(String(255), nullable=True)
    max_rent = Column(DECIMAL(10, 2), nullable=True)
    min_bedrooms = Column(Integer, nullable=True)
    max_bedrooms = Column(Integer, nullable=True)
    property_type = Column(String(100), nullable=True)
    amenities_required = Column(Text, nullable=True)  # JSON array
    
    # Suggested Properties
    suggested_properties = Column(Text, nullable=True)  # JSON array of property IDs
    suggestion_algorithm = Column(String(100), nullable=True)  # ml, rules, collaborative
    suggestion_score = Column(DECIMAL(5, 3), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    viewed_at = Column(DateTime, nullable=True)
    clicked_properties = Column(Text, nullable=True)  # JSON array of clicked property IDs