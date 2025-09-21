# car-service/src/services/car_auction_services.py
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc
from typing import List, Optional, Dict, Any, Tuple
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from decimal import Decimal
import uuid
import logging

from ..models.car_auction_models import (
    CarAuction, CarAuctionBid, CarAuctionWatcher, CarAuctionImage,
    CarAuctionReport, CarAuctionTransaction, AuctionStatus, BidStatus, PaymentStatus
)
from ..models.car_auction_schemas import (
    CarAuctionCreate, CarAuctionUpdate, CarAuctionResponse,
    CarAuctionBidCreate, CarAuctionBidResponse,
    CarAuctionWatcherCreate, CarAuctionWatcherResponse,
    CarAuctionSearchRequest, CarAuctionListResponse,
    CarAuctionStats, SellerDashboard, BidderDashboard
)

logger = logging.getLogger(__name__)

class CarAuctionService:
    def __init__(self, db: Session):
        self.db = db

    async def create_auction(self, auction_data: CarAuctionCreate, seller_id: str) -> CarAuctionResponse:
        """Create a new car auction."""
        try:
            # Verify the car exists and belongs to the seller
            from ..models.car_models import Car
            car = self.db.query(Car).filter(
                and_(Car.id == auction_data.car_id, Car.seller_id == seller_id)
            ).first()
            
            if not car:
                raise HTTPException(status_code=404, detail="Car not found or not authorized")
            
            # Check if car already has an active auction
            existing_auction = self.db.query(CarAuction).filter(
                and_(
                    CarAuction.car_id == auction_data.car_id,
                    CarAuction.status.in_([AuctionStatus.UPCOMING, AuctionStatus.ACTIVE])
                )
            ).first()
            
            if existing_auction:
                raise HTTPException(status_code=400, detail="Car already has an active auction")
            
            # Create auction
            auction_dict = auction_data.dict()
            auction_dict['seller_id'] = seller_id
            auction_dict['current_bid'] = auction_data.starting_price
            
            # Set status based on start time
            now = datetime.utcnow()
            if auction_data.start_time <= now:
                auction_dict['status'] = AuctionStatus.ACTIVE
            else:
                auction_dict['status'] = AuctionStatus.UPCOMING
            
            auction = CarAuction(**auction_dict)
            self.db.add(auction)
            self.db.commit()
            self.db.refresh(auction)
            
            return CarAuctionResponse.from_orm(auction)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating auction: {str(e)}")
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Failed to create auction")

    async def get_auction_by_id(self, auction_id: str) -> Optional[CarAuctionResponse]:
        """Get an auction by ID."""
        auction = self.db.query(CarAuction).filter(CarAuction.id == auction_id).first()
        if auction:
            # Update view count
            auction.view_count += 1
            self.db.commit()
            return CarAuctionResponse.from_orm(auction)
        return None

    async def update_auction(self, auction_id: str, auction_data: CarAuctionUpdate, seller_id: str) -> Optional[CarAuctionResponse]:
        """Update an auction."""
        auction = self.db.query(CarAuction).filter(
            and_(
                CarAuction.id == auction_id,
                CarAuction.seller_id == seller_id,
                CarAuction.status.in_([AuctionStatus.UPCOMING, AuctionStatus.ACTIVE])
            )
        ).first()
        
        if not auction:
            return None
        
        # Don't allow certain updates if auction is active and has bids
        if auction.status == AuctionStatus.ACTIVE and auction.total_bids > 0:
            restricted_fields = ['starting_price', 'reserve_price', 'bid_increment']
            update_dict = auction_data.dict(exclude_unset=True)
            for field in restricted_fields:
                if field in update_dict:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Cannot update {field} on active auction with bids"
                    )
        
        update_dict = auction_data.dict(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(auction, key, value)
        
        auction.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(auction)
        
        return CarAuctionResponse.from_orm(auction)

    async def cancel_auction(self, auction_id: str, seller_id: str) -> bool:
        """Cancel an auction."""
        auction = self.db.query(CarAuction).filter(
            and_(
                CarAuction.id == auction_id,
                CarAuction.seller_id == seller_id,
                CarAuction.status.in_([AuctionStatus.UPCOMING, AuctionStatus.ACTIVE])
            )
        ).first()
        
        if not auction:
            return False
        
        # Can only cancel if no bids or only starting bid
        if auction.total_bids > 0 and auction.current_bid > auction.starting_price:
            raise HTTPException(
                status_code=400, 
                detail="Cannot cancel auction with active bids above starting price"
            )
        
        auction.status = AuctionStatus.CANCELLED
        auction.updated_at = datetime.utcnow()
        self.db.commit()
        
        return True

    async def search_auctions(self, search_request: CarAuctionSearchRequest) -> CarAuctionListResponse:
        """Search auctions with filters."""
        try:
            query = self.db.query(CarAuction)
            
            # Apply filters
            if search_request.filters:
                filters = search_request.filters
                
                if filters.status:
                    query = query.filter(CarAuction.status.in_(filters.status))
                
                if filters.price_from:
                    query = query.filter(CarAuction.current_bid >= filters.price_from)
                
                if filters.price_to:
                    query = query.filter(CarAuction.current_bid <= filters.price_to)
                
                if filters.has_reserve is not None:
                    if filters.has_reserve:
                        query = query.filter(CarAuction.reserve_price.isnot(None))
                    else:
                        query = query.filter(CarAuction.reserve_price.is_(None))
                
                if filters.has_buy_now is not None:
                    if filters.has_buy_now:
                        query = query.filter(CarAuction.buy_now_price.isnot(None))
                    else:
                        query = query.filter(CarAuction.buy_now_price.is_(None))
                
                if filters.ending_soon:
                    # Auctions ending within 24 hours
                    end_time_limit = datetime.utcnow() + timedelta(hours=24)
                    query = query.filter(
                        and_(
                            CarAuction.status == AuctionStatus.ACTIVE,
                            CarAuction.end_time <= end_time_limit
                        )
                    )
                
                if filters.no_reserve:
                    query = query.filter(CarAuction.reserve_price.is_(None))
                
                if filters.featured_only:
                    query = query.filter(CarAuction.is_featured == True)
                
                # Car-specific filters (join with Car table)
                if any([filters.make, filters.model, filters.year_from, filters.year_to, 
                       filters.mileage_from, filters.mileage_to]):
                    from ..models.car_models import Car
                    query = query.join(Car, CarAuction.car_id == Car.id)
                    
                    if filters.make:
                        query = query.filter(Car.make.ilike(f"%{filters.make}%"))
                    
                    if filters.model:
                        query = query.filter(Car.model.ilike(f"%{filters.model}%"))
                    
                    if filters.year_from:
                        query = query.filter(Car.year >= filters.year_from)
                    
                    if filters.year_to:
                        query = query.filter(Car.year <= filters.year_to)
                    
                    if filters.mileage_from:
                        query = query.filter(Car.mileage >= filters.mileage_from)
                    
                    if filters.mileage_to:
                        query = query.filter(Car.mileage <= filters.mileage_to)
            
            # Apply text search
            if search_request.query:
                from ..models.car_models import Car
                if not query.join(Car, CarAuction.car_id == Car.id, isouter=True):
                    query = query.join(Car, CarAuction.car_id == Car.id)
                
                search_term = f"%{search_request.query}%"
                query = query.filter(
                    or_(
                        CarAuction.title.ilike(search_term),
                        CarAuction.description.ilike(search_term),
                        Car.make.ilike(search_term),
                        Car.model.ilike(search_term)
                    )
                )
            
            # Get total count
            total = query.count()
            
            # Apply sorting
            if search_request.sort_by:
                sort_column = getattr(CarAuction, search_request.sort_by, None)
                if sort_column:
                    if search_request.sort_order == "desc":
                        query = query.order_by(desc(sort_column))
                    else:
                        query = query.order_by(asc(sort_column))
            
            # Apply pagination
            offset = (search_request.page - 1) * search_request.per_page
            auctions = query.offset(offset).limit(search_request.per_page).all()
            
            total_pages = (total + search_request.per_page - 1) // search_request.per_page
            
            return CarAuctionListResponse(
                auctions=[CarAuctionResponse.from_orm(auction) for auction in auctions],
                total=total,
                page=search_request.page,
                per_page=search_request.per_page,
                total_pages=total_pages
            )
        except Exception as e:
            logger.error(f"Error searching auctions: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to search auctions")

    async def place_bid(self, bid_data: CarAuctionBidCreate, bidder_id: str) -> CarAuctionBidResponse:
        """Place a bid on an auction."""
        try:
            # Get the auction
            auction = self.db.query(CarAuction).filter(
                CarAuction.id == bid_data.auction_id
            ).first()
            
            if not auction:
                raise HTTPException(status_code=404, detail="Auction not found")
            
            if auction.status != AuctionStatus.ACTIVE:
                raise HTTPException(status_code=400, detail="Auction is not active")
            
            if auction.seller_id == bidder_id:
                raise HTTPException(status_code=400, detail="Cannot bid on your own auction")
            
            # Check if auction has ended
            if datetime.utcnow() > auction.end_time:
                raise HTTPException(status_code=400, detail="Auction has ended")
            
            # Validate bid amount
            min_bid = auction.current_bid + auction.bid_increment
            if bid_data.bid_amount < min_bid:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Bid must be at least {min_bid}"
                )
            
            # Check buy-now price
            if auction.buy_now_price and bid_data.bid_amount >= auction.buy_now_price:
                # This is a buy-now purchase
                bid_data.bid_amount = auction.buy_now_price
                
                # Create the winning bid
                bid_dict = bid_data.dict()
                bid_dict['bidder_id'] = bidder_id
                bid_dict['status'] = BidStatus.WON
                bid_dict['is_winning'] = True
                
                bid = CarAuctionBid(**bid_dict)
                self.db.add(bid)
                
                # Update auction
                auction.current_bid = bid_data.bid_amount
                auction.winning_bidder_id = bidder_id
                auction.winning_bid = bid_data.bid_amount
                auction.status = AuctionStatus.SOLD
                auction.sold_at = datetime.utcnow()
                auction.total_bids += 1
                
                # Check if this is a new bidder
                existing_bidder = self.db.query(CarAuctionBid).filter(
                    and_(
                        CarAuctionBid.auction_id == bid_data.auction_id,
                        CarAuctionBid.bidder_id == bidder_id
                    )
                ).first()
                
                if not existing_bidder:
                    auction.unique_bidders += 1
                
                self.db.commit()
                self.db.refresh(bid)
                
                return CarAuctionBidResponse.from_orm(bid)
            
            # Regular bid processing
            # Mark previous winning bid as outbid
            previous_winning_bid = self.db.query(CarAuctionBid).filter(
                and_(
                    CarAuctionBid.auction_id == bid_data.auction_id,
                    CarAuctionBid.is_winning == True
                )
            ).first()
            
            if previous_winning_bid:
                previous_winning_bid.is_winning = False
                previous_winning_bid.status = BidStatus.OUTBID
            
            # Create new bid
            bid_dict = bid_data.dict()
            bid_dict['bidder_id'] = bidder_id
            bid_dict['status'] = BidStatus.WINNING
            bid_dict['is_winning'] = True
            
            # Handle proxy bidding
            if bid_data.max_bid and bid_data.max_bid > bid_data.bid_amount:
                bid_dict['is_proxy_bid'] = True
            
            bid = CarAuctionBid(**bid_dict)
            self.db.add(bid)
            
            # Update auction
            auction.current_bid = bid_data.bid_amount
            auction.winning_bidder_id = bidder_id
            auction.total_bids += 1
            
            # Check if reserve is met
            if auction.reserve_price and bid_data.bid_amount >= auction.reserve_price:
                auction.is_reserve_met = True
            
            # Check if this is a new bidder
            existing_bidder = self.db.query(CarAuctionBid).filter(
                and_(
                    CarAuctionBid.auction_id == bid_data.auction_id,
                    CarAuctionBid.bidder_id == bidder_id
                )
            ).first()
            
            if not existing_bidder:
                auction.unique_bidders += 1
            
            # Auto-extend auction if bid placed in final minutes
            time_remaining = auction.end_time - datetime.utcnow()
            if time_remaining.total_seconds() < (auction.auto_extend_minutes * 60):
                auction.end_time = datetime.utcnow() + timedelta(minutes=auction.auto_extend_minutes)
            
            self.db.commit()
            self.db.refresh(bid)
            
            return CarAuctionBidResponse.from_orm(bid)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error placing bid: {str(e)}")
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Failed to place bid")

    async def get_auction_bids(self, auction_id: str, page: int = 1, per_page: int = 20) -> List[CarAuctionBidResponse]:
        """Get bids for an auction."""
        query = self.db.query(CarAuctionBid).filter(
            CarAuctionBid.auction_id == auction_id
        )
        
        offset = (page - 1) * per_page
        bids = query.order_by(desc(CarAuctionBid.created_at)).offset(offset).limit(per_page).all()
        
        return [CarAuctionBidResponse.from_orm(bid) for bid in bids]

    async def watch_auction(self, watcher_data: CarAuctionWatcherCreate, user_id: str) -> CarAuctionWatcherResponse:
        """Add auction to user's watchlist."""
        try:
            # Check if already watching
            existing_watcher = self.db.query(CarAuctionWatcher).filter(
                and_(
                    CarAuctionWatcher.auction_id == watcher_data.auction_id,
                    CarAuctionWatcher.user_id == user_id
                )
            ).first()
            
            if existing_watcher:
                raise HTTPException(status_code=400, detail="Already watching this auction")
            
            # Create watcher
            watcher_dict = watcher_data.dict()
            watcher_dict['user_id'] = user_id
            
            watcher = CarAuctionWatcher(**watcher_dict)
            self.db.add(watcher)
            
            # Update auction watch count
            auction = self.db.query(CarAuction).filter(
                CarAuction.id == watcher_data.auction_id
            ).first()
            
            if auction:
                auction.watch_count += 1
            
            self.db.commit()
            self.db.refresh(watcher)
            
            return CarAuctionWatcherResponse.from_orm(watcher)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error watching auction: {str(e)}")
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Failed to watch auction")

    async def unwatch_auction(self, auction_id: str, user_id: str) -> bool:
        """Remove auction from user's watchlist."""
        watcher = self.db.query(CarAuctionWatcher).filter(
            and_(
                CarAuctionWatcher.auction_id == auction_id,
                CarAuctionWatcher.user_id == user_id
            )
        ).first()
        
        if not watcher:
            return False
        
        # Update auction watch count
        auction = self.db.query(CarAuction).filter(CarAuction.id == auction_id).first()
        if auction and auction.watch_count > 0:
            auction.watch_count -= 1
        
        self.db.delete(watcher)
        self.db.commit()
        
        return True

    async def get_user_watched_auctions(self, user_id: str, page: int = 1, per_page: int = 20) -> List[CarAuctionResponse]:
        """Get user's watched auctions."""
        query = self.db.query(CarAuction).join(
            CarAuctionWatcher, CarAuction.id == CarAuctionWatcher.auction_id
        ).filter(
            CarAuctionWatcher.user_id == user_id
        )
        
        offset = (page - 1) * per_page
        auctions = query.order_by(desc(CarAuctionWatcher.created_at)).offset(offset).limit(per_page).all()
        
        return [CarAuctionResponse.from_orm(auction) for auction in auctions]

    async def get_seller_dashboard(self, seller_id: str) -> SellerDashboard:
        """Get seller dashboard data."""
        try:
            active_auctions = self.db.query(CarAuction).filter(
                and_(
                    CarAuction.seller_id == seller_id,
                    CarAuction.status.in_([AuctionStatus.UPCOMING, AuctionStatus.ACTIVE])
                )
            ).count()
            
            completed_auctions = self.db.query(CarAuction).filter(
                and_(
                    CarAuction.seller_id == seller_id,
                    CarAuction.status.in_([AuctionStatus.ENDED, AuctionStatus.SOLD])
                )
            ).count()
            
            # Calculate total sales
            total_sales_result = self.db.query(func.sum(CarAuction.winning_bid)).filter(
                and_(
                    CarAuction.seller_id == seller_id,
                    CarAuction.status == AuctionStatus.SOLD
                )
            ).scalar()
            total_sales = Decimal(str(total_sales_result)) if total_sales_result else Decimal(0)
            
            # Pending payments (sold but not paid)
            pending_payments = self.db.query(CarAuctionTransaction).join(
                CarAuction, CarAuctionTransaction.auction_id == CarAuction.id
            ).filter(
                and_(
                    CarAuction.seller_id == seller_id,
                    CarAuctionTransaction.payment_status == PaymentStatus.PENDING
                )
            ).count()
            
            # Average sale price
            avg_price_result = self.db.query(func.avg(CarAuction.winning_bid)).filter(
                and_(
                    CarAuction.seller_id == seller_id,
                    CarAuction.status == AuctionStatus.SOLD
                )
            ).scalar()
            average_sale_price = Decimal(str(avg_price_result)) if avg_price_result else Decimal(0)
            
            # Success rate (sold / total ended)
            total_ended = self.db.query(CarAuction).filter(
                and_(
                    CarAuction.seller_id == seller_id,
                    CarAuction.status.in_([AuctionStatus.ENDED, AuctionStatus.SOLD])
                )
            ).count()
            
            sold_count = self.db.query(CarAuction).filter(
                and_(
                    CarAuction.seller_id == seller_id,
                    CarAuction.status == AuctionStatus.SOLD
                )
            ).count()
            
            success_rate = Decimal(sold_count / total_ended * 100) if total_ended > 0 else Decimal(0)
            
            # Recent auctions
            recent_auctions_query = self.db.query(CarAuction).filter(
                CarAuction.seller_id == seller_id
            ).order_by(desc(CarAuction.created_at)).limit(5).all()
            
            recent_auctions = [CarAuctionResponse.from_orm(auction) for auction in recent_auctions_query]
            
            return SellerDashboard(
                active_auctions=active_auctions,
                completed_auctions=completed_auctions,
                total_sales=total_sales,
                pending_payments=pending_payments,
                average_sale_price=average_sale_price,
                success_rate=success_rate,
                recent_auctions=recent_auctions
            )
        except Exception as e:
            logger.error(f"Error getting seller dashboard: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to get seller dashboard")

    async def get_stats(self) -> CarAuctionStats:
        """Get auction marketplace statistics."""
        try:
            total_auctions = self.db.query(CarAuction).count()
            active_auctions = self.db.query(CarAuction).filter(
                CarAuction.status == AuctionStatus.ACTIVE
            ).count()
            completed_auctions = self.db.query(CarAuction).filter(
                CarAuction.status.in_([AuctionStatus.ENDED, AuctionStatus.SOLD])
            ).count()
            
            total_bids = self.db.query(func.sum(CarAuction.total_bids)).scalar() or 0
            
            # Average final price
            avg_final_price_result = self.db.query(func.avg(CarAuction.winning_bid)).filter(
                CarAuction.status == AuctionStatus.SOLD
            ).scalar()
            average_final_price = Decimal(str(avg_final_price_result)) if avg_final_price_result else Decimal(0)
            
            # Highest sale
            highest_sale_result = self.db.query(func.max(CarAuction.winning_bid)).filter(
                CarAuction.status == AuctionStatus.SOLD
            ).scalar()
            highest_sale = Decimal(str(highest_sale_result)) if highest_sale_result else Decimal(0)
            
            # Total sales volume
            total_volume_result = self.db.query(func.sum(CarAuction.winning_bid)).filter(
                CarAuction.status == AuctionStatus.SOLD
            ).scalar()
            total_sales_volume = Decimal(str(total_volume_result)) if total_volume_result else Decimal(0)
            
            # Success rate
            sold_count = self.db.query(CarAuction).filter(
                CarAuction.status == AuctionStatus.SOLD
            ).count()
            auction_success_rate = Decimal(sold_count / completed_auctions * 100) if completed_auctions > 0 else Decimal(0)
            
            # Average bidders per auction
            avg_bidders_result = self.db.query(func.avg(CarAuction.unique_bidders)).scalar()
            average_bidders_per_auction = Decimal(str(avg_bidders_result)) if avg_bidders_result else Decimal(0)
            
            return CarAuctionStats(
                total_auctions=total_auctions,
                active_auctions=active_auctions,
                completed_auctions=completed_auctions,
                total_bids=total_bids,
                average_final_price=average_final_price,
                highest_sale=highest_sale,
                total_sales_volume=total_sales_volume,
                popular_makes=[],  # Placeholder
                auction_success_rate=auction_success_rate,
                average_bidders_per_auction=average_bidders_per_auction
            )
        except Exception as e:
            logger.error(f"Error getting auction stats: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to get auction statistics")