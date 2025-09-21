from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc
from typing import List, Optional, Dict, Any
from ..models.electronics_models import ElectronicsListing, ElectronicsImage, ElectronicsFeature, ElectronicsCategory, ElectronicsCondition, ListingStatus
from ..models.electronics_schemas import ElectronicsListingCreate, ElectronicsListingUpdate, ElectronicsSearchParams
import logging
import json

logger = logging.getLogger(__name__)

class ElectronicsRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_electronics_listing(self, electronics_data: ElectronicsListingCreate, user_id: int) -> ElectronicsListing:
        """Create a new electronics listing."""
        try:
            # Create the main electronics listing
            db_electronics = ElectronicsListing(
                **electronics_data.dict(exclude={"images", "features"}),
                user_id=user_id
            )
            
            self.db.add(db_electronics)
            self.db.flush()  # Get the ID without committing
            
            # Add images if provided
            if electronics_data.images:
                for image_data in electronics_data.images:
                    db_image = ElectronicsImage(
                        **image_data.dict(),
                        electronics_listing_id=db_electronics.id
                    )
                    self.db.add(db_image)
            
            # Add features if provided
            if electronics_data.features:
                for feature_data in electronics_data.features:
                    db_feature = ElectronicsFeature(
                        **feature_data.dict(),
                        electronics_listing_id=db_electronics.id
                    )
                    self.db.add(db_feature)
            
            self.db.commit()
            self.db.refresh(db_electronics)
            return db_electronics
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating electronics listing: {e}")
            raise

    def get_electronics_listing(self, electronics_id: int) -> Optional[ElectronicsListing]:
        """Get an electronics listing by ID."""
        return self.db.query(ElectronicsListing).filter(
            ElectronicsListing.id == electronics_id,
            ElectronicsListing.is_active == True
        ).first()

    def get_electronics_listings(self, search_params: ElectronicsSearchParams) -> tuple[List[ElectronicsListing], int]:
        """Get electronics listings with search and pagination."""
        query = self.db.query(ElectronicsListing).filter(ElectronicsListing.is_active == True)
        
        # Apply filters
        if search_params.category:
            query = query.filter(ElectronicsListing.category == search_params.category)
        
        if search_params.brand:
            query = query.filter(ElectronicsListing.brand.ilike(f"%{search_params.brand}%"))
        
        if search_params.condition:
            query = query.filter(ElectronicsListing.condition == search_params.condition)
        
        if search_params.min_price:
            query = query.filter(ElectronicsListing.price >= search_params.min_price)
        
        if search_params.max_price:
            query = query.filter(ElectronicsListing.price <= search_params.max_price)
        
        if search_params.location:
            query = query.filter(ElectronicsListing.location.ilike(f"%{search_params.location}%"))
        
        if search_params.year_from:
            query = query.filter(ElectronicsListing.year >= search_params.year_from)
        
        if search_params.year_to:
            query = query.filter(ElectronicsListing.year <= search_params.year_to)
        
        if search_params.search_query:
            search_term = f"%{search_params.search_query}%"
            query = query.filter(
                or_(
                    ElectronicsListing.title.ilike(search_term),
                    ElectronicsListing.description.ilike(search_term),
                    ElectronicsListing.brand.ilike(search_term),
                    ElectronicsListing.model.ilike(search_term)
                )
            )
        
        if search_params.has_warranty is not None:
            if search_params.has_warranty:
                query = query.filter(ElectronicsListing.warranty_remaining.isnot(None))
            else:
                query = query.filter(ElectronicsListing.warranty_remaining.is_(None))
        
        if search_params.includes_box is not None:
            query = query.filter(ElectronicsListing.includes_original_box == search_params.includes_box)
        
        if search_params.shipping_available is not None:
            query = query.filter(ElectronicsListing.shipping_available == search_params.shipping_available)
        
        # Apply sorting
        if search_params.sort_by == "price":
            if search_params.sort_order == "asc":
                query = query.order_by(asc(ElectronicsListing.price))
            else:
                query = query.order_by(desc(ElectronicsListing.price))
        elif search_params.sort_by == "year":
            if search_params.sort_order == "asc":
                query = query.order_by(asc(ElectronicsListing.year))
            else:
                query = query.order_by(desc(ElectronicsListing.year))
        elif search_params.sort_by == "title":
            if search_params.sort_order == "asc":
                query = query.order_by(asc(ElectronicsListing.title))
            else:
                query = query.order_by(desc(ElectronicsListing.title))
        else:  # default: created_at
            if search_params.sort_order == "asc":
                query = query.order_by(asc(ElectronicsListing.created_at))
            else:
                query = query.order_by(desc(ElectronicsListing.created_at))
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (search_params.page - 1) * search_params.limit
        listings = query.offset(offset).limit(search_params.limit).all()
        
        return listings, total

    def get_user_electronics_listings(self, user_id: int, page: int = 1, limit: int = 20) -> tuple[List[ElectronicsListing], int]:
        """Get electronics listings for a specific user."""
        query = self.db.query(ElectronicsListing).filter(
            ElectronicsListing.user_id == user_id,
            ElectronicsListing.is_active == True
        ).order_by(desc(ElectronicsListing.created_at))
        
        total = query.count()
        offset = (page - 1) * limit
        listings = query.offset(offset).limit(limit).all()
        
        return listings, total

    def update_electronics_listing(self, electronics_id: int, electronics_data: ElectronicsListingUpdate, user_id: int) -> Optional[ElectronicsListing]:
        """Update an electronics listing."""
        try:
            db_electronics = self.db.query(ElectronicsListing).filter(
                ElectronicsListing.id == electronics_id,
                ElectronicsListing.user_id == user_id,
                ElectronicsListing.is_active == True
            ).first()
            
            if not db_electronics:
                return None
            
            # Update fields
            update_data = electronics_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_electronics, field, value)
            
            self.db.commit()
            self.db.refresh(db_electronics)
            return db_electronics
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating electronics listing: {e}")
            raise

    def delete_electronics_listing(self, electronics_id: int, user_id: int) -> bool:
        """Soft delete an electronics listing."""
        try:
            db_electronics = self.db.query(ElectronicsListing).filter(
                ElectronicsListing.id == electronics_id,
                ElectronicsListing.user_id == user_id
            ).first()
            
            if not db_electronics:
                return False
            
            db_electronics.is_active = False
            db_electronics.status = ListingStatus.REMOVED
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting electronics listing: {e}")
            raise

    def mark_as_sold(self, electronics_id: int, user_id: int) -> bool:
        """Mark an electronics listing as sold."""
        try:
            db_electronics = self.db.query(ElectronicsListing).filter(
                ElectronicsListing.id == electronics_id,
                ElectronicsListing.user_id == user_id,
                ElectronicsListing.is_active == True
            ).first()
            
            if not db_electronics:
                return False
            
            db_electronics.status = ListingStatus.SOLD
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error marking electronics listing as sold: {e}")
            raise

    def add_images_to_listing(self, electronics_id: int, user_id: int, image_urls: List[str]) -> bool:
        """Add images to an electronics listing."""
        try:
            # Verify ownership
            electronics_listing = self.db.query(ElectronicsListing).filter(
                ElectronicsListing.id == electronics_id,
                ElectronicsListing.user_id == user_id
            ).first()
            
            if not electronics_listing:
                return False
            
            # Add images
            for url in image_urls:
                db_image = ElectronicsImage(
                    electronics_listing_id=electronics_id,
                    image_url=url,
                    is_primary=False
                )
                self.db.add(db_image)
            
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error adding images: {e}")
            raise

    def remove_image(self, image_id: int, user_id: int) -> bool:
        """Remove an image from an electronics listing."""
        try:
            image = self.db.query(ElectronicsImage).join(ElectronicsListing).filter(
                ElectronicsImage.id == image_id,
                ElectronicsListing.user_id == user_id
            ).first()
            
            if not image:
                return False
            
            self.db.delete(image)
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error removing image: {e}")
            raise

    def get_electronics_statistics(self, user_id: int) -> Dict[str, Any]:
        """Get electronics statistics for a user."""
        try:
            # Get user's listings
            total_listings = self.db.query(ElectronicsListing).filter(
                ElectronicsListing.user_id == user_id
            ).count()
            
            active_listings = self.db.query(ElectronicsListing).filter(
                ElectronicsListing.user_id == user_id,
                ElectronicsListing.is_active == True,
                ElectronicsListing.status == ListingStatus.ACTIVE
            ).count()
            
            sold_listings = self.db.query(ElectronicsListing).filter(
                ElectronicsListing.user_id == user_id,
                ElectronicsListing.status == ListingStatus.SOLD
            ).count()
            
            # Calculate total value and average price
            listings = self.db.query(ElectronicsListing).filter(
                ElectronicsListing.user_id == user_id,
                ElectronicsListing.is_active == True
            ).all()
            
            total_value = sum(listing.price for listing in listings)
            average_price = total_value / len(listings) if listings else 0
            
            return {
                "total_listings": total_listings,
                "active_listings": active_listings,
                "sold_listings": sold_listings,
                "total_value": total_value,
                "average_price": average_price
            }
            
        except Exception as e:
            logger.error(f"Error getting electronics statistics: {e}")
            raise

    def get_featured_listings(self, limit: int = 10) -> List[ElectronicsListing]:
        """Get featured electronics listings."""
        return self.db.query(ElectronicsListing).filter(
            ElectronicsListing.is_active == True,
            ElectronicsListing.status == ListingStatus.ACTIVE
        ).order_by(desc(ElectronicsListing.created_at)).limit(limit).all()