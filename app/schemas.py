
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class MediaType(str, Enum):
    movie = "movie"
    show = "show"
    book = "book"


class ItemStatus(str, Enum):
    planned = "planned"
    watching = "watching"
    reading = "reading"
    completed = "completed"
    dropped = "dropped"


class ItemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    media_type: MediaType
    status: ItemStatus = ItemStatus.planned
    notes: Optional[str] = None
    rating: Optional[float] = None
    priority: Optional[int] = None