# property-service/src/models/loan_models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, DECIMAL, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from .models import Base

class PropertyLoanEstimate(Base):
    __tablename__ = "property_loan_estimates"
    __table_args__ = {'extend_existing': True}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), nullable=True)
    session_id = Column(String(255), nullable=True)
    
    # Loan Details
    property_price = Column(DECIMAL(12, 2), nullable=False)
    down_payment = Column(DECIMAL(12, 2), nullable=False)
    loan_amount = Column(DECIMAL(12, 2), nullable=False)
    interest_rate = Column(DECIMAL(5, 3), nullable=False)
    loan_term_years = Column(Integer, nullable=False)
    loan_term_months = Column(Integer, nullable=False)
    
    # Calculated Results
    monthly_payment = Column(DECIMAL(10, 2), nullable=False)
    total_payment = Column(DECIMAL(12, 2), nullable=False)
    total_interest = Column(DECIMAL(12, 2), nullable=False)
    
    # Additional Costs
    property_tax_monthly = Column(DECIMAL(8, 2), nullable=True)
    insurance_monthly = Column(DECIMAL(8, 2), nullable=True)
    hoa_fees_monthly = Column(DECIMAL(8, 2), nullable=True)
    total_monthly_cost = Column(DECIMAL(10, 2), nullable=True)
    
    # Metadata
    currency = Column(String(3), default="NOK")
    calculation_date = Column(DateTime, default=datetime.utcnow)
    is_saved = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    property = relationship("Property")

class LoanProvider(Base):
    __tablename__ = "loan_providers"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    provider_name = Column(String(255), nullable=False)
    provider_type = Column(String(100), nullable=False)  # bank, credit_union, online_lender
    base_interest_rate = Column(DECIMAL(5, 3), nullable=False)
    min_down_payment_percent = Column(DECIMAL(5, 2), nullable=False)
    max_loan_amount = Column(DECIMAL(12, 2), nullable=True)
    min_credit_score = Column(Integer, nullable=True)
    processing_fee = Column(DECIMAL(8, 2), nullable=True)
    website_url = Column(String(500), nullable=True)
    contact_phone = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class PropertyLoanApplication(Base):
    __tablename__ = "property_loan_applications"
    __table_args__ = {'extend_existing': True}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    estimate_id = Column(UUID(as_uuid=True), ForeignKey("property_loan_estimates.id", ondelete="CASCADE"))
    provider_id = Column(Integer, ForeignKey("loan_providers.id"))
    
    # Applicant Information
    applicant_name = Column(String(255), nullable=False)
    applicant_email = Column(String(255), nullable=False)
    applicant_phone = Column(String(20), nullable=True)
    annual_income = Column(DECIMAL(12, 2), nullable=True)
    credit_score = Column(Integer, nullable=True)
    employment_status = Column(String(100), nullable=True)
    
    # Application Status
    status = Column(String(50), default="pending")  # pending, approved, rejected, processing
    application_date = Column(DateTime, default=datetime.utcnow)
    response_date = Column(DateTime, nullable=True)
    approved_amount = Column(DECIMAL(12, 2), nullable=True)
    approved_rate = Column(DECIMAL(5, 3), nullable=True)
    rejection_reason = Column(Text, nullable=True)
    
    # Relationships
    estimate = relationship("PropertyLoanEstimate")
    provider = relationship("LoanProvider")

class LoanCalculatorPreset(Base):
    __tablename__ = "loan_calculator_presets"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    preset_name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    default_interest_rate = Column(DECIMAL(5, 3), nullable=False)
    default_term_years = Column(Integer, nullable=False)
    default_down_payment_percent = Column(DECIMAL(5, 2), nullable=False)
    property_tax_rate = Column(DECIMAL(5, 4), nullable=True)
    insurance_rate = Column(DECIMAL(5, 4), nullable=True)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)