# selgo-backend/motorcycle-service/src/services/services.py
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, text
from geoalchemy2.functions import ST_DWithin, ST_GeogFromText, ST_Distance
from typing import List, Optional
from decimal import Decimal
import math
import requests
from geoalchemy2.functions import ST_GeogFromText
from ..models import models
from ..models import schemas
from ..utils.auth_client import auth_client

class MotorcycleService:    
    
    @staticmethod
    def create_motorcycle(db: Session, motorcycle: schemas.MotorcycleCreate) -> models.Motorcycle:
        # Create motorcycle data dict
        motorcycle_data = motorcycle.dict(exclude={'images'})
        
        # Convert enum objects to their string values (existing code)
        if hasattr(motorcycle_data.get('condition'), 'value'):
            motorcycle_data['condition'] = motorcycle_data['condition'].value
        elif isinstance(motorcycle_data.get('condition'), str):
            motorcycle_data['condition'] = motorcycle_data['condition']
            
        if hasattr(motorcycle_data.get('motorcycle_type'), 'value'):
            motorcycle_data['motorcycle_type'] = motorcycle_data['motorcycle_type'].value
        elif isinstance(motorcycle_data.get('motorcycle_type'), str):
            motorcycle_data['motorcycle_type'] = motorcycle_data['motorcycle_type']
            
        if hasattr(motorcycle_data.get('seller_type'), 'value'):
            motorcycle_data['seller_type'] = motorcycle_data['seller_type'].value
        elif isinstance(motorcycle_data.get('seller_type'), str):
            motorcycle_data['seller_type'] = motorcycle_data['seller_type']
        
        # NEW: Geocode the address to get coordinates
        address_to_geocode = motorcycle_data.get('address') or motorcycle_data.get('city')
        if address_to_geocode:
            print(f"🐛 DEBUG - Geocoding address: '{address_to_geocode}'")
            coordinates = GeocodeService.geocode_address(address_to_geocode)
            if coordinates:
                lat, lon = coordinates
                motorcycle_data['location'] = f"POINT({lon} {lat})"
                print(f"🐛 DEBUG - Set location to: POINT({lon} {lat})")
            else:
                # Default to Oslo, Norway if geocoding fails
                motorcycle_data['location'] = "POINT(10.7522 59.9139)"
                print(f"🐛 DEBUG - Using default Oslo location")
        else:
            motorcycle_data['location'] = "POINT(10.7522 59.9139)"
            print(f"🐛 DEBUG - No address provided, using default location")
        
        print(f"🐛 DEBUG - Final motorcycle data:")
        print(f"   Address: {motorcycle_data.get('address')}")
        print(f"   City: {motorcycle_data.get('city')}")
        print(f"   Location: {motorcycle_data.get('location')}")
        
        # Create motorcycle
        db_motorcycle = models.Motorcycle(**motorcycle_data)
        
        db.add(db_motorcycle)
        db.commit()
        db.refresh(db_motorcycle)
        
        # Add images (existing code)
        if motorcycle.images:
            for img in motorcycle.images:
                db_image = models.MotorcycleImage(
                    motorcycle_id=db_motorcycle.id,
                    **img.dict()
                )
                db.add(db_image)
            db.commit()
        
        return db_motorcycle

    @staticmethod
    def get_motorcycle(db: Session, motorcycle_id: int) -> Optional[models.Motorcycle]:
        motorcycle = db.query(models.Motorcycle).filter(
            models.Motorcycle.id == motorcycle_id,
            models.Motorcycle.is_active == True
        ).first()
        
        if motorcycle:
            # Increment view count
            motorcycle.views_count += 1
            db.commit()
            
            # Get seller info from auth service
            if motorcycle.seller_id:
                seller_data = auth_client.get_user_by_id(motorcycle.seller_id)
                if seller_data:
                    # Create proper SellerInfo object
                    from ..models.schemas import SellerInfo
                    from datetime import datetime
                    
                    # Parse created_at properly
                    created_at = None
                    if seller_data.get('created_at'):
                        try:
                            if isinstance(seller_data['created_at'], str):
                                # Parse ISO format datetime string
                                created_at = datetime.fromisoformat(seller_data['created_at'].replace('Z', '+00:00'))
                            else:
                                created_at = seller_data['created_at']
                        except:
                            created_at = datetime(2025, 1, 1)
                    
                    motorcycle.seller = SellerInfo(
                        id=seller_data.get('id', motorcycle.seller_id),
                        name=seller_data.get('username', f"User {motorcycle.seller_id}"),
                        email=seller_data.get('email'),
                        phone=seller_data.get('phone'),
                        created_at=created_at
                    )
                else:
                    # Fallback if auth service is unavailable
                    from ..models.schemas import SellerInfo
                    from datetime import datetime
                    motorcycle.seller = SellerInfo(
                        id=motorcycle.seller_id,
                        name=f"User {motorcycle.seller_id}",
                        email=None,
                        phone=None,
                        created_at=datetime(2025, 1, 1)
                    )
            
            # Load images
            images = db.query(models.MotorcycleImage).filter(
                models.MotorcycleImage.motorcycle_id == motorcycle.id
            ).all()
            motorcycle.images = images
            
            # Load category
            if motorcycle.category_id:
                category = db.query(models.MotorcycleCategory).filter(
                    models.MotorcycleCategory.id == motorcycle.category_id
                ).first()
                motorcycle.category = category
                
        return motorcycle
    
    @staticmethod
    def search_motorcycles(
        db: Session, 
        filters: schemas.MotorcycleSearchFilters,
        page: int = 1,
        per_page: int = 20,
        motorcycle_types: List[str] = None  # Add this parameter
    ) -> tuple[List[models.Motorcycle], int]:
        
        # Start with base query
        query = db.query(models.Motorcycle).filter(models.Motorcycle.is_active == True)
        
        # Apply filters (existing logic)
        if filters.category_id:
            query = query.filter(models.Motorcycle.category_id == filters.category_id)
        
        # Handle multiple motorcycle types
        if motorcycle_types and len(motorcycle_types) > 0:
            print(f"🔍 Filtering by motorcycle types: {motorcycle_types}")
            # Use SQL IN clause for multiple types
            query = query.filter(models.Motorcycle.motorcycle_type.in_(motorcycle_types))
        elif filters.motorcycle_type:
            # Fallback to single type filter
            motorcycle_type_value = filters.motorcycle_type.value if hasattr(filters.motorcycle_type, 'value') else filters.motorcycle_type
            query = query.filter(models.Motorcycle.motorcycle_type == motorcycle_type_value)
        
        if filters.brand:
            query = query.filter(models.Motorcycle.brand.ilike(f"%{filters.brand}%"))
            
        if filters.model:
            query = query.filter(models.Motorcycle.model.ilike(f"%{filters.model}%"))
            
        if filters.city:
            query = query.filter(models.Motorcycle.city.ilike(f"%{filters.city}%"))
            
        if filters.condition:
            condition_value = filters.condition.value if hasattr(filters.condition, 'value') else filters.condition
            query = query.filter(models.Motorcycle.condition == condition_value)
            
        if filters.seller_type:
            seller_type_value = filters.seller_type.value if hasattr(filters.seller_type, 'value') else filters.seller_type
            query = query.filter(models.Motorcycle.seller_type == seller_type_value)
            
        if filters.price_min:
            query = query.filter(models.Motorcycle.price >= filters.price_min)
            
        if filters.price_max:
            query = query.filter(models.Motorcycle.price <= filters.price_max)
            
        if filters.year_min:
            query = query.filter(models.Motorcycle.year >= filters.year_min)
            
        if filters.year_max:
            query = query.filter(models.Motorcycle.year <= filters.year_max)
            
        if filters.mileage_min:
            query = query.filter(models.Motorcycle.mileage >= filters.mileage_min)
            
        if filters.mileage_max:
            query = query.filter(models.Motorcycle.mileage <= filters.mileage_max)
            
        if filters.engine_size_min:
            query = query.filter(models.Motorcycle.engine_size >= filters.engine_size_min)
            
        if filters.engine_size_max:
            query = query.filter(models.Motorcycle.engine_size <= filters.engine_size_max)
            
        if filters.search_term:
            search_term = f"%{filters.search_term}%"
            query = query.filter(
                or_(
                    models.Motorcycle.title.ilike(search_term),
                    models.Motorcycle.description.ilike(search_term),
                    models.Motorcycle.brand.ilike(search_term),
                    models.Motorcycle.model.ilike(search_term)
                )
            )
        
        # Get total count before pagination
        total = query.count()   
        # Apply ordering
        ordered_query = query.order_by(
            models.Motorcycle.is_featured.desc(),
            models.Motorcycle.created_at.desc()
        )
        
        # Apply pagination
        motorcycles = ordered_query.offset((page - 1) * per_page).limit(per_page).all()
        
        return motorcycles, total
    
    @staticmethod
    def search_motorcycles_by_location(
        db: Session,
        latitude: float,
        longitude: float,
        radius_km: int,
        filters: Optional[schemas.MotorcycleSearchFilters] = None,
        page: int = 1,
        per_page: int = 20
    ) -> tuple[List[models.Motorcycle], int]:
        
        # Create point from coordinates
        point = func.ST_GeogFromText(f'POINT({longitude} {latitude})')
        
        query = db.query(models.Motorcycle).filter(
            models.Motorcycle.is_active == True,
            models.Motorcycle.location.isnot(None),
            func.ST_DWithin(models.Motorcycle.location, point, radius_km * 1000)  # Convert km to meters
        )
        
        # Apply additional filters if provided
        if filters:
            if filters.motorcycle_type:
                motorcycle_type_value = filters.motorcycle_type.value if hasattr(filters.motorcycle_type, 'value') else filters.motorcycle_type
                query = query.filter(models.Motorcycle.motorcycle_type == motorcycle_type_value)
            if filters.brand:
                query = query.filter(models.Motorcycle.brand.ilike(f"%{filters.brand}%"))
            if filters.condition:
                condition_value = filters.condition.value if hasattr(filters.condition, 'value') else filters.condition
                query = query.filter(models.Motorcycle.condition == condition_value)
            if filters.price_min:
                query = query.filter(models.Motorcycle.price >= filters.price_min)
            if filters.price_max:
                query = query.filter(models.Motorcycle.price <= filters.price_max)
        
        # Get total count
        total = query.count()
        
        # Apply pagination and order by distance
        motorcycles = query.order_by(
            func.ST_Distance(models.Motorcycle.location, point)
        ).offset((page - 1) * per_page).limit(per_page).all()
        
        return motorcycles, total
    
    @staticmethod
    def get_motorcycle_types_with_counts(db: Session) -> dict:
        result = db.query(
            models.Motorcycle.motorcycle_type,
            func.count(models.Motorcycle.id).label('count')
        ).filter(
            models.Motorcycle.is_active == True
        ).group_by(models.Motorcycle.motorcycle_type).all()
        
        return {item.motorcycle_type: item.count for item in result}
    

    
    @staticmethod
    def calculate_loan(
        price: Decimal,
        term_months: int,
        interest_rate: Optional[Decimal] = None
    ) -> schemas.LoanCalculationResponse:
        
        # Default interest rate if not provided
        if interest_rate is None:
            interest_rate = Decimal('7.5')  # 7.5% annual rate
        
        # Convert annual rate to monthly
        monthly_rate = interest_rate / Decimal('100') / Decimal('12')
        
        # Calculate monthly payment using standard loan formula
        if monthly_rate > 0:
            monthly_payment = price * (
                monthly_rate * (1 + monthly_rate) ** term_months
            ) / (
                (1 + monthly_rate) ** term_months - 1
            )
        else:
            monthly_payment = price / term_months
        
        total_amount = monthly_payment * term_months
        total_interest = total_amount - price
        
        return schemas.LoanCalculationResponse(
            price=price,
            term_months=term_months,
            interest_rate=interest_rate,
            monthly_payment=monthly_payment.quantize(Decimal('0.01')),
            total_amount=total_amount.quantize(Decimal('0.01')),
            total_interest=total_interest.quantize(Decimal('0.01'))
        )
        
class MotorcycleCategoryService:
    
    @staticmethod
    def get_all_categories(db: Session) -> List[models.MotorcycleCategory]:
        return db.query(models.MotorcycleCategory).filter(
            models.MotorcycleCategory.is_active == True
        ).all()
    
    @staticmethod
    def create_category(db: Session, category: schemas.MotorcycleCategoryCreate) -> models.MotorcycleCategory:
        db_category = models.MotorcycleCategory(**category.dict())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    
    @staticmethod
    def get_categories_with_counts(db: Session) -> List[dict]:
        result = db.query(
            models.MotorcycleCategory,
            func.count(models.Motorcycle.id).label('motorcycle_count')
        ).outerjoin(
            models.Motorcycle,
            and_(
                models.MotorcycleCategory.id == models.Motorcycle.category_id,
                models.Motorcycle.is_active == True
            )
        ).filter(
            models.MotorcycleCategory.is_active == True
        ).group_by(models.MotorcycleCategory.id).all()
        
        return [
            {
                "id": category.id,
                "name": category.name,
                "slug": category.slug,
                "icon": category.icon,
                "description": category.description,
                "motorcycle_count": count
            }
            for category, count in result
        ]
        
class GeocodeService:
    @staticmethod
    def geocode_address(address: str) -> tuple[float, float] or None:
        """
        Get coordinates from address using OpenStreetMap Nominatim
        Returns (latitude, longitude) or None if not found
        """
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                'q': address,
                'format': 'json',
                'limit': 1,
                'addressdetails': 1,
                'countrycodes': '',
            }
            headers = {
                'User-Agent': 'Selgo-Motorcycle-Service/1.0'
            }
            
            print(f"🔍 Geocoding address: '{address}'")
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    result = data[0]
                    lat = float(result['lat'])
                    lon = float(result['lon'])
                    
                    display_name = result.get('display_name', 'Unknown')
                    print(f"✅ Geocoded '{address}' to:")
                    print(f"   Coordinates: ({lat}, {lon})")
                    print(f"   Full address: {display_name}")
                    
                    return lat, lon
            
            print(f"⚠️ Could not geocode address: {address}")
            return None
            
        except Exception as e:
            print(f"❌ Geocoding error for '{address}': {e}")
            return None
        

class UserFavoriteMotorcycleRepository:
    @staticmethod
    def add_favorite(db: Session, user_id: int, motorcycle_id: int) -> Optional[models.UserFavoriteMotorcycle]:
        # Check if already favorited
        existing = db.query(models.UserFavoriteMotorcycle).filter(
            models.UserFavoriteMotorcycle.user_id == user_id,
            models.UserFavoriteMotorcycle.motorcycle_id == motorcycle_id
        ).first()
        
        if existing:
            return existing
        
        # Create new favorite
        favorite = models.UserFavoriteMotorcycle(user_id=user_id, motorcycle_id=motorcycle_id)
        db.add(favorite)
        db.commit()
        db.refresh(favorite)
        return favorite
    
    @staticmethod
    def remove_favorite(db: Session, user_id: int, motorcycle_id: int) -> bool:
        favorite = db.query(models.UserFavoriteMotorcycle).filter(
            models.UserFavoriteMotorcycle.user_id == user_id,
            models.UserFavoriteMotorcycle.motorcycle_id == motorcycle_id
        ).first()
        
        if favorite:
            db.delete(favorite)
            db.commit()
            return True
        return False
    
    @staticmethod
    def is_favorite(db: Session, user_id: int, motorcycle_id: int) -> bool:
        return db.query(models.UserFavoriteMotorcycle).filter(
            models.UserFavoriteMotorcycle.user_id == user_id,
            models.UserFavoriteMotorcycle.motorcycle_id == motorcycle_id
        ).first() is not None
    
    @staticmethod
    def get_user_favorites(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.UserFavoriteMotorcycle]:
        return db.query(models.UserFavoriteMotorcycle).options(
            joinedload(models.UserFavoriteMotorcycle.motorcycle).joinedload(models.Motorcycle.images)
        ).filter(
            models.UserFavoriteMotorcycle.user_id == user_id
        ).order_by(
            models.UserFavoriteMotorcycle.created_at.desc()
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_favorites_count(db: Session, user_id: int) -> int:
        return db.query(models.UserFavoriteMotorcycle).filter(
            models.UserFavoriteMotorcycle.user_id == user_id
        ).count()

class UserFavoriteMotorcycleService:
    @staticmethod
    def toggle_favorite(db: Session, user_id: int, motorcycle_id: int) -> tuple[bool, str]:
        """Toggle favorite status and return (is_favorite, message)"""
        # Check if motorcycle exists
        motorcycle = db.query(models.Motorcycle).filter(models.Motorcycle.id == motorcycle_id).first()
        if not motorcycle:
            raise ValueError("Motorcycle not found")
        
        # Check current favorite status
        is_currently_favorite = UserFavoriteMotorcycleRepository.is_favorite(db, user_id, motorcycle_id)
        
        if is_currently_favorite:
            # Remove from favorites
            UserFavoriteMotorcycleRepository.remove_favorite(db, user_id, motorcycle_id)
            return False, "Removed from favorites"
        else:
            # Add to favorites
            UserFavoriteMotorcycleRepository.add_favorite(db, user_id, motorcycle_id)
            return True, "Added to favorites"
    
    @staticmethod
    def get_user_favorites(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.UserFavoriteMotorcycle]:
        return UserFavoriteMotorcycleRepository.get_user_favorites(db, user_id, skip, limit)
    
    @staticmethod
    def get_favorites_count(db: Session, user_id: int) -> int:
        return UserFavoriteMotorcycleRepository.get_favorites_count(db, user_id)
    
    @staticmethod
    def is_favorite(db: Session, user_id: int, motorcycle_id: int) -> bool:
        return UserFavoriteMotorcycleRepository.is_favorite(db, user_id, motorcycle_id)