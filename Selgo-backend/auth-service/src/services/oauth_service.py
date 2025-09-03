from authlib.integrations.httpx_client import AsyncOAuth2Client
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from ..config.config import settings
from ..repositories.user_repository import UserRepository
from ..models.user_models import User, AuthProvider, UserRole
from ..utils.auth_utils import create_access_token, create_refresh_token
import httpx

class OAuthService:
    def __init__(self):
        self.user_repo = UserRepository()
    
    async def google_auth_url(self, redirect_uri: str) -> str:
        """Generate Google OAuth authorization URL."""
        client = AsyncOAuth2Client(
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
        )
        
        authorization_url, state = client.create_authorization_url(
            'https://accounts.google.com/o/oauth2/auth',
            redirect_uri=redirect_uri,
            scope=['openid', 'email', 'profile']
        )
        
        return authorization_url
    
    async def google_callback(self, db: Session, code: str, redirect_uri: str) -> tuple[str, str, User]:
        """Handle Google OAuth callback."""
        client = AsyncOAuth2Client(
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
        )
        
        # Exchange code for token
        token = await client.fetch_token(
            'https://oauth2.googleapis.com/token',
            code=code,
            redirect_uri=redirect_uri
        )
        
        # Get user info
        async with httpx.AsyncClient() as http_client:
            response = await http_client.get(
                'https://www.googleapis.com/oauth2/v2/userinfo',
                headers={'Authorization': f'Bearer {token["access_token"]}'}
            )
            user_info = response.json()
        
        # Find or create user
        user = self.user_repo.get_by_provider_id(db, user_info['id'], AuthProvider.GOOGLE.value)
        
        if not user:
            # Check if user exists with same email
            user = self.user_repo.get_by_email(db, user_info['email'])
            if user:
                # Link existing account
                user.provider_id = user_info['id']
                user.auth_provider = AuthProvider.GOOGLE
                db.commit()
            else:
                # Create new user
                user_data = {
                    'username': user_info['email'].split('@')[0],  # Use email prefix as username
                    'email': user_info['email'],
                    'full_name': user_info.get('name'),
                    'avatar_url': user_info.get('picture'),
                    'provider_id': user_info['id'],
                    'auth_provider': AuthProvider.GOOGLE,
                    'is_verified': True,
                    'role': UserRole.BUYER
                }
                user = self.user_repo.create(db, user_data)
        
        # Create tokens
        access_token = self._create_user_access_token(user)
        refresh_token = self._create_user_refresh_token(db, user)
        
        return access_token, refresh_token, user
    
    def _create_user_access_token(self, user: User) -> str:
        """Create access token for user."""
        token_data = {
            "sub": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "is_active": user.is_active
        }
        return create_access_token(token_data)
    
    def _create_user_refresh_token(self, db: Session, user: User) -> str:
        """Create and store refresh token for user."""
        from datetime import datetime, timedelta
        refresh_token = create_refresh_token()
        expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
        self.user_repo.create_refresh_token(db, user.id, refresh_token, expires_at)
        return refresh_token  
