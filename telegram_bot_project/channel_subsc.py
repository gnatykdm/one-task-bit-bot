import requests
from typing import Dict, Any, Optional
from config import AnotherConfig, get_token

BOT_TOKEN: str = get_token()
CHAT_NAME: str = AnotherConfig.CHANNEL_NAME
CHECKER_URL: str = "https://telegram-membership-checker.vercel.app/api/check"

class ChannelSubscChecker:
    @staticmethod
    async def check_subscr_status(user_id: int) -> bool:
        if not user_id:
            raise ValueError("User id is empty.")
        
        params: Dict[str, str] = {
            "token": BOT_TOKEN,
            "user_id": str(user_id),
            "chat_id": CHAT_NAME
        }

        try:
            response: requests.Response = requests.get(
                url=CHECKER_URL,
                params=params,
                timeout=5  
            )
            response.raise_for_status()  

            data: Any = response.json()
            user_info: Optional[Dict[str, Any]] = data.get("data", {})
            subscr_status: bool = bool(user_info.get("status", False))

            return subscr_status
        
        except requests.RequestException as e:
            print(f"[ERROR] Checker connection failed: {e}")
            return False
        except (ValueError, KeyError, TypeError) as e:
            print(f"[ERROR] Invalid response format: {e}")
            return False
