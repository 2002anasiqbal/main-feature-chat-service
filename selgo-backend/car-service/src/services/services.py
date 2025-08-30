from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any, Tuple
from ..repositories.repositories import (
    CarCategoryRepository,
    CarFeatureRepository,
    CarRepository,
    CarImageRepository,
    CarRatingRepository,
    UserFavoriteRepository
)
from ..models.car_models import (
    CarCategory,
    CarFeature,
    Car,
    CarImage,
    CarRating,
    UserFavorite
)
from ..models.car_schemas import (
    CarCategoryCreate,
    CarFeatureCreate,
    CarCreate,
    CarUpdate,
    CarFilterParams,
    CarImageCreate,
    CarRatingCreate,
    LoanEstimateRequest,
    LoanEstimateResponse
)
import math
import logging

logger = logging.getLogger(__name__)

class CarCategoryService:
    @staticmethod
    def create_category(db: Session, category_data: CarCategoryCreate) -> CarCategory:
        return CarCategoryRepository.create(db, category_data.dict())

    @staticmethod
    def get_category_by_id(db: Session, category_id: int) -> Optional[CarCategory]:
        return CarCategoryRepository.get_by_id(db, category_id)

    @staticmethod
    def get_all_categories(db: Session, skip: int = 0, limit: int = 100) -> List[CarCategory]:
        return CarCategoryRepository.get_all(db, skip, limit)

    @staticmethod
    def get_categories_with_counts(db: Session) -> List[Tuple[CarCategory, int]]:
        return CarCategoryRepository.get_all_with_counts(db)

    @staticmethod
    def get_top_level_categories(db: Session) -> List[CarCategory]:
        return CarCategoryRepository.get_by_parent_id(db, None)

    @staticmethod
    def get_subcategories(db: Session, parent_id: int) -> List[CarCategory]:
        return CarCategoryRepository.get_by_parent_id(db, parent_id)

    @staticmethod
    def update_category(db: Session, category_id: int, category_data: CarCategoryCreate) -> Optional[CarCategory]:
        return CarCategoryRepository.update(db, category_id, category_data.dict())

    @staticmethod
    def delete_category(db: Session, category_id: int) -> bool:
        return CarCategoryRepository.delete(db, category_id)

class CarFeatureService:
    @staticmethod
    def create_feature(db: Session, feature_data: CarFeatureCreate) -> CarFeature:
        return CarFeatureRepository.create(db, feature_data.dict())

    @staticmethod
    def get_feature_by_id(db: Session, feature_id: int) -> Optional[CarFeature]:
        return CarFeatureRepository.get_by_id(db, feature_id)

    @staticmethod
    def get_all_features(db: Session, skip: int = 0, limit: int = 100) -> List[CarFeature]:
        return CarFeatureRepository.get_all(db, skip, limit)

    @staticmethod
    def update_feature(db: Session, feature_id: int, feature_data: CarFeatureCreate) -> Optional[CarFeature]:
        return CarFeatureRepository.update(db, feature_id, feature_data.dict())

    @staticmethod
    def delete_feature(db: Session, feature_id: int) -> bool:
        return CarFeatureRepository.delete(db, feature_id)

class CarService:
    @staticmethod
    def create_car(db: Session, car_data: CarCreate, user_id: int) -> Car:
        features = []
        if car_data.features:
            features = CarFeatureRepository.get_by_ids(db, car_data.features)

        images_data = []
        if hasattr(car_data, 'images') and car_data.images:
            images_data = car_data.images

        car_dict = car_data.dict(exclude={'features', 'images'})
        car_dict['user_id'] = user_id

        db_car = CarRepository.create(db, car_dict, features)

        if images_data:
            CarImageRepository.create_many(db, db_car.id, [img.dict() for img in images_data])

        return db_car

    @staticmethod
    def get_featured_cars(db: Session, limit: int = 10) -> List[Car]:
        from sqlalchemy import desc
        query = db.query(Car).filter(Car.status == "active")

        from datetime import datetime, timedelta
        recent_cutoff = datetime.utcnow() - timedelta(hours=24)

        query = query.order_by(
            desc(Car.created_at >= recent_cutoff),
            desc(Car.created_at)
        )
        return query.limit(limit).all()

    @staticmethod
    def get_homepage_cars(db: Session, limit: int = 10) -> List[Car]:
        from sqlalchemy import desc, or_
        query = db.query(Car).filter(Car.status == "active")

        from datetime import datetime, timedelta
        very_recent_cutoff = datetime.utcnow() - timedelta(hours=6)

        query = query.order_by(
            desc(or_(Car.is_featured == True, Car.created_at >= very_recent_cutoff)),
            desc(Car.created_at)
        )
        return query.limit(limit).all()

    @staticmethod
    def get_car_by_id(db: Session, car_id: int, increment_view: bool = False) -> Optional[Car]:
        car = CarRepository.get_by_id(db, car_id)

        if car and increment_view:
            car = CarRepository.increment_view_count(db, car_id)

        return car

    @staticmethod
    def get_all_cars(db: Session, skip: int = 0, limit: int = 100) -> List[Car]:
        return CarRepository.get_all(db, skip, limit)

    @staticmethod
    def filter_cars(db: Session, filters: CarFilterParams) -> Tuple[List[Car], int]:
        return CarRepository.filter_cars(db, filters)

    @staticmethod
    def get_recommended_cars(db: Session, limit: int = 10) -> List[Car]:
        return CarRepository.get_recommended_cars(db, limit)

    @staticmethod
    def update_car(db: Session, car_id: int, car_data: CarUpdate, user_id: int) -> Optional[Car]:
        car = CarRepository.get_by_id(db, car_id)
        if not car or car.user_id != user_id:
            return None

        features = None
        if car_data.features is not None:
            features = CarFeatureRepository.get_by_ids(db, car_data.features)

        car_dict = car_data.dict(exclude_unset=True, exclude={'features'})
        return CarRepository.update(db, car_id, car_dict, features)

    @staticmethod
    def delete_car(db: Session, car_id: int, user_id: int) -> bool:
        car = CarRepository.get_by_id(db, car_id)
        if not car or car.user_id != user_id:
            return False

        return CarRepository.delete(db, car_id)

class CarImageService:
    @staticmethod
    def add_image(db: Session, car_id: int, image_data: CarImageCreate, user_id: int) -> Optional[CarImage]:
        car = CarRepository.get_by_id(db, car_id)
        if not car or car.user_id != user_id:
            return None

        return CarImageRepository.create(db, car_id, image_data.dict())

    @staticmethod
    def get_images(db: Session, car_id: int) -> List[CarImage]:
        return CarImageRepository.get_by_car_id(db, car_id)

    @staticmethod
    def delete_image(db: Session, image_id: int, user_id: int) -> bool:
        image = CarImageRepository.get_by_id(db, image_id)
        if not image:
            return False

        car = CarRepository.get_by_id(db, image.car_id)
        if not car or car.user_id != user_id:
            return False

        return CarImageRepository.delete(db, image_id)

class CarRatingService:
    @staticmethod
    def create_rating(db: Session, rating_data: CarRatingCreate, user_id: int) -> Optional[CarRating]:
        car = CarRepository.get_by_id(db, rating_data.car_id)
        if not car:
            return None

        existing_ratings = CarRatingRepository.get_by_car_id(db, rating_data.car_id)
        for rating in existing_ratings:
            if rating.user_id == user_id:
                return CarRatingRepository.update(db, rating.id, {
                    'stars': rating_data.stars,
                    'review': rating_data.review
                })

        rating_dict = rating_data.dict()
        rating_dict['user_id'] = user_id
        return CarRatingRepository.create(db, rating_dict)

    @staticmethod
    def get_ratings_by_car_id(db: Session, car_id: int, skip: int = 0, limit: int = 100) -> List[CarRating]:
        return CarRatingRepository.get_by_car_id(db, car_id, skip, limit)

    @staticmethod
    def get_avg_rating(db: Session, car_id: int) -> float:
        return CarRatingRepository.get_avg_rating(db, car_id)

    @staticmethod
    def delete_rating(db: Session, rating_id: int, user_id: int) -> bool:
        rating = CarRatingRepository.get_by_id(db, rating_id)
        if not rating or rating.user_id != user_id:
            return False

        return CarRatingRepository.delete(db, rating_id)

class LoanEstimateService:
    @staticmethod
    def calculate_loan(loan_data: LoanEstimateRequest) -> LoanEstimateResponse:
        price = loan_data.price
        duration = loan_data.duration
        interest_rate = loan_data.interest_rate if loan_data.interest_rate is not None else 5.0

        monthly_rate = interest_rate / 12 / 100

        if monthly_rate == 0:
            monthly_payment = price / duration
        else:
            monthly_payment = price * (monthly_rate * math.pow(1 + monthly_rate, duration)) / (math.pow(1 + monthly_rate, duration) - 1)

        total_payable = monthly_payment * duration
        total_interest = total_payable - price

        breakdown = {}
        remaining_balance = price

        for month in range(1, min(duration + 1, 13)):
            if monthly_rate == 0:
                interest_payment = 0
                principal_payment = monthly_payment
            else:
                interest_payment = remaining_balance * monthly_rate
                principal_payment = monthly_payment - interest_payment

            remaining_balance -= principal_payment

            breakdown[f"Month {month}"] = {
                "payment": round(monthly_payment, 2),
                "principal": round(principal_payment, 2),
                "interest": round(interest_payment, 2),
                "remaining_balance": round(remaining_balance, 2)
            }

        return LoanEstimateResponse(
            monthly_payment=round(monthly_payment, 2),
            total_interest=round(total_interest, 2),
            total_payable=round(total_payable, 2),
            breakdown=breakdown
        )

class UserFavoriteService:
    @staticmethod
    def toggle_favorite(db: Session, user_id: int, car_id: int) -> Tuple[bool, str]:
        car = CarRepository.get_by_id(db, car_id)
        if not car:
            raise ValueError("Car not found")

        is_currently_favorite = UserFavoriteRepository.is_favorite(db, user_id, car_id)

        if is_currently_favorite:
            UserFavoriteRepository.remove_favorite(db, user_id, car_id)
            return False, "Removed from favorites"
        else:
            UserFavoriteRepository.add_favorite(db, user_id, car_id)
            return True, "Added to favorites"

    @staticmethod
    def get_user_favorites(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[UserFavorite]:
        return UserFavoriteRepository.get_user_favorites(db, user_id, skip, limit)

    @staticmethod
    def get_favorites_count(db: Session, user_id: int) -> int:
        return UserFavoriteRepository.get_favorites_count(db, user_id)

    @staticmethod
    def is_favorite(db: Session, user_id: int, car_id: int) -> bool:
        return UserFavoriteRepository.is_favorite(db, user_id, car_id)