# selgo-backend/motorcycle-service/create_enums.py
from sqlalchemy import create_engine, text
from src.config import settings
import os

def create_enums():
    """Create PostgreSQL enum types"""
    
    # Database configuration
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "12345")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "selgo_motorcycle")
    
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    engine = create_engine(DATABASE_URL)
    
    try:
        with engine.connect() as connection:
            # Create enum types
            print("Creating enum types...")
            
            # MotorcycleType enum
            connection.execute(text("""
                DO $$ BEGIN
                    CREATE TYPE motorcycletype AS ENUM (
                        'adventure', 'nakne', 'touring', 'sports', 'cruiser', 'scooter'
                    );
                EXCEPTION
                    WHEN duplicate_object THEN null;
                END $$;
            """))
            
            # ConditionEnum enum  
            connection.execute(text("""
                DO $$ BEGIN
                    CREATE TYPE conditionenum AS ENUM (
                        'new', 'like_new', 'excellent', 'good', 'fair', 'poor', 'project_bike'
                    );
                EXCEPTION
                    WHEN duplicate_object THEN null;
                END $$;
            """))
            
            # SellerTypeEnum enum
            connection.execute(text("""
                DO $$ BEGIN
                    CREATE TYPE sellertypeenum AS ENUM (
                        'private', 'dealer'
                    );
                EXCEPTION
                    WHEN duplicate_object THEN null;
                END $$;
            """))
            
            connection.commit()
            print("✅ Enum types created successfully!")
            
    except Exception as e:
        print(f"❌ Error creating enum types: {e}")
        raise

if __name__ == "__main__":
    create_enums()