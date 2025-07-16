# selgo-backend/motorcycle-service/src/database/database.py
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration using your .env file
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "12345")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "selgo_motorcycle")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"🔗 Database URL: postgresql://{DB_USER}:***@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
    Create all database tables
    For production, use Alembic migrations instead
    """
    environment = os.getenv("ENVIRONMENT", "development")
    
    try:
        if environment == "development":
            # Development: Create tables directly for quick setup
            from ..models import models
            models.Base.metadata.create_all(bind=engine)
            print("✅ Database tables created successfully!")
            print("💡 For production, use 'alembic upgrade head' instead")
        else:
            # Production: Use Alembic migrations
            print("🏭 Production environment detected")
            print("⚠️  Please run 'alembic upgrade head' to create/update tables")
            print("⚠️  Do not use create_tables() in production!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise

def test_connection():
    """
    Test database connection
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def check_alembic_version():
    """
    Check current Alembic migration version
    """
    try:
        with engine.connect() as connection:
            # Check if alembic_version table exists
            result = connection.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'alembic_version'
                );
            """))
            
            if result.scalar():
                # Get current version
                version_result = connection.execute(text("SELECT version_num FROM alembic_version"))
                current_version = version_result.scalar()
                print(f"📋 Current Alembic version: {current_version}")
                return current_version
            else:
                print("📋 No Alembic version found - database not initialized with migrations")
                return None
    except Exception as e:
        print(f"❌ Error checking Alembic version: {e}")
        return None

if __name__ == "__main__":
    # Test the database connection when run directly
    test_connection()
    check_alembic_version()