# job-service/src/utils/auth_utils.py
import httpx
from typing import Dict, Any, Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

logger = logging.getLogger(__name__)
security = HTTPBearer()

async def validate_token_with_auth_service(token: str) -> Dict[str, Any]:
    """Validate token with auth service."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8001/api/v1/auth/validate",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token"
                )
                
    except httpx.RequestError as e:
        logger.error(f"Auth service connection error: {str(e)}")
        # Fallback to mock for development
        return get_mock_user()
    except Exception as e:
        logger.error(f"Token validation error: {str(e)}")
        return get_mock_user()

def get_mock_user() -> Dict[str, Any]:
    """Mock user for development."""
    return {
        "user_id": 1,
        "email": "test@example.com",
        "username": "testuser",
        "role": "buyer",
        "is_active": True
    }

def get_user_from_token(token: str) -> Dict[str, Any]:
    """
    Extract user information from token.
    For development, this uses mock data.
    In production, this would validate with the auth service.
    """
    try:
        # For development, return mock user
        # In production, uncomment the line below:
        # return await validate_token_with_auth_service(token)
        return get_mock_user()
    except Exception as e:
        logger.error(f"Error getting user from token: {str(e)}")
        return get_mock_user()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Get current user from authorization header."""
    try:
        token = credentials.credentials
        # For production, use: return await validate_token_with_auth_service(token)
        return get_user_from_token(token)
    except Exception as e:
        logger.error(f"Error getting current user: {str(e)}")
        return get_mock_user()

def get_optional_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[Dict[str, Any]]:
    """Get current user if token is provided, otherwise return None."""
    if not credentials:
        return None
    
    try:
        return get_user_from_token(credentials.credentials)
    except:
        return None