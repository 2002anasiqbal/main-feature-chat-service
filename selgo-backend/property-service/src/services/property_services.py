<<<<<<< HEAD
# property-service/src/services.py
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc, asc
from geoalchemy2 import functions as geo_func
from typing import List, Optional, Dict, Any
from decimal import Decimal
from datetime import datetime, timedelta
import math


from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc, asc, text
from geoalchemy2 import functions as geo_func
from typing import List, Optional, Dict, Any, Tuple
from decimal import Decimal
from datetime import datetime, timedelta, date
import json
import uuid
import math

from ..models.map_models import PropertyMapLocation, PropertyMapSearch, PropertyNearbyPlace
from ..models.comparison_models import (
    PropertyComparisonSession, PropertyComparisonItem, PropertyComparisonNote
)
from ..models.loan_models import (
    PropertyLoanEstimate, LoanProvider, PropertyLoanApplication, LoanCalculatorPreset
)
from ..models.rental_models import (
    RentalProperty, RentalApplication, LeaseContract, LeaseContractTemplate, RentalSuggestion
)
from ..models.property_schemas import (
    PropertyMapSearchRequest, PropertyComparisonSessionCreate, PropertyLoanEstimateRequest,
    RentalPropertyCreate, RentalApplicationCreate, LeaseContractCreate
)


from ..models.models import (
    PropertyCategory, Property, PropertyImage, Facility, PropertyFacility,
    PropertyMessage, PropertyComparison, PropertyLoanRequest, PopularCity,
    RentalTip, Feedback, PropertyPriceInsight, PropertyView, PropertyFavorite
)
from ..models.property_schemas import (
    PropertyCategoryCreate, PropertyCreate, PropertyUpdate, PropertySearchParams,
    PropertyMessageCreate, PropertyComparisonCreate, PropertyLoanEstimateRequest,
    FeedbackCreate, PropertyTypeEnum, PropertyCategoryEnum
)

class PropertyCategoryService:
    @staticmethod
    def get_categories_by_type(db: Session, property_type: PropertyTypeEnum) -> List[PropertyCategory]:
        """Get all categories for a specific property type"""
        return db.query(PropertyCategory).filter(
            PropertyCategory.type == property_type,
            PropertyCategory.is_active == True
        ).order_by(PropertyCategory.sort_order).all()
    
    @staticmethod
    def get_all_categories(db: Session) -> List[PropertyCategory]:
        """Get all active categories"""
        return db.query(PropertyCategory).filter(
            PropertyCategory.is_active == True
        ).order_by(PropertyCategory.type, PropertyCategory.sort_order).all()
    
    @staticmethod
    def create_category(db: Session, category_data: PropertyCategoryCreate) -> PropertyCategory:
        """Create a new property category"""
        db_category = PropertyCategory(**category_data.dict())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

class PropertyService:
    @staticmethod
    def get_properties(
        db: Session, 
        search_params: PropertySearchParams,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get properties with filtering and pagination"""
        query = db.query(Property).filter(Property.status == "active")
        
        # Apply filters
        if search_params.property_type:
            query = query.filter(Property.property_type == search_params.property_type)
        
        if search_params.property_category:
            query = query.filter(Property.property_category == search_params.property_category)
        
        if search_params.min_price:
            query = query.filter(Property.price >= search_params.min_price)
        
        if search_params.max_price:
            query = query.filter(Property.price <= search_params.max_price)
        
        if search_params.city:
            query = query.filter(Property.city.ilike(f"%{search_params.city}%"))
        
        if search_params.bedrooms:
            query = query.filter(Property.bedrooms >= search_params.bedrooms)
        
        if search_params.min_area:
            query = query.filter(Property.use_area >= search_params.min_area)
        
        if search_params.max_area:
            query = query.filter(Property.use_area <= search_params.max_area)
        
        if search_params.keyword:
            query = query.filter(
                or_(
                    Property.title.ilike(f"%{search_params.keyword}%"),
                    Property.description.ilike(f"%{search_params.keyword}%"),
                    Property.city.ilike(f"%{search_params.keyword}%")
                )
            )
        
        # Get total count before pagination
        total = query.count()
        
        # Apply sorting
        if search_params.sort_by == "price":
            if search_params.sort_order == "desc":
                query = query.order_by(desc(Property.price))
            else:
                query = query.order_by(asc(Property.price))
        elif search_params.sort_by == "created_at":
            if search_params.sort_order == "desc":
                query = query.order_by(desc(Property.created_at))
            else:
                query = query.order_by(asc(Property.created_at))
        else:
            # Default: featured first, then by creation date
            query = query.order_by(desc(Property.is_featured), desc(Property.created_at))
        
        # Apply pagination
        offset = (search_params.page - 1) * search_params.size
        properties = query.offset(offset).limit(search_params.size).all()
        
        # Calculate pagination info
        pages = math.ceil(total / search_params.size)
        
        return {
            "items": properties,
            "total": total,
            "page": search_params.page,
            "size": search_params.size,
            "pages": pages
        }
    
    @staticmethod
    def get_property_by_id(db: Session, property_id: str, user_id: Optional[str] = None) -> Optional[Property]:
        """Get a single property by ID and increment view count"""
        property_obj = db.query(Property).filter(Property.id == property_id).first()
        
        if property_obj:
            # Increment view count
            property_obj.views_count += 1
            
            # Track view for analytics (if user_id provided)
            if user_id:
                PropertyService._track_property_view(db, property_id, user_id)
            
            db.commit()
            db.refresh(property_obj)
        
        return property_obj
    
    @staticmethod
    def _track_property_view(db: Session, property_id: str, user_id: str):
        """Track property view for analytics"""
        # Check if user already viewed this property recently (within 24 hours)
        recent_view = db.query(PropertyView).filter(
            PropertyView.property_id == property_id,
            PropertyView.user_id == user_id,
            PropertyView.viewed_at >= datetime.utcnow() - timedelta(hours=24)
        ).first()
        
        if not recent_view:
            view = PropertyView(
                property_id=property_id,
                user_id=user_id,
                viewed_at=datetime.utcnow()
            )
            db.add(view)
    
    @staticmethod
    def get_featured_properties(db: Session, limit: int = 10) -> List[Property]:
        """Get featured properties"""
        return db.query(Property).filter(
            Property.status == "active",
            Property.is_featured == True
        ).order_by(desc(Property.created_at)).limit(limit).all()
    
    @staticmethod
    def get_recommended_properties(
        db: Session, 
        property_type: Optional[PropertyTypeEnum] = None,
        limit: int = 10
    ) -> List[Property]:
        """Get recommended properties (we think you might like these)"""
        query = db.query(Property).filter(Property.status == "active")
        
        if property_type:
            query = query.filter(Property.property_type == property_type)
        
        # Order by popularity (views + favorites) and recency
        return query.order_by(
            desc(Property.views_count + Property.favorites_count),
            desc(Property.created_at)
        ).limit(limit).all()
    
    @staticmethod
    def create_property(db: Session, property_data: PropertyCreate) -> Property:
        """Create a new property"""
        # Convert location coordinates to PostGIS point if provided
        location_point = None
        if property_data.latitude and property_data.longitude:
            location_point = f"POINT({property_data.longitude} {property_data.latitude})"
        
        # Create property object
        property_dict = property_data.dict(exclude={"images", "facilities", "latitude", "longitude"})
        
        db_property = Property(**property_dict)
        
        if location_point:
            db_property.location = location_point
        
        db.add(db_property)
        db.flush()  # Flush to get the property ID
        
        # Add images
        for image_data in property_data.images:
            db_image = PropertyImage(
                property_id=db_property.id,
                **image_data.dict()
            )
            db.add(db_image)
        
        # Add facilities
        for facility_data in property_data.facilities:
            db_facility = PropertyFacility(
                property_id=db_property.id,
                **facility_data.dict()
            )
            db.add(db_facility)
        
        db.commit()
        db.refresh(db_property)
        return db_property
    
    @staticmethod
    def update_property(db: Session, property_id: str, property_data: PropertyUpdate) -> Optional[Property]:
        """Update an existing property"""
        db_property = db.query(Property).filter(Property.id == property_id).first()
        
        if not db_property:
            return None
        
        # Update fields
        update_data = property_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_property, field, value)
        
        db_property.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_property)
        return db_property

class PropertyMessageService:
    @staticmethod
    def send_message(db: Session, message_data: PropertyMessageCreate) -> PropertyMessage:
        """Send a message to property owner"""
        db_message = PropertyMessage(**message_data.dict())
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        
        # Here you would normally send an email notification
        # For now, we'll just return a success response
        return db_message
    
    @staticmethod
    def get_property_messages(db: Session, property_id: str) -> List[PropertyMessage]:
        """Get all messages for a property"""
        return db.query(PropertyMessage).filter(
            PropertyMessage.property_id == property_id
        ).order_by(desc(PropertyMessage.created_at)).all()

class PropertyComparisonService:
    @staticmethod
    def create_comparison(db: Session, comparison_data: PropertyComparisonCreate) -> List[Property]:
        """Create a property comparison"""
        properties = db.query(Property).filter(
            Property.id.in_(comparison_data.property_ids)
        ).all()
        
        # Track comparison for analytics
        for property_id in comparison_data.property_ids:
            db_comparison = PropertyComparison(
                property_id=property_id,
                user_id=comparison_data.user_id,
                session_id=comparison_data.session_id
            )
            db.add(db_comparison)
        
        db.commit()
        return properties

class PropertyLoanService:
    @staticmethod
    def calculate_loan_estimate(db: Session, request: PropertyLoanEstimateRequest) -> Dict[str, Any]:
        """Calculate loan estimate for a property"""
        # Get property to validate it exists
        property_obj = db.query(Property).filter(Property.id == request.property_id).first()
        if not property_obj:
            raise ValueError("Property not found")
        
        # Calculate loan details
        principal = float(request.loan_amount)
        annual_rate = float(request.interest_rate) / 100
        monthly_rate = annual_rate / 12
        num_payments = request.duration_months
        
        # Calculate monthly payment using the formula
        if monthly_rate > 0:
            monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / \
                            ((1 + monthly_rate)**num_payments - 1)
        else:
            monthly_payment = principal / num_payments
        
        total_payment = monthly_payment * num_payments
        total_interest = total_payment - principal
        
        # Save loan request if email provided
        if request.email:
            db_loan_request = PropertyLoanRequest(
                property_id=request.property_id,
                email=request.email,
                phone=request.phone,
                loan_amount=request.loan_amount,
                duration_months=request.duration_months,
                interest_rate=request.interest_rate,
                monthly_payment=Decimal(str(monthly_payment)),
                total_payment=Decimal(str(total_payment))
            )
            db.add(db_loan_request)
            db.commit()
        
        return {
            "property_id": request.property_id,
            "loan_amount": request.loan_amount,
            "duration_months": request.duration_months,
            "interest_rate": request.interest_rate,
            "monthly_payment": Decimal(str(monthly_payment)),
            "total_payment": Decimal(str(total_payment)),
            "total_interest": Decimal(str(total_interest))
        }

class PropertyUtilityService:
    @staticmethod
    def get_popular_cities(db: Session) -> List[PopularCity]:
        """Get popular cities for rentals"""
        return db.query(PopularCity).filter(
            PopularCity.is_featured == True
        ).order_by(desc(PopularCity.rental_count)).all()
    
    @staticmethod
    def get_rental_tips(db: Session) -> List[RentalTip]:
        """Get rental tips"""
        return db.query(RentalTip).filter(
            RentalTip.is_active == True
        ).order_by(RentalTip.sort_order, RentalTip.tip_number).all()
    
    @staticmethod
    def submit_feedback(db: Session, feedback_data: FeedbackCreate, user_id: Optional[str] = None) -> Feedback:
        """Submit user feedback"""
        db_feedback = Feedback(
            **feedback_data.dict(),
            user_id=user_id
        )
        db.add(db_feedback)
        db.commit()
        db.refresh(db_feedback)
        return db_feedback
    
    @staticmethod
    def get_price_insights(db: Session, city: Optional[str] = None) -> List[PropertyPriceInsight]:
        """Get property price insights"""
        query = db.query(PropertyPriceInsight)
        
        if city:
            query = query.filter(PropertyPriceInsight.city.ilike(f"%{city}%"))
        
        return query.order_by(desc(PropertyPriceInsight.created_at)).all()
    
    @staticmethod
    def get_facilities(db: Session) -> List[Facility]:
        """Get all available facilities"""
        return db.query(Facility).filter(Facility.is_active == True).all()
    

# Point 6: Property Map Location Module
class PropertyMapLocationService:
    @staticmethod
    def get_property_location(db: Session, property_id: str) -> Optional[Dict[str, Any]]:
        """Get property coordinates for map embedding"""
        location = db.query(PropertyMapLocation).filter(
            PropertyMapLocation.property_id == property_id
        ).first()
        
        if not location:
            return None
        
        return {
            "property_id": str(location.property_id),
            "latitude": location.latitude,
            "longitude": location.longitude,
            "is_approximate": location.is_approximate,
            "address_components": json.loads(location.address_components) if location.address_components else None
        }
    
    @staticmethod
    def search_properties_by_map(
        db: Session, 
        search_request: PropertyMapSearchRequest,
        user_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search properties within a geographic area using radius"""
        from ..models.models import Property
        
        # Create a point for the search center
        center_point = f"POINT({search_request.center_lng} {search_request.center_lat})"
        
        # Query properties within radius using PostGIS
        query = db.query(Property, PropertyMapLocation).join(
            PropertyMapLocation, Property.id == PropertyMapLocation.property_id
        ).filter(
            func.ST_DWithin(
                PropertyMapLocation.location_point,
                func.ST_GeomFromText(center_point, 4326),
                search_request.radius_km * 1000  # Convert km to meters
            ),
            Property.status == "active"
        )
        
        # Apply additional filters
        if search_request.filters:
            if "min_price" in search_request.filters:
                query = query.filter(Property.price >= search_request.filters["min_price"])
            if "max_price" in search_request.filters:
                query = query.filter(Property.price <= search_request.filters["max_price"])
            if "bedrooms" in search_request.filters:
                query = query.filter(Property.bedrooms >= search_request.filters["bedrooms"])
        
        results = query.all()
        
        # Track the search
        PropertyMapLocationService._track_map_search(db, search_request, len(results), user_id)
        
        # Format results
        formatted_results = []
        for property_obj, location in results:
            formatted_results.append({
                "property_id": str(property_obj.id),
                "title": property_obj.title,
                "price": float(property_obj.price),
                "bedrooms": property_obj.bedrooms,
                "latitude": location.latitude,
                "longitude": location.longitude,
                "city": property_obj.city,
                "property_type": property_obj.property_type,
                "distance_km": PropertyMapLocationService._calculate_distance(
                    search_request.center_lat, search_request.center_lng,
                    location.latitude, location.longitude
                )
            })
        
        return formatted_results
    
    @staticmethod
    def _track_map_search(db: Session, search_request: PropertyMapSearchRequest, results_count: int, user_id: Optional[str]):
        """Track map search for analytics"""
        search_record = PropertyMapSearch(
            user_id=user_id,
            session_id=search_request.session_id,
            center_lat=search_request.center_lat,
            center_lng=search_request.center_lng,
            radius_km=search_request.radius_km,
            search_filters=json.dumps(search_request.filters),
            results_count=results_count
        )
        db.add(search_record)
        db.commit()
    
    @staticmethod
    def _calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points using Haversine formula"""
        R = 6371  # Earth's radius in kilometers
        
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    @staticmethod
    def get_nearby_places(db: Session, property_id: str) -> List[Dict[str, Any]]:
        """Get nearby places for a property"""
        places = db.query(PropertyNearbyPlace).filter(
            PropertyNearbyPlace.property_id == property_id
        ).order_by(PropertyNearbyPlace.distance_km).all()
        
        return [
            {
                "place_name": place.place_name,
                "place_type": place.place_type,
                "distance_km": float(place.distance_km)
            }
            for place in places
        ]

# Point 7: Property Comparison Module
class PropertyComparisonService:
    @staticmethod
    def create_comparison_session(
        db: Session, 
        comparison_data: PropertyComparisonSessionCreate,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a property comparison session"""
        from ..models.models import Property
        
        # Validate that all properties exist
        properties = db.query(Property).filter(
            Property.id.in_(comparison_data.property_ids)
        ).all()
        
        if len(properties) != len(comparison_data.property_ids):
            raise ValueError("One or more properties not found")
        
        if len(comparison_data.property_ids) > 5:
            raise ValueError("Cannot compare more than 5 properties")
        
        # Create comparison session
        session = PropertyComparisonSession(
            user_id=user_id,
            session_id=comparison_data.session_id,
            comparison_name=comparison_data.comparison_name
        )
        db.add(session)
        db.flush()
        
        # Add comparison items
        for index, property_id in enumerate(comparison_data.property_ids):
            item = PropertyComparisonItem(
                session_id=session.id,
                property_id=property_id,
                sort_order=index
            )
            db.add(item)
        
        db.commit()
        db.refresh(session)
        
        return {
            "session_id": str(session.id),
            "properties": properties,
            "comparison_url": f"/property-comparison/{session.id}"
        }
    
    @staticmethod
    def get_comparison_session(db: Session, session_id: str) -> Optional[Dict[str, Any]]:
        """Get a comparison session with all properties"""
        from ..models.models import Property
        
        session = db.query(PropertyComparisonSession).filter(
            PropertyComparisonSession.id == session_id
        ).first()
        
        if not session:
            return None
        
        # Get all comparison items with properties
        items = db.query(PropertyComparisonItem, Property).join(
            Property, PropertyComparisonItem.property_id == Property.id
        ).filter(
            PropertyComparisonItem.session_id == session_id
        ).order_by(PropertyComparisonItem.sort_order).all()
        
        # Get comparison notes
        notes = db.query(PropertyComparisonNote).filter(
            PropertyComparisonNote.session_id == session_id
        ).all()
        
        properties = []
        for item, property_obj in items:
            property_data = {
                "id": str(property_obj.id),
                "title": property_obj.title,
                "price": float(property_obj.price),
                "bedrooms": property_obj.bedrooms,
                "bathrooms": property_obj.bathrooms,
                "use_area": property_obj.use_area,
                "city": property_obj.city,
                "property_type": property_obj.property_type,
                "is_favorite": item.is_favorite,
                "user_rating": item.user_rating,
                "notes": [
                    {
                        "note_text": note.note_text,
                        "note_category": note.note_category,
                        "created_at": note.created_at
                    }
                    for note in notes if note.property_id == property_obj.id
                ]
            }
            properties.append(property_data)
        
        return {
            "session_id": str(session.id),
            "comparison_name": session.comparison_name,
            "properties": properties,
            "created_at": session.created_at
        }
    
    @staticmethod
    def add_comparison_note(
        db: Session, 
        session_id: str, 
        property_id: str, 
        note_text: str, 
        note_category: Optional[str] = None
    ) -> Dict[str, Any]:
        """Add a note to a property in comparison"""
        note = PropertyComparisonNote(
            session_id=session_id,
            property_id=property_id,
            note_text=note_text,
            note_category=note_category
        )
        db.add(note)
        db.commit()
        db.refresh(note)
        
        return {
            "note_id": str(note.id),
            "message": "Note added successfully"
        }

# Point 8: Property Loan Estimator Module
class PropertyLoanEstimatorService:
    @staticmethod
    def calculate_loan_estimate(
        db: Session, 
        loan_request: PropertyLoanEstimateRequest,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Calculate detailed loan estimate for a property"""
        from ..models.models import Property
        
        # Validate property exists
        property_obj = db.query(Property).filter(Property.id == loan_request.property_id).first()
        if not property_obj:
            raise ValueError("Property not found")
        
        # Calculate loan details
        loan_amount = loan_request.property_price - loan_request.down_payment
        annual_rate = float(loan_request.interest_rate) / 100
        monthly_rate = annual_rate / 12
        num_payments = loan_request.loan_term_years * 12
        
        # Calculate monthly payment using loan formula
        if monthly_rate > 0:
            monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / \
                            ((1 + monthly_rate)**num_payments - 1)
        else:
            monthly_payment = loan_amount / num_payments
        
        total_payment = monthly_payment * num_payments
        total_interest = total_payment - loan_amount
        
        # Calculate total monthly cost including additional expenses
        total_monthly_cost = monthly_payment
        if loan_request.property_tax_monthly:
            total_monthly_cost += loan_request.property_tax_monthly
        if loan_request.insurance_monthly:
            total_monthly_cost += loan_request.insurance_monthly
        if loan_request.hoa_fees_monthly:
            total_monthly_cost += loan_request.hoa_fees_monthly
        
        # Save estimate to database
        estimate = PropertyLoanEstimate(
            property_id=loan_request.property_id,
            user_id=user_id,
            session_id=loan_request.session_id,
            property_price=loan_request.property_price,
            down_payment=loan_request.down_payment,
            loan_amount=Decimal(str(loan_amount)),
            interest_rate=loan_request.interest_rate,
            loan_term_years=loan_request.loan_term_years,
            loan_term_months=num_payments,
            monthly_payment=Decimal(str(monthly_payment)),
            total_payment=Decimal(str(total_payment)),
            total_interest=Decimal(str(total_interest)),
            property_tax_monthly=loan_request.property_tax_monthly,
            insurance_monthly=loan_request.insurance_monthly,
            hoa_fees_monthly=loan_request.hoa_fees_monthly,
            total_monthly_cost=Decimal(str(total_monthly_cost))
        )
        db.add(estimate)
        db.commit()
        db.refresh(estimate)
        
        return {
            "estimate_id": str(estimate.id),
            "property_id": str(loan_request.property_id),
            "loan_amount": float(loan_amount),
            "monthly_payment": float(monthly_payment),
            "total_payment": float(total_payment),
            "total_interest": float(total_interest),
            "total_monthly_cost": float(total_monthly_cost),
            "breakdown": {
                "principal_and_interest": float(monthly_payment),
                "property_tax": float(loan_request.property_tax_monthly or 0),
                "insurance": float(loan_request.insurance_monthly or 0),
                "hoa_fees": float(loan_request.hoa_fees_monthly or 0)
            }
        }
    
    @staticmethod
    def get_loan_providers(db: Session) -> List[Dict[str, Any]]:
        """Get available loan providers"""
        providers = db.query(LoanProvider).filter(
            LoanProvider.is_active == True
        ).order_by(LoanProvider.base_interest_rate).all()
        
        return [
            {
                "id": provider.id,
                "provider_name": provider.provider_name,
                "provider_type": provider.provider_type,
                "base_interest_rate": float(provider.base_interest_rate),
                "min_down_payment_percent": float(provider.min_down_payment_percent),
                "website_url": provider.website_url,
                "contact_phone": provider.contact_phone
            }
            for provider in providers
        ]
    
    @staticmethod
    def get_user_loan_estimates(db: Session, user_id: str) -> List[Dict[str, Any]]:
        """Get user's saved loan estimates"""
        estimates = db.query(PropertyLoanEstimate).filter(
            PropertyLoanEstimate.user_id == user_id
        ).order_by(desc(PropertyLoanEstimate.created_at)).all()
        
        return [
            {
                "estimate_id": str(estimate.id),
                "property_id": str(estimate.property_id),
                "loan_amount": float(estimate.loan_amount),
                "monthly_payment": float(estimate.monthly_payment),
                "total_monthly_cost": float(estimate.total_monthly_cost),
                "calculation_date": estimate.calculation_date
            }
            for estimate in estimates
        ]

# Point 9: New Rental Ad Module
class RentalPropertyService:
    @staticmethod
    def create_rental_ad(
        db: Session, 
        rental_data: RentalPropertyCreate,
        landlord_id: str
    ) -> Dict[str, Any]:
        """Create a new rental property advertisement"""
        from ..models.models import Property
        
        # Validate property exists and belongs to landlord
        property_obj = db.query(Property).filter(
            Property.id == rental_data.property_id,
            Property.owner_id == landlord_id
        ).first()
        
        if not property_obj:
            raise ValueError("Property not found or you don't have permission")
        
        # Check if rental already exists for this property
        existing_rental = db.query(RentalProperty).filter(
            RentalProperty.property_id == rental_data.property_id
        ).first()
        
        if existing_rental:
            raise ValueError("Rental advertisement already exists for this property")
        
        # Create rental property
        rental_property = RentalProperty(
            **rental_data.dict(),
            landlord_id=landlord_id
        )
        db.add(rental_property)
        db.commit()
        db.refresh(rental_property)
        
        return {
            "rental_id": str(rental_property.id),
            "property_id": str(rental_property.property_id),
            "monthly_rent": float(rental_property.monthly_rent),
            "available_from": rental_property.available_from.isoformat(),
            "message": "Rental advertisement created successfully"
        }
    
    @staticmethod
    def get_rental_properties(
        db: Session, 
        filters: Optional[Dict[str, Any]] = None,
        page: int = 1,
        size: int = 20
    ) -> Dict[str, Any]:
        """Get rental properties with filters"""
        from ..models.models import Property
        
        query = db.query(RentalProperty, Property).join(
            Property, RentalProperty.property_id == Property.id
        ).filter(
            RentalProperty.is_available == True,
            Property.status == "active"
        )
        
        # Apply filters
        if filters:
            if "max_rent" in filters:
                query = query.filter(RentalProperty.monthly_rent <= filters["max_rent"])
            if "min_bedrooms" in filters:
                query = query.filter(Property.bedrooms >= filters["min_bedrooms"])
            if "city" in filters:
                query = query.filter(Property.city.ilike(f"%{filters['city']}%"))
            if "pets_allowed" in filters:
                query = query.filter(RentalProperty.pets_allowed == filters["pets_allowed"])
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * size
        results = query.offset(offset).limit(size).all()
        
        properties = []
        for rental, property_obj in results:
            properties.append({
                "rental_id": str(rental.id),
                "property_id": str(property_obj.id),
                "title": property_obj.title,
                "monthly_rent": float(rental.monthly_rent),
                "security_deposit": float(rental.security_deposit),
                "bedrooms": property_obj.bedrooms,
                "city": property_obj.city,
                "available_from": rental.available_from.isoformat(),
                "pets_allowed": rental.pets_allowed,
                "parking_included": rental.parking_included,
                "lease_type": rental.lease_type
            })
        
        return {
            "properties": properties,
            "total": total,
            "page": page,
            "size": size,
            "pages": math.ceil(total / size)
        }

# Point 10: Lease Contract Module
class LeaseContractService:
    @staticmethod
    def create_lease_contract(
        db: Session,
        contract_data: LeaseContractCreate,
        landlord_id: str
    ) -> Dict[str, Any]:
        """Create a new lease contract"""
        # Validate rental property belongs to landlord
        rental_property = db.query(RentalProperty).filter(
            RentalProperty.id == contract_data.rental_property_id,
            RentalProperty.landlord_id == landlord_id
        ).first()
        
        if not rental_property:
            raise ValueError("Rental property not found or you don't have permission")
        
        # Generate unique contract number
        contract_number = f"LC-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        
        # Create lease contract
        contract = LeaseContract(
            **contract_data.dict(),
            landlord_id=landlord_id,
            contract_number=contract_number
        )
        db.add(contract)
        db.commit()
        db.refresh(contract)
        
        return {
            "contract_id": str(contract.id),
            "contract_number": contract.contract_number,
            "status": contract.status,
            "message": "Lease contract created successfully"
        }
    
    @staticmethod
    def get_contract_templates(db: Session) -> List[Dict[str, Any]]:
        """Get available lease contract templates"""
        templates = db.query(LeaseContractTemplate).filter(
            LeaseContractTemplate.is_active == True
        ).order_by(LeaseContractTemplate.is_default.desc()).all()
        
        return [
            {
                "template_id": template.id,
                "template_name": template.template_name,
                "template_type": template.template_type,
                "jurisdiction": template.jurisdiction,
                "is_default": template.is_default,
                "approved_by_legal": template.approved_by_legal
            }
            for template in templates
        ]
    
    @staticmethod
    def sign_contract(
        db: Session,
        contract_id: str,
        user_id: str,
        user_type: str  # "landlord" or "tenant"
    ) -> Dict[str, Any]:
        """Sign a lease contract"""
        contract = db.query(LeaseContract).filter(
            LeaseContract.id == contract_id
        ).first()
        
        if not contract:
            raise ValueError("Contract not found")
        
        # Validate user can sign this contract
        if user_type == "landlord" and contract.landlord_id != user_id:
            raise ValueError("You are not authorized to sign as landlord")
        elif user_type == "tenant" and contract.tenant_id != user_id:
            raise ValueError("You are not authorized to sign as tenant")
        
        # Update signature
        now = datetime.utcnow()
        if user_type == "landlord":
            contract.landlord_signed = True
            contract.landlord_signature_date = now
        else:
            contract.tenant_signed = True
            contract.tenant_signature_date = now
        
        # Update contract status if both parties signed
        if contract.landlord_signed and contract.tenant_signed:
            contract.status = "signed"
        
        db.commit()
        
        return {
            "contract_id": str(contract.id),
            "status": contract.status,
            "landlord_signed": contract.landlord_signed,
            "tenant_signed": contract.tenant_signed,
            "message": f"Contract signed successfully as {user_type}"
        }
=======
from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from ..repositories.repositories import PropertyCategoryRepository, PropertyRepository
from ..models.models import PropertyCategory, Property
from ..models.property_schemas import PropertyCategoryCreate, PropertyCreate, PropertyUpdate, PropertyFilterParams

class PropertyCategoryService:
    @staticmethod
    def create_category(db: Session, category_data: PropertyCategoryCreate) -> PropertyCategory:
        return PropertyCategoryRepository.create(db, category_data.dict())
    
    @staticmethod
    def get_category_by_id(db: Session, category_id: int) -> Optional[PropertyCategory]:
        return PropertyCategoryRepository.get_by_id(db, category_id)
    
    @staticmethod
    def get_all_categories(db: Session, skip: int = 0, limit: int = 100) -> List[PropertyCategory]:
        return PropertyCategoryRepository.get_all(db, skip, limit)
    
    @staticmethod
    def update_category(db: Session, category_id: int, category_data: PropertyCategoryCreate) -> Optional[PropertyCategory]:
        return PropertyCategoryRepository.update(db, category_id, category_data.dict())
    
    @staticmethod
    def delete_category(db: Session, category_id: int) -> bool:
        return PropertyCategoryRepository.delete(db, category_id)

class PropertyService:
    @staticmethod
    def create_property(db: Session, property_data: PropertyCreate, user_id: str) -> Property:
        property_dict = property_data.dict()
        property_dict['owner_id'] = user_id
        return PropertyRepository.create(db, property_dict)
    
    @staticmethod
    def get_property_by_id(db: Session, property_id: str, increment_view: bool = False) -> Optional[Property]:
        prop = PropertyRepository.get_by_id(db, property_id)
        if prop and increment_view:
            return PropertyRepository.increment_view_count(db, property_id)
        return prop
    
    @staticmethod
    def get_all_properties(db: Session, skip: int = 0, limit: int = 100) -> List[Property]:
        return PropertyRepository.get_all(db, skip, limit)
    
    @staticmethod
    def filter_properties(db: Session, filters: PropertyFilterParams) -> Tuple[List[Property], int]:
        return PropertyRepository.filter_properties(db, filters)

    @staticmethod
    def update_property(db: Session, property_id: str, property_data: PropertyUpdate, user_id: str) -> Optional[Property]:
        prop = PropertyRepository.get_by_id(db, property_id)
        if not prop or str(prop.owner_id) != user_id:
            return None
        
        property_dict = property_data.dict(exclude_unset=True)
        return PropertyRepository.update(db, property_id, property_dict)
    
    @staticmethod
    def delete_property(db: Session, property_id: str, user_id: str) -> bool:
        prop = PropertyRepository.get_by_id(db, property_id)
        if not prop or str(prop.owner_id) != user_id:
            return False
        
        return PropertyRepository.delete(db, property_id)
>>>>>>> ef864b3 (Replace Features branch with selgo-feature contents)
