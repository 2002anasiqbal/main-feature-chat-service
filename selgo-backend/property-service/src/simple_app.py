# property-service/src/simple_app.py
"""
Simplified app.py for testing - use this if complex imports fail
Copy this as app.py temporarily to test basic functionality
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Create FastAPI application
app = FastAPI(
    title="Selgo Property Service",
    description="Property management service for Selgo marketplace",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Startup event - simplified"""
    print("🚀 Property Service (Simple Mode) started!")
    print("⚠️  Database initialization skipped for testing")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Selgo Property Service",
        "status": "running (simple mode)",
        "version": "2.0.0",
        "message": "Service is running in simple mode for testing"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "property-service",
        "version": "2.0.0",
        "mode": "simple"
    }

@app.get("/test")
async def test_endpoint():
    """Test endpoint"""
    return {
        "message": "Property service is working!",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "database_host": os.getenv("DB_HOST", "localhost"),
        "api_port": os.getenv("API_PORT", "8004")
    }