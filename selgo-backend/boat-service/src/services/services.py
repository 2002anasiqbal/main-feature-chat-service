from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any, Tuple
from ..repositories.repositories import (
    BoatCategoryRepository, 
    BoatFeatureRepository, 
    BoatRepository, 
    BoatImageRepository, 
    BoatRatingRepository, 
    BoatFixDoneRequestRepository,
    UserFavoriteRepository
)
from ..models.boat_models import (
    BoatCategory, 
    BoatFeature, 
    Boat, 
    BoatImage, 
    BoatRating, 
    BoatFixDoneRequest,
    UserFavorite,
    FixRequestStatus
)
from ..models.boat_schemas import (
    BoatCategoryCreate, 
    BoatCategoryResponse, 
    BoatFeatureCreate, 
    BoatCreate, 
    BoatUpdate, 
    BoatFilterParams, 
    BoatImageCreate, 
    BoatRatingCreate, 
    BoatFixDoneRequestCreate,
    BoatFixDoneRequestStatusUpdate,
    LoanEstimateRequest, 
    LoanEstimateResponse,
    GeoPoint
)
import math
import logging

logger = logging.getLogger(__name__)

class BoatCategoryService:
    @staticmethod
    def create_category(db: Session, category_data: BoatCategoryCreate) -> BoatCategory:
        return BoatCategoryRepository.create(db, category_data.dict())
    
    @staticmethod
    def get_category_by_id(db: Session, category_id: int) -> Optional[BoatCategory]:
        return BoatCategoryRepository.get_by_id(db, category_id)
    
    @staticmethod
    def get_all_categories(db: Session, skip: int = 0, limit: int = 100) -> List[BoatCategory]:
        return BoatCategoryRepository.get_all(db, skip, limit)
    
    @staticmethod
    def get_categories_with_counts(db: Session) -> List[Tuple[BoatCategory, int]]:
        return BoatCategoryRepository.get_all_with_counts(db)
    
    @staticmethod
    def get_top_level_categories(db: Session) -> List[BoatCategory]:
        return BoatCategoryRepository.get_by_parent_id(db, None)
    
    @staticmethod
    def get_subcategories(db: Session, parent_id: int) -> List[BoatCategory]:
        return BoatCategoryRepository.get_by_parent_id(db, parent_id)
    
    @staticmethod
    def update_category(db: Session, category_id: int, category_data: BoatCategoryCreate) -> Optional[BoatCategory]:
        return BoatCategoryRepository.update(db, category_id, category_data.dict())
    
    @staticmethod
    def delete_category(db: Session, category_id: int) -> bool:
        return BoatCategoryRepository.delete(db, category_id)

class BoatFeatureService:
    @staticmethod
    def create_feature(db: Session, feature_data: BoatFeatureCreate) -> BoatFeature:
        return BoatFeatureRepository.create(db, feature_data.dict())
    
    @staticmethod
    def get_feature_by_id(db: Session, feature_id: int) -> Optional[BoatFeature]:
        return BoatFeatureRepository.get_by_id(db, feature_id)
    
    @staticmethod
    def get_all_features(db: Session, skip: int = 0, limit: int = 100) -> List[BoatFeature]:
        return BoatFeatureRepository.get_all(db, skip, limit)
    
    @staticmethod
    def update_feature(db: Session, feature_id: int, feature_data: BoatFeatureCreate) -> Optional[BoatFeature]:
        return BoatFeatureRepository.update(db, feature_id, feature_data.dict())
    
    @staticmethod
    def delete_feature(db: Session, feature_id: int) -> bool:
        return BoatFeatureRepository.delete(db, feature_id)

class BoatService:
    
    @staticmethod
    def search_boats_with_types(
        db: Session, 
        filters: BoatFilterParams,
        boat_types: List[str] = None
    ) -> Tuple[List[Boat], int]:
        """
        Search boats with support for multiple boat types
        """
        return BoatRepository.filter_boats_with_types(db, filters, boat_types)
    
    @staticmethod
    def create_boat(db: Session, boat_data: BoatCreate, user_id: int) -> Boat:
        # Get features if provided
        features = []
        if boat_data.features:
            features = BoatFeatureRepository.get_by_ids(db, boat_data.features)
        
        # Extract images data to handle separately
        images_data = []
        if hasattr(boat_data, 'images') and boat_data.images:
            images_data = boat_data.images
        
        # Create the boat
        boat_dict = boat_data.dict(exclude={'features', 'images'})
        boat_dict['user_id'] = user_id
        
        db_boat = BoatRepository.create(db, boat_dict, features)
        
        # Add images if provided
        if images_data:
            BoatImageRepository.create_many(db, db_boat.id, [img.dict() for img in images_data])
        
        return db_boat
    
    @staticmethod
    def get_featured_boats(db: Session, limit: int = 10) -> List[Boat]:
        """
        Get featured boats - prioritize newly created ones
        """
        from sqlalchemy import desc
        query = db.query(Boat).filter(Boat.status == "active")
        
        # Check for newly created boats (within last 24 hours)
        from datetime import datetime, timedelta
        recent_cutoff = datetime.utcnow() - timedelta(hours=24)
        
        # First get recent boats, then older ones
        query = query.order_by(
            desc(Boat.created_at >= recent_cutoff),  # Recent boats first
            desc(Boat.created_at)  # Then by creation date
        )
        return query.limit(limit).all()
    
    @staticmethod
    def get_homepage_boats(db: Session, limit: int = 10) -> List[Boat]:
        """
        Get boats for homepage display - mix of new and featured
        """
        from sqlalchemy import desc, or_
        query = db.query(Boat).filter(Boat.status == "active")
        
        # Prioritize: featured boats OR newly created boats (last 6 hours)
        from datetime import datetime, timedelta
        very_recent_cutoff = datetime.utcnow() - timedelta(hours=6)
        
        query = query.order_by(
            desc(or_(Boat.is_featured == True, Boat.created_at >= very_recent_cutoff)),
            desc(Boat.created_at)
        )
        return query.limit(limit).all()
    
    @staticmethod
    def get_boat_by_id(db: Session, boat_id: int, increment_view: bool = False) -> Optional[Boat]:
        boat = BoatRepository.get_by_id(db, boat_id)
        
        # Increment view count if requested
        if boat and increment_view:
            boat = BoatRepository.increment_view_count(db, boat_id)
        
        return boat
    
    @staticmethod
    def get_all_boats(db: Session, skip: int = 0, limit: int = 100) -> List[Boat]:
        return BoatRepository.get_all(db, skip, limit)
    
    @staticmethod
    def filter_boats(db: Session, filters) -> Tuple[List[Boat], int]:
        """
        Enhanced filter method that handles boat types properly
        """
        
        # ✅ Check if we have boat_types and use the appropriate repository method
        if hasattr(filters, 'boat_types') and filters.boat_types and len(filters.boat_types) > 0:
            return BoatRepository.filter_boats_with_types(db, filters, filters.boat_types)
        else:
            return BoatRepository.filter_boats(db, filters)
    
    @staticmethod
    def get_recommended_boats(db: Session, limit: int = 10) -> List[Boat]:
        return BoatRepository.get_recommended_boats(db, limit)
    
    @staticmethod
    def update_boat(db: Session, boat_id: int, boat_data: BoatUpdate, user_id: int) -> Optional[Boat]:
        # Check boat exists and belongs to user
        boat = BoatRepository.get_by_id(db, boat_id)
        if not boat or boat.user_id != user_id:
            return None
        
        # Get features if provided
        features = None
        if boat_data.features is not None:
            features = BoatFeatureRepository.get_by_ids(db, boat_data.features)
        
        # Update the boat
        boat_dict = boat_data.dict(exclude_unset=True, exclude={'features'})
        return BoatRepository.update(db, boat_id, boat_dict, features)
    
    @staticmethod
    def delete_boat(db: Session, boat_id: int, user_id: int) -> bool:
        # Check boat exists and belongs to user
        boat = BoatRepository.get_by_id(db, boat_id)
        if not boat or boat.user_id != user_id:
            return False
        
        return BoatRepository.delete(db, boat_id)

class BoatImageService:
    @staticmethod
    def add_image(db: Session, boat_id: int, image_data: BoatImageCreate, user_id: int) -> Optional[BoatImage]:
        # Check boat exists and belongs to user
        boat = BoatRepository.get_by_id(db, boat_id)
        if not boat or boat.user_id != user_id:
            return None
        
        return BoatImageRepository.create(db, boat_id, image_data.dict())
    
    @staticmethod
    def get_images(db: Session, boat_id: int) -> List[BoatImage]:
        return BoatImageRepository.get_by_boat_id(db, boat_id)
    
    @staticmethod
    def delete_image(db: Session, image_id: int, user_id: int) -> bool:
        # Check image exists and belongs to user's boat
        image = BoatImageRepository.get_by_id(db, image_id)
        if not image:
            return False
        
        boat = BoatRepository.get_by_id(db, image.boat_id)
        if not boat or boat.user_id != user_id:
            return False
        
        return BoatImageRepository.delete(db, image_id)

class BoatRatingService:
    @staticmethod
    def create_rating(db: Session, rating_data: BoatRatingCreate, user_id: int) -> Optional[BoatRating]:
        # Check if boat exists
        boat = BoatRepository.get_by_id(db, rating_data.boat_id)
        if not boat:
            return None
        
        # Check if user has already rated this boat
        existing_ratings = BoatRatingRepository.get_by_boat_id(db, rating_data.boat_id)
        for rating in existing_ratings:
            if rating.user_id == user_id:
                # Update existing rating instead of creating a new one
                return BoatRatingRepository.update(db, rating.id, {
                    'stars': rating_data.stars,
                    'review': rating_data.review
                })
        
        # Create new rating
        rating_dict = rating_data.dict()
        rating_dict['user_id'] = user_id
        return BoatRatingRepository.create(db, rating_dict)
    
    @staticmethod
    def get_ratings_by_boat_id(db: Session, boat_id: int, skip: int = 0, limit: int = 100) -> List[BoatRating]:
        return BoatRatingRepository.get_by_boat_id(db, boat_id, skip, limit)
    
    @staticmethod
    def get_avg_rating(db: Session, boat_id: int) -> float:
        return BoatRatingRepository.get_avg_rating(db, boat_id)
    
    @staticmethod
    def delete_rating(db: Session, rating_id: int, user_id: int) -> bool:
        # Check rating exists and belongs to user
        rating = BoatRatingRepository.get_by_id(db, rating_id)
        if not rating or rating.user_id != user_id:
            return False
        
        return BoatRatingRepository.delete(db, rating_id)

class BoatFixDoneRequestService:
    @staticmethod
    def create_request(db: Session, request_data: BoatFixDoneRequestCreate, buyer_id: int) -> Optional[BoatFixDoneRequest]:
        # Check if boat exists
        boat = BoatRepository.get_by_id(db, request_data.boat_id)
        if not boat:
            return None
        
        # Ensure buyer is not the seller
        if boat.user_id == buyer_id:
            return None
        
        # Create the request
        request_dict = request_data.dict()
        request_dict['buyer_id'] = buyer_id
        request_dict['seller_id'] = boat.user_id
        request_dict['status'] = FixRequestStatus.REQUESTED
        
        return BoatFixDoneRequestRepository.create(db, request_dict)
    
    @staticmethod
    def get_request_by_id(db: Session, request_id: int) -> Optional[BoatFixDoneRequest]:
        return BoatFixDoneRequestRepository.get_by_id(db, request_id)
    
    @staticmethod
    def get_requests_by_boat_id(db: Session, boat_id: int) -> List[BoatFixDoneRequest]:
        return BoatFixDoneRequestRepository.get_by_boat_id(db, boat_id)
    
    @staticmethod
    def get_requests_by_buyer_id(db: Session, buyer_id: int) -> List[BoatFixDoneRequest]:
        return BoatFixDoneRequestRepository.get_by_buyer_id(db, buyer_id)
    
    @staticmethod
    def get_requests_by_seller_id(db: Session, seller_id: int) -> List[BoatFixDoneRequest]:
        return BoatFixDoneRequestRepository.get_by_seller_id(db, seller_id)
    
    @staticmethod
    def update_request_status(
        db: Session, 
        request_id: int, 
        status_update: BoatFixDoneRequestStatusUpdate, 
        user_id: int
    ) -> Optional[BoatFixDoneRequest]:
        # Check request exists
        request = BoatFixDoneRequestRepository.get_by_id(db, request_id)
        if not request:
            return None
        
        # Validate if user is authorized (either buyer or seller depending on the status change)
        if status_update.status == FixRequestStatus.APPROVED or status_update.status == FixRequestStatus.DECLINED:
            # Only seller can approve or decline
            if request.seller_id != user_id:
                return None
        elif status_update.status == FixRequestStatus.CANCELLED:
            # Only buyer can cancel
            if request.buyer_id != user_id:
                return None
        elif status_update.status == FixRequestStatus.COMPLETED:
            # Both buyer and seller can mark as completed
            if request.buyer_id != user_id and request.seller_id != user_id:
                return None
        
        # Validate status transitions
        valid_transitions = {
            FixRequestStatus.REQUESTED: [FixRequestStatus.APPROVED, FixRequestStatus.DECLINED, FixRequestStatus.CANCELLED],
            FixRequestStatus.APPROVED: [FixRequestStatus.COMPLETED, FixRequestStatus.CANCELLED],
            FixRequestStatus.DECLINED: [],
            FixRequestStatus.COMPLETED: [],
            FixRequestStatus.CANCELLED: []
        }
        
        if status_update.status not in valid_transitions.get(request.status, []):
            return None
        
        return BoatFixDoneRequestRepository.update_status(db, request_id, status_update.status)

class LoanEstimateService:
    @staticmethod
    def calculate_loan(loan_data: LoanEstimateRequest) -> LoanEstimateResponse:
        """
        Calculate loan payments based on the price, duration, and interest rate.
        
        Formula: PMT = P * (r * (1 + r)^n) / ((1 + r)^n - 1)
        Where:
        - PMT is the monthly payment
        - P is the principal (loan amount)
        - r is the monthly interest rate (annual rate / 12 / 100)
        - n is the total number of payments (loan term in months)
        """
        price = loan_data.price
        duration = loan_data.duration
        
        # Use default interest rate if not provided
        interest_rate = loan_data.interest_rate if loan_data.interest_rate is not None else 5.0
        
        # Convert annual interest rate to monthly decimal
        monthly_rate = interest_rate / 12 / 100
        
        if monthly_rate == 0:
            # If interest rate is zero, simple division
            monthly_payment = price / duration
        else:
            # PMT formula
            monthly_payment = price * (monthly_rate * math.pow(1 + monthly_rate, duration)) / (math.pow(1 + monthly_rate, duration) - 1)
        
        total_payable = monthly_payment * duration
        total_interest = total_payable - price
        
        # Create monthly breakdown
        breakdown = {}
        remaining_balance = price
        
        for month in range(1, min(duration + 1, 13)):  # Show first 12 months or fewer if duration is shorter
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


#Favourites
class UserFavoriteService:
    @staticmethod
    def toggle_favorite(db: Session, user_id: int, boat_id: int) -> Tuple[bool, str]:
        """Toggle favorite status and return (is_favorite, message)"""
        # Check if boat exists
        boat = BoatRepository.get_by_id(db, boat_id)
        if not boat:
            raise ValueError("Boat not found")
        
        # Check current favorite status
        is_currently_favorite = UserFavoriteRepository.is_favorite(db, user_id, boat_id)
        
        if is_currently_favorite:
            # Remove from favorites
            UserFavoriteRepository.remove_favorite(db, user_id, boat_id)
            return False, "Removed from favorites"
        else:
            # Add to favorites
            UserFavoriteRepository.add_favorite(db, user_id, boat_id)
            return True, "Added to favorites"
    
    @staticmethod
    def get_user_favorites(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[UserFavorite]:
        return UserFavoriteRepository.get_user_favorites(db, user_id, skip, limit)
    
    @staticmethod
    def get_favorites_count(db: Session, user_id: int) -> int:
        return UserFavoriteRepository.get_favorites_count(db, user_id)
    
    @staticmethod
    def is_favorite(db: Session, user_id: int, boat_id: int) -> bool:
        return UserFavoriteRepository.is_favorite(db, user_id, boat_id)