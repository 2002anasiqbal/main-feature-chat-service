import os
import sys
import logging
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from geoalchemy2 import WKTElement
# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Load environment variables from .env file
load_dotenv()

from src.database.database import SessionLocal
import random
from src.models.boat_models import BoatCategory, BoatFeature, Boat, BoatImage, BoatCondition, SellerType, AdType



# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def seed_boat_categories(db: Session):
    """
    Seed the database with boat categories.
    """
    # Check if we already have categories
    existing_categories = db.query(BoatCategory).all()
    if existing_categories:
        logger.info(f"Database already has {len(existing_categories)} categories. Skipping seeding.")
        return
    
    # Define top-level categories
    top_level_categories = [
        {"label": "Buy Boats", "icon": "1.svg"},
        {"label": "Buy Boats Abroad", "icon": "2.svg"},
        {"label": "Boats in Norway", "icon": "3.svg"},
        {"label": "Vans abroad", "icon": "4.svg"},
        {"label": "Boats parts", "icon": "5.svg"},
        {"label": "Boats", "icon": "6.svg"},
        {"label": "Boats for rent", "icon": "7.svg"},
        {"label": "Boats for sale", "icon": "8.svg"},
    ]
    
    # Create and add top-level categories
    created_categories = {}
    for category_data in top_level_categories:
        category = BoatCategory(**category_data)
        db.add(category)
        db.flush()  # Flush to get the ID
        created_categories[category.label] = category
    
    # Define subcategories
    subcategories = [
        # Buy Boats subcategories
        {"label": "Motor Boats", "icon": "motor_boat.svg", "parent": "Buy Boats"},
        {"label": "Sail Boats", "icon": "sail_boat.svg", "parent": "Buy Boats"},
        {"label": "Fishing Boats", "icon": "fishing_boat.svg", "parent": "Buy Boats"},
        {"label": "Yachts", "icon": "yacht.svg", "parent": "Buy Boats"},
        {"label": "Jet Skis", "icon": "jet_ski.svg", "parent": "Buy Boats"},
        
        # Boats subcategories
        {"label": "Kayaks", "icon": "kayak.svg", "parent": "Boats"},
        {"label": "Canoes", "icon": "canoe.svg", "parent": "Boats"},
        {"label": "Dinghies", "icon": "dinghy.svg", "parent": "Boats"},
        {"label": "Inflatable Boats", "icon": "inflatable.svg", "parent": "Boats"},
        
        # Boats for rent subcategories
        {"label": "Daily Rental", "icon": "daily.svg", "parent": "Boats for rent"},
        {"label": "Weekly Rental", "icon": "weekly.svg", "parent": "Boats for rent"},
        {"label": "Monthly Rental", "icon": "monthly.svg", "parent": "Boats for rent"},
    ]
    
    # Create and add subcategories
    for subcategory_data in subcategories:
        parent_label = subcategory_data.pop("parent")
        parent = created_categories.get(parent_label)
        if parent:
            subcategory_data["parent_id"] = parent.id
            subcategory = BoatCategory(**subcategory_data)
            db.add(subcategory)
    
    # Commit the transaction
    db.commit()
    
    logger.info(f"Added {len(top_level_categories)} top-level categories and {len(subcategories)} subcategories")

def seed_boat_features(db: Session):
    """
    Seed the database with boat features.
    """
    # Check if we already have features
    existing_features = db.query(BoatFeature).all()
    if existing_features:
        logger.info(f"Database already has {len(existing_features)} features. Skipping seeding.")
        return
    
    # Define features
    features = [
        {"name": "GPS Navigation"},
        {"name": "Fish Finder"},
        {"name": "Radar"},
        {"name": "Autopilot"},
        {"name": "Cabin"},
        {"name": "Toilet"},
        {"name": "Shower"},
        {"name": "Kitchen"},
        {"name": "Refrigerator"},
        {"name": "Air Conditioning"},
        {"name": "Heating"},
        {"name": "TV"},
        {"name": "Sound System"},
        {"name": "Swimming Platform"},
        {"name": "Anchor Winch"},
        {"name": "Bow Thruster"},
        {"name": "Life Jackets"},
        {"name": "Safety Equipment"},
        {"name": "Fishing Equipment"},
        {"name": "Water Sports Equipment"},
    ]
    
    # Create and add features
    for feature_data in features:
        feature = BoatFeature(**feature_data)
        db.add(feature)
    
    # Commit the transaction
    db.commit()
    
    logger.info(f"Added {len(features)} boat features")

# Modify your seed-db.py script to include boat listings


def seed_boat_listings(db: Session):
    """
    Seed the database with sample boat listings.
    """
    # Check if boats already exist
    existing_boats = db.query(Boat).all()
    if existing_boats:
        logger.info(f"Database already has {len(existing_boats)} boats. Skipping seeding.")
        return
    
    # Get categories and features for reference
    categories = db.query(BoatCategory).all()
    features = db.query(BoatFeature).all()
    
    if not categories or not features:
        logger.warning("No categories or features found. Make sure to run seed_boat_categories and seed_boat_features first.")
        return
    
    # Define sample boats
    boats = [
        {
            "title": "Luxury Yacht 2023",
            "description": "Beautiful yacht in excellent condition with spacious cabin, modern navigation equipment, and powerful engines. Perfect for luxury cruising and entertaining guests.",
            "price": 150000.0,
            "category_id": next((c.id for c in categories if c.label == "Buy Boats"), categories[0].id),
            "condition": BoatCondition.EXCELLENT,
            "year": 2023,
            "make": "Sea Ray",
            "model": "Sundancer",
            "length": 35.0,
            "beam": 10.0,
            "draft": 3.0,
            "fuel_type": "Diesel",
            "hull_material": "Fiberglass",
            "engine_make": "Mercury",
            "engine_model": "Verado",
            "engine_hours": 120,
            "engine_power": 350,
            "user_id": 1,
            "location": WKTElement(f'POINT(-80.1918 25.7617)', srid=4326),
            "location_name": "Miami, FL",
            "seller_type": SellerType.DEALER,
            "ad_type": AdType.FOR_SALE,
            "is_featured": True,
            "status": "active"
        },
        {
            "title": "Sailboat for Weekend Adventures",
            "description": "Perfect sailboat for casual sailing with family and friends. Well-maintained, easy to handle, and ready for your next adventure on the water.",
            "price": 45000.0,
            "category_id": next((c.id for c in categories if "Sail" in c.label), categories[0].id),
            "condition": BoatCondition.GOOD,
            "year": 2019,
            "make": "Catalina",
            "model": "27",
            "length": 27.0,
            "beam": 8.5,
            "draft": 4.0,
            "fuel_type": "Gasoline",
            "hull_material": "Fiberglass",
            "user_id": 1,
            "location": WKTElement(f'POINT(-117.1611 32.7157)', srid=4326),
            "location_name": "San Diego, CA",
            "seller_type": SellerType.PRIVATE,
            "ad_type": AdType.FOR_SALE,
            "status": "active"
        },
        {
            "title": "Fishing Boat with Equipment",
            "description": "Great fishing boat with all necessary equipment included. Features fish finder, rod holders, live well, and plenty of storage. Ready for your next fishing trip.",
            "price": 28500.0,
            "category_id": next((c.id for c in categories if "Fishing" in c.label), categories[0].id),
            "condition": BoatCondition.GOOD,
            "year": 2020,
            "make": "Boston Whaler",
            "model": "190 Montauk",
            "length": 19.0,
            "beam": 8.0,
            "user_id": 1,
            "location": WKTElement(f'POINT(-82.4572 27.9506)', srid=4326),
            "location_name": "Tampa, FL",
            "seller_type": SellerType.PRIVATE,
            "ad_type": AdType.FOR_SALE,
            "status": "active"
        },
        {
            "title": "Pontoon Boat for Rent",
            "description": "Spacious pontoon boat available for daily or weekly rental. Perfect for parties, fishing, or relaxing on the water with family and friends.",
            "price": 250.0,  # Daily rental price
            "category_id": next((c.id for c in categories if "rent" in c.label.lower()), categories[0].id),
            "condition": BoatCondition.EXCELLENT,
            "year": 2022,
            "make": "Bennington",
            "model": "S Series",
            "length": 22.0,
            "user_id": 1,
            "location_name": "Lake Tahoe, NV",
            "seller_type": SellerType.DEALER,
            "ad_type": AdType.FOR_RENT,
            "status": "active"
        },
        {
            "title": "Classic Wooden Sailboat",
            "description": "Beautiful wooden sailboat with classic design and craftsmanship. Lovingly maintained and restored. Must see to appreciate the detailed woodwork.",
            "price": 35000.0,
            "category_id": next((c.id for c in categories if "Boats" in c.label), categories[0].id),
            "condition": BoatCondition.GOOD,
            "year": 1985,
            "make": "Custom",
            "model": "Ketch",
            "length": 30.0,
            "beam": 9.0,
            "draft": 4.5,
            "hull_material": "Wood",
            "user_id": 1,
            "location_name": "Portland, ME",
            "seller_type": SellerType.PRIVATE,
            "ad_type": AdType.FOR_SALE,
            "status": "active"
        },
        {
            "title": "Jet Ski - 2021 Model",
            "description": "Like-new jet ski with low hours. Fast, fun, and ready for the water. Includes trailer and life vests.",
            "price": 9500.0,
            "category_id": next((c.id for c in categories if c.label == "Boats"), categories[0].id),
            "condition": BoatCondition.LIKE_NEW,
            "year": 2021,
            "make": "Yamaha",
            "model": "WaveRunner VX",
            "length": 11.0,
            "user_id": 1,
            "location_name": "Orlando, FL",
            "seller_type": SellerType.PRIVATE,
            "ad_type": AdType.FOR_SALE,
            "status": "active"
        },
        {
            "title": "Aluminum Fishing Boat Package",
            "description": "Complete fishing boat package with motor, trailer, and electronics. Perfect for lakes and rivers. Includes fish finder and trolling motor.",
            "price": 12000.0,
            "category_id": next((c.id for c in categories if c.label == "Boats for sale"), categories[0].id),
            "condition": BoatCondition.GOOD,
            "year": 2018,
            "make": "Lund",
            "model": "1600 Fury",
            "length": 16.0,
            "user_id": 1,
            "location_name": "Minneapolis, MN",
            "seller_type": SellerType.PRIVATE,
            "ad_type": AdType.FOR_SALE,
            "status": "active"
        },
        {
            "title": "Boat Engine - Mercury Outboard",
            "description": "Mercury outboard engine in excellent condition. Low hours, regular maintenance. Perfect replacement or upgrade for your boat.",
            "price": 4500.0,
            "category_id": next((c.id for c in categories if "parts" in c.label.lower()), categories[0].id),
            "condition": BoatCondition.EXCELLENT,
            "year": 2020,
            "make": "Mercury",
            "model": "115HP Four Stroke",
            "user_id": 1,
            "location_name": "Seattle, WA",
            "seller_type": SellerType.DEALER,
            "ad_type": AdType.FOR_SALE,
            "status": "active"
        }
    ]
    
    # Sample image URLs (using placeholder images)
    sample_images = [
        "https://picsum.photos/800/600?random=1",
        "https://picsum.photos/800/600?random=2",
        "https://picsum.photos/800/600?random=3",
        "https://picsum.photos/800/600?random=4",
        "https://picsum.photos/800/600?random=5",
        "https://picsum.photos/800/600?random=6",
        "https://picsum.photos/800/600?random=7",
        "https://picsum.photos/800/600?random=8"
    ]
    
    # Create and add boats
    for boat_data in boats:
        boat = Boat(**boat_data)
        
        # Add some features - select 2-4 random features
        num_features = min(random.randint(2, 4), len(features))
        boat.features = random.sample(features, num_features)
        
        db.add(boat)
        db.commit()
        db.refresh(boat)
        
        # Add images - 2-4 random images, first one is primary
        num_images = random.randint(2, 4)
        images_for_boat = []
        
        for i in range(num_images):
            image_url = random.choice(sample_images)
            is_primary = (i == 0)  # First image is primary
            
            image = BoatImage(
                boat_id=boat.id,
                image_url=image_url,
                is_primary=is_primary
            )
            images_for_boat.append(image)
        
        db.add_all(images_for_boat)
    
    # Commit all images
    db.commit()
    logger.info(f"Added {len(boats)} sample boats with images and features")


def main():
    """
    Main function to seed the database.
    """
    db = SessionLocal()
    try:
        logger.info("Starting database seeding...")
        
        # Seed boat categories
        seed_boat_categories(db)
        
        # Seed boat features
        seed_boat_features(db)
        
        # Seed boat listings
        seed_boat_listings(db)
        logger.info("Database seeding completed successfully")
    
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
    
    finally:
        db.close()

if __name__ == "__main__":
    main()
