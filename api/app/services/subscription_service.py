import sys
import os
from typing import Optional
from datetime import datetime, timedelta

# Add parent directory to path to import from existing bot services
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

try:
    from bot.services.marzban_service import MarzbanService
    from bot.services.user_service import UserService
except ImportError:
    # Fallback if imports fail
    MarzbanService = None
    UserService = None


class SubscriptionServiceAPI:
    """Service for managing subscriptions via API"""
    
    def __init__(self):
        self.marzban_service = MarzbanService() if MarzbanService else None
        self.user_service = UserService() if UserService else None
    
    async def get_subscription_uri(self, user_id: int) -> Optional[dict]:
        """
        Get subscription URI for user
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Subscription data or None
        """
        try:
            if not self.marzban_service or not self.user_service:
                # Mock data for development
                return {
                    'user_id': user_id,
                    'subscription_uri': f'v2ray://mock-subscription-{user_id}',
                    'expires_at': (datetime.now() + timedelta(days=30)).isoformat(),
                    'is_active': True,
                    'subscription_type': 'premium'
                }
            
            # Get user from database
            user = await self.user_service.get_user(user_id)
            
            if not user:
                return None
            
            # Get subscription from Marzban
            subscription_data = await self.marzban_service.get_user_subscription(user.marzban_username)
            
            if not subscription_data:
                return None
            
            return {
                'user_id': user_id,
                'subscription_uri': subscription_data.get('subscription_url'),
                'expires_at': subscription_data.get('expire', ''),
                'is_active': subscription_data.get('status') == 'active',
                'subscription_type': subscription_data.get('data_limit_reset_strategy', 'unknown')
            }
            
        except Exception as e:
            print(f"Error getting subscription: {e}")
            return None
    
    async def track_activation(self, user_id: int, platform: str) -> bool:
        """
        Track activation event
        
        Args:
            user_id: Telegram user ID
            platform: Platform name
            
        Returns:
            Success status
        """
        try:
            # Here you can log activation to database or analytics
            print(f"User {user_id} activated subscription on {platform}")
            return True
        except Exception as e:
            print(f"Error tracking activation: {e}")
            return False


subscription_service = SubscriptionServiceAPI()
