# car-service/src/api/car_auction_routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

from ..database.database import get_db
from ..services.car_auction_services import CarAuctionService
from ..models.car_auction_schemas import (
    CarAuctionCreate, CarAuctionUpdate, CarAuctionResponse,
    CarAuctionBidCreate, CarAuctionBidResponse,
    CarAuctionWatcherCreate, CarAuctionWatcherResponse,
    CarAuctionSearchRequest, CarAuctionListResponse,
    CarAuctionStats, SellerDashboard, BidderDashboard,
    AuctionStatus, CarAuctionSearchFilters
)
from ..utils.auth import get_current_user_id, get_current_user_data
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/car-auctions", tags=["car-auctions"])

# Auction Management
@router.post("/", response_model=CarAuctionResponse, status_code=status.HTTP_201_CREATED)
async def create_auction(
    auction_data: CarAuctionCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Create a new car auction."""
    service = CarAuctionService(db)
    return await service.create_auction(auction_data, user_id)

@router.get("/search", response_model=CarAuctionListResponse)
async def search_auctions(
    query: Optional[str] = Query(None, description="Search query"),
    status_filter: Optional[List[AuctionStatus]] = Query(None, description="Filter by auction status"),
    make: Optional[str] = Query(None, description="Car make"),
    model: Optional[str] = Query(None, description="Car model"),
    year_from: Optional[int] = Query(None, description="Minimum year"),
    year_to: Optional[int] = Query(None, description="Maximum year"),
    price_from: Optional[Decimal] = Query(None, description="Minimum current bid"),
    price_to: Optional[Decimal] = Query(None, description="Maximum current bid"),
    mileage_from: Optional[int] = Query(None, description="Minimum mileage"),
    mileage_to: Optional[int] = Query(None, description="Maximum mileage"),
    location: Optional[str] = Query(None, description="Location filter"),
    has_reserve: Optional[bool] = Query(None, description="Has reserve price"),
    has_buy_now: Optional[bool] = Query(None, description="Has buy now price"),
    ending_soon: Optional[bool] = Query(None, description="Ending within 24 hours"),
    no_reserve: Optional[bool] = Query(None, description="No reserve auctions only"),
    featured_only: Optional[bool] = Query(None, description="Featured auctions only"),
    seller_type: Optional[str] = Query(None, description="Seller type filter"),
    sort_by: Optional[str] = Query("end_time", description="Sort field"),
    sort_order: Optional[str] = Query("asc", description="Sort order"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Search car auctions with filters."""
    filters = CarAuctionSearchFilters(
        status=status_filter,
        make=make,
        model=model,
        year_from=year_from,
        year_to=year_to,
        price_from=price_from,
        price_to=price_to,
        mileage_from=mileage_from,
        mileage_to=mileage_to,
        location=location,
        has_reserve=has_reserve,
        has_buy_now=has_buy_now,
        ending_soon=ending_soon,
        no_reserve=no_reserve,
        featured_only=featured_only,
        seller_type=seller_type
    )
    
    search_request = CarAuctionSearchRequest(
        query=query,
        filters=filters,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        per_page=per_page
    )
    
    service = CarAuctionService(db)
    return await service.search_auctions(search_request)

@router.get("/{auction_id}", response_model=CarAuctionResponse)
async def get_auction(
    auction_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific auction by ID."""
    service = CarAuctionService(db)
    auction = await service.get_auction_by_id(auction_id)
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    return auction

@router.put("/{auction_id}", response_model=CarAuctionResponse)
async def update_auction(
    auction_id: str,
    auction_data: CarAuctionUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Update an auction."""
    service = CarAuctionService(db)
    auction = await service.update_auction(auction_id, auction_data, user_id)
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found or not authorized")
    return auction

@router.delete("/{auction_id}/cancel", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_auction(
    auction_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Cancel an auction."""
    service = CarAuctionService(db)
    success = await service.cancel_auction(auction_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Auction not found or not authorized")

# Bidding
@router.post("/bids", response_model=CarAuctionBidResponse, status_code=status.HTTP_201_CREATED)
async def place_bid(
    bid_data: CarAuctionBidCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Place a bid on an auction."""
    service = CarAuctionService(db)
    return await service.place_bid(bid_data, user_id)

@router.get("/{auction_id}/bids", response_model=List[CarAuctionBidResponse])
async def get_auction_bids(
    auction_id: str,
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Get bids for a specific auction."""
    service = CarAuctionService(db)
    return await service.get_auction_bids(auction_id, page, per_page)

# Watchlist
@router.post("/watch", response_model=CarAuctionWatcherResponse, status_code=status.HTTP_201_CREATED)
async def watch_auction(
    watcher_data: CarAuctionWatcherCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Add auction to watchlist."""
    service = CarAuctionService(db)
    return await service.watch_auction(watcher_data, user_id)

@router.delete("/{auction_id}/unwatch", status_code=status.HTTP_204_NO_CONTENT)
async def unwatch_auction(
    auction_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Remove auction from watchlist."""
    service = CarAuctionService(db)
    success = await service.unwatch_auction(auction_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Auction not in watchlist")

@router.get("/watchlist/my-watched", response_model=List[CarAuctionResponse])
async def get_watched_auctions(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get user's watched auctions."""
    service = CarAuctionService(db)
    return await service.get_user_watched_auctions(user_id, page, per_page)

# Dashboard and Statistics
@router.get("/dashboard/seller", response_model=SellerDashboard)
async def get_seller_dashboard(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get seller dashboard data."""
    service = CarAuctionService(db)
    return await service.get_seller_dashboard(user_id)

@router.get("/stats/overview", response_model=CarAuctionStats)
async def get_auction_stats(db: Session = Depends(get_db)):
    """Get auction marketplace statistics."""
    service = CarAuctionService(db)
    return await service.get_stats()

# Featured and Popular
@router.get("/featured/list", response_model=CarAuctionListResponse)
async def get_featured_auctions(
    limit: int = Query(10, ge=1, le=50, description="Number of featured auctions"),
    db: Session = Depends(get_db)
):
    """Get featured auctions."""
    filters = CarAuctionSearchFilters(featured_only=True)
    search_request = CarAuctionSearchRequest(
        filters=filters,
        sort_by="end_time",
        sort_order="asc",
        page=1,
        per_page=limit
    )
    
    service = CarAuctionService(db)
    return await service.search_auctions(search_request)

@router.get("/ending-soon/list", response_model=CarAuctionListResponse)
async def get_ending_soon_auctions(
    limit: int = Query(10, ge=1, le=50, description="Number of auctions ending soon"),
    db: Session = Depends(get_db)
):
    """Get auctions ending soon (within 24 hours)."""
    filters = CarAuctionSearchFilters(ending_soon=True)
    search_request = CarAuctionSearchRequest(
        filters=filters,
        sort_by="end_time",
        sort_order="asc",
        page=1,
        per_page=limit
    )
    
    service = CarAuctionService(db)
    return await service.search_auctions(search_request)

@router.get("/no-reserve/list", response_model=CarAuctionListResponse)
async def get_no_reserve_auctions(
    limit: int = Query(20, ge=1, le=50, description="Number of no-reserve auctions"),
    db: Session = Depends(get_db)
):
    """Get no-reserve auctions."""
    filters = CarAuctionSearchFilters(no_reserve=True, status=[AuctionStatus.ACTIVE])
    search_request = CarAuctionSearchRequest(
        filters=filters,
        sort_by="end_time",
        sort_order="asc",
        page=1,
        per_page=limit
    )
    
    service = CarAuctionService(db)
    return await service.search_auctions(search_request)

@router.get("/categories/popular")
async def get_popular_categories(db: Session = Depends(get_db)):
    """Get popular auction categories."""
    # This would typically query the database for popular makes/models
    # For now, return a placeholder response
    return {
        "categories": [
            {"make": "BMW", "count": 45, "average_price": 25000},
            {"make": "Mercedes-Benz", "count": 38, "average_price": 32000},
            {"make": "Audi", "count": 32, "average_price": 28000},
            {"make": "Volkswagen", "count": 28, "average_price": 18000},
            {"make": "Toyota", "count": 25, "average_price": 22000},
            {"make": "Porsche", "count": 18, "average_price": 65000}
        ]
    }

@router.get("/trends/weekly")
async def get_weekly_trends(db: Session = Depends(get_db)):
    """Get weekly auction trends."""
    # This would typically analyze auction data for trends
    # For now, return a placeholder response
    return {
        "trends": {
            "total_auctions_this_week": 156,
            "total_bids_this_week": 2847,
            "average_final_price": 24500,
            "success_rate": 78.5,
            "top_selling_make": "BMW",
            "most_active_day": "Sunday",
            "peak_bidding_hour": "20:00"
        }
    }