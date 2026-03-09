
from datetime import datetime
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

class ItemResponse(BaseModel):
    id: int
    title: str = Field(max_length=200)
    media_type: str = Field(max_length=50)
    status: str = Field(max_length=50)
    notes: str | None = Field(default=None, max_length=500)
    rating: float | None = None
    priority: int | None = None
    created_at: datetime

class ItemUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    media_type: MediaType | None = None
    status: ItemStatus | None = None
    notes: str | None = Field(default=None, max_length=500)
    rating: float | None = None
    priority: int | None = None