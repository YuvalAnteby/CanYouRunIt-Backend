from datetime import datetime
from typing import List

from bson import ObjectId
from pydantic import BaseModel


class Game(BaseModel):
    """
    Schema for creating a new game with the relevant attributes
    """
    game_id: str
    name: str
    publisher: str
    developer: str
    release_date: int
    genres: List[str]
    desc: str
    trailer_url: str
    portrait_url: str
    buy_links: List[str]
    landscape_s: str
    landscape_m: str
    landscape_l: str
    landscape_xl: str
    available_resolutions: List[str]
    supported_settings: List[str]
    is_ssd_recommended: bool
    upscale_support: List[str]
    api_support: List[str]
    created_at: datetime
    # Convert ObjectId to string
    id: str

    class Config:
        json_encoders = {
            ObjectId: str  # This will convert ObjectId to a string automatically
        }
