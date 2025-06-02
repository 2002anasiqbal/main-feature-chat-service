# delete_test_boats.py

from sqlalchemy.orm import Session
from sqlalchemy import text
from src.database.database import SessionLocal, engine
from src.models.boat_models import Boat, BoatImage

def delete_test_boats():
    """Delete test boats from the database"""
    db = SessionLocal()
    try:
        # Method 1: Delete by specific patterns used in test boats
        # This targets the test boats created by your add_test_boats.py script
        
        # Find test boats by title patterns or make/model patterns
        test_boat_queries = [
            # By title patterns
            db.query(Boat).filter(Boat.title.like('%Test Boat%')),
            db.query(Boat).filter(Boat.title.like('%TEST%')),
            db.query(Boat).filter(Boat.title.like('%FilterTest%')),
            
            # By make/model patterns
            db.query(Boat).filter(Boat.make == 'Test'),
            db.query(Boat).filter(Boat.model.like('FilterTest-%')),
            
            # By specific test locations
            db.query(Boat).filter(Boat.location_name.in_([
                'Oslo, Norway', 
                'Stockholm, Sweden', 
                'Copenhagen, Denmark'
            ])).filter(Boat.make == 'Test')
        ]
        
        # Collect all test boats
        test_boats = set()  # Use set to avoid duplicates
        for query in test_boat_queries:
            boats = query.all()
            test_boats.update(boats)
        
        test_boats = list(test_boats)
        
        if not test_boats:
            print("No test boats found to delete.")
            return
        
        print(f"Found {len(test_boats)} test boats:")
        for boat in test_boats:
            print(f"  - ID: {boat.id}, Title: {boat.title}, Make: {boat.make}, Model: {boat.model}")
        
        # Ask for confirmation
        response = input(f"\nAre you sure you want to delete these {len(test_boats)} test boats? (y/N): ")
        if response.lower() not in ['y', 'yes']:
            print("Deletion cancelled.")
            return
        
        # Delete associated images first (due to foreign key constraints)
        boat_ids = [boat.id for boat in test_boats]
        images_deleted = db.query(BoatImage).filter(BoatImage.boat_id.in_(boat_ids)).delete(synchronize_session=False)
        
        # Delete the boats
        boats_deleted = 0
        for boat in test_boats:
            db.delete(boat)
            boats_deleted += 1
        
        # Commit the changes
        db.commit()
        
        print(f"Successfully deleted:")
        print(f"  - {boats_deleted} test boats")
        print(f"  - {images_deleted} associated images")
        
    except Exception as e:
        print(f"Error deleting test boats: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def delete_boats_by_ids(boat_ids):
    """Delete specific boats by their IDs"""
    db = SessionLocal()
    try:
        # Convert to list if single ID provided
        if isinstance(boat_ids, int):
            boat_ids = [boat_ids]
        
        # Find boats
        boats = db.query(Boat).filter(Boat.id.in_(boat_ids)).all()
        
        if not boats:
            print("No boats found with the provided IDs.")
            return
        
        print(f"Found {len(boats)} boats to delete:")
        for boat in boats:
            print(f"  - ID: {boat.id}, Title: {boat.title}")
        
        # Ask for confirmation
        response = input(f"\nAre you sure you want to delete these {len(boats)} boats? (y/N): ")
        if response.lower() not in ['y', 'yes']:
            print("Deletion cancelled.")
            return
        
        # Delete associated images first
        images_deleted = db.query(BoatImage).filter(BoatImage.boat_id.in_(boat_ids)).delete(synchronize_session=False)
        
        # Delete boats
        boats_deleted = 0
        for boat in boats:
            db.delete(boat)
            boats_deleted += 1
        
        db.commit()
        
        print(f"Successfully deleted:")
        print(f"  - {boats_deleted} boats")
        print(f"  - {images_deleted} associated images")
        
    except Exception as e:
        print(f"Error deleting boats: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def list_all_boats():
    """List all boats in the database for reference"""
    db = SessionLocal()
    try:
        boats = db.query(Boat).all()
        print(f"Total boats in database: {len(boats)}")
        
        if boats:
            print("\nAll boats:")
            for boat in boats:
                print(f"  - ID: {boat.id}, Title: {boat.title}, Make: {boat.make}, Model: {boat.model}")
    except Exception as e:
        print(f"Error listing boats: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "list":
            list_all_boats()
        elif sys.argv[1] == "ids":
            if len(sys.argv) < 3:
                print("Usage: python delete_test_boats.py ids <id1> <id2> ...")
                sys.exit(1)
            try:
                boat_ids = [int(id_str) for id_str in sys.argv[2:]]
                delete_boats_by_ids(boat_ids)
            except ValueError:
                print("Error: All IDs must be valid integers")
                sys.exit(1)
        else:
            print("Usage:")
            print("  python delete_test_boats.py           # Delete test boats by pattern")
            print("  python delete_test_boats.py list      # List all boats")
            print("  python delete_test_boats.py ids 1 2 3 # Delete specific boats by ID")
    else:
        delete_test_boats()