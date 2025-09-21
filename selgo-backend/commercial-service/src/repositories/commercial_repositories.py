from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc
from typing import List, Optional, Dict, Any, Tuple
from ..models.commercial_models import CommercialVehicleListing, CommercialVehicleImage, CommercialVehicleFeature, ListingStatus
from ..models.commercial_schemas import CommercialVehicleSearchRequest
import logging

logger = logging.getLogger(__name__)

class CommercialVehicleRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create_listing(self, listing_data: Dict[str, Any]) -> CommercialVehicleListing:
        """Create a new commercial vehicle listing."""
        listing = CommercialVehicleListing(**listing_data)
        self.db.add(listing)
        self.db.commit()
        self.db.refresh(listing)
        return listing

    async def get_listing_by_id(self, listing_id: int) -> Optional[CommercialVehicleListing]:
        """Get a commercial vehicle listing by ID."""
        return self.db.query(CommercialVehicleListing).filter(
            CommercialVehicleListing.id == listing_id
        ).first()

    async def update_listing(self, listing_id: int, update_data: Dict[str, Any]) -> Optional[CommercialVehicleListing]:
        """Update a commercial vehicle listing."""
        listing = self.db.query(CommercialVehicleListing).filter(
            CommercialVehicleListing.id == listing_id
        ).first()
        
        if listing:
            for key, value in update_data.items():
                setattr(listing, key, value)
            self.db.commit()
            self.db.refresh(listing)
        
        return listing

    async def delete_listing(self, listing_id: int) -> bool:
        """Delete a commercial vehicle listing."""
        listing = self.db.query(CommercialVehicleListing).filter(
            CommercialVehicleListing.id == listing_id
        ).first()
        
        if listing:
            self.db.delete(listing)
            self.db.commit()
            return True
        return False

    async def search_listings(self, search_request: CommercialVehicleSearchRequest) -> Tuple[List[CommercialVehicleListing], int]:
        """Search commercial vehicle listings with filters."""
        query = self.db.query(CommercialVehicleListing).filter(
            CommercialVehicleListing.is_active == True
        )
        
        # Apply filters
        if search_request.filters:
            filters = search_request.filters
            
            if filters.vehicle_type:
                query = query.filter(CommercialVehicleListing.vehicle_type.in_(filters.vehicle_type))
            
            if filters.make:
                query = query.filter(CommercialVehicleListing.make.in_(filters.make))
            
            if filters.model:
                query = query.filter(CommercialVehicleListing.model.in_(filters.model))
            
            if filters.year_from:
                query = query.filter(CommercialVehicleListing.year >= filters.year_from)
            
            if filters.year_to:
                query = query.filter(CommercialVehicleListing.year <= filters.year_to)
            
            if filters.price_from:
                query = query.filter(CommercialVehicleListing.price >= filters.price_from)
            
            if filters.price_to:
                query = query.filter(CommercialVehicleListing.price <= filters.price_to)
            
            if filters.mileage_from:
                query = query.filter(CommercialVehicleListing.mileage >= filters.mileage_from)
            
            if filters.mileage_to:
                query = query.filter(CommercialVehicleListing.mileage <= filters.mileage_to)
            
            if filters.fuel_type:
                query = query.filter(CommercialVehicleListing.fuel_type.in_(filters.fuel_type))
            
            if filters.transmission:
                query = query.filter(CommercialVehicleListing.transmission.in_(filters.transmission))
            
            if filters.condition:
                query = query.filter(CommercialVehicleListing.condition.in_(filters.condition))
            
            if filters.location:
                query = query.filter(CommercialVehicleListing.location.ilike(f"%{filters.location}%"))
            
            if filters.payload_capacity_from:
                query = query.filter(CommercialVehicleListing.payload_capacity >= filters.payload_capacity_from)
            
            if filters.payload_capacity_to:
                query = query.filter(CommercialVehicleListing.payload_capacity <= filters.payload_capacity_to)
            
            if filters.has_valid_inspection is not None:
                query = query.filter(CommercialVehicleListing.has_valid_inspection == filters.has_valid_inspection)
            
            if filters.delivery_available is not None:
                query = query.filter(CommercialVehicleListing.delivery_available == filters.delivery_available)
        
        # Apply text search
        if search_request.query:
            search_term = f"%{search_request.query}%"
            query = query.filter(
                or_(
                    CommercialVehicleListing.title.ilike(search_term),
                    CommercialVehicleListing.description.ilike(search_term),
                    CommercialVehicleListing.make.ilike(search_term),
                    CommercialVehicleListing.model.ilike(search_term)
                )
            )
        
        # Get total count
        total = query.count()
        
        # Apply sorting
        if search_request.sort_by:
            sort_column = getattr(CommercialVehicleListing, search_request.sort_by, None)
            if sort_column:
                if search_request.sort_order == "desc":
                    query = query.order_by(desc(sort_column))
                else:
                    query = query.order_by(asc(sort_column))
        
        # Apply pagination
        offset = (search_request.page - 1) * search_request.per_page
        listings = query.offset(offset).limit(search_request.per_page).all()
        
        return listings, total

    async def get_user_listings(self, user_id: int, page: int = 1, per_page: int = 20) -> Tuple[List[CommercialVehicleListing], int]:
        """Get user's commercial vehicle listings."""
        query = self.db.query(CommercialVehicleListing).filter(
            CommercialVehicleListing.user_id == user_id
        )
        
        total = query.count()
        
        offset = (page - 1) * per_page
        listings = query.order_by(desc(CommercialVehicleListing.created_at)).offset(offset).limit(per_page).all()
        
        return listings, total

    async def create_image(self, image_data: Dict[str, Any]) -> CommercialVehicleImage:
        """Create a new commercial vehicle image."""
        image = CommercialVehicleImage(**image_data)
        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)
        return image

    async def delete_image(self, image_id: int) -> bool:
        """Delete a commercial vehicle image."""
        image = self.db.query(CommercialVehicleImage).filter(
            CommercialVehicleImage.id == image_id
        ).first()
        
        if image:
            self.db.delete(image)
            self.db.commit()
            return True
        return False

    async def create_feature(self, feature_data: Dict[str, Any]) -> CommercialVehicleFeature:
        """Create a new commercial vehicle feature."""
        feature = CommercialVehicleFeature(**feature_data)
        self.db.add(feature)
        self.db.commit()
        self.db.refresh(feature)
        return feature

    async def get_stats(self) -> Dict[str, Any]:
        """Get commercial vehicle marketplace statistics."""
        total_listings = self.db.query(CommercialVehicleListing).count()
        active_listings = self.db.query(CommercialVehicleListing).filter(
            CommercialVehicleListing.is_active == True
        ).count()
        sold_listings = self.db.query(CommercialVehicleListing).filter(
            CommercialVehicleListing.status == ListingStatus.SOLD
        ).count()
        
        # Average price
        avg_price_result = self.db.query(func.avg(CommercialVehicleListing.price)).filter(
            CommercialVehicleListing.is_active == True
        ).scalar()
        average_price = float(avg_price_result) if avg_price_result else 0.0
        
        # Listings by type
        type_stats = self.db.query(
            CommercialVehicleListing.vehicle_type,
            func.count(CommercialVehicleListing.id)
        ).filter(
            CommercialVehicleListing.is_active == True
        ).group_by(CommercialVehicleListing.vehicle_type).all()
        
        listings_by_type = {str(vehicle_type): count for vehicle_type, count in type_stats}
        
        # Listings by condition
        condition_stats = self.db.query(
            CommercialVehicleListing.condition,
            func.count(CommercialVehicleListing.id)
        ).filter(
            CommercialVehicleListing.is_active == True
        ).group_by(CommercialVehicleListing.condition).all()
        
        listings_by_condition = {str(condition): count for condition, count in condition_stats}
        
        # Listings by fuel type
        fuel_stats = self.db.query(
            CommercialVehicleListing.fuel_type,
            func.count(CommercialVehicleListing.id)
        ).filter(
            CommercialVehicleListing.is_active == True
        ).group_by(CommercialVehicleListing.fuel_type).all()
        
        listings_by_fuel_type = {str(fuel_type): count for fuel_type, count in fuel_stats}
        
        return {
            "total_listings": total_listings,
            "active_listings": active_listings,
            "sold_listings": sold_listings,
            "average_price": average_price,
            "listings_by_type": listings_by_type,
            "listings_by_condition": listings_by_condition,
            "listings_by_fuel_type": listings_by_fuel_type
        }

    async def get_makes(self, vehicle_type: Optional[str] = None) -> List[str]:
        """Get list of available commercial vehicle makes."""
        query = self.db.query(CommercialVehicleListing.make).filter(
            CommercialVehicleListing.is_active == True
        ).distinct()
        
        if vehicle_type:
            query = query.filter(CommercialVehicleListing.vehicle_type == vehicle_type)
        
        makes = [make[0] for make in query.all()]
        return sorted(makes)

    async def get_models(self, make: str, vehicle_type: Optional[str] = None) -> List[str]:
        """Get list of available commercial vehicle models for a specific make."""
        query = self.db.query(CommercialVehicleListing.model).filter(
            and_(
                CommercialVehicleListing.is_active == True,
                CommercialVehicleListing.make == make
            )
        ).distinct()
        
        if vehicle_type:
            query = query.filter(CommercialVehicleListing.vehicle_type == vehicle_type)
        
        models = [model[0] for model in query.all()]
        return sorted(models)

    async def get_featured_listings(self, limit: int = 10) -> List[CommercialVehicleListing]:
        """Get featured commercial vehicle listings."""
        return self.db.query(CommercialVehicleListing).filter(
            CommercialVehicleListing.is_active == True
        ).order_by(desc(CommercialVehicleListing.created_at)).limit(limit).all()