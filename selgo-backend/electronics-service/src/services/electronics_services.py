from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from ..repositories.electronics_repositories import ElectronicsRepository
from ..models.electronics_schemas import (
    ElectronicsListingCreate, ElectronicsListingUpdate, ElectronicsSearchParams,
    ElectronicsListing, ElectronicsListResponse, ElectronicsStatsResponse
)
from ..utils.file_utils import file_utils
from fastapi import UploadFile, HTTPException
import logging
import math

logger = logging.getLogger(__name__)

class ElectronicsService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ElectronicsRepository(db)

    async def create_electronics_listing(self, electronics_data: ElectronicsListingCreate, user_id: int) -> ElectronicsListing:
        """Create a new electronics listing."""
        try:
            db_electronics = self.repository.create_electronics_listing(electronics_data, user_id)
            return ElectronicsListing.from_orm(db_electronics)
        except Exception as e:
            logger.error(f"Error in electronics service create_electronics_listing: {e}")
            raise HTTPException(status_code=500, detail="Error creating electronics listing")

    async def get_electronics_listing(self, electronics_id: int) -> Optional[ElectronicsListing]:
        """Get an electronics listing by ID."""
        try:
            db_electronics = self.repository.get_electronics_listing(electronics_id)
            return ElectronicsListing.from_orm(db_electronics) if db_electronics else None
        except Exception as e:
            logger.error(f"Error in electronics service get_electronics_listing: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving electronics listing")

    async def search_electronics_listings(self, search_params: ElectronicsSearchParams) -> ElectronicsListResponse:
        """Search electronics listings with filters and pagination."""
        try:
            listings, total = self.repository.get_electronics_listings(search_params)
            
            electronics_listings = [ElectronicsListing.from_orm(listing) for listing in listings]
            total_pages = math.ceil(total / search_params.limit)
            
            return ElectronicsListResponse(
                items=electronics_listings,
                total=total,
                page=search_params.page,
                limit=search_params.limit,
                total_pages=total_pages
            )
        except Exception as e:
            logger.error(f"Error in electronics service search_electronics_listings: {e}")
            raise HTTPException(status_code=500, detail="Error searching electronics listings")

    async def get_user_electronics_listings(self, user_id: int, page: int = 1, limit: int = 20) -> ElectronicsListResponse:
        """Get electronics listings for a specific user."""
        try:
            listings, total = self.repository.get_user_electronics_listings(user_id, page, limit)
            
            electronics_listings = [ElectronicsListing.from_orm(listing) for listing in listings]
            total_pages = math.ceil(total / limit)
            
            return ElectronicsListResponse(
                items=electronics_listings,
                total=total,
                page=page,
                limit=limit,
                total_pages=total_pages
            )
        except Exception as e:
            logger.error(f"Error in electronics service get_user_electronics_listings: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving user electronics listings")

    async def update_electronics_listing(self, electronics_id: int, electronics_data: ElectronicsListingUpdate, user_id: int) -> Optional[ElectronicsListing]:
        """Update an electronics listing."""
        try:
            db_electronics = self.repository.update_electronics_listing(electronics_id, electronics_data, user_id)
            return ElectronicsListing.from_orm(db_electronics) if db_electronics else None
        except Exception as e:
            logger.error(f"Error in electronics service update_electronics_listing: {e}")
            raise HTTPException(status_code=500, detail="Error updating electronics listing")

    async def delete_electronics_listing(self, electronics_id: int, user_id: int) -> bool:
        """Delete an electronics listing."""
        try:
            return self.repository.delete_electronics_listing(electronics_id, user_id)
        except Exception as e:
            logger.error(f"Error in electronics service delete_electronics_listing: {e}")
            raise HTTPException(status_code=500, detail="Error deleting electronics listing")

    async def mark_as_sold(self, electronics_id: int, user_id: int) -> bool:
        """Mark an electronics listing as sold."""
        try:
            return self.repository.mark_as_sold(electronics_id, user_id)
        except Exception as e:
            logger.error(f"Error in electronics service mark_as_sold: {e}")
            raise HTTPException(status_code=500, detail="Error marking listing as sold")

    async def upload_electronics_images(self, electronics_id: int, user_id: int, files: List[UploadFile]) -> Dict[str, Any]:
        """Upload images for an electronics listing."""
        try:
            # Save files
            file_paths = await file_utils.save_multiple_files(files, f"electronics/{electronics_id}")
            
            # Generate URLs
            image_urls = [file_utils.get_file_url(path) for path in file_paths]
            
            # Add to database
            success = self.repository.add_images_to_listing(electronics_id, user_id, image_urls)
            
            if success:
                return {
                    "message": "Images uploaded successfully",
                    "image_urls": image_urls,
                    "count": len(image_urls)
                }
            else:
                raise HTTPException(status_code=404, detail="Electronics listing not found or access denied")
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in electronics service upload_electronics_images: {e}")
            raise HTTPException(status_code=500, detail="Error uploading images")

    async def remove_electronics_image(self, image_id: int, user_id: int) -> bool:
        """Remove an image from an electronics listing."""
        try:
            return self.repository.remove_image(image_id, user_id)
        except Exception as e:
            logger.error(f"Error in electronics service remove_electronics_image: {e}")
            raise HTTPException(status_code=500, detail="Error removing image")

    async def get_electronics_statistics(self, user_id: int) -> ElectronicsStatsResponse:
        """Get electronics statistics for a user."""
        try:
            stats = self.repository.get_electronics_statistics(user_id)
            return ElectronicsStatsResponse(**stats)
        except Exception as e:
            logger.error(f"Error in electronics service get_electronics_statistics: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving statistics")

    async def get_featured_listings(self, limit: int = 10) -> List[ElectronicsListing]:
        """Get featured electronics listings."""
        try:
            listings = self.repository.get_featured_listings(limit)
            return [ElectronicsListing.from_orm(listing) for listing in listings]
        except Exception as e:
            logger.error(f"Error in electronics service get_featured_listings: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving featured listings")