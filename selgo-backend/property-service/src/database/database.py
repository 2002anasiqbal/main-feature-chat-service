# property-service/src/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Database configuration
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "12345")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "selgo_property")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_database():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """Initialize database tables"""
    from .models import Base
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def seed_initial_data():
    """Seed database with initial data"""
    from .models import PropertyCategory, Facility, PopularCity, RentalTip, PropertyPriceInsight
    from .schemas import PropertyTypeEnum, PropertyCategoryEnum
    from datetime import datetime, timedelta
    from decimal import Decimal
    
    db = SessionLocal()
    try:
        # Check if categories already exist
        existing_categories = db.query(PropertyCategory).count()
        if existing_categories > 0:
            print("Categories already exist, skipping seed...")
            return
        
        # Seed Property Categories
        categories = [
            {"label": "Plots", "type": PropertyTypeEnum.PURCHASE, "icon": "1.svg", "route": "/plots"},
            {"label": "Residence Abroad", "type": PropertyTypeEnum.PURCHASE, "icon": "2.svg", "route": "/residence-abroad"},
            {"label": "Housing for Sale", "type": PropertyTypeEnum.PURCHASE, "icon": "3.svg", "route": "/housing-sale"},
            {"label": "New Homes", "type": PropertyTypeEnum.PURCHASE, "icon": "4.svg", "route": "/new-homes"},
            {"label": "Vacation Homes", "type": PropertyTypeEnum.PURCHASE, "icon": "5.svg", "route": "/vacation-homes"},
            {"label": "Leisure Plots", "type": PropertyTypeEnum.PURCHASE, "icon": "6.svg", "route": "/leisure-plots"},
            {"label": "Apartments for Rent", "type": PropertyTypeEnum.RENT, "icon": "7.svg", "route": "/apartments-rent"},
            {"label": "Houses for Rent", "type": PropertyTypeEnum.RENT, "icon": "8.svg", "route": "/houses-rent"},
            {"label": "Commercial Rent", "type": PropertyTypeEnum.RENT, "icon": "9.svg", "route": "/commercial-rent"}
        ]
        
        for cat_data in categories:
            category = PropertyCategory(**cat_data)
            db.add(category)
        
        # Seed Facilities
        facilities = [
            {"name": "Unfurnished", "category": "furnishing"},
            {"name": "Furnished", "category": "furnishing"},
            {"name": "Semi-furnished", "category": "furnishing"},
            {"name": "Balcony/Terrace", "category": "outdoor"},
            {"name": "Garden", "category": "outdoor"},
            {"name": "Parking", "category": "parking"},
            {"name": "Garage", "category": "parking"},
            {"name": "Fireplace", "category": "indoor"},
            {"name": "Central Heating", "category": "heating"},
            {"name": "Air Conditioning", "category": "climate"},
            {"name": "Elevator", "category": "accessibility"},
            {"name": "Swimming Pool", "category": "luxury"},
            {"name": "Gym", "category": "amenity"},
            {"name": "Security System", "category": "security"},
            {"name": "Pet Friendly", "category": "policy"}
        ]
        
        for fac_data in facilities:
            facility = Facility(**fac_data)
            db.add(facility)
        
        # Seed Popular Cities
        cities = [
            {"name": "Oslo", "rental_count": 15420, "avg_price": Decimal("18500")},
            {"name": "Bergen", "rental_count": 8930, "avg_price": Decimal("16200")},
            {"name": "Trondheim", "rental_count": 6780, "avg_price": Decimal("14800")},
            {"name": "Stavanger", "rental_count": 5940, "avg_price": Decimal("17300")},
            {"name": "Drammen", "rental_count": 3420, "avg_price": Decimal("13900")},
            {"name": "Kristiansand", "rental_count": 2890, "avg_price": Decimal("13200")},
            {"name": "Tromsø", "rental_count": 2340, "avg_price": Decimal("15600")},
            {"name": "Ålesund", "rental_count": 1980, "avg_price": Decimal("12800")}
        ]
        
        for city_data in cities:
            city = PopularCity(**city_data, is_featured=True)
            db.add(city)
        
        # Seed Rental Tips
        tips = [
            {
                "title": "Write a lease with a notice period",
                "content": "Use FINN's rental contract completely free of charge. This ensures both landlord and tenant rights are protected.",
                "tip_number": 1,
                "category": "legal"
            },
            {
                "title": "Secure your deposit properly",
                "content": "Make sure you have a deposit in your own account in your name (deposit account). Never pay deposits to personal accounts.",
                "tip_number": 2,
                "category": "financial"
            },
            {
                "title": "Document property condition",
                "content": "Document any errors or defects in the home upon moving in. Take photos and make written notes.",
                "tip_number": 3,
                "category": "inspection"
            },
            {
                "title": "Report repairs to landlord",
                "content": "Report any repairs to the landlord. It is not your responsibility as a tenant to fix structural issues!",
                "tip_number": 4,
                "category": "maintenance"
            },
            {
                "title": "Consider electricity costs",
                "content": "Remember that the electricity bill is often not included in the rent, take this into account in the calculation.",
                "tip_number": 5,
                "category": "costs"
            }
        ]
        
        for tip_data in tips:
            tip = RentalTip(**tip_data)
            db.add(tip)
        
        # Seed Price Insights
        insights = [
            {
                "city": "Bergen",
                "avg_price_per_sqm": Decimal("54123.50"),
                "period_start": datetime.now() - timedelta(days=30),
                "period_end": datetime.now(),
                "sample_size": 234
            },
            {
                "city": "Oslo", 
                "avg_price_per_sqm": Decimal("62000.00"),
                "period_start": datetime.now() - timedelta(days=30),
                "period_end": datetime.now(),
                "sample_size": 456
            },
            {
                "city": "Stavanger",
                "avg_price_per_sqm": Decimal("49500.00"),
                "period_start": datetime.now() - timedelta(days=30),
                "period_end": datetime.now(),
                "sample_size": 189
            },
            {
                "city": "Trondheim",
                "avg_price_per_sqm": Decimal("56000.00"),
                "period_start": datetime.now() - timedelta(days=30),
                "period_end": datetime.now(),
                "sample_size": 298
            },
            {
                "city": "Drammen",
                "avg_price_per_sqm": Decimal("48000.00"),
                "period_start": datetime.now() - timedelta(days=30),
                "period_end": datetime.now(),
                "sample_size": 145
            },
            {
                "city": "Kristiansand",
                "avg_price_per_sqm": Decimal("51000.00"),
                "period_start": datetime.now() - timedelta(days=30),
                "period_end": datetime.now(),
                "sample_size": 167
            }
        ]
        
        for insight_data in insights:
            insight = PropertyPriceInsight(**insight_data)
            db.add(insight)
        
        db.commit()
        print("Initial data seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()