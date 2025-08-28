from pydantic import BaseModel

class UserGeoDataDTO(BaseModel):
    user_id: int
    chat_id: int
    timezone: str