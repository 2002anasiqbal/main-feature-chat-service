import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
import sys

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app import app
from src.database.database import get_db, Base
from src.models.boat_models import BoatCategory, BoatFeature, Boat, BoatImage, BoatRating, BoatFixDoneRequest
from src.utils.auth import get_current_user_id

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """
    Create a clean database session for a test.
    
    Yields:
        Session: The database session
    """
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create a new session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        
        # Drop all tables
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """
    Create a FastAPI TestClient with a clean database session.
    
    Args:
        db_session: The database session fixture
        
    Yields:
        TestClient: The FastAPI test client
    """
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass  # Session is closed in the db_session fixture
    
    # Override the get_db dependency
    app.dependency_overrides[get_db] = _get_test_db
    
    # Mock the authentication
    app.dependency_overrides[get_current_user_id] = lambda: 1  # Mock user ID
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clear the dependency overrides
    app.dependency_overrides.clear()

@pytest.fixture
def seed_categories(db_session):
    """
    Seed the database with categories.
    
    Args:
        db_session: The database session fixture
        
    Returns:
        list: The created categories
    """
    categories = [
        BoatCategory(label="Motor Boats", icon="motor_boat.svg"),
        BoatCategory(label="Sail Boats", icon="sail_boat.svg"),
        BoatCategory(label="Fishing Boats", icon="fishing_boat.svg"),
    ]
    
    for category in categories:
        db_session.add(category)
    
    db_session.commit()
    
    # Refresh to get the IDs
    for category in categories:
        db_session.refresh(category)
    
    return categories

@pytest.fixture
def seed_features(db_session):
    """
    Seed the database with features.
    
    Args:
        db_session: The database session fixture
        
    Returns:
        list: The created features
    """
    features = [
        BoatFeature(name="GPS Navigation"),
        BoatFeature(name="Fish Finder"),
        BoatFeature(name="Radar"),
        BoatFeature(name="Autopilot"),
    ]
    
    for feature in features:
        db_session.add(feature)
    
    db_session.commit()
    
    # Refresh to get the IDs
    for feature in features:
        db_session.refresh(feature)
    
    return features

@pytest.fixture
def seed_boat(db_session, seed_categories, seed_features):
    """
    Seed the database with a boat.
    
    Args:
        db_session: The database session fixture
        seed_categories: The categories fixture
        seed_features: The features fixture
        
    Returns:
        Boat: The created boat
    """
    # Create a boat
    boat = Boat(
        title="Test Boat",
        description="This is a test boat",
        price=50000.0,
        category_id=seed_categories[0].id,
        year=2020,
        make="Test Make",
        model="Test Model",
        length=20.0,
        beam=5.0,
        draft=2.0,
        user_id=1,  # Mock user ID
        location_name="Test Location",
    )
    
    # Add features
    boat.features = seed_features[:2]  # First two features
    
    db_session.add(boat)
    db_session.commit()
    db_session.refresh(boat)
    
    # Add images
    images = [
        BoatImage(boat_id=boat.id, image_url="test1.jpg", is_primary=True),
        BoatImage(boat_id=boat.id, image_url="test2.jpg", is_primary=False),
    ]
    
    for image in images:
        db_session.add(image)
    
    db_session.commit()
    
    # Refresh the boat to include the relationships
    db_session.refresh(boat)
    
    return boat

@pytest.fixture
def seed_ratings(db_session, seed_boat):
    """
    Seed the database with ratings for a boat.
    
    Args:
        db_session: The database session fixture
        seed_boat: The boat fixture
        
    Returns:
        list: The created ratings
    """
    ratings = [
        BoatRating(boat_id=seed_boat.id, user_id=2, stars=5, review="Great boat!"),
        BoatRating(boat_id=seed_boat.id, user_id=3, stars=4, review="Nice boat!"),
    ]
    
    for rating in ratings:
        db_session.add(rating)
    
    db_session.commit()
    
    # Refresh to get the IDs
    for rating in ratings:
        db_session.refresh(rating)
    
    return ratings

@pytest.fixture
def seed_fix_request(db_session, seed_boat):
    """
    Seed the database with a fix request.
    
    Args:
        db_session: The database session fixture
        seed_boat: The boat fixture
        
    Returns:
        BoatFixDoneRequest: The created fix request
    """
    fix_request = BoatFixDoneRequest(
        boat_id=seed_boat.id,
        buyer_id=2,
        seller_id=1,  # Same as the boat's user_id
        status="requested",
        price=seed_boat.price,
        message="I want to buy this boat",
    )
    
    db_session.add(fix_request)
    db_session.commit()
    db_session.refresh(fix_request)
    
    return fix_request
