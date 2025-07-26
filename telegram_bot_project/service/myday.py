from sqlalchemy import text
from typing import Optional
from config import get_session

from abc import ABC, abstractmethod

# Will be implemented later
class MyDayService(ABC):
    @staticmethod
    @abstractmethod
    async def get_myday_by_user_id(user_id: int) -> Optional[dict]:
        pass