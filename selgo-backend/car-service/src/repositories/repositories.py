from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, or_, asc, desc
from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_Distance, ST_Transform, ST_SetSRID, ST_MakePoint
from typing import List, Optional, Dict, Any, Tuple
from ..models.car_models import CarCategory, Car, CarImage, CarFeature, CarRating, UserFavorite
from ..models.car_schemas import CarFilterParams, GeoPoint, CarCondition, SellerType, AdType
import logging

logger = logging.getLogger(__name__)

class CarCategoryRepository:
    @staticmethod
    def create(db: Session, category_data: Dict[str, Any]) -> CarCategory:
        db_category = CarCategory(**category_data)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    @staticmethod
    def get_by_id(db: Session, category_id: int) -> Optional[CarCategory]:
        return db.query(CarCategory).filter(CarCategory.id == category_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[CarCategory]:
        return db.query(CarCategory).offset(skip).limit(limit).all()

    @staticmethod
    def get_all_with_counts(db: Session) -> List[Tuple[CarCategory, int]]:
        query = db.query(
            CarCategory,
            func.count(Car.id).label('count')
        ).outerjoin(
            Car, CarCategory.id == Car.category_id
        ).group_by(CarCategory.id)

        return query.all()

    @staticmethod
    def get_by_parent_id(db: Session, parent_id: Optional[int] = None) -> List[CarCategory]:
        if parent_id is None:
            return db.query(CarCategory).filter(CarCategory.parent_id.is_(None)).all()
        else:
            return db.query(CarCategory).filter(CarCategory.parent_id == parent_id).all()

    @staticmethod
    def update(db: Session, category_id: int, category_data: Dict[str, Any]) -> Optional[CarCategory]:
        db_category = db.query(CarCategory).filter(CarCategory.id == category_id).first()
        if db_category:
            for key, value in category_data.items():
                setattr(db_category, key, value)
            db.commit()
            db.refresh(db_category)
        return db_category

    @staticmethod
    def delete(db: Session, category_id: int) -> bool:
        db_category = db.query(CarCategory).filter(CarCategory.id == category_id).first()
        if db_category:
            db.delete(db_category)
            db.commit()
            return True
        return False

class CarFeatureRepository:
    @staticmethod
    def create(db: Session, feature_data: Dict[str, Any]) -> CarFeature:
        db_feature = CarFeature(**feature_data)
        db.add(db_feature)
        db.commit()
        db.refresh(db_feature)
        return db_feature

    @staticmethod
    def get_by_id(db: Session, feature_id: int) -> Optional[CarFeature]:
        return db.query(CarFeature).filter(CarFeature.id == feature_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[CarFeature]:
        return db.query(CarFeature).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_ids(db: Session, feature_ids: List[int]) -> List[CarFeature]:
        return db.query(CarFeature).filter(CarFeature.id.in_(feature_ids)).all()

    @staticmethod
    def update(db: Session, feature_id: int, feature_data: Dict[str, Any]) -> Optional[CarFeature]:
        db_feature = db.query(CarFeature).filter(CarFeature.id == feature_id).first()
        if db_feature:
            for key, value in feature_data.items():
                setattr(db_feature, key, value)
            db.commit()
            db.refresh(db_feature)
        return db_feature

    @staticmethod
    def delete(db: Session, feature_id: int) -> bool:
        db_feature = db.query(CarFeature).filter(CarFeature.id == feature_id).first()
        if db_feature:
            db.delete(db_feature)
            db.commit()
            return True
        return False

class CarRepository:
    @staticmethod
    def create(db: Session, car_data: Dict[str, Any], features: List[CarFeature] = None) -> Car:
        if 'location' in car_data and car_data['location'] is not None:
            location = car_data.pop('location')
            lat, lon = location.latitude, location.longitude
            car_data['location'] = f'SRID=4326;POINT({lon} {lat})'

        db_car = Car(**car_data)

        if features:
            db_car.features = features

        db.add(db_car)
        db.commit()
        db.refresh(db_car)
        return db_car

    @staticmethod
    def get_by_id(db: Session, car_id: int) -> Optional[Car]:
        return db.query(Car).filter(Car.id == car_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Car]:
        return db.query(Car).offset(skip).limit(limit).all()

    @staticmethod
    def filter_cars(db: Session, filters: CarFilterParams) -> Tuple[List[Car], int]:
        query = db.query(Car).filter(Car.status == "active")

        if filters.category_id:
            query = query.filter(Car.category_id == filters.category_id)

        if filters.condition:
            query = query.filter(Car.condition == filters.condition)

        if filters.price_min is not None:
            query = query.filter(Car.price >= filters.price_min)

        if filters.price_max is not None:
            query = query.filter(Car.price <= filters.price_max)

        if filters.year_min is not None:
            query = query.filter(Car.year >= filters.year_min)

        if filters.year_max is not None:
            query = query.filter(Car.year <= filters.year_max)

        if filters.mileage_min is not None:
            query = query.filter(Car.mileage >= filters.mileage_min)

        if filters.mileage_max is not None:
            query = query.filter(Car.mileage <= filters.mileage_max)

        if filters.seller_type:
            query = query.filter(Car.seller_type == filters.seller_type)

        if filters.ad_type:
            query = query.filter(Car.ad_type == filters.ad_type)

        if filters.location and filters.distance:
            point = ST_SetSRID(ST_MakePoint(filters.location.longitude, filters.location.latitude), 4326)
            distance_meters = filters.distance * 1000
            query = query.filter(
                ST_Distance(
                    ST_Transform(Car.location, 3857),
                    ST_Transform(point, 3857)
                ) <= distance_meters
            )

        if filters.features:
            for feature_id in filters.features:
                query = query.filter(Car.features.any(CarFeature.id == feature_id))

        if filters.search_term:
            search_term = f"%{filters.search_term}%"
            query = query.filter(
                or_(
                    Car.title.ilike(search_term),
                    Car.description.ilike(search_term),
                    Car.make.ilike(search_term),
                    Car.model.ilike(search_term),
                    Car.location_name.ilike(search_term)
                )
            )

        if filters.sort_by and filters.sort_order:
            order_column = getattr(Car, filters.sort_by, Car.created_at)
            if filters.sort_order.lower() == "desc":
                query = query.order_by(desc(order_column))
            else:
                query = query.order_by(asc(order_column))

        total = query.count()

        query = query.offset(filters.offset).limit(filters.limit)

        cars = query.all()

        return cars, total

    @staticmethod
    def get_recommended_cars(db: Session, limit: int = 10) -> List[Car]:
        query = db.query(Car).filter(Car.status == "active")
        query = query.order_by(desc(Car.created_at))
        return query.limit(limit).all()

    @staticmethod
    def update(db: Session, car_id: int, car_data: Dict[str, Any], features: List[CarFeature] = None) -> Optional[Car]:
        db_car = db.query(Car).filter(Car.id == car_id).first()

        if not db_car:
            return None

        if 'location' in car_data and car_data['location'] is not None:
            location = car_data.pop('location')
            lat, lon = location.latitude, location.longitude
            car_data['location'] = f'SRID=4326;POINT({lon} {lat})'

        for key, value in car_data.items():
            if hasattr(db_car, key):
                setattr(db_car, key, value)

        if features is not None:
            db_car.features = features

        db.commit()
        db.refresh(db_car)
        return db_car

    @staticmethod
    def delete(db: Session, car_id: int) -> bool:
        db_car = db.query(Car).filter(Car.id == car_id).first()
        if db_car:
            db.delete(db_car)
            db.commit()
            return True
        return False

    @staticmethod
    def increment_view_count(db: Session, car_id: int) -> Optional[Car]:
        db_car = db.query(Car).filter(Car.id == car_id).first()
        if db_car:
            db_car.view_count += 1
            db.commit()
            db.refresh(db_car)
        return db_car

class CarImageRepository:
    @staticmethod
    def create(db: Session, car_id: int, image_data: Dict[str, Any]) -> CarImage:
        db_image = CarImage(**image_data, car_id=car_id)
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        return db_image

    @staticmethod
    def create_many(db: Session, car_id: int, images_data: List[Dict[str, Any]]) -> List[CarImage]:
        db_images = [CarImage(**image_data, car_id=car_id) for image_data in images_data]
        db.add_all(db_images)
        db.commit()

        for image in db_images:
            db.refresh(image)

        return db_images

    @staticmethod
    def get_by_id(db: Session, image_id: int) -> Optional[CarImage]:
        return db.query(CarImage).filter(CarImage.id == image_id).first()

    @staticmethod
    def get_by_car_id(db: Session, car_id: int) -> List[CarImage]:
        return db.query(CarImage).filter(CarImage.car_id == car_id).all()

    @staticmethod
    def update(db: Session, image_id: int, image_data: Dict[str, Any]) -> Optional[CarImage]:
        db_image = db.query(CarImage).filter(CarImage.id == image_id).first()
        if db_image:
            for key, value in image_data.items():
                setattr(db_image, key, value)
            db.commit()
            db.refresh(db_image)
        return db_image

    @staticmethod
    def delete(db: Session, image_id: int) -> bool:
        db_image = db.query(CarImage).filter(CarImage.id == image_id).first()
        if db_image:
            db.delete(db_image)
            db.commit()
            return True
        return False

    @staticmethod
    def delete_by_car_id(db: Session, car_id: int) -> bool:
        db.query(CarImage).filter(CarImage.car_id == car_id).delete()
        db.commit()
        return True

class CarRatingRepository:
    @staticmethod
    def create(db: Session, rating_data: Dict[str, Any]) -> CarRating:
        db_rating = CarRating(**rating_data)
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        return db_rating

    @staticmethod
    def get_by_id(db: Session, rating_id: int) -> Optional[CarRating]:
        return db.query(CarRating).filter(CarRating.id == rating_id).first()

    @staticmethod
    def get_by_car_id(db: Session, car_id: int, skip: int = 0, limit: int = 100) -> List[CarRating]:
        return db.query(CarRating).filter(CarRating.car_id == car_id).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[CarRating]:
        return db.query(CarRating).filter(CarRating.user_id == user_id).offset(skip).limit(limit).all()

    @staticmethod
    def get_avg_rating(db: Session, car_id: int) -> float:
        avg_rating = db.query(func.avg(CarRating.stars)).filter(CarRating.car_id == car_id).scalar()
        return float(avg_rating) if avg_rating is not None else 0.0

    @staticmethod
    def get_rating_count(db: Session, car_id: int) -> int:
        return db.query(CarRating).filter(CarRating.car_id == car_id).count()

    @staticmethod
    def update(db: Session, rating_id: int, rating_data: Dict[str, Any]) -> Optional[CarRating]:
        db_rating = db.query(CarRating).filter(CarRating.id == rating_id).first()
        if db_rating:
            for key, value in rating_data.items():
                setattr(db_rating, key, value)
            db.commit()
            db.refresh(db_rating)
        return db_rating

    @staticmethod
    def delete(db: Session, rating_id: int) -> bool:
        db_rating = db.query(CarRating).filter(CarRating.id == rating_id).first()
        if db_rating:
            db.delete(db_rating)
            db.commit()
            return True
        return False

class UserFavoriteRepository:
    @staticmethod
    def add_favorite(db: Session, user_id: int, car_id: int) -> Optional[UserFavorite]:
        existing = db.query(UserFavorite).filter(
            UserFavorite.user_id == user_id,
            UserFavorite.car_id == car_id
        ).first()

        if existing:
            return existing

        favorite = UserFavorite(user_id=user_id, car_id=car_id)
        db.add(favorite)
        db.commit()
        db.refresh(favorite)
        return favorite

    @staticmethod
    def remove_favorite(db: Session, user_id: int, car_id: int) -> bool:
        favorite = db.query(UserFavorite).filter(
            UserFavorite.user_id == user_id,
            UserFavorite.car_id == car_id
        ).first()

        if favorite:
            db.delete(favorite)
            db.commit()
            return True
        return False

    @staticmethod
    def is_favorite(db: Session, user_id: int, car_id: int) -> bool:
        return db.query(UserFavorite).filter(
            UserFavorite.user_id == user_id,
            UserFavorite.car_id == car_id
        ).first() is not None

    @staticmethod
    def get_user_favorites(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[UserFavorite]:
        return db.query(UserFavorite).options(
            joinedload(UserFavorite.car).joinedload(Car.images)
        ).filter(
            UserFavorite.user_id == user_id
        ).order_by(
            UserFavorite.created_at.desc()
        ).offset(skip).limit(limit).all()

    @staticmethod
    def get_favorites_count(db: Session, user_id: int) -> int:
        return db.query(UserFavorite).filter(UserFavorite.user_id == user_id).count()