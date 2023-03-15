from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class EventBase(BaseModel):
    title: str
    description: str
    is_active: bool
    created_at: datetime = Field(default=datetime.now(tz=None))
    coordinates: str
    start_at: datetime = Field(default=datetime.now(tz=None))
    end_at: datetime = Field(default=datetime.now(tz=None))


class UpdateEvent(EventBase):
    updated_at: datetime = Field(default=datetime.now(tz=None))


class Event(EventBase):
    id: int
    updated_at: Optional[datetime] = Field(default=datetime.now(tz=None))
