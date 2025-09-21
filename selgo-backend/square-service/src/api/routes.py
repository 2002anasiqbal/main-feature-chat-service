from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
from ..services.services import (
    ItemCategoryService,
    ItemService,
    ItemImageService,
    ItemRatingService,
    UserFavoriteService
)
from ..models.item_schemas import (
    UserFavoriteCreate,
    UserFavoriteResponse,
    FavoriteToggleResponse,
    ItemCategoryCreate,
    ItemCategoryResponse,
    ItemCreate,
    ItemUpdate,
    ItemResponse,
    ItemDetailResponse,
    ItemListResponse,
    ItemFilterParams,
    ItemImageCreate,
    ItemImageResponse,
    ItemRatingCreate,
    ItemRatingResponse,
    PaginatedResponse
)
from ..database.database import get_db
from ..config.config import settings
from ..utils.auth import get_current_user_id, get_current_admin_user_id

router = APIRouter(
    prefix="/api/v1/square",
    tags=["square"],
    responses={404: {"description": "Not found"}}
)

@router.post("/categories", response_model=ItemCategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_item_category(
    category: ItemCategoryCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_admin_user_id)
):
    return ItemCategoryService.create_category(db, category)

@router.get("/categories", response_model=List[ItemCategoryResponse])
async def get_all_item_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return ItemCategoryService.get_all_categories(db, skip, limit)

@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    return ItemService.create_item(db, item, current_user_id)

@router.post("/filter", response_model=PaginatedResponse)
async def filter_items(
    filters: ItemFilterParams,
    db: Session = Depends(get_db)
):
    items, total = ItemService.filter_items(db, filters)

    item_list_responses = [ItemListResponse.from_orm(item) for item in items]

    return PaginatedResponse(
        items=item_list_responses,
        total=total,
        limit=filters.limit,
        offset=filters.offset
    )

@router.get("/recommended", response_model=List[ItemListResponse])
async def get_recommended_items(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    items = ItemService.get_recommended_items(db, limit)
    return [ItemListResponse.from_orm(item) for item in items]

@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item: ItemUpdate,
    item_id: int = Path(..., description="The ID of the item to update"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    updated_item = ItemService.update_item(db, item_id, item, current_user_id)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found or you don't have permission to update it")
    return updated_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int = Path(..., description="The ID of the item to delete"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    success = ItemService.delete_item(db, item_id, current_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found or you don't have permission to delete it")
    return {"detail": "Item deleted successfully"}

@router.post("/{item_id}/images", response_model=ItemImageResponse, status_code=status.HTTP_201_CREATED)
async def add_item_image(
    image_data: ItemImageCreate,
    item_id: int = Path(..., description="The ID of the item to add an image to"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    image = ItemImageService.add_image(db, item_id, image_data, current_user_id)
    if not image:
        raise HTTPException(status_code=404, detail="Item not found or you don't have permission to add images")
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

@router.post("/{item_id}/ratings", response_model=ItemRatingResponse, status_code=status.HTTP_201_CREATED)
async def create_item_rating(
    rating: ItemRatingCreate,
    item_id: int = Path(..., description="The ID of the item to rate"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    if rating.item_id != item_id:
        raise HTTPException(status_code=400, detail="Item ID in path and body do not match")

    item_rating = ItemRatingService.create_rating(db, rating, current_user_id)
    if not item_rating:
        raise HTTPException(status_code=404, detail="Item not found")
    return item_rating

@router.post("/favorites/toggle", response_model=FavoriteToggleResponse)
async def toggle_favorite(
    favorite_data: UserFavoriteCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    try:
        is_favorite, message = UserFavoriteService.toggle_favorite(
            db, current_user_id, favorite_data.item_id
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

@router.get("/{item_id}", response_model=ItemDetailResponse)
async def get_item(
    item_id: int = Path(..., description="The ID of the item to get"),
    increment_view: bool = Query(False, description="Whether to increment the view count"),
    db: Session = Depends(get_db)
):
    item = ItemService.get_item_by_id(db, item_id, increment_view)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    avg_rating = ItemRatingService.get_avg_rating(db, item_id)

    response_dict = ItemResponse.from_orm(item).dict()
    response_dict["avg_rating"] = avg_rating

    if item.location:
        try:
            from geoalchemy2.shape import to_shape
            point = to_shape(item.location)
            response_dict["location"] = {"latitude": point.y, "longitude": point.x}
        except:
            response_dict["location"] = None
    else:
        response_dict["location"] = None

    return ItemDetailResponse(**response_dict)