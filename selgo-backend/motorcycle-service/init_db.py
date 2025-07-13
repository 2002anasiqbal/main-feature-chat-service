# selgo-backend/motorcycle-service/init_db.py
from src.database import SessionLocal, create_tables
from src.models import MotorcycleCategory, User, Motorcycle, MotorcycleImage
from decimal import Decimal
import random

def seed_database():
    """Seed database with initial data"""
    db = SessionLocal()
    
    try:
        # Create tables
        create_tables()
        
        # Check if data already exists
        if db.query(MotorcycleCategory).first():
            print("Database already seeded")
            return
        
        print("🌱 Seeding database with initial data...")
        
        # Create categories
        categories = [
            {"name": "Thresher 6000", "slug": "thresher-6000", "icon": "1.svg"},
            {"name": "Suzuki 6000", "slug": "suzuki-6000", "icon": "2.svg"},
            {"name": "Motorcycles 6000", "slug": "motorcycles-6000", "icon": "3.svg"},
            {"name": "Auto bikes 6000", "slug": "auto-bikes-6000", "icon": "4.svg"},
            {"name": "Tractor 6000", "slug": "tractor-6000", "icon": "5.svg"},
            {"name": "Bikes 6000", "slug": "bikes-6000", "icon": "6.svg"},
        ]
        
        for cat_data in categories:
            category = MotorcycleCategory(**cat_data)
            db.add(category)
        
        db.commit()
        print("✅ Categories created")
        
        # Create sample users
        users = [
            {"name": "John Doe", "email": "john@example.com", "phone": "+47 123 45 678"},
            {"name": "Jane Smith", "email": "jane@example.com", "phone": "+47 987 65 432"},
            {"name": "Mike Johnson", "email": "mike@example.com", "phone": "+47 555 12 345"},
        ]
        
        for user_data in users:
            user = User(**user_data)
            db.add(user)
        
        db.commit()
        print("✅ Users created")
        
        # Get created categories and users
        db_categories = db.query(MotorcycleCategory).all()
        db_users = db.query(User).all()
        
        # Create sample motorcycles
        brands = ["Honda", "Yamaha", "Kawasaki", "Suzuki", "BMW", "Harley-Davidson", "Ducati"]
        models = ["CBR", "R1", "Ninja", "GSX-R", "GS", "Street", "Panigale"]
        cities = ["Oslo", "Bergen", "Trondheim", "Stavanger", "Kristiansand"]
        
        # Use string values directly
        conditions = ["new", "like_new", "excellent", "good", "fair", "poor"]
        motorcycle_types = ["adventure", "nakne", "touring", "sports", "cruiser", "scooter"]
        seller_types = ["private", "dealer"]
        
        for i in range(20):
            motorcycle = Motorcycle(
                title=f"{random.choice(brands)} {random.choice(models)} {random.randint(600, 1200)}",
                description=f"Excellent motorcycle in great condition. Well maintained and ready to ride.",
                brand=random.choice(brands),
                model=random.choice(models),
                year=random.randint(2010, 2024),
                engine_size=random.randint(250, 1200),
                mileage=random.randint(1000, 50000),
                price=Decimal(str(random.randint(50000, 500000))),
                condition=random.choice(conditions),
                motorcycle_type=random.choice(motorcycle_types),
                seller_type=random.choice(seller_types),
                city=random.choice(cities),
                address=f"Test Address {i+1}",
                category_id=random.choice(db_categories).id,
                seller_id=random.choice(db_users).id,
                is_featured=random.choice([True, False]),
                netbill=random.choice([True, False])
            )
            db.add(motorcycle)
            
            # Add some sample images
            if i % 3 == 0:  # Add images to every 3rd motorcycle
                db.flush()  # Get the motorcycle ID
                image = MotorcycleImage(
                    motorcycle_id=motorcycle.id,
                    image_url=f"https://picsum.photos/400/300?random={i}",
                    is_primary=True,
                    alt_text=f"{motorcycle.brand} {motorcycle.model}"
                )
                db.add(image)
        
        db.commit()
        print("✅ Sample motorcycles created")
        print("🎉 Database seeded successfully!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()