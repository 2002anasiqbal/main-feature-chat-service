from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from datetime import datetime
from ..models.user_models import User, RefreshToken

class UserRepository:
    def create(self, db: Session, user_data: Dict[str, Any]) -> User:
        """Create a new user."""
        db_user = User(**user_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get user by email."""
        return db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """Get user by username."""
        return db.query(User).filter(User.username == username).first()
    
    def get_by_provider_id(self, db: Session, provider_id: str, provider: str) -> Optional[User]:
        """Get user by OAuth provider ID."""
        return db.query(User).filter(
            User.provider_id == provider_id,
            User.auth_provider == provider
        ).first()
    
    def update(self, db: Session, user_id: int, user_data: Dict[str, Any]) -> Optional[User]:
        """Update user."""
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            for field, value in user_data.items():
                setattr(db_user, field, value)
            db.commit()
            db.refresh(db_user)
        return db_user
    
    def update_last_login(self, db: Session, user_id: int) -> bool:
        """Update user's last login timestamp."""
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db_user.last_login = datetime.utcnow()
            db.commit()
            return True
        return False
    
    def update_password(self, db: Session, user_id: int, hashed_password: str) -> bool:
        """Update user password."""
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db_user.hashed_password = hashed_password
            db.commit()
            return True
        return False
    
    def create_refresh_token(self, db: Session, user_id: int, token: str, expires_at: datetime) -> RefreshToken:
        """Create a refresh token."""
        db_token = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at
        )
        db.add(db_token)
        db.commit()
        db.refresh(db_token)
        return db_token
    
    def get_refresh_token(self, db: Session, token: str) -> Optional[RefreshToken]:
        """Get refresh token."""
        return db.query(RefreshToken).filter(RefreshToken.token == token).first()
    
    def revoke_refresh_token(self, db: Session, token: str) -> bool:
        """Revoke a refresh token."""
        db_token = db.query(RefreshToken).filter(RefreshToken.token == token).first()
        if db_token:
            db_token.is_revoked = True
            db.commit()
            return True
        return False  
