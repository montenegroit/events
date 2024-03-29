from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, BaseSettings


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


class Settings(BaseSettings):
    db_host: str = "events-db"
    db_port: int = 5432
    db_user: str = "events"
    db_pass: str = "events"
    db_name: str = "events"
    sentry_sdk: str = "https://0f3c1cc149a0488e9c57e5c7ef692697@o4504875436539904.ingest.sentry.io/4504875437588480"


class TestSettings(BaseSettings):
    test_db_host: str = "localhost"
    test_db_port: int = 5432
    test_db_user: str = "postgres"
    test_db_pass: str = "postgres"
    test_db_name: str = "postgres"


DEBUG = False
settings = Settings() if DEBUG is False else TestSettings()
