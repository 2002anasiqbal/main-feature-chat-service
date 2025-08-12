# property-service/src/routes.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from ..database.database import get_database
from ..services.property_services import (
    PropertyCategoryService, PropertyService, PropertyMessageService,
    PropertyComparisonService, PropertyLoanService, PropertyUtilityService
)
from ..models.property_schemas import (
    PropertyCategoryResponse, PropertyResponse, PropertySummaryResponse,
    PropertySearchParams, PropertyCreate, PropertyUpdate, PropertyMessageCreate,
    PropertyMessageResponse, PropertyComparisonCreate, PropertyLoanEstimateRequest,
    PropertyLoanEstimateResponse, PopularCityResponse, RentalTipResponse,
    FeedbackCreate, FeedbackResponse, PropertyPriceInsightResponse,
    PropertyTypeEnum, PaginatedResponse,  PropertyMapSearchRequest, PropertyComparisonSessionCreate, PropertyLoanEstimateRequest,
    RentalPropertyCreate, RentalApplicationCreate, LeaseContractCreate,
    SuccessResponse, ErrorResponse, AuthenticatedUser
)

from fastapi import APIRouter, Depends, HTTPException, Query, status, Header
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from uuid import UUID

from ..database.database import get_database
from ..services.property_services import (
    PropertyMapLocationService, PropertyComparisonService, 
    PropertyLoanEstimatorService, RentalPropertyService, LeaseContractService
)

from ..utils.auth import get_current_user, require_authentication

# Create router instance
router = APIRouter(prefix="/api/properties", tags=["Properties"])
# Create additional router for new endpoints
advanced_router = APIRouter(prefix="/api/properties", tags=["Properties Advanced"])

# Point 1: PropertyCategoryModule - Fetch property subcategories
@router.get("/categories", response_model=List[PropertyCategoryResponse])
async def get_property_categories(
    property_type: Optional[PropertyTypeEnum] = Query(None, description="Filter by property type"),
    db: Session = Depends(get_database)
):
    """
    Fetch property subcategories under Purchase, Rent, Sell, and Nutrition
    (e.g., Plots, New Homes, Vacation Homes)
    """
    if property_type:
        categories = PropertyCategoryService.get_categories_by_type(db, property_type)
    else:
        categories = PropertyCategoryService.get_all_categories(db)
    
    return categories

# Point 2: PropertySearchModule - Search listings for sale, rent, or vacation
@router.get("/search", response_model=PaginatedResponse)
async def search_properties(
    property_type: Optional[PropertyTypeEnum] = Query(None),
    property_category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    city: Optional[str] = Query(None),
    bedrooms: Optional[int] = Query(None),
    min_area: Optional[float] = Query(None),
    max_area: Optional[float] = Query(None),
    keyword: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    db: Session = Depends(get_database)
):
    """
    Search listings for sale, rent, or vacation based on filters like location, type, price, etc.
    """
    search_params = PropertySearchParams(
        property_type=property_type,
        property_category=property_category,
        min_price=min_price,
        max_price=max_price,
        city=city,
        bedrooms=bedrooms,
        min_area=min_area,
        max_area=max_area,
        keyword=keyword,
        page=page,
        size=size,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
    result = PropertyService.get_properties(db, search_params)
    return result

# Point 3: PropertyListingModule - Return "We think you might like these" suggestions
@router.get("/featured", response_model=List[PropertySummaryResponse])
async def get_featured_properties(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_database)
):
    """
    Return "We think you might like these" suggestions - featured properties
    """
    properties = PropertyService.get_featured_properties(db, limit)
    
    # Convert to summary response format for listing
    return [
        PropertySummaryResponse(
            id=prop.id,
            title=prop.title,
            price=prop.price,
            property_type=prop.property_type,
            property_category=prop.property_category,
            city=prop.city,
            bedrooms=prop.bedrooms,
            use_area=prop.use_area,
            primary_image=prop.images[0].image_url if prop.images else None,
            is_featured=prop.is_featured,
            created_at=prop.created_at
        )
        for prop in properties
    ]

@router.get("/recommended", response_model=List[PropertySummaryResponse])
async def get_recommended_properties(
    property_type: Optional[PropertyTypeEnum] = Query(None),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_database)
):
    """
    Get recommended properties based on popularity and recency
    """
    properties = PropertyService.get_recommended_properties(db, property_type, limit)
    
    return [
        PropertySummaryResponse(
            id=prop.id,
            title=prop.title,
            price=prop.price,
            property_type=prop.property_type,
            property_category=prop.property_category,
            city=prop.city,
            bedrooms=prop.bedrooms,
            use_area=prop.use_area,
            primary_image=prop.images[0].image_url if prop.images else None,
            is_featured=prop.is_featured,
            created_at=prop.created_at
        )
        for prop in properties
    ]

# Point 4: PropertyDetailModule - Full detail of a selected property
@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property_detail(
    property_id: UUID,
    user_id: Optional[str] = Query(None, description="User ID for tracking views"),
    db: Session = Depends(get_database)
):
    """
    Get full detail of a selected property including specs, images, seller info, description, and map location
    """
    property_obj = PropertyService.get_property_by_id(db, str(property_id), user_id)
    
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    return property_obj

# Point 5: PropertyContactModule - Contact property owner
@router.post("/{property_id}/contact", response_model=dict)
async def contact_property_owner(
    property_id: UUID,
    message_data: PropertyMessageCreate,
    db: Session = Depends(get_database)
):
    """
    Contact property owner (send message or interest)
    """
    # Verify property exists
    property_obj = PropertyService.get_property_by_id(db, str(property_id))
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    # Update message data with property_id
    message_data.property_id = property_id
    
    # Save message to database
    message = PropertyMessageService.send_message(db, message_data)
    
    # For now, return success message as email setup is not required
    return {
        "success": True,
        "message": "Your message has been received. Email functionality coming soon!",
        "message_id": str(message.id),
        "property_owner": property_obj.owner_name,
        "sent_at": message.created_at.isoformat()
    }

# Additional endpoints for supporting functionality

@router.post("/", response_model=PropertyResponse)
async def create_property(
    property_data: PropertyCreate,
    db: Session = Depends(get_database)
):
    """
    Create a new property listing
    """
    try:
        property_obj = PropertyService.create_property(db, property_data)
        return property_obj
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating property: {str(e)}"
        )

@router.put("/{property_id}", response_model=PropertyResponse)
async def update_property(
    property_id: UUID,
    property_data: PropertyUpdate,
    db: Session = Depends(get_database)
):
    """
    Update an existing property
    """
    property_obj = PropertyService.update_property(db, str(property_id), property_data)
    
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    return property_obj

@router.post("/compare", response_model=List[PropertyResponse])
async def compare_properties(
    comparison_data: PropertyComparisonCreate,
    db: Session = Depends(get_database)
):
    """
    Compare selected properties side by side
    """
    if len(comparison_data.property_ids) > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot compare more than 5 properties at once"
        )
    
    properties = PropertyComparisonService.create_comparison(db, comparison_data)
    
    if len(properties) != len(comparison_data.property_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or more properties not found"
        )
    
    return properties

@router.post("/loan-estimate", response_model=PropertyLoanEstimateResponse)
async def calculate_property_loan(
    loan_request: PropertyLoanEstimateRequest,
    db: Session = Depends(get_database)
):
    """
    Calculate estimated loan cost per month for a property
    """
    try:
        result = PropertyLoanService.calculate_loan_estimate(db, loan_request)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error calculating loan: {str(e)}"
        )

# Utility endpoints

@router.get("/utils/popular-cities", response_model=List[PopularCityResponse])
async def get_popular_cities(
    db: Session = Depends(get_database)
):
    """
    Get popular cities for property rentals
    """
    cities = PropertyUtilityService.get_popular_cities(db)
    return cities

@router.get("/utils/rental-tips", response_model=List[RentalTipResponse])
async def get_rental_tips(
    db: Session = Depends(get_database)
):
    """
    Get rental tips for tenants and landlords
    """
    tips = PropertyUtilityService.get_rental_tips(db)
    return tips

@router.post("/utils/feedback", response_model=dict)
async def submit_feedback(
    feedback_data: FeedbackCreate,
    user_id: Optional[str] = Query(None),
    db: Session = Depends(get_database)
):
    """
    Submit user feedback for the property section
    """
    feedback = PropertyUtilityService.submit_feedback(db, feedback_data, user_id)
    
    return {
        "success": True,
        "message": "Thank you for your feedback!",
        "feedback_id": str(feedback.id)
    }

@router.get("/utils/price-insights", response_model=List[PropertyPriceInsightResponse])
async def get_price_insights(
    city: Optional[str] = Query(None, description="Filter by city name"),
    db: Session = Depends(get_database)
):
    """
    Get property price insights by area/city
    """
    insights = PropertyUtilityService.get_price_insights(db, city)
    
    # Format the response
    formatted_insights = []
    for insight in insights:
        period_days = (insight.period_end - insight.period_start).days
        period_description = f"On average per advertisement in last {period_days} days"
        
        formatted_insights.append(PropertyPriceInsightResponse(
            city=insight.city,
            area=insight.area,
            avg_price_per_sqm=insight.avg_price_per_sqm,
            currency=insight.currency,
            period_description=period_description,
            sample_size=insight.sample_size,
            property_type=insight.property_type
        ))
    
    return formatted_insights

# Property location endpoint for map integration
@router.get("/{property_id}/location", response_model=dict)
async def get_property_location(
    property_id: UUID,
    db: Session = Depends(get_database)
):
    """
    Get property coordinates for map embedding
    """
    property_obj = PropertyService.get_property_by_id(db, str(property_id))
    
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    # Extract coordinates from PostGIS point if available
    latitude = None
    longitude = None
    
    if property_obj.location:
        # This would need proper PostGIS coordinate extraction
        # For now, we'll use a placeholder
        latitude = 59.9139  # Oslo latitude as example
        longitude = 10.7522  # Oslo longitude as example
    
    return {
        "property_id": str(property_obj.id),
        "address": property_obj.address,
        "city": property_obj.city,
        "latitude": latitude,
        "longitude": longitude,
        "location_name": f"{property_obj.city}, {property_obj.country}" if property_obj.city else property_obj.country
    }
    

# Point 6: PropertyMapLocationModule
@advanced_router.get("/{property_id}/location", response_model=Dict[str, Any])
async def get_property_location(
    property_id: UUID,
    db: Session = Depends(get_database)
):
    """
    Return coordinates for embedding on detail page
    """
    location_data = PropertyMapLocationService.get_property_location(db, str(property_id))
    
    if not location_data:
        # Fallback to property data if no specific location data
        from ..models.models import Property
        property_obj = db.query(Property).filter(Property.id == property_id).first()
        if not property_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found"
            )
        
        # Default Norway coordinates
        location_data = {
            "property_id": str(property_obj.id),
            "latitude": 59.9139,  # Oslo
            "longitude": 10.7522,
            "is_approximate": True,
            "address": property_obj.address,
            "city": property_obj.city,
            "location_name": f"{property_obj.city}, {property_obj.country}" if property_obj.city else property_obj.country
        }
    
    return location_data

@advanced_router.post("/map/search", response_model=List[Dict[str, Any]])
async def search_properties_by_map(
    search_request: PropertyMapSearchRequest,
    current_user: Optional[AuthenticatedUser] = Depends(get_current_user),
    db: Session = Depends(get_database)
):
    """
    Return properties constrained to geographic area via radius
    """
    try:
        user_id = str(current_user.user_id) if current_user else None
        properties = PropertyMapLocationService.search_properties_by_map(
            db, search_request, user_id
        )
        return properties
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Map search failed: {str(e)}"
        )

@advanced_router.get("/{property_id}/nearby", response_model=List[Dict[str, Any]])
async def get_nearby_places(
    property_id: UUID,
    db: Session = Depends(get_database)
):
    """
    Get nearby places for a property (schools, hospitals, etc.)
    """
    places = PropertyMapLocationService.get_nearby_places(db, str(property_id))
    return places

# Point 7: PropertyComparisonModule
@advanced_router.post("/compare", response_model=Dict[str, Any])
async def create_property_comparison(
    comparison_data: PropertyComparisonSessionCreate,
    current_user: Optional[AuthenticatedUser] = Depends(get_current_user),
    db: Session = Depends(get_database)
):
    """
    Compare selected properties side by side
    """
    try:
        user_id = str(current_user.user_id) if current_user else None
        result = PropertyComparisonService.create_comparison_session(
            db, comparison_data, user_id
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@advanced_router.get("/compare/{session_id}", response_model=Dict[str, Any])
async def get_property_comparison(
    session_id: UUID,
    db: Session = Depends(get_database)
):
    """
    Get comparison session with all properties
    """
    comparison = PropertyComparisonService.get_comparison_session(db, str(session_id))
    
    if not comparison:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comparison session not found"
        )
    
    return comparison

@advanced_router.post("/compare/{session_id}/notes", response_model=SuccessResponse)
async def add_comparison_note(
    session_id: UUID,
    property_id: UUID,
    note_text: str,
    note_category: Optional[str] = None,
    current_user: AuthenticatedUser = Depends(require_authentication),
    db: Session = Depends(get_database)
):
    """
    Add a note to a property in comparison
    """
    try:
        result = PropertyComparisonService.add_comparison_note(
            db, str(session_id), str(property_id), note_text, note_category
        )
        return SuccessResponse(
            success=True,
            message="Note added successfully",
            data=result
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to add note: {str(e)}"
        )

# Point 8: PropertyLoanEstimatorModule
@advanced_router.post("/loan-estimate", response_model=Dict[str, Any])
async def calculate_property_loan_estimate(
    loan_request: PropertyLoanEstimateRequest,
    current_user: Optional[AuthenticatedUser] = Depends(get_current_user),
    db: Session = Depends(get_database)
):
    """
    Show estimated loan cost per month for a property
    """
    try:
        user_id = str(current_user.user_id) if current_user else None
        result = PropertyLoanEstimatorService.calculate_loan_estimate(
            db, loan_request, user_id
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Loan calculation failed: {str(e)}"
        )

@advanced_router.get("/loan-providers", response_model=List[Dict[str, Any]])
async def get_loan_providers(
    db: Session = Depends(get_database)
):
    """
    Get available loan providers for property financing
    """
    providers = PropertyLoanEstimatorService.get_loan_providers(db)
    return providers

@advanced_router.get("/users/{user_id}/loan-estimates", response_model=List[Dict[str, Any]])
async def get_user_loan_estimates(
    user_id: UUID,
    current_user: AuthenticatedUser = Depends(require_authentication),
    db: Session = Depends(get_database)
):
    """
    Get user's saved loan estimates
    """
    # Ensure user can only access their own estimates
    if str(current_user.user_id) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    estimates = PropertyLoanEstimatorService.get_user_loan_estimates(db, str(user_id))
    return estimates

# Point 9: NewRentalAdModule
@advanced_router.post("/rentals", response_model=Dict[str, Any])
async def create_rental_advertisement(
    rental_data: RentalPropertyCreate,
    current_user: AuthenticatedUser = Depends(require_authentication),
    db: Session = Depends(get_database)
):
    """
    Allows landlords to post new rental ads
    """
    try:
        result = RentalPropertyService.create_rental_ad(
            db, rental_data, str(current_user.user_id)
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@advanced_router.get("/rentals", response_model=Dict[str, Any])
async def get_rental_properties(
    max_rent: Optional[float] = Query(None),
    min_bedrooms: Optional[int] = Query(None),
    city: Optional[str] = Query(None),
    pets_allowed: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_database)
):
    """
    Get available rental properties with filters
    """
    filters = {}
    if max_rent is not None:
        filters["max_rent"] = max_rent
    if min_bedrooms is not None:
        filters["min_bedrooms"] = min_bedrooms
    if city is not None:
        filters["city"] = city
    if pets_allowed is not None:
        filters["pets_allowed"] = pets_allowed
    
    result = RentalPropertyService.get_rental_properties(db, filters, page, size)
    return result

@advanced_router.post("/rentals/{rental_id}/applications", response_model=Dict[str, Any])
async def submit_rental_application(
    rental_id: UUID,
    application_data: RentalApplicationCreate,
    current_user: AuthenticatedUser = Depends(require_authentication),
    db: Session = Depends(get_database)
):
    """
    Submit an application for a rental property
    """
    from ..models.rental_models import RentalApplication
    
    # Check if user already applied for this rental
    existing_application = db.query(RentalApplication).filter(
        RentalApplication.rental_property_id == rental_id,
        RentalApplication.applicant_id == current_user.user_id
    ).first()
    
    if existing_application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already applied for this rental"
        )
    
    # Create application
    application = RentalApplication(
        **application_data.dict(),
        applicant_id=current_user.user_id
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    
    return {
        "application_id": str(application.id),
        "status": application.status,
        "message": "Rental application submitted successfully"
    }

# Point 10: LeaseContractModule
@advanced_router.get("/lease/templates", response_model=List[Dict[str, Any]])
async def get_lease_contract_templates(
    db: Session = Depends(get_database)
):
    """
    Returns available lease contract templates (downloadable)
    """
    templates = LeaseContractService.get_contract_templates(db)
    return templates

@advanced_router.post("/lease/contracts", response_model=Dict[str, Any])
async def create_lease_contract(
    contract_data: LeaseContractCreate,
    current_user: AuthenticatedUser = Depends(require_authentication),
    db: Session = Depends(get_database)
):
    """
    Create a new lease contract
    """
    try:
        result = LeaseContractService.create_lease_contract(
            db, contract_data, str(current_user.user_id)
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@advanced_router.post("/lease/contracts/{contract_id}/sign", response_model=Dict[str, Any])
async def sign_lease_contract(
    contract_id: UUID,
    user_type: str = Query(..., regex="^(landlord|tenant)$"),
    current_user: AuthenticatedUser = Depends(require_authentication),
    db: Session = Depends(get_database)
):
    """
    Sign a lease contract (landlord or tenant)
    """
    try:
        result = LeaseContractService.sign_contract(
            db, str(contract_id), str(current_user.user_id), user_type
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

@advanced_router.get("/lease/contracts/{contract_id}", response_model=Dict[str, Any])
async def get_lease_contract(
    contract_id: UUID,
    current_user: AuthenticatedUser = Depends(require_authentication),
    db: Session = Depends(get_database)
):
    """
    Get lease contract details
    """
    from ..models.rental_models import LeaseContract
    
    contract = db.query(LeaseContract).filter(
        LeaseContract.id == contract_id
    ).filter(
        or_(
            LeaseContract.landlord_id == current_user.user_id,
            LeaseContract.tenant_id == current_user.user_id
        )
    ).first()
    
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found or access denied"
        )
    
    return {
        "contract_id": str(contract.id),
        "contract_number": contract.contract_number,
        "lease_start_date": contract.lease_start_date.isoformat(),
        "lease_end_date": contract.lease_end_date.isoformat(),
        "monthly_rent": float(contract.monthly_rent),
        "security_deposit": float(contract.security_deposit),
        "status": contract.status,
        "landlord_signed": contract.landlord_signed,
        "tenant_signed": contract.tenant_signed,
        "lease_terms": contract.lease_terms,
        "special_conditions": contract.special_conditions
    }

# Rental suggestions endpoint
@advanced_router.get("/rentals/suggestions", response_model=List[Dict[str, Any]])
async def get_rental_suggestions(
    preferred_location: Optional[str] = Query(None),
    max_rent: Optional[float] = Query(None),
    min_bedrooms: Optional[int] = Query(None),
    max_bedrooms: Optional[int] = Query(None),
    property_type: Optional[str] = Query(None),
    current_user: Optional[AuthenticatedUser] = Depends(get_current_user),
    db: Session = Depends(get_database)
):
    """
    Suggest listings like "Hill", "Room", "Luxury House"
    """
    from ..models.models import Property
    from ..models.rental_models import RentalProperty
    
    query = db.query(Property, RentalProperty).join(
        RentalProperty, Property.id == RentalProperty.property_id
    ).filter(
        RentalProperty.is_available == True,
        Property.status == "active"
    )
    
    # Apply filters
    if preferred_location:
        query = query.filter(Property.city.ilike(f"%{preferred_location}%"))
    if max_rent:
        query = query.filter(RentalProperty.monthly_rent <= max_rent)
    if min_bedrooms:
        query = query.filter(Property.bedrooms >= min_bedrooms)
    if max_bedrooms:
        query = query.filter(Property.bedrooms <= max_bedrooms)
    
    # Get top suggestions based on views and features
    suggestions = query.order_by(
        desc(Property.views_count),
        desc(RentalProperty.is_featured)
    ).limit(5).all()
    
    return [
        {
            "property_id": str(prop.id),
            "rental_id": str(rental.id),
            "title": prop.title,
            "monthly_rent": float(rental.monthly_rent),
            "bedrooms": prop.bedrooms,
            "city": prop.city,
            "property_type": prop.property_type
        }
        for prop, rental in suggestions
    ]