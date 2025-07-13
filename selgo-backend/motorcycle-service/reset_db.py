# selgo-backend/motorcycle-service/reset_db.py
from sqlalchemy import create_engine, text
import os

def reset_database():
    """Reset database - drop and recreate everything"""
    
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "12345")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "selgo_motorcycle")
    
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    engine = create_engine(DATABASE_URL)
    
    try:
        with engine.connect() as connection:
            print("🗑️  Dropping existing objects...")
            
            # Drop tables first (they depend on enums)
            connection.execute(text("DROP TABLE IF EXISTS loan_offers CASCADE;"))
            connection.execute(text("DROP TABLE IF EXISTS messages CASCADE;"))
            connection.execute(text("DROP TABLE IF EXISTS motorcycle_images CASCADE;"))
            connection.execute(text("DROP TABLE IF EXISTS motorcycles CASCADE;"))
            connection.execute(text("DROP TABLE IF EXISTS motorcycle_categories CASCADE;"))
            connection.execute(text("DROP TABLE IF EXISTS users CASCADE;"))
            
            # Drop enum types
            connection.execute(text("DROP TYPE IF EXISTS conditionenum CASCADE;"))
            connection.execute(text("DROP TYPE IF EXISTS motorcycletype CASCADE;"))
            connection.execute(text("DROP TYPE IF EXISTS sellertypeenum CASCADE;"))
            
            connection.commit()
            print("✅ Database reset completed!")
            
    except Exception as e:
        print(f"❌ Error resetting database: {e}")
        raise

if __name__ == "__main__":
    reset_database()