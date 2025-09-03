<<<<<<< HEAD
# property-service/src/app.py (Fixed for your folder structure)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

# Import database functions (absolute imports)
from src.database.database import init_database, seed_initial_data
from src.database.migrations import create_all_tables, seed_additional_data

# Import routes (absolute imports)
from src.api.routes import router, advanced_router

# Create FastAPI application
app = FastAPI(
    title="Selgo Property Service",
    description="Property management service for Selgo marketplace - Points 1-10 Implementation",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
=======
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import logging

from .config.config import settings
from .database.database import engine, Base
from .api.routes import router as property_router
from .models.models import *
from .utils.auth import auth_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Selgo Property Service",
    description="API for property listings and related operations",
    version="0.1.0",
>>>>>>> ef864b3 (Replace Features branch with selgo-feature contents)
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
<<<<<<< HEAD
    allow_origins=["*"],  # In production, replace with specific origins
=======
    allow_origins=["*"],
>>>>>>> ef864b3 (Replace Features branch with selgo-feature contents)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< HEAD
# Include routes
app.include_router(router)  # Original routes (points 1-5)
app.include_router(advanced_router)  # New routes (points 6-10)

@app.on_event("startup")
async def startup_event():
    """Initialize database and seed data on startup"""
    try:
        print("🚀 Starting Property Service...")
        
        # Create all tables (points 1-10)
        print("📊 Creating database tables...")
        create_all_tables()
        
        # Seed initial data (points 1-5)
        print("🌱 Seeding initial data...")
        seed_initial_data()
        
        # Seed additional data (points 6-10)
        print("🌱 Seeding additional data...")
        seed_additional_data()
        
        print("✅ Property service started successfully!")
        print("📊 Available endpoints:")
        print("   - Points 1-5: /api/properties/* (basic features)")
        print("   - Points 6-10: /api/properties/* (advanced features)")
        print("   - API Docs: /docs")
        
    except Exception as e:
        print(f"❌ Error during startup: {e}")
        print("🔍 Check database connection and credentials")
        # Don't raise - let the app start for debugging

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Selgo Property Service",
        "status": "running",
        "version": "2.0.0",
        "features": [
            "Property Categories (Point 1)",
            "Property Search (Point 2)", 
            "Property Listings (Point 3)",
            "Property Details (Point 4)",
            "Property Contact (Point 5)",
            "Property Map Location (Point 6)",
            "Property Comparison (Point 7)",
            "Property Loan Estimator (Point 8)",
            "New Rental Ads (Point 9)",
            "Lease Contracts (Point 10)"
        ],
        "documentation": "/docs",
        "endpoints": {
            "health": "/health",
            "features": "/api/properties/features",
            "categories": "/api/properties/categories",
            "search": "/api/properties/search",
            "featured": "/api/properties/featured"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "property-service",
        "version": "2.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.get("/api/properties/features")
async def get_available_features():
    """Get list of implemented property features"""
    return {
        "implemented_points": [
            {
                "point": 1,
                "name": "PropertyCategoryModule",
                "description": "Fetch property subcategories",
                "endpoints": ["/api/properties/categories"],
                "auth_required": False
            },
            {
                "point": 2,
                "name": "PropertySearchModule", 
                "description": "Search listings with filters",
                "endpoints": ["/api/properties/search"],
                "auth_required": False
            },
            {
                "point": 3,
                "name": "PropertyListingModule",
                "description": "Featured and recommended properties",
                "endpoints": ["/api/properties/featured", "/api/properties/recommended"],
                "auth_required": False
            },
            {
                "point": 4,
                "name": "PropertyDetailModule",
                "description": "Full property details",
                "endpoints": ["/api/properties/{id}"],
                "auth_required": False
            },
            {
                "point": 5,
                "name": "PropertyContactModule",
                "description": "Contact property owner",
                "endpoints": ["/api/properties/{id}/contact"],
                "auth_required": False
            },
            {
                "point": 6,
                "name": "PropertyMapLocationModule",
                "description": "Map coordinates and nearby search",
                "endpoints": [
                    "/api/properties/{id}/location", 
                    "/api/properties/map/search",
                    "/api/properties/{id}/nearby"
                ],
                "auth_required": False
            },
            {
                "point": 7,
                "name": "PropertyComparisonModule",
                "description": "Compare properties side by side",
                "endpoints": [
                    "/api/properties/compare", 
                    "/api/properties/compare/{session_id}",
                    "/api/properties/compare/{session_id}/notes"
                ],
                "auth_required": "Optional (notes require auth)"
            },
            {
                "point": 8,
                "name": "PropertyLoanEstimatorModule",
                "description": "Calculate monthly loan payments",
                "endpoints": [
                    "/api/properties/loan-estimate", 
                    "/api/properties/loan-providers",
                    "/api/properties/users/{user_id}/loan-estimates"
                ],
                "auth_required": "Optional (user estimates require auth)"
            },
            {
                "point": 9,
                "name": "NewRentalAdModule",
                "description": "Post and manage rental ads",
                "endpoints": [
                    "/api/properties/rentals",
                    "/api/properties/rentals/{id}/applications",
                    "/api/properties/rentals/suggestions"
                ],
                "auth_required": "Required for creating ads and applications"
            },
            {
                "point": 10,
                "name": "LeaseContractModule",
                "description": "Create and sign lease contracts",
                "endpoints": [
                    "/api/properties/lease/contracts", 
                    "/api/properties/lease/templates",
                    "/api/properties/lease/contracts/{id}/sign"
                ],
                "auth_required": "Required for contract management"
            }
        ],
        "total_endpoints": 25,
        "database_tables": 20,
        "authentication_integration": "auth-service:8001"
    }

# Optional: Add middleware for debugging
@app.middleware("http")
async def debug_middleware(request, call_next):
    """Debug middleware to log requests in development"""
    if os.getenv("ENVIRONMENT") == "development":
        print(f"🔍 {request.method} {request.url}")
    
    response = await call_next(request)
    return response

# # property-service/src/app.py (Simplified version - replace your current app.py with this)
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# import os

# # Create FastAPI application
# app = FastAPI(
#     title="Selgo Property Service",
#     description="Property management service for Selgo marketplace",
#     version="2.0.0",
#     docs_url="/docs",
#     redoc_url="/redoc"
# )

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.on_event("startup")
# async def startup_event():
#     """Startup event"""
#     try:
#         print("🚀 Property Service started successfully!")
#         print("📊 API Documentation: /docs")
#         print("⚠️  Database initialization temporarily disabled for testing")
#     except Exception as e:
#         print(f"❌ Startup error: {e}")

# @app.get("/")
# async def root():
#     """Root endpoint"""
#     return {
#         "service": "Selgo Property Service",
#         "status": "running",
#         "version": "2.0.0",
#         "message": "Service is running in test mode",
#         "endpoints": {
#             "health": "/health",
#             "docs": "/docs",
#             "test": "/test"
#         }
#     }

# @app.get("/health")
# async def health_check():
#     """Health check endpoint"""
#     return {
#         "status": "healthy",
#         "service": "property-service",
#         "version": "2.0.0",
#         "environment": os.getenv("ENVIRONMENT", "development")
#     }

# @app.get("/test")
# async def test_endpoint():
#     """Test endpoint to verify service is working"""
#     return {
#         "message": "Property service is working!",
#         "environment": os.getenv("ENVIRONMENT", "development"),
#         "database_host": os.getenv("DB_HOST", "localhost"),
#         "database_name": os.getenv("DB_NAME", "selgo_property"),
#         "api_port": os.getenv("API_PORT", "8004"),
#         "timestamp": "2024-01-01T12:00:00Z"
#     }

# @app.get("/api/properties/categories")
# async def get_categories():
#     """Temporary mock endpoint for testing"""
#     return [
#         {"id": 1, "label": "Plots", "type": "purchase", "icon": "1.svg"},
#         {"id": 2, "label": "Housing for Sale", "type": "purchase", "icon": "3.svg"},
#         {"id": 3, "label": "Apartments for Rent", "type": "rent", "icon": "7.svg"}
#     ]

# @app.get("/api/properties/featured")
# async def get_featured():
#     """Temporary mock endpoint for testing"""
#     return [
#         {
#             "id": "123e4567-e89b-12d3-a456-426614174000",
#             "title": "Beautiful Oslo Apartment",
#             "price": 4500000,
#             "bedrooms": 3,
#             "city": "Oslo",
#             "property_type": "purchase"
#         },
#         {
#             "id": "123e4567-e89b-12d3-a456-426614174001", 
#             "title": "Bergen House with Garden",
#             "price": 3200000,
#             "bedrooms": 4,
#             "city": "Bergen",
#             "property_type": "purchase"
#         }
#     ]

# # Add debug middleware
# @app.middleware("http")
# async def debug_middleware(request, call_next):
#     """Debug middleware"""
#     if os.getenv("ENVIRONMENT") == "development":
#         print(f"🔍 {request.method} {request.url}")
    
#     response = await call_next(request)
#     return response
=======
# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)

# Mount static files directory for uploads
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_FOLDER), name="uploads")

# Include routers
app.include_router(property_router)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "property", "version": "0.1.0"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "service": "property",
        "version": "0.1.0",
        "description": "API for property listings and related operations",
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
>>>>>>> ef864b3 (Replace Features branch with selgo-feature contents)
