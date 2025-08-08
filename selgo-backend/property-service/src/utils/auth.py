# property-service/src/utils/auth.py
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Optional
import httpx
import os
from uuid import UUID

from ..models.property_schemas import AuthenticatedUser

# Auth service configuration
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8001")

async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(None)  # We'll get this from the route
) -> Optional[AuthenticatedUser]:
    """
    Get current user from auth service (optional - returns None if not authenticated)
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None
    
    token = authorization.split(" ")[1]
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{AUTH_SERVICE_URL}/api/auth/verify",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                user_data = response.json()
                return AuthenticatedUser(
                    user_id=UUID(user_data["user_id"]),
                    email=user_data["email"],
                    is_verified=user_data.get("is_verified", False),
                    roles=user_data.get("roles", [])
                )
    except Exception as e:
        print(f"Auth verification failed: {e}")
        return None
    
    return None

async def require_authentication(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(None)
) -> AuthenticatedUser:
    """
    Require authentication - raises exception if not authenticated
    """
    user = await get_current_user(authorization, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

async def require_role(required_role: str):
    """
    Require specific role
    """
    async def _require_role(current_user: AuthenticatedUser = Depends(require_authentication)):
        if required_role not in current_user.roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{required_role}' required"
            )
        return current_user
    
    return _require_role

async def require_verified_user(
    current_user: AuthenticatedUser = Depends(require_authentication)
) -> AuthenticatedUser:
    """
    Require verified user account
    """
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email verification required"
        )
    
    return current_user