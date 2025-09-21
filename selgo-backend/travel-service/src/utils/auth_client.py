import httpx
from fastapi import HTTPException, status
from typing import Dict, Any, Optional
from ..config.config import settings
import logging
import asyncio

logger = logging.getLogger(__name__)

class AuthClient:
    def __init__(self):
        self.auth_service_url = getattr(settings, 'AUTH_SERVICE_URL', 'http://localhost:8001')
        self.client = None
        self._create_client()

    def _create_client(self):
        """Create HTTP client with proper configuration."""
        try:
            self.client = httpx.AsyncClient(
                timeout=httpx.Timeout(10.0),
                limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
            )
        except Exception as e:
            logger.error(f"Failed to create HTTP client: {e}")

    async def validate_token(self, token: str) -> Dict[str, Any]:
        """Validate token with auth service and return user data."""
        if not self.client:
            self._create_client()
            
        try:
            logger.info(f"Validating token with auth service at {self.auth_service_url}")
            response = await self.client.post(
                f"{self.auth_service_url}/api/v1/auth/validate",
                headers={"Authorization": f"Bearer {token}"},
                timeout=5.0
            )
            
            logger.info(f"Auth service response status: {response.status_code}")
            
            if response.status_code == 200:
                user_data = response.json()
                logger.info(f"Token validation successful for user: {user_data.get('username')}")
                return user_data
            else:
                logger.warning(f"Token validation failed with status {response.status_code}: {response.text}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token"
                )
        except httpx.RequestError as e:
            logger.error(f"Auth service request failed: {e}")
            # Fallback to development mode if auth service is unavailable
            if settings.ENVIRONMENT == "development":
                logger.info("Falling back to development mode authentication")
                return self._mock_user_data()
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication service unavailable"
            )
        except httpx.TimeoutException as e:
            logger.error(f"Auth service timeout: {e}")
            if settings.ENVIRONMENT == "development":
                logger.info("Falling back to development mode due to timeout")
                return self._mock_user_data()
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication service timeout"
            )

    def _mock_user_data(self) -> Dict[str, Any]:
        """Mock user data for development."""
        return {
            "user_id": 1,
            "username": "testuser",
            "email": "test@example.com",
            "role": "buyer",
            "is_active": True
        }

    async def close(self):
        """Close the HTTP client."""
        if self.client:
            await self.client.aclose()

# Global auth client instance
auth_client = AuthClient()