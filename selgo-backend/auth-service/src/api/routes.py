from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from ..database.database import get_db
from ..services.auth_service import AuthService
from ..models.user_schemas import (
    UserCreate, UserResponse, LoginRequest, LoginResponse, 
    RefreshTokenRequest, TokenResponse, ChangePasswordRequest,
    TokenValidationResponse
)
from ..utils.auth_utils import get_user_from_token
from ..config.config import settings

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/token")

auth_service = AuthService()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    return auth_service.register_user(db, user_data)

@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login with username/email and password."""
    access_token, refresh_token, user = auth_service.authenticate_user(db, login_data)
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(user)  # Updated for Pydantic v2
    )

@router.post("/token", response_model=LoginResponse)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """OAuth2 compatible token endpoint."""
    login_data = LoginRequest(username=form_data.username, password=form_data.password)
    access_token, refresh_token, user = auth_service.authenticate_user(db, login_data)
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(user)  # Updated for Pydantic v2
    )

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(token_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Refresh access token."""
    access_token = auth_service.refresh_access_token(db, token_data.refresh_token)
    return TokenResponse(
        access_token=access_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

@router.post("/logout")
def logout(token_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Logout (revoke refresh token)."""
    success = auth_service.revoke_refresh_token(db, token_data.refresh_token)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid refresh token"
        )
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get current user information."""
    user_data = get_user_from_token(token)
    user = auth_service.user_repo.get_by_id(db, user_data["user_id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse.model_validate(user)  # Updated for Pydantic v2

@router.post("/change-password")
def change_password(
    password_data: ChangePasswordRequest,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Change user password."""
    user_data = get_user_from_token(token)
    success = auth_service.change_password(
        db, user_data["user_id"], 
        password_data.current_password, 
        password_data.new_password
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to change password"
        )
    return {"message": "Password changed successfully"}

# Token validation endpoint for other services
@router.post("/validate", response_model=TokenValidationResponse)
def validate_token(token: str = Depends(oauth2_scheme)):
    """Validate token and return user information. Used by other microservices."""
    user_data = get_user_from_token(token)
    return TokenValidationResponse(**user_data)