from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class EventBase(BaseModel):
    title: str
    description: str
    is_active: bool
    created_at: datetime
    coordinates: str
    start_at: datetime
    end_at: datetime


class UpdateEvent(EventBase):
    updated_at: datetime


class Event(EventBase):
    id: int
    updated_at: Optional[datetime]
