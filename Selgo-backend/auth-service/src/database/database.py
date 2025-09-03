  
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config.config import settings
import logging

logger = logging.getLogger(__name__)

try:
    engine = create_engine(settings.DATABASE_URL)
    logger.info("Auth database engine created successfully")
except Exception as e:
    logger.error(f"Failed to create auth database engine: {e}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()