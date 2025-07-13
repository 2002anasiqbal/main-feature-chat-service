# selgo-backend/motorcycle-service/src/auth_client.py
import requests
from typing import Optional, Dict, Any
from .config import settings

class AuthServiceClient:
    def __init__(self):
        self.auth_base_url = settings.AUTH_SERVICE_URL or "http://localhost:8001"
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user details from auth service"""
        try:
            response = requests.get(
                f"{self.auth_base_url}/api/v1/users/{user_id}",
                timeout=5  # 5 second timeout
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                print(f"⚠️ User {user_id} not found in auth service")
                return None
            else:
                print(f"❌ Auth service error: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to fetch user from auth service: {e}")
            return None
    
    def get_multiple_users(self, user_ids: list[int]) -> Dict[int, Dict[str, Any]]:
        """Get multiple users by IDs"""
        users = {}
        
        for user_id in user_ids:
            user_data = self.get_user_by_id(user_id)
            if user_data:
                users[user_id] = user_data
                    
        return users

# Global instance
auth_client = AuthServiceClient()