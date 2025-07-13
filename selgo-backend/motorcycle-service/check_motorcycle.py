# selgo-backend/motorcycle-service/check_motorcycle.py
from src.database import SessionLocal
from src.models import Motorcycle, MotorcycleCategory
from sqlalchemy import desc, text

def check_motorcycles():
    """Check motorcycles in database"""
    db = SessionLocal()
    
    try:
        # Get total count
        total = db.query(Motorcycle).count()
        active_total = db.query(Motorcycle).filter(Motorcycle.is_active == True).count()
        print(f"📊 Total motorcycles: {total}")
        print(f"📊 Active motorcycles: {active_total}")
        
        # Get all motorcycles ordered by ID
        motorcycles = db.query(Motorcycle).order_by(desc(Motorcycle.id)).all()
        
        print(f"\n🏍️ All motorcycles (latest first):")
        for i, motorcycle in enumerate(motorcycles):
            print(f"{i+1:2d}. ID: {motorcycle.id:2d} | Active: {motorcycle.is_active} | Title: {motorcycle.title[:50]}")
        
        # Check the search query that frontend uses
        print(f"\n🔍 Testing search query (active motorcycles, latest first):")
        search_result = db.query(Motorcycle).filter(
            Motorcycle.is_active == True
        ).order_by(
            Motorcycle.is_featured.desc(),
            Motorcycle.created_at.desc()
        ).limit(20).all()
        
        print(f"Search result count: {len(search_result)}")
        for i, motorcycle in enumerate(search_result):
            print(f"{i+1:2d}. ID: {motorcycle.id:2d} | Featured: {motorcycle.is_featured} | Created: {motorcycle.created_at}")
        
        # Check the newest motorcycle specifically
        newest = db.query(Motorcycle).order_by(desc(Motorcycle.id)).first()
        if newest:
            print(f"\n🆕 Newest motorcycle details:")
            print(f"ID: {newest.id}")
            print(f"Title: {newest.title}")
            print(f"Active: {newest.is_active}")
            print(f"Featured: {newest.is_featured}")
            print(f"Category ID: {newest.category_id}")
            print(f"Created: {newest.created_at}")
            
            # Check if it has images
            print(f"Images: {len(newest.images) if newest.images else 0}")
            if newest.images:
                for img in newest.images:
                    print(f"  - {img.image_url} (Primary: {img.is_primary})")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_motorcycles()