import asyncio
import pytest
import pytest_asyncio

from datetime import datetime
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.schemas import TestSettings
from src.db import get_session, Base


test_settings = TestSettings()
SQLALCHEMY_DATABASE_URL_TEST = f"postgresql+asyncpg://{test_settings.test_db_user}:{test_settings.test_db_pass}@{test_settings.test_db_host}:{test_settings.test_db_port}/{test_settings.test_db_name}"
engine_test = create_async_engine(SQLALCHEMY_DATABASE_URL_TEST, echo=False)
test_async_session = sessionmaker(
    engine_test, expire_on_commit=False, class_=AsyncSession
)


async def override_get_session():
    async with test_async_session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def get_app():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(
    autouse=True,
    scope="session",
)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
class TestsEndpoints:
    async def test_smoke_get_events(
        self,
        get_app,
    ):
        response = await get_app.get("/events/")
        assert response.status_code == status.HTTP_200_OK

    async def test_smoke_post_event(
        self,
        get_app,
    ):
        data = {
            "title": "string",
            "description": "TEST DESCRIPTION",
            "is_active": True,
            "created_at": str(datetime.now(tz=None)),
            "coordinates": "string",
            "start_at": str(datetime.now(tz=None)),
            "end_at": str(datetime.now(tz=None)),
        }
        headers = {"Content-Type": "application/json"}
        response = await get_app.post(
            "/events/",
            json=data,
            headers=headers,
        )
        assert response.status_code == status.HTTP_201_CREATED

    async def test_smoke_get_event_by_id(
        self,
        get_app,
    ):
        response = await get_app.get("/events/1/")
        assert response.status_code == status.HTTP_200_OK

    async def test_smoke_put_request_event(
        self,
        get_app,
    ):
        data = {
            "title": "string",
            "description": "PUT TESTS",
            "is_active": True,
            "created_at": str(datetime.now(tz=None)),
            "coordinates": "string",
            "start_at": str(datetime.now(tz=None)),
            "end_at": str(datetime.now(tz=None)),
            "updated_at": str(datetime.now(tz=None)),
        }
        headers = {"Content-Type": "application/json"}
        response = await get_app.put(
            "/events/1/",
            json=data,
            headers=headers,
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    async def test_smoke_delete_event(
        self,
        get_app,
    ):
        response = await get_app.delete("/events/1/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
