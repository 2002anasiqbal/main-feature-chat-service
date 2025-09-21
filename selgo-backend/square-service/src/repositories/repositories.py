from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, or_, asc, desc
from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_Distance, ST_Transform, ST_SetSRID, ST_MakePoint
from typing import List, Optional, Dict, Any, Tuple
from ..models.item_models import ItemCategory, Item, ItemImage, ItemRating, UserFavorite
from ..models.item_schemas import ItemFilterParams, GeoPoint, ItemCondition, SellerType, AdType
import logging

logger = logging.getLogger(__name__)

class ItemCategoryRepository:
    @staticmethod
    def create(db: Session, category_data: Dict[str, Any]) -> ItemCategory:
        db_category = ItemCategory(**category_data)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    @staticmethod
    def get_by_id(db: Session, category_id: int) -> Optional[ItemCategory]:
        return db.query(ItemCategory).filter(ItemCategory.id == category_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[ItemCategory]:
        return db.query(ItemCategory).offset(skip).limit(limit).all()

    @staticmethod
    def get_all_with_counts(db: Session) -> List[Tuple[ItemCategory, int]]:
        query = db.query(
            ItemCategory,
            func.count(Item.id).label('count')
        ).outerjoin(
            Item, ItemCategory.id == Item.category_id
        ).group_by(ItemCategory.id)

        return query.all()

    @staticmethod
    def get_by_parent_id(db: Session, parent_id: Optional[int] = None) -> List[ItemCategory]:
        if parent_id is None:
            return db.query(ItemCategory).filter(ItemCategory.parent_id.is_(None)).all()
        else:
            return db.query(ItemCategory).filter(ItemCategory.parent_id == parent_id).all()

    @staticmethod
    def update(db: Session, category_id: int, category_data: Dict[str, Any]) -> Optional[ItemCategory]:
        db_category = db.query(ItemCategory).filter(ItemCategory.id == category_id).first()
        if db_category:
            for key, value in category_data.items():
                setattr(db_category, key, value)
            db.commit()
            db.refresh(db_category)
        return db_category

    @staticmethod
    def delete(db: Session, category_id: int) -> bool:
        db_category = db.query(ItemCategory).filter(ItemCategory.id == category_id).first()
        if db_category:
            db.delete(db_category)
            db.commit()
            return True
        return False

class ItemRepository:
    @staticmethod
    def create(db: Session, item_data: Dict[str, Any]) -> Item:
        if 'location' in item_data and item_data['location'] is not None:
            location = item_data.pop('location')
            lat, lon = location.latitude, location.longitude
            item_data['location'] = f'SRID=4326;POINT({lon} {lat})'

        db_item = Item(**item_data)

        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    def get_by_id(db: Session, item_id: int) -> Optional[Item]:
        return db.query(Item).filter(Item.id == item_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
        return db.query(Item).offset(skip).limit(limit).all()

    @staticmethod
    def filter_items(db: Session, filters: ItemFilterParams) -> Tuple[List[Item], int]:
        query = db.query(Item).filter(Item.status == "active")

        if filters.category_id:
            query = query.filter(Item.category_id == filters.category_id)

        if filters.condition:
            query = query.filter(Item.condition == filters.condition)

        if filters.price_min is not None:
            query = query.filter(Item.price >= filters.price_min)

        if filters.price_max is not None:
            query = query.filter(Item.price <= filters.price_max)

        if filters.seller_type:
            query = query.filter(Item.seller_type == filters.seller_type)

        if filters.ad_type:
            query = query.filter(Item.ad_type == filters.ad_type)

        if filters.location and filters.distance:
            point = ST_SetSRID(ST_MakePoint(filters.location.longitude, filters.location.latitude), 4326)
            distance_meters = filters.distance * 1000
            query = query.filter(
                ST_Distance(
                    ST_Transform(Item.location, 3857),
                    ST_Transform(point, 3857)
                ) <= distance_meters
            )

        if filters.search_term:
            search_term = f"%{filters.search_term}%"
            query = query.filter(
                or_(
                    Item.title.ilike(search_term),
                    Item.description.ilike(search_term),
                    Item.location_name.ilike(search_term)
                )
            )

        if filters.sort_by and filters.sort_order:
            order_column = getattr(Item, filters.sort_by, Item.created_at)
            if filters.sort_order.lower() == "desc":
                query = query.order_by(desc(order_column))
            else:
                query = query.order_by(asc(order_column))

        total = query.count()

        query = query.offset(filters.offset).limit(filters.limit)

        items = query.all()

        return items, total

    @staticmethod
    def get_recommended_items(db: Session, limit: int = 10) -> List[Item]:
        query = db.query(Item).filter(Item.status == "active")
        query = query.order_by(desc(Item.created_at))
        return query.limit(limit).all()

    @staticmethod
    def update(db: Session, item_id: int, item_data: Dict[str, Any]) -> Optional[Item]:
        db_item = db.query(Item).filter(Item.id == item_id).first()

        if not db_item:
            return None

        if 'location' in item_data and item_data['location'] is not None:
            location = item_data.pop('location')
            lat, lon = location.latitude, location.longitude
            item_data['location'] = f'SRID=4326;POINT({lon} {lat})'

        for key, value in item_data.items():
            if hasattr(db_item, key):
                setattr(db_item, key, value)

        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    def delete(db: Session, item_id: int) -> bool:
        db_item = db.query(Item).filter(Item.id == item_id).first()
        if db_item:
            db.delete(db_item)
            db.commit()
            return True
        return False

    @staticmethod
    def increment_view_count(db: Session, item_id: int) -> Optional[Item]:
        db_item = db.query(Item).filter(Item.id == item_id).first()
        if db_item:
            db_item.view_count += 1
            db.commit()
            db.refresh(db_item)
        return db_item

class ItemImageRepository:
    @staticmethod
    def create(db: Session, item_id: int, image_data: Dict[str, Any]) -> ItemImage:
        db_image = ItemImage(**image_data, item_id=item_id)
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        return db_image

    @staticmethod
    def create_many(db: Session, item_id: int, images_data: List[Dict[str, Any]]) -> List[ItemImage]:
        db_images = [ItemImage(**image_data, item_id=item_id) for image_data in images_data]
        db.add_all(db_images)
        db.commit()

        for image in db_images:
            db.refresh(image)

        return db_images

    @staticmethod
    def get_by_id(db: Session, image_id: int) -> Optional[ItemImage]:
        return db.query(ItemImage).filter(ItemImage.id == image_id).first()

    @staticmethod
    def get_by_item_id(db: Session, item_id: int) -> List[ItemImage]:
        return db.query(ItemImage).filter(ItemImage.item_id == item_id).all()

    @staticmethod
    def update(db: Session, image_id: int, image_data: Dict[str, Any]) -> Optional[ItemImage]:
        db_image = db.query(ItemImage).filter(ItemImage.id == image_id).first()
        if db_image:
            for key, value in image_data.items():
                setattr(db_image, key, value)
            db.commit()
            db.refresh(db_image)
        return db_image

    @staticmethod
    def delete(db: Session, image_id: int) -> bool:
        db_image = db.query(ItemImage).filter(ItemImage.id == image_id).first()
        if db_image:
            db.delete(db_image)
            db.commit()
            return True
        return False

    @staticmethod
    def delete_by_item_id(db: Session, item_id: int) -> bool:
        db.query(ItemImage).filter(ItemImage.item_id == item_id).delete()
        db.commit()
        return True

class ItemRatingRepository:
    @staticmethod
    def create(db: Session, rating_data: Dict[str, Any]) -> ItemRating:
        db_rating = ItemRating(**rating_data)
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        return db_rating

    @staticmethod
    def get_by_id(db: Session, rating_id: int) -> Optional[ItemRating]:
        return db.query(ItemRating).filter(ItemRating.id == rating_id).first()

    @staticmethod
    def get_by_item_id(db: Session, item_id: int, skip: int = 0, limit: int = 100) -> List[ItemRating]:
        return db.query(ItemRating).filter(ItemRating.item_id == item_id).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[ItemRating]:
        return db.query(ItemRating).filter(ItemRating.user_id == user_id).offset(skip).limit(limit).all()

    @staticmethod
    def get_avg_rating(db: Session, item_id: int) -> float:
        avg_rating = db.query(func.avg(ItemRating.stars)).filter(ItemRating.item_id == item_id).scalar()
        return float(avg_rating) if avg_rating is not None else 0.0

    @staticmethod
    def get_rating_count(db: Session, item_id: int) -> int:
        return db.query(ItemRating).filter(ItemRating.item_id == item_id).count()

    @staticmethod
    def update(db: Session, rating_id: int, rating_data: Dict[str, Any]) -> Optional[ItemRating]:
        db_rating = db.query(ItemRating).filter(ItemRating.id == rating_id).first()
        if db_rating:
            for key, value in rating_data.items():
                setattr(db_rating, key, value)
            db.commit()
            db.refresh(db_rating)
        return db_rating

    @staticmethod
    def delete(db: Session, rating_id: int) -> bool:
        db_rating = db.query(ItemRating).filter(ItemRating.id == rating_id).first()
        if db_rating:
            db.delete(db_rating)
            db.commit()
            return True
        return False

class UserFavoriteRepository:
    @staticmethod
    def add_favorite(db: Session, user_id: int, item_id: int) -> Optional[UserFavorite]:
        existing = db.query(UserFavorite).filter(
            UserFavorite.user_id == user_id,
            UserFavorite.item_id == item_id
        ).first()

        if existing:
            return existing

        favorite = UserFavorite(user_id=user_id, item_id=item_id)
        db.add(favorite)
        db.commit()
        db.refresh(favorite)
        return favorite

    @staticmethod
    def remove_favorite(db: Session, user_id: int, item_id: int) -> bool:
        favorite = db.query(UserFavorite).filter(
            UserFavorite.user_id == user_id,
            UserFavorite.item_id == item_id
        ).first()

        if favorite:
            db.delete(favorite)
            db.commit()
            return True
        return False

    @staticmethod
    def is_favorite(db: Session, user_id: int, item_id: int) -> bool:
        return db.query(UserFavorite).filter(
            UserFavorite.user_id == user_id,
            UserFavorite.item_id == item_id
        ).first() is not None

    @staticmethod
    def get_user_favorites(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[UserFavorite]:
        return db.query(UserFavorite).options(
            joinedload(UserFavorite.item).joinedload(Item.images)
        ).filter(
            UserFavorite.user_id == user_id
        ).order_by(
            UserFavorite.created_at.desc()
        ).offset(skip).limit(limit).all()

    @staticmethod
    def get_favorites_count(db: Session, user_id: int) -> int:
        return db.query(UserFavorite).filter(UserFavorite.user_id == user_id).count()