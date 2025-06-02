# add_test_boats.py (improved version)

from sqlalchemy.orm import Session
from sqlalchemy import text
from src.database.database import SessionLocal, engine
from src.models.boat_models import Boat, BoatImage, BoatCondition, SellerType, AdType
import random

def add_test_boats():
    db = SessionLocal()
    try:
        # Get existing categories and features for reference
        from src.models.boat_models import BoatCategory, BoatFeature
        categories = db.query(BoatCategory).all()
        features = db.query(BoatFeature).all()
        
        # Make sure we have categories and features
        if not categories or not features:
            print("No categories or features found. Please run the main seed script first.")
            return
        
        # Create diverse test boats
        test_boats = [
            # New boat with specific location
            {
                "title": "NEW Test Boat with Location",
                "description": "Test boat for filtering",
                "price": 25000.0,
                "category_id": categories[0].id,
                "condition": BoatCondition.NEW,
                "year": 2023,
                "make": "Test",
                "model": "FilterTest-1",
                "length": 25.0,
                "user_id": 1,
                "location_name": "Oslo, Norway",
                "seller_type": SellerType.DEALER,
                "ad_type": AdType.FOR_SALE,
                "status": "active"
            },
            # Project boat with location
            {
                "title": "PROJECT BOAT Test",
                "description": "Test project boat for filtering",
                "price": 5000.0,
                "category_id": categories[0].id,
                "condition": BoatCondition.PROJECT_BOAT,
                "year": 2000,
                "make": "Test",
                "model": "FilterTest-2",
                "length": 15.0,
                "user_id": 1,
                "location_name": "Stockholm, Sweden",
                "seller_type": SellerType.PRIVATE,
                "ad_type": AdType.FOR_SALE,
                "status": "active"
            },
            # Rental boat
            {
                "title": "FOR RENT Test Boat",
                "description": "Test boat for rent",
                "price": 200.0,
                "category_id": categories[0].id,
                "condition": BoatCondition.EXCELLENT,
                "year": 2022,
                "make": "Test",
                "model": "FilterTest-3",
                "length": 30.0,
                "user_id": 1,
                "location_name": "Copenhagen, Denmark",
                "seller_type": SellerType.DEALER,
                "ad_type": AdType.FOR_RENT,
                "status": "active"
            }
        ]
        
        # Dictionary to store created boat IDs
        created_boat_ids = {}
        
        # Add the test boats to database
        for i, boat_data in enumerate(test_boats):
            # Make a copy to avoid modifying the original
            data_for_boat = boat_data.copy()
            
            boat = Boat(**data_for_boat)
            
            # Add some features to each boat
            num_features = min(random.randint(2, 4), len(features))
            boat.features = random.sample(features, num_features)
            
            db.add(boat)
            db.commit()
            db.refresh(boat)
            
            # Store the ID for location update
            created_boat_ids[i] = boat.id
            
            # Add a sample image
            image = BoatImage(
                boat_id=boat.id,
                image_url="https://picsum.photos/800/600?random=" + str(random.randint(1, 1000)),
                is_primary=True
            )
            db.add(image)
            db.commit()
        
        # Now update locations using proper SQLAlchemy text() function
        locations = [
            (0, "SRID=4326;POINT(10.7522 59.9139)"),  # Oslo for boat 1
            (1, "SRID=4326;POINT(18.0686 59.3293)"),  # Stockholm for boat 2
            (2, "SRID=4326;POINT(12.5683 55.6761)")   # Copenhagen for boat 3
        ]
        
        # Use proper SQLAlchemy text() for raw SQL
        with engine.connect() as connection:
            for i, location_wkt in locations:
                boat_id = created_boat_ids.get(i)
                if boat_id:
                    sql = text(f"UPDATE boats SET location = ST_GeomFromEWKT(:location) WHERE id = :id")
                    connection.execute(sql, {"location": location_wkt, "id": boat_id})
            
            connection.commit()
        
        print(f"Added {len(test_boats)} test boats for filter testing with IDs: {list(created_boat_ids.values())}")
        
    except Exception as e:
        print(f"Error adding test boats: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_test_boats()