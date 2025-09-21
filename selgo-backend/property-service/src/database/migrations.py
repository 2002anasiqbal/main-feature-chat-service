# property-service/src/database/migrations.py (Fixed imports)
"""
Database migration and table creation script
Run this to create all tables for points 1-10
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime, date
from decimal import Decimal

# Import all models with absolute imports (adjust to your structure)
try:
    # Try absolute imports first
    from src.models.models import Base, Property, PropertyCategory, PropertyImage, Facility, PropertyFacility
    from src.models.map_models import PropertyMapLocation, PropertyMapSearch, PropertyNearbyPlace
    from src.models.comparison_models import PropertyComparisonSession, PropertyComparisonItem, PropertyComparisonNote
    from src.models.loan_models import PropertyLoanEstimate, LoanProvider, PropertyLoanApplication
    from src.models.rental_models import RentalProperty, RentalApplication, LeaseContract, LeaseContractTemplate
except ImportError:
    # Fallback to relative imports
    try:
        from ..models.models import Base, Property, PropertyCategory, PropertyImage, Facility, PropertyFacility
        from ..models.map_models import PropertyMapLocation, PropertyMapSearch, PropertyNearbyPlace
        from ..models.comparison_models import PropertyComparisonSession, PropertyComparisonItem, PropertyComparisonNote
        from ..models.loan_models import PropertyLoanEstimate, LoanProvider, PropertyLoanApplication
        from ..models.rental_models import RentalProperty, RentalApplication, LeaseContract, LeaseContractTemplate
    except ImportError:
        # Last fallback - direct imports (if running from project root)
        from models.models import Base, Property, PropertyCategory, PropertyImage, Facility, PropertyFacility
        from models.map_models import PropertyMapLocation, PropertyMapSearch, PropertyNearbyPlace
        from models.comparison_models import PropertyComparisonSession, PropertyComparisonItem, PropertyComparisonNote
        from models.loan_models import PropertyLoanEstimate, LoanProvider, PropertyLoanApplication
        from models.rental_models import RentalProperty, RentalApplication, LeaseContract, LeaseContractTemplate

def create_all_tables():
    """Create all database tables"""
    # Database configuration
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "12345")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "selgo_property")

    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    engine = create_engine(DATABASE_URL)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully!")
    
    return engine

def seed_additional_data():
    """Seed data for points 6-10"""
    engine = create_all_tables()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Seed Loan Providers
        print("Seeding loan providers...")
        loan_providers = [
            {
                "provider_name": "DNB Bank",
                "provider_type": "bank",
                "base_interest_rate": Decimal("3.5"),
                "min_down_payment_percent": Decimal("20.0"),
                "website_url": "https://www.dnb.no",
                "contact_phone": "+47 915 03000"
            },
            {
                "provider_name": "Nordea Bank",
                "provider_type": "bank", 
                "base_interest_rate": Decimal("3.7"),
                "min_down_payment_percent": Decimal("15.0"),
                "website_url": "https://www.nordea.no",
                "contact_phone": "+47 22 48 50 00"
            },
            {
                "provider_name": "Sparebank 1",
                "provider_type": "bank",
                "base_interest_rate": Decimal("3.4"),
                "min_down_payment_percent": Decimal("20.0"),
                "website_url": "https://www.sparebank1.no",
                "contact_phone": "+47 915 02400"
            },
            {
                "provider_name": "Handelsbanken",
                "provider_type": "bank",
                "base_interest_rate": Decimal("3.8"),
                "min_down_payment_percent": Decimal("25.0"),
                "website_url": "https://www.handelsbanken.no",
                "contact_phone": "+47 22 39 70 00"
            }
        ]
        
        for provider_data in loan_providers:
            existing = db.query(LoanProvider).filter(
                LoanProvider.provider_name == provider_data["provider_name"]
            ).first()
            if not existing:
                provider = LoanProvider(**provider_data)
                db.add(provider)
        
        # Seed Lease Contract Templates
        print("Seeding lease contract templates...")
        templates = [
            {
                "template_name": "Standard Residential Lease - Norway",
                "template_type": "standard",
                "jurisdiction": "Norway",
                "template_content": """
                <h1>STANDARD RESIDENTIAL LEASE AGREEMENT</h1>
                <p>This lease agreement is made between [LANDLORD_NAME] (Landlord) and [TENANT_NAME] (Tenant).</p>
                
                <h2>PROPERTY DETAILS</h2>
                <p>Address: [PROPERTY_ADDRESS]</p>
                <p>Monthly Rent: [MONTHLY_RENT] NOK</p>
                <p>Security Deposit: [SECURITY_DEPOSIT] NOK</p>
                
                <h2>LEASE TERMS</h2>
                <p>Lease Period: [LEASE_START_DATE] to [LEASE_END_DATE]</p>
                <p>Payment Due: 1st of each month</p>
                
                <h2>TENANT RESPONSIBILITIES</h2>
                <ul>
                    <li>Pay rent on time</li>
                    <li>Maintain property in good condition</li>
                    <li>Follow building rules and regulations</li>
                    <li>Give proper notice before moving out</li>
                </ul>
                
                <h2>LANDLORD RESPONSIBILITIES</h2>
                <ul>
                    <li>Maintain property in habitable condition</li>
                    <li>Handle major repairs</li>
                    <li>Respect tenant privacy rights</li>
                    <li>Return security deposit as per law</li>
                </ul>
                
                <p>Signatures:</p>
                <p>Landlord: _________________ Date: _________</p>
                <p>Tenant: _________________ Date: _________</p>
                """,
                "is_default": True,
                "approved_by_legal": True,
                "version": "2.0"
            },
            {
                "template_name": "Furnished Apartment Lease - Norway",
                "template_type": "furnished",
                "jurisdiction": "Norway", 
                "template_content": """
                <h1>FURNISHED APARTMENT LEASE AGREEMENT</h1>
                <p>This furnished apartment lease agreement includes all furniture and appliances listed in Appendix A.</p>
                
                <h2>FURNISHED ITEMS</h2>
                <p>Tenant acknowledges receipt of furnished items in good condition and agrees to return them in same condition, normal wear excepted.</p>
                
                <h2>ADDITIONAL DEPOSIT</h2>
                <p>An additional furniture deposit of [FURNITURE_DEPOSIT] NOK is required.</p>
                
                <p>All other terms follow the standard residential lease agreement.</p>
                """,
                "is_default": False,
                "approved_by_legal": True,
                "version": "1.5"
            }
        ]
        
        for template_data in templates:
            existing = db.query(LeaseContractTemplate).filter(
                LeaseContractTemplate.template_name == template_data["template_name"]
            ).first()
            if not existing:
                template = LeaseContractTemplate(**template_data)
                db.add(template)
        
        # Seed some sample nearby places for properties (if any properties exist)
        print("Checking for existing properties to add sample nearby places...")
        sample_property = db.query(Property).first()
        if sample_property:
            nearby_places = [
                {
                    "property_id": sample_property.id,
                    "place_name": "Oslo Central Station",
                    "place_type": "transport",
                    "distance_km": 2.5
                },
                {
                    "property_id": sample_property.id,
                    "place_name": "Ullevål Hospital",
                    "place_type": "hospital",
                    "distance_km": 3.2
                },
                {
                    "property_id": sample_property.id,
                    "place_name": "University of Oslo",
                    "place_type": "school",
                    "distance_km": 1.8
                },
                {
                    "property_id": sample_property.id,
                    "place_name": "Grünerløkka Shopping",
                    "place_type": "shopping",
                    "distance_km": 1.2
                }
            ]
            
            for place_data in nearby_places:
                existing = db.query(PropertyNearbyPlace).filter(
                    PropertyNearbyPlace.property_id == place_data["property_id"],
                    PropertyNearbyPlace.place_name == place_data["place_name"]
                ).first()
                if not existing:
                    place = PropertyNearbyPlace(**place_data)
                    db.add(place)
        
        db.commit()
        print("✅ Additional data seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🔄 Creating database tables and seeding data...")
    seed_additional_data()
    print("🎉 Database setup complete!")