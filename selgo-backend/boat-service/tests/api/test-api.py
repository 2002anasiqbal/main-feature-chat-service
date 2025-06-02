import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.app import app
from src.database.database import get_db, Base
from src.models.boat_models import BoatCategory, BoatFeature

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
@pytest.fixture
def override_get_db():
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    
    # Create a new session for each test
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        
        # Drop all tables after the test
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_client(override_get_db):
    # Override the get_db dependency
    def _get_test_db():
        try:
            db = override_get_db
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = _get_test_db
    
    # Create a test client
    with TestClient(app) as client:
        yield client
    
    # Reset the dependency override
    app.dependency_overrides = {}

@pytest.fixture
def seed_test_data(override_get_db):
    """
    Seed test data into the database
    """
    db = override_get_db
    
    # Create test categories
    category1 = BoatCategory(label="Test Category 1", icon="test1.svg")
    category2 = BoatCategory(label="Test Category 2", icon="test2.svg")
    db.add(category1)
    db.add(category2)
    
    # Create test features
    feature1 = BoatFeature(name="Test Feature 1")
    feature2 = BoatFeature(name="Test Feature 2")
    db.add(feature1)
    db.add(feature2)
    
    db.commit()
    
    # Refresh to get the IDs
    db.refresh(category1)
    db.refresh(category2)
    db.refresh(feature1)
    db.refresh(feature2)
    
    # Return the test data for use in tests
    return {
        "categories": [category1, category2],
        "features": [feature1, feature2]
    }

# Mock current user ID for testing
@pytest.fixture
def mock_current_user_id():
    """
    Mock the get_current_user_id dependency to return a fixed user ID
    """
    app.dependency_overrides[get_current_user_id] = lambda: 1
    yield
    app.dependency_overrides = {}

# Tests for boat categories API
class TestBoatCategoriesAPI:
    def test_get_all_categories(self, test_client, seed_test_data):
        response = test_client.get("/api/v1/boats/categories")
        assert response.status_code == 200
        assert len(response.json()) == 2
        
    def test_get_category_by_id(self, test_client, seed_test_data):
        category_id = seed_test_data["categories"][0].id
        response = test_client.get(f"/api/v1/boats/categories/{category_id}")
        assert response.status_code == 200
        assert response.json()["id"] == category_id
        
    def test_create_category(self, test_client, mock_current_user_id):
        category_data = {
            "label": "New Test Category",
            "icon": "new_test.svg"
        }
        response = test_client.post(
            "/api/v1/boats/categories",
            json=category_data
        )
        assert response.status_code == 201
        assert response.json()["label"] == category_data["label"]
        
    def test_update_category(self, test_client, seed_test_data, mock_current_user_id):
        category_id = seed_test_data["categories"][0].id
        updated_data = {
            "label": "Updated Test Category",
            "icon": "updated_test.svg"
        }
        response = test_client.put(
            f"/api/v1/boats/categories/{category_id}",
            json=updated_data
        )
        assert response.status_code == 200
        assert response.json()["label"] == updated_data["label"]
        
    def test_delete_category(self, test_client, seed_test_data, mock_current_user_id):
        category_id = seed_test_data["categories"][0].id
        response = test_client.delete(f"/api/v1/boats/categories/{category_id}")
        assert response.status_code == 204
        
        # Verify it's deleted
        response = test_client.get(f"/api/v1/boats/categories/{category_id}")
        assert response.status_code == 404

# Tests for boat features API
class TestBoatFeaturesAPI:
    def test_get_all_features(self, test_client, seed_test_data):
        response = test_client.get("/api/v1/boats/features")
        assert response.status_code == 200
        assert len(response.json()) == 2
        
    def test_get_feature_by_id(self, test_client, seed_test_data):
        feature_id = seed_test_data["features"][0].id
        response = test_client.get(f"/api/v1/boats/features/{feature_id}")
        assert response.status_code == 200
        assert response.json()["id"] == feature_id
        
    def test_create_feature(self, test_client, mock_current_user_id):
        feature_data = {
            "name": "New Test Feature"
        }
        response = test_client.post(
            "/api/v1/boats/features",
            json=feature_data
        )
        assert response.status_code == 201
        assert response.json()["name"] == feature_data["name"]
        
    def test_update_feature(self, test_client, seed_test_data, mock_current_user_id):
        feature_id = seed_test_data["features"][0].id
        updated_data = {
            "name": "Updated Test Feature"
        }
        response = test_client.put(
            f"/api/v1/boats/features/{feature_id}",
            json=updated_data
        )
        assert response.status_code == 200
        assert response.json()["name"] == updated_data["name"]
        
    def test_delete_feature(self, test_client, seed_test_data, mock_current_user_id):
        feature_id = seed_test_data["features"][0].id
        response = test_client.delete(f"/api/v1/boats/features/{feature_id}")
        assert response.status_code == 204
        
        # Verify it's deleted
        response = test_client.get(f"/api/v1/boats/features/{feature_id}")
        assert response.status_code == 404

# Tests for boat listings API
class TestBoatListingsAPI:
    # You can add more tests for boat listings here
    pass

# Tests for loan estimation API
class TestLoanEstimationAPI:
    def test_loan_estimation(self, test_client):
        loan_data = {
            "price": 50000,
            "duration": 60,  # 5 years
            "interest_rate": 5.5
        }
        response = test_client.post(
            "/api/v1/boats/loan-estimate",
            json=loan_data
        )
        assert response.status_code == 200
        result = response.json()
        assert "monthly_payment" in result
        assert "total_interest" in result
        assert "total_payable" in result
        assert "breakdown" in result
