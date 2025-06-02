# update_boat_locations.py
import os
import sys
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from geoalchemy2 import WKTElement
import random

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
load_dotenv()

from src.database.database import SessionLocal
from src.models.boat_models import Boat

def add_locations_to_boats():
    db = SessionLocal()
    try:
        # Get all boats without location
        boats_without_location = db.query(Boat).filter(Boat.location == None).all()
        
        # List of sample locations
        locations = [
            {"lat": 25.7617, "lon": -80.1918, "name": "Miami, FL"},
            {"lat": 32.7157, "lon": -117.1611, "name": "San Diego, CA"},
            {"lat": 27.9506, "lon": -82.4572, "name": "Tampa, FL"},
            {"lat": 47.6062, "lon": -122.3321, "name": "Seattle, WA"},
            {"lat": 41.8781, "lon": -87.6298, "name": "Chicago, IL"},
            {"lat": 29.7604, "lon": -95.3698, "name": "Houston, TX"},
            {"lat": 42.3601, "lon": -71.0589, "name": "Boston, MA"},
            {"lat": 33.4484, "lon": -112.0740, "name": "Phoenix, AZ"},
        ]
        
        for boat in boats_without_location:
            # Pick a random location
            location = random.choice(locations)
            
            # Update the boat
            boat.location = WKTElement(f'POINT({location["lon"]} {location["lat"]})', srid=4326)
            boat.location_name = location["name"]
            
            print(f"Updated boat {boat.id} - {boat.title} with location {location['name']}")
        
        db.commit()
        print(f"Successfully updated {len(boats_without_location)} boats with locations")
        
    except Exception as e:
        print(f"Error updating locations: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_locations_to_boats()