from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import logging

from .config.config import settings
from .database.database import engine, Base
from .api.routes import router as boat_router
from .models.boat_models import *
from .utils.auth_client import auth_client  # Add this import

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Selgo Boat Service",
    description="API for boat listings and related operations",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)

# Mount static files directory for uploads
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_FOLDER), name="uploads")

# Include routers
app.include_router(boat_router)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "boat", "version": "0.1.0"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "service": "boat",
        "version": "0.1.0",
        "description": "API for boat listings and related operations",
        "documentation": "/docs",
    }

# Create tables on startup (for development)
@app.on_event("startup")
async def startup_event():
    try:
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")

# Add shutdown event to close auth client
@app.on_event("shutdown")
async def shutdown_event():
    try:
        await auth_client.close()
        logger.info("Auth client closed successfully")
    except Exception as e:
        logger.error(f"Error closing auth client: {e}")