# Create this file to add real users
from src.database import SessionLocal
from src.models import User
from datetime import datetime

def create_real_users():
    db = SessionLocal()
    
    try:
        # Check if users exist
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"Found {existing_users} existing users")
            return
        
        # Create real users
        users = [
            {"name": "John Smith", "email": "john.smith@example.com", "phone": "+47 123 45 678"},
            {"name": "Sarah Johnson", "email": "sarah.johnson@example.com", "phone": "+47 987 65 432"},
            {"name": "Mike Anderson", "email": "mike.anderson@example.com", "phone": "+47 555 12 345"},
            {"name": "Emma Wilson", "email": "emma.wilson@example.com", "phone": "+47 444 33 222"},
            {"name": "David Brown", "email": "david.brown@example.com", "phone": "+47 777 88 999"},
        ]
        
        for user_data in users:
            user = User(**user_data)
            db.add(user)
        
        db.commit()
        print("✅ Real users created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_real_users()