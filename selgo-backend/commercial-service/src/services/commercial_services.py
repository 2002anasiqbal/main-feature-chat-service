from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc
from typing import List, Optional, Dict, Any
from fastapi import HTTPException, UploadFile
from ..models.commercial_models import CommercialVehicleListing, CommercialVehicleImage, CommercialVehicleFeature
from ..models.commercial_schemas import (
    CommercialVehicleListingCreate, CommercialVehicleListingUpdate, CommercialVehicleListingResponse,
    CommercialVehicleListingListResponse, CommercialVehicleSearchRequest, CommercialVehicleStats,
    ListingStatusEnum
)
from ..repositories.commercial_repositories import CommercialVehicleRepository
import os
import uuid
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class CommercialVehicleService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = CommercialVehicleRepository(db)

    async def create_listing(self, listing_data: CommercialVehicleListingCreate, user_id: int) -> CommercialVehicleListingResponse:
        """Create a new commercial vehicle listing."""
        try:
            # Create the main listing
            listing_dict = listing_data.dict(exclude={'images', 'features'})
            listing_dict['user_id'] = user_id
            
            listing = await self.repository.create_listing(listing_dict)
            
            # Add images if provided
            if listing_data.images:
                for image_data in listing_data.images:
                    image_dict = image_data.dict()
                    image_dict['vehicle_listing_id'] = listing.id
                    await self.repository.create_image(image_dict)
            
            # Add features if provided
            if listing_data.features:
                for feature_data in listing_data.features:
                    feature_dict = feature_data.dict()
                    feature_dict['vehicle_listing_id'] = listing.id
                    await self.repository.create_feature(feature_dict)
            
            # Refresh to get related data
            self.db.refresh(listing)
            return CommercialVehicleListingResponse.from_orm(listing)
            
        except Exception as e:
            logger.error(f"Error creating commercial vehicle listing: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to create commercial vehicle listing")

    async def get_listing_by_id(self, listing_id: int) -> Optional[CommercialVehicleListingResponse]:
        """Get a commercial vehicle listing by ID."""
        listing = await self.repository.get_listing_by_id(listing_id)
        if listing:
            return CommercialVehicleListingResponse.from_orm(listing)
        return None

    async def update_listing(self, listing_id: int, listing_data: CommercialVehicleListingUpdate, user_id: int) -> Optional[CommercialVehicleListingResponse]:
        """Update a commercial vehicle listing."""
        # Check if listing exists and belongs to user
        existing_listing = await self.repository.get_listing_by_id(listing_id)
        if not existing_listing or existing_listing.user_id != user_id:
            return None
        
        # Update the listing
        update_dict = listing_data.dict(exclude_unset=True)
        listing = await self.repository.update_listing(listing_id, update_dict)
        
        if listing:
            return CommercialVehicleListingResponse.from_orm(listing)
        return None

    async def delete_listing(self, listing_id: int, user_id: int) -> bool:
        """Delete a commercial vehicle listing."""
        # Check if listing exists and belongs to user
        existing_listing = await self.repository.get_listing_by_id(listing_id)
        if not existing_listing or existing_listing.user_id != user_id:
            return False
        
        return await self.repository.delete_listing(listing_id)

    async def search_listings(self, search_request: CommercialVehicleSearchRequest) -> CommercialVehicleListingListResponse:
        """Search commercial vehicle listings with filters."""
        try:
            listings, total = await self.repository.search_listings(search_request)
            
            total_pages = (total + search_request.per_page - 1) // search_request.per_page
            
            return CommercialVehicleListingListResponse(
                listings=[CommercialVehicleListingResponse.from_orm(listing) for listing in listings],
                total=total,
                page=search_request.page,
                per_page=search_request.per_page,
                total_pages=total_pages
            )
        except Exception as e:
            logger.error(f"Error searching commercial vehicle listings: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to search commercial vehicle listings")

    async def get_user_listings(self, user_id: int, page: int = 1, per_page: int = 20) -> CommercialVehicleListingListResponse:
        """Get user's commercial vehicle listings."""
        try:
            listings, total = await self.repository.get_user_listings(user_id, page, per_page)
            
            total_pages = (total + per_page - 1) // per_page
            
            return CommercialVehicleListingListResponse(
                listings=[CommercialVehicleListingResponse.from_orm(listing) for listing in listings],
                total=total,
                page=page,
                per_page=per_page,
                total_pages=total_pages
            )
        except Exception as e:
            logger.error(f"Error getting user commercial vehicle listings: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to get user commercial vehicle listings")

    async def upload_images(self, listing_id: int, files: List[UploadFile], user_id: int) -> Dict[str, Any]:
        """Upload images for a commercial vehicle listing."""
        # Check if listing exists and belongs to user
        existing_listing = await self.repository.get_listing_by_id(listing_id)
        if not existing_listing or existing_listing.user_id != user_id:
            raise HTTPException(status_code=404, detail="Commercial vehicle listing not found or not authorized")
        
        uploaded_images = []
        upload_dir = "uploads/commercial-vehicles"
        os.makedirs(upload_dir, exist_ok=True)
        
        for file in files:
            try:
                # Generate unique filename
                file_extension = os.path.splitext(file.filename)[1]
                unique_filename = f"{uuid.uuid4()}{file_extension}"
                file_path = os.path.join(upload_dir, unique_filename)
                
                # Save file
                with open(file_path, "wb") as buffer:
                    content = await file.read()
                    buffer.write(content)
                
                # Create thumbnail if it's an image
                if file_extension.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
                    try:
                        with Image.open(file_path) as img:
                            img.thumbnail((800, 600))
                            img.save(file_path, optimize=True, quality=85)
                    except Exception as e:
                        logger.warning(f"Failed to create thumbnail: {str(e)}")
                
                # Save to database
                image_data = {
                    'vehicle_listing_id': listing_id,
                    'image_url': f"/uploads/commercial-vehicles/{unique_filename}",
                    'alt_text': f"Commercial vehicle image",
                    'is_primary': len(uploaded_images) == 0  # First image is primary
                }
                
                image = await self.repository.create_image(image_data)
                uploaded_images.append(image)
                
            except Exception as e:
                logger.error(f"Error uploading image {file.filename}: {str(e)}")
                continue
        
        return {
            "message": f"Successfully uploaded {len(uploaded_images)} images",
            "images": uploaded_images
        }

    async def delete_image(self, listing_id: int, image_id: int, user_id: int) -> bool:
        """Delete an image from a commercial vehicle listing."""
        # Check if listing exists and belongs to user
        existing_listing = await self.repository.get_listing_by_id(listing_id)
        if not existing_listing or existing_listing.user_id != user_id:
            return False
        
        return await self.repository.delete_image(image_id)

    async def get_stats(self) -> CommercialVehicleStats:
        """Get commercial vehicle marketplace statistics."""
        try:
            stats = await self.repository.get_stats()
            return CommercialVehicleStats(**stats)
        except Exception as e:
            logger.error(f"Error getting commercial vehicle stats: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to get commercial vehicle statistics")

    async def get_makes(self, vehicle_type: Optional[str] = None) -> List[str]:
        """Get list of available commercial vehicle makes."""
        return await self.repository.get_makes(vehicle_type)

    async def get_models(self, make: str, vehicle_type: Optional[str] = None) -> List[str]:
        """Get list of available commercial vehicle models for a specific make."""
        return await self.repository.get_models(make, vehicle_type)

    async def get_featured_listings(self, limit: int = 10) -> CommercialVehicleListingListResponse:
        """Get featured commercial vehicle listings."""
        try:
            listings = await self.repository.get_featured_listings(limit)
            
            return CommercialVehicleListingListResponse(
                listings=[CommercialVehicleListingResponse.from_orm(listing) for listing in listings],
                total=len(listings),
                page=1,
                per_page=limit,
                total_pages=1
            )
        except Exception as e:
            logger.error(f"Error getting featured commercial vehicle listings: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to get featured commercial vehicle listings")

    async def mark_as_sold(self, listing_id: int, user_id: int) -> bool:
        """Mark a commercial vehicle listing as sold."""
        # Check if listing exists and belongs to user
        existing_listing = await self.repository.get_listing_by_id(listing_id)
        if not existing_listing or existing_listing.user_id != user_id:
            return False
        
        update_data = {
            'status': ListingStatusEnum.SOLD,
            'is_active': False
        }
        
        listing = await self.repository.update_listing(listing_id, update_data)
        return listing is not None

    async def mark_as_available(self, listing_id: int, user_id: int) -> bool:
        """Mark a commercial vehicle listing as available."""
        # Check if listing exists and belongs to user
        existing_listing = await self.repository.get_listing_by_id(listing_id)
        if not existing_listing or existing_listing.user_id != user_id:
            return False
        
        update_data = {
            'status': ListingStatusEnum.ACTIVE,
            'is_active': True
        }
        
        listing = await self.repository.update_listing(listing_id, update_data)
        return listing is not None