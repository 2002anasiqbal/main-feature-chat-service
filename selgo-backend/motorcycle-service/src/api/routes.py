# selgo-backend/motorcycle-service/src/routes.py
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session, joinedload  # Add joinedload here
from sqlalchemy import func
from typing import List, Optional
import math
import base64
import os
import uuid
import traceback

from ..database.database import get_db
from ..services.services import MotorcycleService, MotorcycleCategoryService
from ..models.schemas import (
    Motorcycle, MotorcycleCreate, MotorcycleUpdate, MotorcycleListResponse,
    MotorcycleSearchFilters, MapFilterRequest, PaginatedResponse,
    MotorcycleCategory, MotorcycleCategoryCreate, LoanCalculationRequest, LoanCalculationResponse
)
from ..models import models

router = APIRouter()

# 1. MotorcycleAdPostModule
@router.post("/motorcycles/new", response_model=Motorcycle)
async def create_motorcycle(
    motorcycle: MotorcycleCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Post a new motorcycle ad (Sell with Netbill or normally)
    URL: /api/motorcycles/new
    """
    try:
        print(f"📝 Received motorcycle data:")
        print(f"  Title: {motorcycle.title}")
        print(f"  Brand: {motorcycle.brand}")
        print(f"  Model: {motorcycle.model}")
        print(f"  Category ID: {motorcycle.category_id}")
        print(f"  Seller ID: {motorcycle.seller_id}")
        
        # Verify category exists
        category = db.query(models.MotorcycleCategory).filter(
            models.MotorcycleCategory.id == motorcycle.category_id
        ).first()
        
        if category:
            print(f"✅ Category found: {category.name} (ID: {category.id})")
        else:
            print(f"❌ Category ID {motorcycle.category_id} not found!")
            raise HTTPException(status_code=400, detail=f"Category ID {motorcycle.category_id} not found")
        
        # Handle base64 image data
        processed_images = []
        if motorcycle.images:
            print(f"🖼️ Processing {len(motorcycle.images)} images...")
            for i, img_data in enumerate(motorcycle.images):
                try:
                    if img_data.image_url.startswith('data:image'):
                        # Save base64 image to file
                        header, data = img_data.image_url.split(',', 1)
                        img_bytes = base64.b64decode(data)
                        
                        # Generate filename
                        file_extension = header.split('/')[1].split(';')[0]
                        filename = f"motorcycle_{uuid.uuid4()}.{file_extension}"
                        
                        # Create uploads directory if it doesn't exist
                        os.makedirs("uploads/motorcycles", exist_ok=True)
                        
                        # Save file
                        file_path = f"uploads/motorcycles/{filename}"
                        with open(file_path, 'wb') as f:
                            f.write(img_bytes)
                        
                        # Update image URL to be accessible via the web server
                        img_data.image_url = f"http://localhost:8003/uploads/motorcycles/{filename}"
                        processed_images.append(img_data)
                        print(f"✅ Processed image {i+1}: {filename}")
                    else:
                        processed_images.append(img_data)
                        print(f"✅ Using existing image URL {i+1}: {img_data.image_url}")
                except Exception as e:
                    print(f"❌ Error processing image {i+1}: {e}")
                    continue
        
        # Update motorcycle data with processed images
        motorcycle_dict = motorcycle.dict()
        motorcycle_dict['images'] = processed_images
        
        print(f"📊 Creating motorcycle with category ID: {motorcycle.category_id}")
        new_motorcycle = MotorcycleService.create_motorcycle(db, MotorcycleCreate(**motorcycle_dict))
        
        # Verify the created motorcycle
        print(f"✅ Motorcycle created successfully:")
        print(f"  ID: {new_motorcycle.id}")
        print(f"  Title: {new_motorcycle.title}")
        print(f"  Category ID: {new_motorcycle.category_id}")
        if new_motorcycle.category:
            print(f"  Category Name: {new_motorcycle.category.name}")
        
        # If netbill is enabled, add background task for processing
        if motorcycle.netbill:
            background_tasks.add_task(process_netbill_transaction, new_motorcycle.id)
        
        return new_motorcycle
        
    except Exception as e:
        print(f"❌ Error creating motorcycle: {e}")
        print(f"📄 Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))
    
# 2. MotorcycleSearchModule
@router.get("/motorcycles/search", response_model=PaginatedResponse)
async def search_motorcycles(
    motorcycle_type: Optional[str] = None,
    brand: Optional[str] = None,
    model: Optional[str] = None,
    city: Optional[str] = None,
    condition: Optional[str] = None,
    seller_type: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    year_min: Optional[int] = None,
    year_max: Optional[int] = None,
    mileage_min: Optional[int] = None,
    mileage_max: Optional[int] = None,
    search_term: Optional[str] = None,
    category_id: Optional[int] = None,
    category_name: Optional[str] = None,  # Add this parameter
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Show bikes based on type (Adventure, Nakne, Touring, Sports)
    URL: /api/motorcycles/search
    """
    
    # If category_name is provided, find the category_id
    if category_name and not category_id:
        category = db.query(models.MotorcycleCategory).filter(
            models.MotorcycleCategory.name == category_name
        ).first()
        if category:
            category_id = category.id
            print(f"✅ Found category '{category_name}' with ID: {category_id}")
        else:
            print(f"❌ Category '{category_name}' not found")
    
    # First, let's check total count in database
    total_in_db = db.query(models.Motorcycle).count()
    active_in_db = db.query(models.Motorcycle).filter(models.Motorcycle.is_active == True).count()
    
    filters = MotorcycleSearchFilters(
        category_id=category_id,
        category_name=category_name,  # Include this
        motorcycle_type=motorcycle_type,
        brand=brand,
        model=model,
        city=city,
        condition=condition,
        seller_type=seller_type,
        price_min=price_min,
        price_max=price_max,
        year_min=year_min,
        year_max=year_max,
        mileage_min=mileage_min,
        mileage_max=mileage_max,
        search_term=search_term
    )
    
    motorcycles, total = MotorcycleService.search_motorcycles(db, filters, page, per_page)
 
    # Convert to response format
    items = []
    for motorcycle in motorcycles:
        primary_image = None
        if motorcycle.images:
            primary_img = next((img for img in motorcycle.images if img.is_primary), None)
            primary_image = primary_img.image_url if primary_img else motorcycle.images[0].image_url
        
        item = MotorcycleListResponse(
            id=motorcycle.id,
            title=motorcycle.title,
            brand=motorcycle.brand,
            model=motorcycle.model,
            year=motorcycle.year,
            price=motorcycle.price,
            condition=motorcycle.condition,
            motorcycle_type=motorcycle.motorcycle_type,
            city=motorcycle.city,
            is_featured=motorcycle.is_featured,
            views_count=motorcycle.views_count,
            created_at=motorcycle.created_at,
            primary_image=primary_image
        )
        items.append(item)
    
    pages = math.ceil(total / per_page)
    
    response = PaginatedResponse(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
        pages=pages,
        has_next=page < pages,
        has_prev=page > 1
    )
    
  
    
    return response

# 3. MotorcycleDetailModule
@router.get("/motorcycles/{motorcycle_id}", response_model=Motorcycle)
async def get_motorcycle_detail(
    motorcycle_id: int,
    db: Session = Depends(get_db)
):
    """
    Show bike detail page including specs, images, seller info, and contact button
    URL: /api/motorcycles/{id}
    """
    motorcycle = MotorcycleService.get_motorcycle(db, motorcycle_id)
    if not motorcycle:
        raise HTTPException(status_code=404, detail="Motorcycle not found")
    
    return motorcycle

# 4. MotorcycleMapFilterModule
@router.post("/motorcycles/filter/map", response_model=PaginatedResponse)
async def filter_motorcycles_by_map(
    map_filter: MapFilterRequest,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Geo-filter motorcycles using map location + radius slider
    URL: /api/motorcycles/filter/map
    """
    motorcycles, total = MotorcycleService.search_motorcycles_by_location(
        db=db,
        latitude=map_filter.latitude,
        longitude=map_filter.longitude,
        radius_km=map_filter.radius_km,
        filters=map_filter.filters,
        page=page,
        per_page=per_page
    )
    
    # Convert to response format
    items = []
    for motorcycle in motorcycles:
        primary_image = None
        if motorcycle.images:
            primary_img = next((img for img in motorcycle.images if img.is_primary), None)
            primary_image = primary_img.image_url if primary_img else motorcycle.images[0].image_url
        
        items.append(MotorcycleListResponse(
            id=motorcycle.id,
            title=motorcycle.title,
            brand=motorcycle.brand,
            model=motorcycle.model,
            year=motorcycle.year,
            price=motorcycle.price,
            condition=motorcycle.condition,
            motorcycle_type=motorcycle.motorcycle_type,
            city=motorcycle.city,
            is_featured=motorcycle.is_featured,
            views_count=motorcycle.views_count,
            created_at=motorcycle.created_at,
            primary_image=primary_image
        ))
    
    pages = math.ceil(total / per_page)
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
        pages=pages,
        has_next=page < pages,
        has_prev=page > 1
    )

# 5. MotorcycleFilterSidebarModule
@router.get("/motorcycles/filter/sidebar")
async def get_filter_options(db: Session = Depends(get_db)):
    """
    Dynamic filtering based on category, model, city, price range, seller type, year, etc.
    URL: /api/motorcycles/filter/sidebar
    """
    
    # Get motorcycle types with counts
    type_counts = MotorcycleService.get_motorcycle_types_with_counts(db)
    
    # Get categories with counts
    categories = MotorcycleCategoryService.get_categories_with_counts(db)
    
    # Get available brands
    brands = db.query(models.Motorcycle.brand).distinct().filter(
        models.Motorcycle.is_active == True
    ).all()
    brands = [brand[0] for brand in brands if brand[0]]
    
    # Get cities
    cities = db.query(models.Motorcycle.city).distinct().filter(
        models.Motorcycle.is_active == True,
        models.Motorcycle.city.isnot(None)
    ).all()
    cities = [city[0] for city in cities if city[0]]
    
    # Get price range
    price_range = db.query(
        func.min(models.Motorcycle.price).label('min_price'),
        func.max(models.Motorcycle.price).label('max_price')
    ).filter(models.Motorcycle.is_active == True).first()
    
    # Get year range
    year_range = db.query(
        func.min(models.Motorcycle.year).label('min_year'),
        func.max(models.Motorcycle.year).label('max_year')
    ).filter(models.Motorcycle.is_active == True).first()
    
    return {
        "motorcycle_types": type_counts,
        "categories": categories,
        "brands": sorted(brands),
        "cities": sorted(cities),
        "price_range": {
            "min": float(price_range.min_price) if price_range.min_price else 0,
            "max": float(price_range.max_price) if price_range.max_price else 0
        },
        "year_range": {
            "min": year_range.min_year if year_range.min_year else 1990,
            "max": year_range.max_year if year_range.max_year else 2024
        },
        "conditions": [condition.value for condition in models.ConditionEnum],
        "seller_types": [seller_type.value for seller_type in models.SellerTypeEnum]
    }

# # 6. MotorcycleContactModule
# @router.post("/messages/motorcycle/send", response_model=Message)
# async def send_motorcycle_message(
#     message: MessageCreate,
#     background_tasks: BackgroundTasks,
#     db: Session = Depends(get_db)
# ):
#     """
#     Contact seller via form (sends email)
#     URL: /api/messages/motorcycle/send
#     """
#     try:
#         # Get motorcycle to verify it exists
#         motorcycle = db.query(models.Motorcycle).filter(
#             models.Motorcycle.id == message.motorcycle_id
#         ).first()
        
#         if not motorcycle:
#             raise HTTPException(status_code=404, detail="Motorcycle not found")
        
#         # Create message
#         new_message = MotorcycleService.send_message(db, message)
        
#         # Send email notification in background
#         background_tasks.add_task(
#             send_email_notification,
#             motorcycle.seller.email,
#             motorcycle.title,
#             message.content,
#             message.phone,
#             message.email
#         )
        
#         return new_message
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# 7. MotorcycleLoanOfferModule
@router.post("/tools/motorcycle-loans", response_model=LoanCalculationResponse)
async def calculate_motorcycle_loan(loan_request: LoanCalculationRequest):
    """
    Show monthly loan cost estimates
    URL: /api/tools/motorcycle-loans
    """
    try:
        return MotorcycleService.calculate_loan(
            price=loan_request.price,
            term_months=loan_request.term_months,
            interest_rate=loan_request.interest_rate
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Additional routes for categories
@router.get("/motorcycles/categories", response_model=List[MotorcycleCategory])
async def get_motorcycle_categories(db: Session = Depends(get_db)):
    """
    Fetch subcategories under motorcycles like "Tractor", "Suzuki", "Auto Bikes", etc.
    URL: /api/motorcycles/categories
    """
    return MotorcycleCategoryService.get_all_categories(db)

@router.post("/motorcycles/categories", response_model=MotorcycleCategory)
async def create_motorcycle_category(
    category: MotorcycleCategoryCreate,
    db: Session = Depends(get_db)
):
    """Create a new motorcycle category"""
    return MotorcycleCategoryService.create_category(db, category)

@router.get("/motorcycles/categories/{category_name}")
async def get_motorcycles_by_category_name(
    category_name: str,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get motorcycles by category name (e.g., "Thresher 6000", "Suzuki 6000")
    """
    
    # Find category by name
    category = db.query(models.MotorcycleCategory).filter(
        models.MotorcycleCategory.name == category_name
    ).first()
    
    if not category:
        print(f"❌ Category '{category_name}' not found")
        # Return empty result instead of error
        return PaginatedResponse(
            items=[],
            total=0,
            page=page,
            per_page=per_page,
            pages=0,
            has_next=False,
            has_prev=False
        )
    
    print(f"✅ Found category: {category.name} (ID: {category.id})")
    
    # Get motorcycles for this category
    filters = MotorcycleSearchFilters(category_id=category.id)
    motorcycles, total = MotorcycleService.search_motorcycles(db, filters, page, per_page)
    
    # Convert to response format
    items = []
    for motorcycle in motorcycles:
        primary_image = None
        if motorcycle.images:
            primary_img = next((img for img in motorcycle.images if img.is_primary), None)
            primary_image = primary_img.image_url if primary_img else motorcycle.images[0].image_url
        
        items.append(MotorcycleListResponse(
            id=motorcycle.id,
            title=motorcycle.title,
            brand=motorcycle.brand,
            model=motorcycle.model,
            year=motorcycle.year,
            price=motorcycle.price,
            condition=motorcycle.condition,
            motorcycle_type=motorcycle.motorcycle_type,
            city=motorcycle.city,
            is_featured=motorcycle.is_featured,
            views_count=motorcycle.views_count,
            created_at=motorcycle.created_at,
            primary_image=primary_image
        ))
    
    pages = math.ceil(total / per_page) if total > 0 else 0
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
        pages=pages,
        has_next=page < pages,
        has_prev=page > 1
    )

@router.get("/categories/all")
async def get_all_categories(db: Session = Depends(get_db)):
    """Get all categories with motorcycle counts"""
    try:
        categories = MotorcycleCategoryService.get_categories_with_counts(db)
        return {"categories": categories}
    except Exception as e:
        print(f"❌ Error getting categories: {e}")
        return {"categories": [], "error": str(e)}

# Helper functions for background tasks
async def process_netbill_transaction(motorcycle_id: int):
    """Process netbill transaction in background"""

async def send_email_notification(
    seller_email: str,
    motorcycle_title: str,
    message_content: str,
    sender_phone: str,
    sender_email: str
):
    """Send email notification to seller"""
    print(f"Sending email to {seller_email} about {motorcycle_title}")
    print(f"Message: {message_content}")
    print(f"From: {sender_email}, Phone: {sender_phone}")

# Import models here to avoid circular imports
from ..models import models
from sqlalchemy import func