from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config.config import settings
from .database.database import engine, Base
from .api.routes import router as auth_router, user_router  # Import both routers
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Selgo Auth Service",
    description="Centralized authentication service for Selgo marketplace",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include both routers
app.include_router(auth_router)      # /api/v1/auth/*
app.include_router(user_router)      # /api/v1/users/*

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "auth", "version": "1.0.0"}

@app.get("/")
def root():
    return {
        "service": "auth",
        "version": "1.0.0",
        "description": "Centralized authentication service for Selgo marketplace"
    }

@app.on_event("startup")
def startup_event():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Auth database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating auth database tables: {e}")