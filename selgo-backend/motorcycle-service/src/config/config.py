# selgo-backend/motorcycle-service/src/config/config.py
import os
from typing import Optional, List

class Settings:
    # Database
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "12345")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "selgo_motorcycle")
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # API
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8003"))
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == "development"
    
    # Auth Service
    AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
    
    # File Upload (using your existing settings)
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    ALLOWED_IMAGE_EXTENSIONS: set = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads/motorcycles")
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Loan Calculations (using your existing settings)
    DEFAULT_INTEREST_RATE: float = float(os.getenv("DEFAULT_INTEREST_RATE", "7.5"))  # 7.5% annual
    MIN_LOAN_TERM: int = int(os.getenv("MIN_LOAN_TERM", "12"))  # months
    MAX_LOAN_TERM: int = int(os.getenv("MAX_LOAN_TERM", "84"))  # months
    
    # Email (if implementing email notifications)
    SMTP_HOST: Optional[str] = os.getenv("SMTP_HOST")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: Optional[str] = os.getenv("SMTP_USER")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
    
    # CORS (using your existing settings)
    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001")
        origins = [origin.strip() for origin in origins_str.split(",")]
        
        # Add production origins if in production
        if self.ENVIRONMENT == "production":
            origins.extend([
                "https://selgo.com",
                "https://www.selgo.com",
            ])
        
        return origins

settings = Settings()