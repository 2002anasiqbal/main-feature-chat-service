import os
from pydantic_settings import BaseSettings  # Updated import
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Database settings
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "12345")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "selgo_auth")
    
    DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # API settings
    API_HOST: str = os.getenv("API_HOST", "localhost")
    API_PORT: int = int(os.getenv("API_PORT", "8001"))
    API_PREFIX: str = "/api/v1"
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30"))
    
    # OAuth settings
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    TWITTER_CLIENT_ID: str = os.getenv("TWITTER_CLIENT_ID", "")
    TWITTER_CLIENT_SECRET: str = os.getenv("TWITTER_CLIENT_SECRET", "")
    
    # Frontend settings
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # Service URLs (for inter-service communication)
    BOAT_SERVICE_URL: str = os.getenv("BOAT_SERVICE_URL", "http://localhost:8000")
    JOB_SERVICE_URL: str = os.getenv("JOB_SERVICE_URL", "http://localhost:8002")
    PROPERTY_SERVICE_URL: str = os.getenv("PROPERTY_SERVICE_URL", "http://localhost:8003")
    
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    class Config:
        env_file = ".env"

settings = Settings()