# import os
# from pydantic_settings import BaseSettings
# from dotenv import load_dotenv

# load_dotenv()

# class Settings(BaseSettings):
#     # Database settings
#     DB_USER: str = os.getenv("DB_USER", "postgres")
#     DB_PASSWORD: str = os.getenv("DB_PASSWORD", "12345")
#     DB_HOST: str = os.getenv("DB_HOST", "localhost")
#     DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
#     DB_NAME: str = os.getenv("DB_NAME", "selgo_job")
    
#     DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
#     # API settings
#     API_HOST: str = os.getenv("API_HOST", "localhost")
#     API_PORT: int = int(os.getenv("API_PORT", "8002"))
#     API_PREFIX: str = "/api/v1"
    
#     # Auth service settings
#     AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
    
#     # File upload settings
#     UPLOAD_DIR: str = "uploads"
#     MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
#     ALLOWED_FILE_TYPES: list = [".pdf", ".doc", ".docx", ".jpg", ".jpeg", ".png"]
    
#     # Redis settings (for caching)
#     REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
#     # Environment
#     ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
#     class Config:
#         env_file = ".env"

# settings = Settings()

import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Database settings
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "12345")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "selgo_job")
    
    DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # API settings
    API_HOST: str = os.getenv("API_HOST", "localhost")
    API_PORT: int = int(os.getenv("API_PORT", "8002"))
    API_PREFIX: str = "/api/v1"
    
    # Auth service settings
    AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
    
    # File upload settings
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: list = [".pdf", ".doc", ".docx", ".jpg", ".jpeg", ".png"]
    
    # Redis settings (for caching)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # CORS Configuration
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000", 
        "https://mzvlqu-ip-175-107-245-22.tunnelmole.net ",  # Your frontend tunnel
        "http://mzvlqu-ip-175-107-245-22.tunnelmole.net",   # HTTP version
        # Tunnel URLs for other services
        
        "https://1z2vyu-ip-175-107-245-22.tunnelmole.net",  # Boat service tunnel
       
        
        "https://voyqji-ip-175-107-245-22.tunnelmole.net",  # Auth service tunnel
        
        "https://wnipcy-ip-175-107-245-22.tunnelmole.net",  # Motorcycle service tunnel
    ]
    
    # CORS Headers  
    ALLOWED_METHODS: list = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
    ALLOWED_HEADERS: list = [
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type", 
        "Authorization",
        "X-Requested-With",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers"
    ]
    
    class Config:
        env_file = ".env"

settings = Settings()