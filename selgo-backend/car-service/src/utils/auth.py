from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Dict, Any, Optional
from ..config.config import settings
from .auth_client import auth_client
import logging

logger = logging.getLogger(__name__)

# OAuth2 password bearer token scheme - Updated tokenUrl
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8001/api/v1/auth/token")

async def get_current_user_data(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """
    Get current user data by validating token with auth service.
    """
    try:
        logger.info(f"Attempting to validate token: {token[:20]}...")
        user_data = await auth_client.validate_token(token)
        logger.info(f"Successfully validated user: {user_data.get('username')}")
        return user_data
    except HTTPException as e:
        logger.error(f"HTTP exception during token validation: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error during token validation: {e}")
        # Fallback for development
        if settings.ENVIRONMENT == "development":
            logger.info("Using development fallback authentication")
            return {
                "user_id": 1,
                "username": "testuser",
                "email": "test@example.com",
                "role": "buyer",
                "is_active": True
            }
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user_id(user_data: Dict[str, Any] = Depends(get_current_user_data)) -> int:
    """Get current user ID from validated user data."""
    user_id = user_data.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user data"
        )
    return int(user_id)

async def get_current_admin_user_id(user_data: Dict[str, Any] = Depends(get_current_user_data)) -> int:
    """Get current user ID and verify admin role."""
    if user_data.get("role") not in ["admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return int(user_data["user_id"])

async def get_optional_user_data(token: Optional[str] = Depends(oauth2_scheme)) -> Optional[Dict[str, Any]]:
    """Get user data if token is valid, otherwise return None."""
    if not token:
        return None
    try:
        return await get_current_user_data(token)
    except HTTPException:
        return None