from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
from datetime import datetime
import logging
logger = logging.getLogger(__name__)  # Add this line
from ..services.services import (
    BoatCategoryService, 
    BoatFeatureService, 
    BoatService, 
    BoatImageService, 
    BoatRatingService, 
    BoatFixDoneRequestService,
    LoanEstimateService
)
from ..models.boat_schemas import (
    BoatCategoryCreate,
    BoatCategoryResponse,
    BoatCategoryWithCountResponse,
    BoatCategoryNestedResponse,
    BoatFeatureCreate,
    BoatFeatureResponse,
    BoatCreate,
    BoatUpdate,
    BoatResponse,
    BoatDetailResponse,
    BoatListResponse,
    BoatFilterParams,
    BoatImageCreate,
    BoatImageResponse,
    BoatRatingCreate,
    BoatRatingResponse,
    BoatFixDoneRequestCreate,
    BoatFixDoneRequestResponse,
    BoatFixDoneRequestStatusUpdate,
    LoanEstimateRequest,
    LoanEstimateResponse,
    PaginatedResponse,
    GeoPoint
)
from ..database.database import get_db
from ..config.config import settings
# from ..utils.auth import get_current_user_id
from ..utils.auth import get_current_user_id, get_current_admin_user_id
# Create router
router = APIRouter(
    prefix="/api/v1/boats",
    tags=["boats"],
    responses={404: {"description": "Not found"}}
)

# ==================== Boat Category Routes ====================

@router.post("/categories", response_model=BoatCategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_boat_category(
    category: BoatCategoryCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_admin_user_id)
):
    """
    Create a new boat category.
    This endpoint is typically restricted to admin users.
    """
    return BoatCategoryService.create_category(db, category)

@router.get("/categories", response_model=List[BoatCategoryResponse])
async def get_all_boat_categories(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all boat categories.
    """
    return BoatCategoryService.get_all_categories(db, skip, limit)

@router.get("/categories/with-counts", response_model=List[BoatCategoryWithCountResponse])
async def get_categories_with_counts(db: Session = Depends(get_db)):
    """
    Get all boat categories with counts of boats in each category.
    """
    categories_with_counts = BoatCategoryService.get_categories_with_counts(db)
    result = []
    
    for category, count in categories_with_counts:
        category_data = BoatCategoryResponse.from_orm(category).dict()
        category_data['count'] = count
        result.append(BoatCategoryWithCountResponse(**category_data))
    
    return result

@router.get("/categories/top-level", response_model=List[BoatCategoryResponse])
async def get_top_level_categories(db: Session = Depends(get_db)):
    """
    Get all top-level boat categories (with no parent).
    """
    return BoatCategoryService.get_top_level_categories(db)

@router.get("/categories/{category_id}", response_model=BoatCategoryResponse)
async def get_boat_category(
    category_id: int = Path(..., description="The ID of the category to get"),
    db: Session = Depends(get_db)
):
    """
    Get a specific boat category by ID.
    """
    category = BoatCategoryService.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/categories/{category_id}/subcategories", response_model=List[BoatCategoryResponse])
async def get_subcategories(
    category_id: int = Path(..., description="The ID of the parent category"),
    db: Session = Depends(get_db)
):
    """
    Get all subcategories of a specific boat category.
    """
    return BoatCategoryService.get_subcategories(db, category_id)

@router.put("/categories/{category_id}", response_model=BoatCategoryResponse)
async def update_boat_category(
    category: BoatCategoryCreate,
    category_id: int = Path(..., description="The ID of the category to update"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_admin_user_id)
):
    """
    Update a boat category.
    This endpoint is typically restricted to admin users.
    """
    updated_category = BoatCategoryService.update_category(db, category_id, category)
    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category

@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_boat_category(
    category_id: int = Path(..., description="The ID of the category to delete"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_admin_user_id)
):
    """
    Delete a boat category.
    This endpoint is typically restricted to admin users.
    """
    success = BoatCategoryService.delete_category(db, category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"detail": "Category deleted successfully"}


# ==================== Boat Feature Routes ====================

@router.post("/features", response_model=BoatFeatureResponse, status_code=status.HTTP_201_CREATED)
async def create_boat_feature(
    feature: BoatFeatureCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_admin_user_id)
):
    """
    Create a new boat feature.
    This endpoint is typically restricted to admin users.
    """
    return BoatFeatureService.create_feature(db, feature)

@router.get("/features", response_model=List[BoatFeatureResponse])
async def get_all_boat_features(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all boat features.
    """
    return BoatFeatureService.get_all_features(db, skip, limit)

@router.get("/features/{feature_id}", response_model=BoatFeatureResponse)
async def get_boat_feature(
    feature_id: int = Path(..., description="The ID of the feature to get"),
    db: Session = Depends(get_db)
):
    """
    Get a specific boat feature by ID.
    """
    feature = BoatFeatureService.get_feature_by_id(db, feature_id)
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")
    return feature

@router.put("/features/{feature_id}", response_model=BoatFeatureResponse)
async def update_boat_feature(
    feature: BoatFeatureCreate,
    feature_id: int = Path(..., description="The ID of the feature to update"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_admin_user_id)
):
    """
    Update a boat feature.
    This endpoint is typically restricted to admin users.
    """
    updated_feature = BoatFeatureService.update_feature(db, feature_id, feature)
    if not updated_feature:
        raise HTTPException(status_code=404, detail="Feature not found")
    return updated_feature

@router.delete("/features/{feature_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_boat_feature(
    feature_id: int = Path(..., description="The ID of the feature to delete"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_admin_user_id)
):
    """
    Delete a boat feature.
    This endpoint is typically restricted to admin users.
    """
    success = BoatFeatureService.delete_feature(db, feature_id)
    if not success:
        raise HTTPException(status_code=404, detail="Feature not found")
    return {"detail": "Feature deleted successfully"}

# ==================== Boat Routes ====================

@router.post("", response_model=BoatResponse, status_code=status.HTTP_201_CREATED)
async def create_boat(
    boat: BoatCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Create a new boat listing.
    """
    return BoatService.create_boat(db, boat, current_user_id)

@router.get("", response_model=PaginatedResponse)
async def get_all_boats(
    skip: int = 0, 
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get all boat listings with pagination.
    """
    boats = BoatService.get_all_boats(db, skip, limit)
    total = len(boats)
    
    boat_list_responses = [BoatListResponse(
        id=boat.id,
        title=boat.title,
        price=boat.price,
        location_name=boat.location_name,
        year=boat.year,
        make=boat.make,
        model=boat.model,
        length=boat.length,
        created_at=boat.created_at,
        primary_image=next((img.image_url for img in boat.images if img.is_primary), 
                          next((img.image_url for img in boat.images), None) if boat.images else None)
    ) for boat in boats]
    
    return PaginatedResponse(
        items=boat_list_responses,
        total=total,
        limit=limit,
        offset=skip
    )


@router.post("/filter", response_model=PaginatedResponse)
async def filter_boats(
    filters: BoatFilterParams,
    db: Session = Depends(get_db)
):
    """
    Filter boat listings based on various criteria.
    """
    boats, total = BoatService.filter_boats(db, filters)
    
    boat_list_responses = [BoatListResponse(
        id=boat.id,
        title=boat.title,
        price=boat.price,
        location_name=boat.location_name,
        year=boat.year,
        make=boat.make,
        model=boat.model,
        length=boat.length,
        created_at=boat.created_at,
        primary_image=next((img.image_url for img in boat.images if img.is_primary), 
                          next((img.image_url for img in boat.images), None) if boat.images else None)
    ) for boat in boats]
    
    return PaginatedResponse(
        items=boat_list_responses,
        total=total,
        limit=filters.limit,
        offset=filters.offset
    )

@router.get("/recommended", response_model=List[BoatListResponse])
async def get_recommended_boats(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get recommended boat listings.
    """
    boats = BoatService.get_recommended_boats(db, limit)
    
    return [BoatListResponse(
        id=boat.id,
        title=boat.title,
        price=boat.price,
        location_name=boat.location_name,
        year=boat.year,
        make=boat.make,
        model=boat.model,
        length=boat.length,
        created_at=boat.created_at,
        primary_image=next((img.image_url for img in boat.images if img.is_primary), 
                          next((img.image_url for img in boat.images), None) if boat.images else None)
    ) for boat in boats]


@router.get("/featured", response_model=List[BoatListResponse])
async def get_featured_boats(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get featured boat listings for homepage slider.
    """
    boats = BoatService.get_featured_boats(db, limit)
    
    return [BoatListResponse(
        id=boat.id,
        title=boat.title,
        price=boat.price,
        location_name=boat.location_name,
        year=boat.year,
        make=boat.make,
        model=boat.model,
        length=boat.length,
        created_at=boat.created_at,
        primary_image=next((img.image_url for img in boat.images if img.is_primary), 
                          next((img.image_url for img in boat.images), None) if boat.images else None)
    ) for boat in boats]

@router.get("/homepage", response_model=List[BoatListResponse])
async def get_homepage_boats(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get boats for homepage 'Find the boats that suits you' section.
    """
    boats = BoatService.get_homepage_boats(db, limit)
    
    return [BoatListResponse(
        id=boat.id,
        title=boat.title,
        price=boat.price,
        location_name=boat.location_name,
        year=boat.year,
        make=boat.make,
        model=boat.model,
        length=boat.length,
        created_at=boat.created_at,
        primary_image=next((img.image_url for img in boat.images if img.is_primary), 
                          next((img.image_url for img in boat.images), None) if boat.images else None)
    ) for boat in boats]


@router.get("/{boat_id}", response_model=BoatDetailResponse)
async def get_boat(
    boat_id: int = Path(..., description="The ID of the boat to get"),
    increment_view: bool = Query(False, description="Whether to increment the view count"),
    db: Session = Depends(get_db)
):
    """
    Get a specific boat listing by ID.
    """
    boat = BoatService.get_boat_by_id(db, boat_id, increment_view)
    if not boat:
        raise HTTPException(status_code=404, detail="Boat not found")
    
    avg_rating = BoatRatingService.get_avg_rating(db, boat_id)
    
    response_dict = {
        "id": boat.id,
        "title": boat.title,
        "description": boat.description,
        "price": boat.price,
        "category_id": boat.category_id,
        "condition": boat.condition,
        "year": boat.year,
        "make": boat.make,
        "model": boat.model,
        "length": boat.length,
        "beam": boat.beam,
        "draft": boat.draft,
        "fuel_type": boat.fuel_type,
        "hull_material": boat.hull_material,
        "engine_make": boat.engine_make,
        "engine_model": boat.engine_model,
        "engine_hours": boat.engine_hours,
        "engine_power": boat.engine_power,
        "seller_type": boat.seller_type,
        "ad_type": boat.ad_type,
        "is_featured": boat.is_featured,
        "location_name": boat.location_name,
        "status": boat.status,
        "user_id": boat.user_id,
        "view_count": boat.view_count,
        "created_at": boat.created_at,
        "updated_at": boat.updated_at,
        "category": boat.category,
        "images": boat.images,
        "features": boat.features,
        "fix_requests": boat.fix_requests,
        "ratings": boat.ratings,
        "avg_rating": avg_rating
    }
    
    if boat.location:
        try:
            from geoalchemy2.shape import to_shape
            point = to_shape(boat.location)
            response_dict["location"] = {"latitude": point.y, "longitude": point.x}
        except:
            response_dict["location"] = None
    else:
        response_dict["location"] = None
    
    return BoatDetailResponse(**response_dict)

@router.put("/{boat_id}", response_model=BoatResponse)
async def update_boat(
    boat: BoatUpdate,
    boat_id: int = Path(..., description="The ID of the boat to update"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Update a specific boat listing.
    """
    updated_boat = BoatService.update_boat(db, boat_id, boat, current_user_id)
    if not updated_boat:
        raise HTTPException(status_code=404, detail="Boat not found or you don't have permission to update it")
    return updated_boat

@router.delete("/{boat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_boat(
    boat_id: int = Path(..., description="The ID of the boat to delete"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Delete a specific boat listing.
    """
    success = BoatService.delete_boat(db, boat_id, current_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Boat not found or you don't have permission to delete it")
    return {"detail": "Boat deleted successfully"}

# ==================== Boat Image Routes ====================

@router.post("/{boat_id}/images", response_model=BoatImageResponse, status_code=status.HTTP_201_CREATED)
async def add_boat_image(
    image_data: BoatImageCreate,
    boat_id: int = Path(..., description="The ID of the boat to add an image to"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Add an image to a boat listing.
    """
    image = BoatImageService.add_image(db, boat_id, image_data, current_user_id)
    if not image:
        raise HTTPException(status_code=404, detail="Boat not found or you don't have permission to add images")
    return image

@router.get("/{boat_id}/images", response_model=List[BoatImageResponse])
async def get_boat_images(
    boat_id: int = Path(..., description="The ID of the boat to get images for"),
    db: Session = Depends(get_db)
):
    """
    Get all images for a specific boat listing.
    """
    return BoatImageService.get_images(db, boat_id)

@router.delete("/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_boat_image(
    image_id: int = Path(..., description="The ID of the image to delete"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Delete a specific boat image.
    """
    success = BoatImageService.delete_image(db, image_id, current_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Image not found or you don't have permission to delete it")
    return {"detail": "Image deleted successfully"}

# ==================== File Upload Route for Boat Images ====================

@router.post("/upload-image", response_model=dict)
async def upload_image(
    file: UploadFile = File(...),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Upload an image file for a boat.
    Returns a URL to the uploaded image.
    """
    allowed_types = ["image/jpeg", "image/png", "image/gif"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG, and GIF files are allowed")
    
    os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
    
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_FOLDER, unique_filename)
    
    try:
        with open(file_path, "wb") as buffer:
            contents = await file.read()
            buffer.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    file_url = f"/uploads/{unique_filename}"
    
    return {"url": file_url, "filename": unique_filename}

# ==================== Boat Rating Routes ====================

@router.post("/{boat_id}/ratings", response_model=BoatRatingResponse, status_code=status.HTTP_201_CREATED)
async def create_boat_rating(
    rating: BoatRatingCreate,
    boat_id: int = Path(..., description="The ID of the boat to rate"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Rate a boat listing.
    """
    if rating.boat_id != boat_id:
        raise HTTPException(status_code=400, detail="Boat ID in path and body do not match")
    
    boat_rating = BoatRatingService.create_rating(db, rating, current_user_id)
    if not boat_rating:
        raise HTTPException(status_code=404, detail="Boat not found")
    return boat_rating


@router.get("/{boat_id}/ratings", response_model=List[BoatRatingResponse])
async def get_boat_ratings(
    boat_id: int = Path(..., description="The ID of the boat to get ratings for"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all ratings for a specific boat listing.
    """
    return BoatRatingService.get_ratings_by_boat_id(db, boat_id, skip, limit)

@router.delete("/ratings/{rating_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_boat_rating(
    rating_id: int = Path(..., description="The ID of the rating to delete"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Delete a specific boat rating.
    """
    success = BoatRatingService.delete_rating(db, rating_id, current_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rating not found or you don't have permission to delete it")
    return {"detail": "Rating deleted successfully"}

# ==================== Fix Done Request Routes ====================

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
from datetime import datetime
import logging  # Add this import

# Configure logging
logger = logging.getLogger(__name__)  # Add this line

from ..services.services import (
    BoatCategoryService, 
    BoatFeatureService, 
    BoatService, 
    BoatImageService, 
    BoatRatingService, 
    BoatFixDoneRequestService,
    LoanEstimateService
)
# ... rest of your imports ...

# Then modify your create_fix_done_request endpoint
@router.post("/{boat_id}/fix-requests", response_model=BoatFixDoneRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_fix_done_request(
    request: BoatFixDoneRequestCreate,
    boat_id: int = Path(..., description="The ID of the boat to create a fix request for"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Create a new "Fix Done" request for a boat listing.
    """
    logger.info(f"Processing fix request for boat ID: {boat_id}, user ID: {current_user_id}")
    
    # Check if the boat exists
    boat = BoatService.get_boat_by_id(db, boat_id)
    if not boat:
        logger.error(f"Boat with ID {boat_id} not found")
        raise HTTPException(status_code=404, detail="Boat not found")
    
    logger.info(f"Boat found: {boat.id}, owner: {boat.user_id}")
    
    # Check if user is trying to create a fix request for their own boat
    if boat.user_id == current_user_id:
        logger.warning(f"User {current_user_id} attempted to create fix request for their own boat {boat_id}")
        raise HTTPException(status_code=400, detail="You cannot create a fix request for your own boat")
    
    if request.boat_id != boat_id:
        logger.warning(f"Boat ID mismatch: request.boat_id={request.boat_id}, path boat_id={boat_id}")
        raise HTTPException(status_code=400, detail="Boat ID in path and body do not match")
    
    logger.info(f"Creating fix request: boat_id={boat_id}, buyer_id={current_user_id}, seller_id={boat.user_id}")
    
    try:
        fix_request = BoatFixDoneRequestService.create_request(db, request, current_user_id)
        if not fix_request:
            logger.error(f"Failed to create fix request for boat {boat_id}")
            raise HTTPException(status_code=500, detail="Failed to create fix request")
        
        logger.info(f"Fix request created successfully: {fix_request.id}")
        return fix_request
    except Exception as e:
        logger.error(f"Exception creating fix request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating fix request: {str(e)}")

@router.get("/{boat_id}/fix-requests", response_model=List[BoatFixDoneRequestResponse])
async def get_fix_done_requests_by_boat(
    boat_id: int = Path(..., description="The ID of the boat to get fix requests for"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Get all "Fix Done" requests for a specific boat listing.
    """
    boat = BoatService.get_boat_by_id(db, boat_id)
    if not boat or boat.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="You don't have permission to view these requests")
    
    return BoatFixDoneRequestService.get_requests_by_boat_id(db, boat_id)

@router.get("/fix-requests/buyer", response_model=List[BoatFixDoneRequestResponse])
async def get_fix_done_requests_as_buyer(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Get all "Fix Done" requests where the current user is the buyer.
    """
    return BoatFixDoneRequestService.get_requests_by_buyer_id(db, current_user_id)

@router.get("/fix-requests/seller", response_model=List[BoatFixDoneRequestResponse])
async def get_fix_done_requests_as_seller(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Get all "Fix Done" requests where the current user is the seller.
    """
    return BoatFixDoneRequestService.get_requests_by_seller_id(db, current_user_id)

@router.put("/fix-requests/{request_id}/status", response_model=BoatFixDoneRequestResponse)
async def update_fix_done_request_status(
    status_update: BoatFixDoneRequestStatusUpdate,
    request_id: int = Path(..., description="The ID of the fix request to update"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Update the status of a "Fix Done" request.
    """
    updated_request = BoatFixDoneRequestService.update_request_status(db, request_id, status_update, current_user_id)
    if not updated_request:
        raise HTTPException(
            status_code=404, 
            detail="Request not found or you don't have permission to update its status"
        )
    return updated_request

# ==================== Loan Estimate Route ====================

@router.post("/loan-estimate", response_model=LoanEstimateResponse)
async def calculate_loan_estimate(loan_data: LoanEstimateRequest):
    """
    Calculate loan payments for a boat.
    """
    return LoanEstimateService.calculate_loan(loan_data)
