# selgo-backend/motorcycle-service/src/utils/auth_utils.py
from fastapi import HTTPException, Depends, Header
from typing import Optional

import requests
from ..config.config import settings

class AuthenticationError(Exception):
    pass

def get_current_user_id(authorization: Optional[str] = Header(None)) -> int:
    
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    token = authorization.split(" ")[1]
    
    try:        
        # Option 2: Validate token via auth service
        user_data = validate_token_with_auth_service(token)
        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return user_data.get("user_id") or user_data.get("id")
        
    except Exception as e:
        print(f"❌ Token validation error: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")

def validate_token_with_auth_service(token: str) -> Optional[dict]:
    """
    Validate token with the auth service
    """
    try:
        response = requests.post(
            f"{settings.AUTH_SERVICE_URL}/api/v1/auth/validate-token",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Auth service validation failed: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Auth service request failed: {e}")
        return None

def get_optional_user_id(authorization: Optional[str] = Header(None)) -> Optional[int]:
    """
    Get user ID if authenticated, None if not (for optional authentication)
    """
    try:
        return get_current_user_id(authorization)
    except HTTPException:
        return None