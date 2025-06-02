from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, asc, desc
from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_Distance, ST_Transform, ST_SetSRID, ST_MakePoint
from typing import List, Optional, Dict, Any, Tuple
from ..models.boat_models import BoatCategory, Boat, BoatImage, BoatFeature, BoatRating, BoatFixDoneRequest
from ..models.boat_schemas import BoatFilterParams, GeoPoint, BoatCondition, SellerType, AdType
import logging

logger = logging.getLogger(__name__)

class BoatCategoryRepository:
    @staticmethod
    def create(db: Session, category_data: Dict[str, Any]) -> BoatCategory:
        db_category = BoatCategory(**category_data)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    
    @staticmethod
    def get_by_id(db: Session, category_id: int) -> Optional[BoatCategory]:
        return db.query(BoatCategory).filter(BoatCategory.id == category_id).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[BoatCategory]:
        return db.query(BoatCategory).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_all_with_counts(db: Session) -> List[Tuple[BoatCategory, int]]:
        query = db.query(
            BoatCategory,
            func.count(Boat.id).label('count')
        ).outerjoin(
            Boat, BoatCategory.id == Boat.category_id
        ).group_by(BoatCategory.id)
        
        return query.all()
    
    @staticmethod
    def get_by_parent_id(db: Session, parent_id: Optional[int] = None) -> List[BoatCategory]:
        if parent_id is None:
            # Get top-level categories (with no parent)
            return db.query(BoatCategory).filter(BoatCategory.parent_id.is_(None)).all()
        else:
            # Get children of specified parent
            return db.query(BoatCategory).filter(BoatCategory.parent_id == parent_id).all()
    
    @staticmethod
    def update(db: Session, category_id: int, category_data: Dict[str, Any]) -> Optional[BoatCategory]:
        db_category = db.query(BoatCategory).filter(BoatCategory.id == category_id).first()
        if db_category:
            for key, value in category_data.items():
                setattr(db_category, key, value)
            db.commit()
            db.refresh(db_category)
        return db_category
    
    @staticmethod
    def delete(db: Session, category_id: int) -> bool:
        db_category = db.query(BoatCategory).filter(BoatCategory.id == category_id).first()
        if db_category:
            db.delete(db_category)
            db.commit()
            return True
        return False

class BoatFeatureRepository:
    @staticmethod
    def create(db: Session, feature_data: Dict[str, Any]) -> BoatFeature:
        db_feature = BoatFeature(**feature_data)
        db.add(db_feature)
        db.commit()
        db.refresh(db_feature)
        return db_feature
    
    @staticmethod
    def get_by_id(db: Session, feature_id: int) -> Optional[BoatFeature]:
        return db.query(BoatFeature).filter(BoatFeature.id == feature_id).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[BoatFeature]:
        return db.query(BoatFeature).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_ids(db: Session, feature_ids: List[int]) -> List[BoatFeature]:
        return db.query(BoatFeature).filter(BoatFeature.id.in_(feature_ids)).all()
    
    @staticmethod
    def update(db: Session, feature_id: int, feature_data: Dict[str, Any]) -> Optional[BoatFeature]:
        db_feature = db.query(BoatFeature).filter(BoatFeature.id == feature_id).first()
        if db_feature:
            for key, value in feature_data.items():
                setattr(db_feature, key, value)
            db.commit()
            db.refresh(db_feature)
        return db_feature
    
    @staticmethod
    def delete(db: Session, feature_id: int) -> bool:
        db_feature = db.query(BoatFeature).filter(BoatFeature.id == feature_id).first()
        if db_feature:
            db.delete(db_feature)
            db.commit()
            return True
        return False

class BoatRepository:
    @staticmethod
    def create(db: Session, boat_data: Dict[str, Any], features: List[BoatFeature] = None) -> Boat:
        # Process location if provided
        if 'location' in boat_data and boat_data['location'] is not None:
            location = boat_data.pop('location')
            lat, lon = location.latitude, location.longitude
            boat_data['location'] = f'SRID=4326;POINT({lon} {lat})'
        
        # Create new boat instance
        db_boat = Boat(**boat_data)
        
        # Add features if provided
        if features:
            db_boat.features = features
        
        db.add(db_boat)
        db.commit()
        db.refresh(db_boat)
        return db_boat

    @staticmethod
    def get_by_id(db: Session, boat_id: int) -> Optional[Boat]:
        return db.query(Boat).filter(Boat.id == boat_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Boat]:
        return db.query(Boat).offset(skip).limit(limit).all()

    @staticmethod
    def filter_boats(db: Session, filters) -> Tuple[List[Boat], int]:
        from ..models.boat_schemas import BoatFilterParams
        query = db.query(Boat)
        
        # print(f"Filtering boats with full parameters: {filters}")
        
        # Apply filters if provided
        if hasattr(filters, 'category_id') and filters.category_id:
            print(f"Applying category filter: {filters.category_id}")
            query = query.filter(Boat.category_id == filters.category_id)
        
        if hasattr(filters, 'condition') and filters.condition:
            print(f"Applying condition filter: {filters.condition}")
            query = query.filter(Boat.condition == filters.condition)
        
        if hasattr(filters, 'price_min') and filters.price_min is not None:
            print(f"Applying price_min filter: {filters.price_min}")
            query = query.filter(Boat.price >= filters.price_min)
        
        if hasattr(filters, 'price_max') and filters.price_max is not None:
            print(f"Applying price_max filter: {filters.price_max}")
            query = query.filter(Boat.price <= filters.price_max)
        
        if hasattr(filters, 'year_min') and filters.year_min is not None:
            print(f"Applying year_min filter: {filters.year_min}")
            query = query.filter(Boat.year >= filters.year_min)
        
        if hasattr(filters, 'year_max') and filters.year_max is not None:
            print(f"Applying year_max filter: {filters.year_max}")
            query = query.filter(Boat.year <= filters.year_max)
        
        if hasattr(filters, 'length_min') and filters.length_min is not None:
            print(f"Applying length_min filter: {filters.length_min}")
            query = query.filter(Boat.length >= filters.length_min)
        
        if hasattr(filters, 'length_max') and filters.length_max is not None:
            print(f"Applying length_max filter: {filters.length_max}")
            query = query.filter(Boat.length <= filters.length_max)
        
        if hasattr(filters, 'seller_type') and filters.seller_type:
            print(f"Applying seller_type filter: {filters.seller_type}")
            query = query.filter(Boat.seller_type == filters.seller_type)
        
        if hasattr(filters, 'ad_type') and filters.ad_type:
            print(f"Applying ad_type filter: {filters.ad_type}")
            query = query.filter(Boat.ad_type == filters.ad_type)
        
        # Apply location-based filtering (distance search)
        if hasattr(filters, 'location') and hasattr(filters, 'distance') and filters.location and filters.distance:
            print(f"Applying location filter: {filters.location} with distance: {filters.distance}km")
            from geoalchemy2.functions import ST_Distance, ST_Transform, ST_SetSRID, ST_MakePoint
            # Create a point from lat/lon
            point = ST_SetSRID(ST_MakePoint(filters.location.longitude, filters.location.latitude), 4326)
            
            # Calculate distance in meters (convert km to m)
            distance_meters = filters.distance * 1000
            
            # Filter by distance
            query = query.filter(
                ST_Distance(
                    ST_Transform(Boat.location, 3857),
                    ST_Transform(point, 3857)
                ) <= distance_meters
            )
        
        # Apply feature filtering
        if hasattr(filters, 'features') and filters.features and len(filters.features) > 0:
            print(f"Applying features filter: {filters.features}")
            # This requires a join with the association table
            for feature_id in filters.features:
                query = query.filter(Boat.features.any(BoatFeature.id == feature_id))
        
        # Apply text search
        if hasattr(filters, 'search_term') and filters.search_term:
            print(f"Applying search_term filter: {filters.search_term}")
            from sqlalchemy import or_
            search_term = f"%{filters.search_term}%"
            query = query.filter(
                or_(
                    Boat.title.ilike(search_term),
                    Boat.description.ilike(search_term),
                    Boat.make.ilike(search_term),
                    Boat.model.ilike(search_term),
                    Boat.location_name.ilike(search_term)
                )
            
            )
        from sqlalchemy import asc, desc
        #Always sort by creation date (newest first)
        query = query.order_by(desc(Boat.created_at))
        # Get total count before pagination
        total = query.count()
        print(f"Total matches before pagination: {total}")
        
        # Apply sorting
        
        # if hasattr(filters, 'sort_by') and filters.sort_by:
        #     sort_column = getattr(Boat, filters.sort_by, Boat.created_at)
        #     if hasattr(filters, 'sort_order') and filters.sort_order == "asc":
        #         query = query.order_by(asc(sort_column))
        #     else:
        #         query = query.order_by(desc(sort_column))
        # else:
        #     # Default sort by created_at descending
        #     query = query.order_by(desc(Boat.created_at))
        
        # Apply pagination
        if hasattr(filters, 'offset') and hasattr(filters, 'limit'):
            query = query.offset(filters.offset).limit(filters.limit)
        
        return query.all(), total

    @staticmethod
    def get_recommended_boats(db: Session, limit: int = 10) -> List[Boat]:
        """
        Get recommended boats - simply get newest ones first
        """
        from sqlalchemy import desc
        # Just sort by creation date to get newest boats
        query = db.query(Boat).filter(Boat.status == "active")
        query = query.order_by(desc(Boat.created_at))
        return query.limit(limit).all()

    @staticmethod
    def update(db: Session, boat_id: int, boat_data: Dict[str, Any], features: List[BoatFeature] = None) -> Optional[Boat]:
        db_boat = db.query(Boat).filter(Boat.id == boat_id).first()
        
        if not db_boat:
            return None
        
        # Process location if provided
        if 'location' in boat_data and boat_data['location'] is not None:
            location = boat_data.pop('location')
            lat, lon = location.latitude, location.longitude
            boat_data['location'] = f'SRID=4326;POINT({lon} {lat})'
        
        # Update boat attributes
        for key, value in boat_data.items():
            if hasattr(db_boat, key):
                setattr(db_boat, key, value)
        
        # Update features if provided
        if features is not None:
            db_boat.features = features
        
        db.commit()
        db.refresh(db_boat)
        return db_boat

    @staticmethod
    def delete(db: Session, boat_id: int) -> bool:
        db_boat = db.query(Boat).filter(Boat.id == boat_id).first()
        if db_boat:
            db.delete(db_boat)
            db.commit()
            return True
        return False
    
    @staticmethod
    def increment_view_count(db: Session, boat_id: int) -> Optional[Boat]:
        db_boat = db.query(Boat).filter(Boat.id == boat_id).first()
        if db_boat:
            db_boat.view_count += 1
            db.commit()
            db.refresh(db_boat)
        return db_boat
    

class BoatImageRepository:
    @staticmethod
    def create(db: Session, boat_id: int, image_data: Dict[str, Any]) -> BoatImage:
        # Create the image
        db_image = BoatImage(**image_data, boat_id=boat_id)
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        return db_image
    
    @staticmethod
    def create_many(db: Session, boat_id: int, images_data: List[Dict[str, Any]]) -> List[BoatImage]:
        # Create multiple images
        db_images = [BoatImage(**image_data, boat_id=boat_id) for image_data in images_data]
        db.add_all(db_images)
        db.commit()
        
        for image in db_images:
            db.refresh(image)
        
        return db_images
    
    @staticmethod
    def get_by_id(db: Session, image_id: int) -> Optional[BoatImage]:
        return db.query(BoatImage).filter(BoatImage.id == image_id).first()
    
    @staticmethod
    def get_by_boat_id(db: Session, boat_id: int) -> List[BoatImage]:
        return db.query(BoatImage).filter(BoatImage.boat_id == boat_id).all()
    
    @staticmethod
    def update(db: Session, image_id: int, image_data: Dict[str, Any]) -> Optional[BoatImage]:
        db_image = db.query(BoatImage).filter(BoatImage.id == image_id).first()
        if db_image:
            for key, value in image_data.items():
                setattr(db_image, key, value)
            db.commit()
            db.refresh(db_image)
        return db_image
    
    @staticmethod
    def delete(db: Session, image_id: int) -> bool:
        db_image = db.query(BoatImage).filter(BoatImage.id == image_id).first()
        if db_image:
            db.delete(db_image)
            db.commit()
            return True
        return False
    
    @staticmethod
    def delete_by_boat_id(db: Session, boat_id: int) -> bool:
        db.query(BoatImage).filter(BoatImage.boat_id == boat_id).delete()
        db.commit()
        return True

class BoatRatingRepository:
    @staticmethod
    def create(db: Session, rating_data: Dict[str, Any]) -> BoatRating:
        db_rating = BoatRating(**rating_data)
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        return db_rating
    
    @staticmethod
    def get_by_id(db: Session, rating_id: int) -> Optional[BoatRating]:
        return db.query(BoatRating).filter(BoatRating.id == rating_id).first()
    
    @staticmethod
    def get_by_boat_id(db: Session, boat_id: int, skip: int = 0, limit: int = 100) -> List[BoatRating]:
        return db.query(BoatRating).filter(BoatRating.boat_id == boat_id).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[BoatRating]:
        return db.query(BoatRating).filter(BoatRating.user_id == user_id).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_avg_rating(db: Session, boat_id: int) -> float:
        avg_rating = db.query(func.avg(BoatRating.stars)).filter(BoatRating.boat_id == boat_id).scalar()
        return float(avg_rating) if avg_rating is not None else 0.0
    
    @staticmethod
    def get_rating_count(db: Session, boat_id: int) -> int:
        return db.query(BoatRating).filter(BoatRating.boat_id == boat_id).count()
    
    @staticmethod
    def update(db: Session, rating_id: int, rating_data: Dict[str, Any]) -> Optional[BoatRating]:
        db_rating = db.query(BoatRating).filter(BoatRating.id == rating_id).first()
        if db_rating:
            for key, value in rating_data.items():
                setattr(db_rating, key, value)
            db.commit()
            db.refresh(db_rating)
        return db_rating
    
    @staticmethod
    def delete(db: Session, rating_id: int) -> bool:
        db_rating = db.query(BoatRating).filter(BoatRating.id == rating_id).first()
        if db_rating:
            db.delete(db_rating)
            db.commit()
            return True
        return False

class BoatFixDoneRequestRepository:
    @staticmethod
    def create(db: Session, request_data: Dict[str, Any]) -> BoatFixDoneRequest:
        db_request = BoatFixDoneRequest(**request_data)
        db.add(db_request)
        db.commit()
        db.refresh(db_request)
        return db_request
    
    @staticmethod
    def get_by_id(db: Session, request_id: int) -> Optional[BoatFixDoneRequest]:
        return db.query(BoatFixDoneRequest).filter(BoatFixDoneRequest.id == request_id).first()
    
    @staticmethod
    def get_by_boat_id(db: Session, boat_id: int) -> List[BoatFixDoneRequest]:
        return db.query(BoatFixDoneRequest).filter(BoatFixDoneRequest.boat_id == boat_id).all()
    
    @staticmethod
    def get_by_buyer_id(db: Session, buyer_id: int) -> List[BoatFixDoneRequest]:
        return db.query(BoatFixDoneRequest).filter(BoatFixDoneRequest.buyer_id == buyer_id).all()
    
    @staticmethod
    def get_by_seller_id(db: Session, seller_id: int) -> List[BoatFixDoneRequest]:
        return db.query(BoatFixDoneRequest).filter(BoatFixDoneRequest.seller_id == seller_id).all()
    
    @staticmethod
    def update_status(db: Session, request_id: int, status) -> Optional[BoatFixDoneRequest]:
        db_request = db.query(BoatFixDoneRequest).filter(BoatFixDoneRequest.id == request_id).first()
        if db_request:
            db_request.status = status
            db.commit()
            db.refresh(db_request)
        return db_request
    
    @staticmethod
    def update(db: Session, request_id: int, request_data: Dict[str, Any]) -> Optional[BoatFixDoneRequest]:
        db_request = db.query(BoatFixDoneRequest).filter(BoatFixDoneRequest.id == request_id).first()
        if db_request:
            for key, value in request_data.items():
                setattr(db_request, key, value)
            db.commit()
            db.refresh(db_request)
        return db_request
    
    @staticmethod
    def delete(db: Session, request_id: int) -> bool:
        db_request = db.query(BoatFixDoneRequest).filter(BoatFixDoneRequest.id == request_id).first()
        if db_request:
            db.delete(db_request)
            db.commit()
            return True
        return False
