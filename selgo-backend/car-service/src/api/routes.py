from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
from ..services.services import (
    CarCategoryService,
    CarFeatureService,
    CarService,
    CarImageService,
    CarRatingService,
    LoanEstimateService,
    UserFavoriteService
)
from .car_auction_routes import router as auction_router
from ..models.car_schemas import (
    UserFavoriteCreate,
    UserFavoriteResponse,
    FavoriteToggleResponse,
    CarCategoryCreate,
    CarCategoryResponse,
    CarFeatureCreate,
    CarFeatureResponse,
    CarCreate,
    CarUpdate,
    CarResponse,
    CarDetailResponse,
    CarListResponse,
    CarFilterParams,
    CarImageCreate,
    CarImageResponse,
    CarRatingCreate,
    CarRatingResponse,
    LoanEstimateRequest,
    LoanEstimateResponse,
    PaginatedResponse
)
from ..database.database import get_db
from ..config.config import settings
from ..utils.auth import get_current_user_id, get_current_admin_user_id

router = APIRouter(
    prefix="/api/v1/cars",
    tags=["cars"],
    responses={404: {"description": "Not found"}}
)

# Include auction routes
router.include_router(auction_router, prefix="", tags=["Car Auctions"])

# ==================== Car Category Routes ====================

@router.post("/categories", response_model=CarCategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_car_category(
    category: CarCategoryCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_admin_user_id)
):
    return CarCategoryService.create_category(db, category)

@router.get("/categories", response_model=List[CarCategoryResponse])
async def get_all_car_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return CarCategoryService.get_all_categories(db, skip, limit)

@router.get("/categories/{category_id}", response_model=CarCategoryResponse)
async def get_car_category(
    category_id: int = Path(..., description="The ID of the category to get"),
    db: Session = Depends(get_db)
):
    category = CarCategoryService.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# ==================== Car Feature Routes ====================

@router.post("/features", response_model=CarFeatureResponse, status_code=status.HTTP_201_CREATED)
async def create_car_feature(
    feature: CarFeatureCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_admin_user_id)
):
    return CarFeatureService.create_feature(db, feature)

@router.get("/features", response_model=List[CarFeatureResponse])
async def get_all_car_features(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return CarFeatureService.get_all_features(db, skip, limit)

# ==================== Car Routes ====================

@router.post("", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
async def create_car(
    car: CarCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    return CarService.create_car(db, car, current_user_id)

@router.get("", response_model=PaginatedResponse)
async def get_all_cars(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    cars, total = CarService.get_all_cars(db, skip, limit)

    car_list_responses = [CarListResponse.from_orm(car) for car in cars]

    return PaginatedResponse(
        items=car_list_responses,
        total=total,
        limit=limit,
        offset=skip
    )

@router.post("/filter", response_model=PaginatedResponse)
async def filter_cars(
    filters: CarFilterParams,
    db: Session = Depends(get_db)
):
    cars, total = CarService.filter_cars(db, filters)

    car_list_responses = [CarListResponse.from_orm(car) for car in cars]

    return PaginatedResponse(
        items=car_list_responses,
        total=total,
        limit=filters.limit,
        offset=filters.offset
    )

@router.get("/recommended", response_model=List[CarListResponse])
async def get_recommended_cars(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    cars = CarService.get_recommended_cars(db, limit)
    return [CarListResponse.from_orm(car) for car in cars]

@router.get("/featured", response_model=List[CarListResponse])
async def get_featured_cars(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    cars = CarService.get_featured_cars(db, limit)
    return [CarListResponse.from_orm(car) for car in cars]

@router.get("/homepage", response_model=List[CarListResponse])
async def get_homepage_cars(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    cars = CarService.get_homepage_cars(db, limit)
    return [CarListResponse.from_orm(car) for car in cars]

@router.put("/{car_id}", response_model=CarResponse)
async def update_car(
    car: CarUpdate,
    car_id: int = Path(..., description="The ID of the car to update"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    updated_car = CarService.update_car(db, car_id, car, current_user_id)
    if not updated_car:
        raise HTTPException(status_code=404, detail="Car not found or you don't have permission to update it")
    return updated_car

@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(
    car_id: int = Path(..., description="The ID of the car to delete"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    success = CarService.delete_car(db, car_id, current_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Car not found or you don't have permission to delete it")
    return {"detail": "Car deleted successfully"}

@router.post("/{car_id}/images", response_model=CarImageResponse, status_code=status.HTTP_201_CREATED)
async def add_car_image(
    image_data: CarImageCreate,
    car_id: int = Path(..., description="The ID of the car to add an image to"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    image = CarImageService.add_image(db, car_id, image_data, current_user_id)
    if not image:
        raise HTTPException(status_code=404, detail="Car not found or you don't have permission to add images")
    return image

@router.post("/upload-image", response_model=dict)
async def upload_image(
    file: UploadFile = File(...),
    current_user_id: int = Depends(get_current_user_id)
):
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

@router.post("/{car_id}/ratings", response_model=CarRatingResponse, status_code=status.HTTP_201_CREATED)
async def create_car_rating(
    rating: CarRatingCreate,
    car_id: int = Path(..., description="The ID of the car to rate"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    if rating.car_id != car_id:
        raise HTTPException(status_code=400, detail="Car ID in path and body do not match")

    car_rating = CarRatingService.create_rating(db, rating, current_user_id)
    if not car_rating:
        raise HTTPException(status_code=404, detail="Car not found")
    return car_rating

@router.post("/loan-estimate", response_model=LoanEstimateResponse)
async def calculate_loan_estimate(loan_data: LoanEstimateRequest):
    return LoanEstimateService.calculate_loan(loan_data)

@router.post("/favorites/toggle", response_model=FavoriteToggleResponse)
async def toggle_favorite(
    favorite_data: UserFavoriteCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    try:
        is_favorite, message = UserFavoriteService.toggle_favorite(
            db, current_user_id, favorite_data.car_id
        )
        return FavoriteToggleResponse(is_favorite=is_favorite, message=message)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/favorites", response_model=List[UserFavoriteResponse])
async def get_user_favorites(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    return UserFavoriteService.get_user_favorites(db, current_user_id, skip, limit)

@router.get("/{car_id}", response_model=CarDetailResponse)
async def get_car(
    car_id: int = Path(..., description="The ID of the car to get"),
    increment_view: bool = Query(False, description="Whether to increment the view count"),
    db: Session = Depends(get_db)
):
    car = CarService.get_car_by_id(db, car_id, increment_view)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    avg_rating = CarRatingService.get_avg_rating(db, car_id)

    response_dict = CarResponse.from_orm(car).dict()
    response_dict["avg_rating"] = avg_rating

    if car.location:
        try:
            from geoalchemy2.shape import to_shape
            point = to_shape(car.location)
            response_dict["location"] = {"latitude": point.y, "longitude": point.x}
        except:
            response_dict["location"] = None
    else:
        response_dict["location"] = None

    return CarDetailResponse(**response_dict)