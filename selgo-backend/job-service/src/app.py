# File: job-service/src/app.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config.config import settings
from .database.database import engine, Base
from .api.routes import router as main_router
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Selgo Job Service",
    description="Job management and CV builder service for Selgo marketplace",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploads
uploads_dir = "uploads"
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)
    os.makedirs(os.path.join(uploads_dir, "cvs"))
    os.makedirs(os.path.join(uploads_dir, "profiles"))

app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Include routers
app.include_router(main_router, prefix=settings.API_PREFIX)

@app.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "service": "job", 
        "version": "1.0.0",
        "database": "connected"
    }

@app.get("/")
def root():
    return {
        "service": "job",
        "version": "1.0.0",
        "description": "Job management and CV builder service for Selgo marketplace",
        "docs": "/docs"
    }

@app.on_event("startup")
def startup_event():
    try:
        # Create database tables
        Base.metadata.create_all(bind=engine)
        logger.info("Job database tables created successfully")
        
        # Create CV template file if it doesn't exist
        template_dir = "templates"
        if not os.path.exists(template_dir):
            os.makedirs(template_dir)
        
        template_file = os.path.join(template_dir, "cv_template.html")
        if not os.path.exists(template_file):
            from .utils.pdf_utils import create_cv_template_html
            with open(template_file, 'w') as f:
                f.write(create_cv_template_html())
            logger.info("CV template created successfully")
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")