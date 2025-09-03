# property-service/setup_database.py (Fixed version)
"""
Fixed script to setup database tables and seed data
"""

import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
from decimal import Decimal

# Add src to path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def create_database_connection():
    """Create database connection"""
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "12345")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "selgo_property")

    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    return engine, SessionLocal

def create_tables_manually():
    """Create tables manually using SQL"""
    engine, SessionLocal = create_database_connection()
    
    with engine.connect() as conn:
        print("📊 Creating tables manually...")
        
        # Enable UUID extension
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"))
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
        
        # Create property_categories table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS property_categories (
                id SERIAL PRIMARY KEY,
                label VARCHAR(100) NOT NULL,
                type VARCHAR(50) NOT NULL,
                icon VARCHAR(255),
                route VARCHAR(255),
                description TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                sort_order INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        
        # Create properties table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS properties (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                title VARCHAR(255) NOT NULL,
                description TEXT,
                price DECIMAL(12, 2) NOT NULL,
                category_id INTEGER REFERENCES property_categories(id),
                property_type VARCHAR(50) NOT NULL,
                property_category VARCHAR(50) NOT NULL,
                status VARCHAR(50) DEFAULT 'active',
                bedrooms INTEGER,
                bathrooms INTEGER,
                rooms INTEGER,
                use_area FLOAT,
                plot_area FLOAT,
                year_built INTEGER,
                housing_type VARCHAR(100),
                ownership_form VARCHAR(50),
                condition VARCHAR(50),
                address VARCHAR(500),
                city VARCHAR(100),
                state VARCHAR(100),
                postal_code VARCHAR(20),
                country VARCHAR(100) DEFAULT 'Norway',
                location GEOMETRY(POINT),
                is_furnished BOOLEAN DEFAULT FALSE,
                has_balcony BOOLEAN DEFAULT FALSE,
                has_terrace BOOLEAN DEFAULT FALSE,
                has_fireplace BOOLEAN DEFAULT FALSE,
                has_parking BOOLEAN DEFAULT FALSE,
                parking_spaces INTEGER DEFAULT 0,
                has_garden BOOLEAN DEFAULT FALSE,
                has_basement BOOLEAN DEFAULT FALSE,
                has_garage BOOLEAN DEFAULT FALSE,
                energy_rating VARCHAR(5),
                heating_type VARCHAR(100),
                monthly_costs DECIMAL(10, 2),
                deposit_amount DECIMAL(10, 2),
                shared_costs DECIMAL(10, 2),
                property_tax DECIMAL(10, 2),
                owner_id UUID NOT NULL,
                owner_name VARCHAR(255),
                owner_phone VARCHAR(20),
                owner_email VARCHAR(255),
                is_agent BOOLEAN DEFAULT FALSE,
                agent_company VARCHAR(255),
                is_featured BOOLEAN DEFAULT FALSE,
                is_premium BOOLEAN DEFAULT FALSE,
                views_count INTEGER DEFAULT 0,
                favorites_count INTEGER DEFAULT 0,
                featured_until TIMESTAMP,
                meta_title VARCHAR(255),
                meta_description VARCHAR(500),
                slug VARCHAR(255) UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                published_at TIMESTAMP,
                sold_at TIMESTAMP
            );
        """))
        
        # Create property_images table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS property_images (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                property_id UUID REFERENCES properties(id) ON DELETE CASCADE,
                image_url VARCHAR(500) NOT NULL,
                alt_text VARCHAR(255),
                is_primary BOOLEAN DEFAULT FALSE,
                sort_order INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        
        # Create facilities table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS facilities (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE,
                icon VARCHAR(255),
                category VARCHAR(50),
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        
        # Create property_facilities table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS property_facilities (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                property_id UUID REFERENCES properties(id) ON DELETE CASCADE,
                facility_id INTEGER REFERENCES facilities(id),
                value VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        
        # Create popular_cities table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS popular_cities (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                state VARCHAR(100),
                country VARCHAR(100) DEFAULT 'Norway',
                image_url VARCHAR(500),
                rental_count INTEGER DEFAULT 0,
                avg_price DECIMAL(10, 2),
                is_featured BOOLEAN DEFAULT FALSE,
                sort_order INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        
        # Create rental_tips table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS rental_tips (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                content TEXT NOT NULL,
                tip_number INTEGER,
                category VARCHAR(50),
                is_active BOOLEAN DEFAULT TRUE,
                sort_order INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        
        # Create property_price_insights table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS property_price_insights (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                city VARCHAR(100) NOT NULL,
                area VARCHAR(100),
                avg_price_per_sqm DECIMAL(10, 2) NOT NULL,
                currency VARCHAR(3) DEFAULT 'NOK',
                period_start TIMESTAMP NOT NULL,
                period_end TIMESTAMP NOT NULL,
                sample_size INTEGER NOT NULL,
                property_type VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        
        # Create feedback table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS feedback (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                page_url VARCHAR(500),
                user_id UUID,
                email VARCHAR(255),
                message TEXT NOT NULL,
                rating INTEGER,
                is_processed BOOLEAN DEFAULT FALSE,
                admin_notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        
        # Create property_messages table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS property_messages (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                property_id UUID REFERENCES properties(id) ON DELETE CASCADE,
                sender_name VARCHAR(255) NOT NULL,
                sender_email VARCHAR(255) NOT NULL,
                sender_phone VARCHAR(20),
                message TEXT NOT NULL,
                is_read BOOLEAN DEFAULT FALSE,
                is_replied BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        
        # Commit the transaction
        conn.commit()
        print("✅ All basic tables created successfully!")

def seed_initial_data():
    """Seed initial data"""
    engine, SessionLocal = create_database_connection()
    db = SessionLocal()
    
    try:
        print("🌱 Seeding initial data...")
        
        # Seed Property Categories
        categories_data = [
            ("Plots", "purchase", "1.svg", "/plots", 1),
            ("Residence Abroad", "purchase", "2.svg", "/residence-abroad", 2),
            ("Housing for Sale", "purchase", "3.svg", "/housing-sale", 3),
            ("New Homes", "purchase", "4.svg", "/new-homes", 4),
            ("Vacation Homes", "purchase", "5.svg", "/vacation-homes", 5),
            ("Leisure Plots", "purchase", "6.svg", "/leisure-plots", 6),
            ("Apartments for Rent", "rent", "7.svg", "/apartments-rent", 7),
            ("Houses for Rent", "rent", "8.svg", "/houses-rent", 8),
            ("Commercial Rent", "rent", "9.svg", "/commercial-rent", 9)
        ]
        
        for label, ptype, icon, route, sort_order in categories_data:
            db.execute(text("""
                INSERT INTO property_categories (label, type, icon, route, sort_order)
                VALUES (:label, :type, :icon, :route, :sort_order)
                ON CONFLICT (label) DO NOTHING
            """), {"label": label, "type": ptype, "icon": icon, "route": route, "sort_order": sort_order})
        
        # Seed Facilities
        facilities_data = [
            ("Unfurnished", "furnishing"),
            ("Furnished", "furnishing"),
            ("Semi-furnished", "furnishing"),
            ("Balcony/Terrace", "outdoor"),
            ("Garden", "outdoor"),
            ("Parking", "parking"),
            ("Garage", "parking"),
            ("Fireplace", "indoor"),
            ("Central Heating", "heating"),
            ("Air Conditioning", "climate"),
            ("Elevator", "accessibility"),
            ("Swimming Pool", "luxury"),
            ("Gym", "amenity"),
            ("Security System", "security"),
            ("Pet Friendly", "policy")
        ]
        
        for name, category in facilities_data:
            db.execute(text("""
                INSERT INTO facilities (name, category)
                VALUES (:name, :category)
                ON CONFLICT (name) DO NOTHING
            """), {"name": name, "category": category})
        
        # Seed Popular Cities
        cities_data = [
            ("Oslo", 15420, 18500),
            ("Bergen", 8930, 16200),
            ("Trondheim", 6780, 14800),
            ("Stavanger", 5940, 17300),
            ("Drammen", 3420, 13900),
            ("Kristiansand", 2890, 13200),
            ("Tromsø", 2340, 15600),
            ("Ålesund", 1980, 12800)
        ]
        
        for name, rental_count, avg_price in cities_data:
            db.execute(text("""
                INSERT INTO popular_cities (name, rental_count, avg_price, is_featured)
                VALUES (:name, :rental_count, :avg_price, TRUE)
                ON CONFLICT (name) DO NOTHING
            """), {"name": name, "rental_count": rental_count, "avg_price": avg_price})
        
        # Seed Rental Tips
        tips_data = [
            ("Write a lease with a notice period", "Use FINN's rental contract completely free of charge. This ensures both landlord and tenant rights are protected.", 1, "legal"),
            ("Secure your deposit properly", "Make sure you have a deposit in your own account in your name (deposit account). Never pay deposits to personal accounts.", 2, "financial"),
            ("Document property condition", "Document any errors or defects in the home upon moving in. Take photos and make written notes.", 3, "inspection"),
            ("Report repairs to landlord", "Report any repairs to the landlord. It is not your responsibility as a tenant to fix structural issues!", 4, "maintenance"),
            ("Consider electricity costs", "Remember that the electricity bill is often not included in the rent, take this into account in the calculation.", 5, "costs")
        ]
        
        for title, content, tip_number, category in tips_data:
            db.execute(text("""
                INSERT INTO rental_tips (title, content, tip_number, category)
                VALUES (:title, :content, :tip_number, :category)
            """), {"title": title, "content": content, "tip_number": tip_number, "category": category})
        
        # Seed Price Insights
        insights_data = [
            ("Bergen", 54123.50, 234),
            ("Oslo", 62000.00, 456),
            ("Stavanger", 49500.00, 189),
            ("Trondheim", 56000.00, 298),
            ("Drammen", 48000.00, 145),
            ("Kristiansand", 51000.00, 167)
        ]
        
        period_start = datetime.now().replace(day=1)  # First of current month
        period_end = datetime.now()
        
        for city, avg_price, sample_size in insights_data:
            db.execute(text("""
                INSERT INTO property_price_insights (city, avg_price_per_sqm, period_start, period_end, sample_size)
                VALUES (:city, :avg_price, :period_start, :period_end, :sample_size)
            """), {
                "city": city, 
                "avg_price": avg_price, 
                "period_start": period_start, 
                "period_end": period_end, 
                "sample_size": sample_size
            })
        
        # Create a sample property
        sample_owner_id = "123e4567-e89b-12d3-a456-426614174000"
        db.execute(text("""
            INSERT INTO properties (
                id, title, description, price, property_type, property_category, 
                bedrooms, bathrooms, use_area, city, country, owner_id, owner_name, 
                is_featured, views_count
            )
            VALUES (
                :id, :title, :description, :price, :property_type, :property_category,
                :bedrooms, :bathrooms, :use_area, :city, :country, :owner_id, :owner_name,
                :is_featured, :views_count
            )
            ON CONFLICT (id) DO NOTHING
        """), {
            "id": sample_owner_id,
            "title": "Beautiful Oslo Apartment",
            "description": "A stunning apartment in the heart of Oslo with modern amenities and beautiful city views.",
            "price": 4500000,
            "property_type": "purchase",
            "property_category": "housing_sale",
            "bedrooms": 3,
            "bathrooms": 2,
            "use_area": 95.5,
            "city": "Oslo",
            "country": "Norway",
            "owner_id": sample_owner_id,
            "owner_name": "Property Owner",
            "is_featured": True,
            "views_count": 156
        })
        
        # Add sample property image
        db.execute(text("""
            INSERT INTO property_images (property_id, image_url, is_primary)
            VALUES (:property_id, :image_url, :is_primary)
        """), {
            "property_id": sample_owner_id,
            "image_url": "/assets/property/property.jpeg",
            "is_primary": True
        })
        
        db.commit()
        print("✅ Initial data seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding data: {e}")
        raise
    finally:
        db.close()

def main():
    """Main function"""
    print("🚀 Property Service Database Setup")
    print("=" * 40)
    
    try:
        # Create tables
        create_tables_manually()
        
        # Seed data
        seed_initial_data()
        
        print("\n🎉 Database setup complete!")
        print("✅ You can now run: python main.py")
        
    except Exception as e:
        print(f"\n❌ Database setup failed: {e}")
        print("🔧 Make sure PostgreSQL is running and accessible")

if __name__ == "__main__":
    main()